import sqlite3
import json
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import config

# Indian Standard Time (IST) Timezone (UTC +05:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now() -> datetime:
    return datetime.now(IST)

def get_ist_now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now(IST).strftime(fmt)

def format_timestamp_ist(ts_str: Any) -> str:
    """Converts a timestamp string or object to human-friendly IST format."""
    if not ts_str:
        return ""
    try:
        ts_clean = str(ts_str).replace("Z", "+00:00")
        if "+" in ts_clean or "-" in ts_clean[10:]:
            dt = datetime.fromisoformat(ts_clean).astimezone(IST)
        else:
            dt = datetime.fromisoformat(ts_clean).replace(tzinfo=IST)
        return dt.strftime("%d %b %Y, %I:%M %p IST")
    except Exception:
        return f"{ts_str} (IST)"

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

def supabase_auth_signup(email: str, password: str, full_name: str, username: str) -> tuple[bool, Optional[dict], str]:
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        return False, None, "Supabase credentials missing."
    url = f"{config.SUPABASE_URL.rstrip('/')}/auth/v1/signup"
    headers = {
        "apikey": config.SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    clean_email = email.strip().lower()
    clean_user = username.strip().lower()
    clean_name = full_name.strip()
    payload = {
        "email": clean_email,
        "password": password.strip(),
        "data": {
            "full_name": clean_name,
            "username": clean_user
        }
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=5)
        if r.status_code in (200, 201):
            data = r.json()
            user_obj = data.get("user", data)
            user_info = {
                "id": user_obj.get("id"),
                "email": clean_email,
                "username": clean_user,
                "full_name": clean_name,
                "created_at": user_obj.get("created_at") or datetime.now().isoformat()
            }
            return True, user_info, "User registered in Supabase Cloud!"
        else:
            err_json = r.json() if r.content else {}
            err = err_json.get("msg") or err_json.get("error_description") or err_json.get("message") or f"Status {r.status_code}"
            return False, None, f"Supabase error: {err}"
    except Exception as e:
        return False, None, f"Supabase connection error: {e}"

def supabase_auth_login(email_or_username: str, password: str) -> tuple[bool, Optional[dict], str]:
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        return False, None, "Supabase credentials missing."
    url = f"{config.SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": config.SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    cleaned = email_or_username.strip().lower()
    candidate_emails = [cleaned]
    if "@" not in cleaned:
        # Also try default domain or query from users table
        candidate_emails.append(f"{cleaned}@plantvision.ai")

    for email_candidate in candidate_emails:
        payload = {
            "email": email_candidate,
            "password": password.strip()
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=4)
            if r.status_code == 200:
                data = r.json()
                user_obj = data.get("user", {})
                user_meta = user_obj.get("user_metadata", {})
                user_info = {
                    "id": user_obj.get("id"),
                    "email": user_obj.get("email", email_candidate),
                    "username": user_meta.get("username", cleaned),
                    "full_name": user_meta.get("full_name", user_meta.get("name", "Farmer")),
                    "created_at": user_obj.get("created_at")
                }
                return True, user_info, "Login successful via Supabase Cloud!"
        except Exception:
            pass

    return False, None, "Invalid username/email or password."

def register_user(username: str, full_name: str, email: str, raw_password: str) -> tuple[bool, Optional[Any], str]:
    clean_user = username.strip().lower()
    clean_email = email.strip().lower()
    clean_name = full_name.strip()
    import auth
    password_hash = auth.hash_password(raw_password)

    # 1. Direct Insert to Supabase public.users Table
    sup_res = _supabase_request("POST", "users", data={
        "username": clean_user,
        "full_name": clean_name,
        "email": clean_email,
        "password_hash": password_hash
    })
    
    sup_id = None
    if sup_res is not None:
        if sup_res.status_code in (200, 201):
            try:
                res_data = sup_res.json()
                if isinstance(res_data, list) and len(res_data) > 0:
                    sup_id = res_data[0].get("id")
            except Exception:
                pass
        elif sup_res.status_code == 409:
            return False, None, "Username or email is already registered in Supabase."

    # 2. Also register in Supabase Auth backend
    supabase_auth_signup(clean_email, raw_password, clean_name, clean_user)

    # 3. Mirror in local SQLite
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (clean_user, clean_name, clean_email, password_hash))
        conn.commit()
        local_id = cursor.lastrowid
        conn.close()
    except Exception:
        local_id = 1

    return True, sup_id or local_id, "User registered successfully in Supabase Cloud!"

def verify_user_credentials(username_or_email: str, raw_password: str) -> tuple[bool, Optional[Dict[str, Any]], str]:
    cleaned = username_or_email.strip().lower()
    import auth
    password_hash = auth.hash_password(raw_password)

    # 1. Check Supabase public.users Table with clean ilike queries
    user_record = None
    
    # Check by email
    res_email = _supabase_request("GET", "users", params={"email": f"ilike.{cleaned}"})
    if res_email is not None and res_email.status_code == 200:
        try:
            records = res_email.json()
            if isinstance(records, list) and len(records) > 0:
                user_record = records[0]
        except Exception:
            pass

    # Check by username if not found by email
    if not user_record:
        res_user = _supabase_request("GET", "users", params={"username": f"ilike.{cleaned}"})
        if res_user is not None and res_user.status_code == 200:
            try:
                records = res_user.json()
                if isinstance(records, list) and len(records) > 0:
                    user_record = records[0]
            except Exception:
                pass

    if user_record:
        stored_hash = str(user_record.get("password_hash", "")).strip()
        input_hash = str(password_hash).strip()
        input_raw = str(raw_password).strip()

        # Match SHA-256 hash or plain text (type-safe string comparison)
        if stored_hash and (stored_hash == input_hash or stored_hash == input_raw):
            user_data = {
                "id": user_record.get("id"),
                "username": user_record.get("username"),
                "full_name": user_record.get("full_name"),
                "email": user_record.get("email"),
                "created_at": user_record.get("created_at")
            }
            return True, user_data, "Login successful!"
        else:
            return False, None, "Incorrect password. Please verify and try again."


    # 2. Check Supabase Auth API
    sup_ok, sup_user, sup_msg = supabase_auth_login(cleaned, raw_password)
    if sup_ok and sup_user:
        return True, sup_user, "Login successful!"


    # 3. Check Local SQLite
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

    ist_time_str = get_ist_now_str()

    # 1. Try Supabase Cloud
    scan_payload = {
        "user_id": int(user_id) if str(user_id).isdigit() else user_id,
        "plant": plant,
        "disease": disease,
        "confidence": float(confidence),
        "severity": severity,
        "is_healthy": bool(is_healthy),
        "image_path": str(image_path),
        "symptoms_json": symptoms_str,
        "remedies_json": remedies_str,
        "timestamp": ist_time_str
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
    elif sup_res is not None:
        print(f"Supabase scan insert failed with status {sup_res.status_code}: {sup_res.text}")

    # 2. Always persist to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (
            user_id, plant, disease, confidence, severity, is_healthy,
            image_path, symptoms_json, remedies_json, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        plant,
        disease,
        float(confidence),
        severity,
        1 if is_healthy else 0,
        str(image_path),
        symptoms_str,
        remedies_str,
        ist_time_str
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
    # 1. Try Supabase Cloud First
    params = {
        "user_id": f"eq.{user_id}",
        "order": "id.desc"
    }
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



