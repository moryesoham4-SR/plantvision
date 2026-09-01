import sqlite3
import json
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
import config

def _get_supabase_headers():
    return {
        "apikey": config.SUPABASE_KEY,
        "Authorization": f"Bearer {config.SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def _supabase_request(method: str, endpoint: str, data: dict = None, params: dict = None):
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        return None
    url = f"{config.SUPABASE_URL.rstrip('/')}/rest/v1/{endpoint}"
    headers = _get_supabase_headers()
    try:
        response = requests.request(method, url, json=data, params=params, headers=headers, timeout=4)
        return response
    except Exception:
        return None

def get_connection():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Scans History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plant TEXT NOT NULL,
            disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            severity TEXT NOT NULL,
            is_healthy INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            symptoms_json TEXT,
            remedies_json TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Seed Default User if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        import auth
        default_pwd_hash = auth.hash_password("password123")
        cursor.execute("""
            INSERT INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, ("farmer_john", "Farmer John", "john@plantvision.ai", default_pwd_hash))

    conn.commit()
    conn.close()

def register_user(username: str, full_name: str, email: str, password_hash: str) -> tuple[bool, Optional[int], str]:
    clean_user = username.strip().lower()
    clean_email = email.strip().lower()
    clean_name = full_name.strip()

    # 1. Try Supabase Cloud Database First (Permanent persistence)
    sup_res = _supabase_request("POST", "users", data={
        "username": clean_user,
        "full_name": clean_name,
        "email": clean_email,
        "password_hash": password_hash
    })
    
    if sup_res is not None:
        if sup_res.status_code in (200, 201):
            try:
                res_data = sup_res.json()
                if isinstance(res_data, list) and len(res_data) > 0:
                    sup_user_id = res_data[0].get("id")
                    # Also mirror in local SQLite
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT OR REPLACE INTO users (id, username, full_name, email, password_hash)
                            VALUES (?, ?, ?, ?, ?)
                        """, (sup_user_id, clean_user, clean_name, clean_email, password_hash))
                        conn.commit()
                        conn.close()
                    except Exception:
                        pass
                    return True, sup_user_id, "Account registered successfully in Supabase Cloud!"
            except Exception:
                pass
        elif sup_res.status_code == 409:
            return False, None, "Username or email is already registered."

    # 2. Local SQLite Fallback
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (clean_user, clean_name, clean_email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        return True, user_id, "User registered successfully."
    except sqlite3.IntegrityError as e:
        if "users.username" in str(e):
            return False, None, "Username is already taken."
        elif "users.email" in str(e):
            return False, None, "Email is already registered."
        return False, None, f"Database error: {str(e)}"
    finally:
        conn.close()

def verify_user_credentials(username_or_email: str, password_hash: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
    cleaned = username_or_email.strip().lower()

    # 1. Check Supabase Cloud Database First
    sup_res = _supabase_request("GET", "users", params={"or": f"(username.eq.{cleaned},email.eq.{cleaned})"})
    if sup_res is not None and sup_res.status_code == 200:
        try:
            records = sup_res.json()
            if isinstance(records, list) and len(records) > 0:
                row = records[0]
                if row.get("password_hash") == password_hash:
                    user_data = {
                        "id": row.get("id"),
                        "username": row.get("username"),
                        "full_name": row.get("full_name"),
                        "email": row.get("email"),
                        "created_at": row.get("created_at")
                    }
                    return True, user_data, "Login successful!"
                else:
                    return False, None, "Incorrect password. Please verify and try again."
        except Exception:
            pass

    # 2. Check Local SQLite Fallback
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, full_name, email, password_hash, created_at
        FROM users
        WHERE (username = ? OR email = ?)
    """, (cleaned, cleaned))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, None, "Account not found for this username or email. Please click 'Create New Account' below to register."
    
    if row["password_hash"] != password_hash:
        return False, None, "Incorrect password. Please verify and try again."
        
    user_data = {
        "id": row["id"],
        "username": row["username"],
        "full_name": row["full_name"],
        "email": row["email"],
        "created_at": row["created_at"]
    }
    return True, user_data, "Login successful!"

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    # 1. Try Supabase
    sup_res = _supabase_request("GET", "users", params={"id": f"eq.{user_id}"})
    if sup_res is not None and sup_res.status_code == 200:
        try:
            records = sup_res.json()
            if isinstance(records, list) and len(records) > 0:
                row = records[0]
                return {
                    "id": row.get("id"),
                    "username": row.get("username"),
                    "full_name": row.get("full_name"),
                    "email": row.get("email"),
                    "created_at": row.get("created_at")
                }
        except Exception:
            pass

    # 2. Fallback SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def save_scan(
    user_id: int,
    plant: str,
    disease: str,
    confidence: float,
    severity: str,
    is_healthy: bool,
    image_path: str,
    symptoms: List[str],
    remedies: Dict[str, List[str]]
) -> int:
    symptoms_str = json.dumps(symptoms)
    remedies_str = json.dumps(remedies)

    # 1. Try Supabase Cloud
    scan_payload = {
        "user_id": user_id,
        "plant": plant,
        "disease": disease,
        "confidence": float(confidence),
        "severity": severity,
        "is_healthy": bool(is_healthy),
        "image_path": str(image_path),
        "symptoms_json": symptoms_str,
        "remedies_json": remedies_str
    }
    sup_res = _supabase_request("POST", "scans", data=scan_payload)
    sup_scan_id = None
    if sup_res is not None and sup_res.status_code in (200, 201):
        try:
            records = sup_res.json()
            if isinstance(records, list) and len(records) > 0:
                sup_scan_id = records[0].get("id")
        except Exception:
            pass

    # 2. Always persist to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (
            user_id, plant, disease, confidence, severity, is_healthy,
            image_path, symptoms_json, remedies_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        plant,
        disease,
        float(confidence),
        severity,
        1 if is_healthy else 0,
        str(image_path),
        symptoms_str,
        remedies_str
    ))
    conn.commit()
    sqlite_id = cursor.lastrowid
    conn.close()
    return sup_scan_id or sqlite_id

def get_user_scans(
    user_id: int,
    plant_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    search_term: Optional[str] = None
) -> List[Dict[str, Any]]:
    # 1. Try Supabase
    params = {"user_id": f"eq.{user_id}", "order": "timestamp.desc"}
    if plant_filter and plant_filter.lower() != "all":
        params["plant"] = f"ilike.{plant_filter.strip()}"
    if status_filter:
        if status_filter.lower() == "healthy":
            params["is_healthy"] = "eq.true"
        elif status_filter.lower() == "diseased":
            params["is_healthy"] = "eq.false"

    sup_res = _supabase_request("GET", "scans", params=params)
    if sup_res is not None and sup_res.status_code == 200:
        try:
            records = sup_res.json()
            if isinstance(records, list):
                if search_term:
                    st_lower = search_term.lower()
                    records = [r for r in records if st_lower in r.get("disease", "").lower() or st_lower in r.get("plant", "").lower()]
                return records
        except Exception:
            pass

    # 2. Fallback SQLite
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM scans WHERE user_id = ?"
    params = [user_id]

    if plant_filter and plant_filter.lower() != "all":
        query += " AND LOWER(plant) = ?"
        params.append(plant_filter.lower())

    if status_filter:
        if status_filter.lower() == "healthy":
            query += " AND is_healthy = 1"
        elif status_filter.lower() == "diseased":
            query += " AND is_healthy = 0"

    if search_term:
        query += " AND (LOWER(disease) LIKE ? OR LOWER(plant) LIKE ?)"
        params.extend([f"%{search_term.lower()}%", f"%{search_term.lower()}%"])

    query += " ORDER BY timestamp DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_scan(scan_id: int, user_id: int) -> bool:
    # 1. Try Supabase
    _supabase_request("DELETE", "scans", params={"id": f"eq.{scan_id}", "user_id": f"eq.{user_id}"})

    # 2. SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ? AND user_id = ?", (scan_id, user_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_user_analytics(user_id: int) -> Dict[str, Any]:
    scans = get_user_scans(user_id)
    total_scans = len(scans)
    healthy_count = sum(1 for s in scans if s.get("is_healthy") in (1, True))
    diseased_count = total_scans - healthy_count

    plant_counts = {}
    disease_counts = {}

    for s in scans:
        p = s.get("plant", "Unknown")
        plant_counts[p] = plant_counts.get(p, 0) + 1
        if not s.get("is_healthy"):
            d = s.get("disease", "Unknown")
            disease_counts[d] = disease_counts.get(d, 0) + 1

    return {
        "total_scans": total_scans,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "plant_counts": plant_counts,
        "disease_counts": disease_counts
    }



