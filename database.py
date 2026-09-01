import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
import config

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
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (username.strip().lower(), full_name.strip(), email.strip().lower(), password_hash))
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
    conn = get_connection()
    cursor = conn.cursor()
    cleaned = username_or_email.strip().lower()
    cursor.execute("""
        SELECT id, username, full_name, email, password_hash, created_at
        FROM users
        WHERE (username = ? OR email = ?)
    """, (cleaned, cleaned))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, None, "Account not found for this username or email. If the server recently restarted, please click 'Create New Account' below to register."
    
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
        json.dumps(symptoms),
        json.dumps(remedies)
    ))
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

def get_user_scans(
    user_id: int,
    plant_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    search_term: Optional[str] = None
) -> List[Dict[str, Any]]:
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ? AND user_id = ?", (scan_id, user_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_user_analytics(user_id: int) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans WHERE user_id = ?", (user_id,))
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE user_id = ? AND is_healthy = 1", (user_id,))
    healthy_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE user_id = ? AND is_healthy = 0", (user_id,))
    diseased_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT plant, COUNT(*) as count
        FROM scans
        WHERE user_id = ?
        GROUP BY plant
    """, (user_id,))
    plant_counts = {row["plant"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT disease, COUNT(*) as count
        FROM scans
        WHERE user_id = ? AND is_healthy = 0
        GROUP BY disease
        ORDER BY count DESC
        LIMIT 10
    """, (user_id,))
    disease_counts = {row["disease"]: row["count"] for row in cursor.fetchall()}

    conn.close()

    return {
        "total_scans": total_scans,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "plant_counts": plant_counts,
        "disease_counts": disease_counts
    }

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


