import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute("
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ")
    
    # Scans Table
    cursor.execute("
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
    ")
    
    conn.commit()
    conn.close()

def register_user(username, full_name, email, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            INSERT INTO users (username, full_name, email, password_hash) VALUES (?, ?, ?, ?),
            (username.strip().lower(), full_name.strip(), email.strip().lower(), password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return True, user_id, Registration successful!
    except sqlite3.IntegrityError as e:
        if username in str(e).lower():
            return False, None, Username already exists. Please choose another.
        elif email in str(e).lower():
            return False, None, Email is already registered.
        return False, None, Registration failed: Duplicate user entry.
    finally:
        conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SELECT * FROM users WHERE username = ?, (username.strip().lower(),))
    user = cursor.fetchone()
    conn.close()
    return user

def save_scan(user_id, plant, disease, confidence, severity, is_healthy, image_path, symptoms=None, remedies=None):
    conn = get_connection()
    cursor = conn.cursor()
    symptoms_str = json.dumps(symptoms or [])
    remedies_str = json.dumps(remedies or {})
    
    cursor.execute("
        INSERT INTO scans (user_id, plant, disease, confidence, severity, is_healthy, image_path, symptoms_json, remedies_json, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ", (
        user_id, plant, disease, confidence, severity, 1 if is_healthy else 0,
        image_path, symptoms_str, remedies_str, datetime.now().strftime(%Y-%m-%d %H:%M:%S)
    ))
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id

def get_user_scans(user_id, plant_filter=None, status_filter=None, search_term=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = SELECT * FROM scans WHERE user_id = ?
    params = [user_id]
    
    if plant_filter and plant_filter.lower() != all:
        query +=  AND LOWER(plant) = ?
        params.append(plant_filter.lower())
        
    if status_filter and status_filter.lower() != all:
        if status_filter.lower() == healthy:
            query +=  AND is_healthy = 1
        elif status_filter.lower() == diseased:
            query +=  AND is_healthy = 0
            
    if search_term:
        query +=  AND (LOWER(disease) LIKE ? OR LOWER(plant) LIKE ?)
        term = f%{search_term.lower()}%
        params.extend([term, term])
        
    query +=  ORDER BY timestamp DESC
    
    cursor.execute(query, params)
    scans = cursor.fetchall()
    conn.close()
    return scans

def delete_scan(scan_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(DELETE FROM scans WHERE id = ? AND user_id = ?, (scan_id, user_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_user_analytics(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total Scans
    cursor.execute(SELECT COUNT(*) FROM scans WHERE user_id = ?, (user_id,))
    total_scans = cursor.fetchone()[0]
    
    # Healthy vs Diseased
    cursor.execute(SELECT is_healthy, COUNT(*) FROM scans WHERE user_id = ? GROUP BY is_healthy, (user_id,))
    health_counts = dict(cursor.fetchall())
    healthy_count = health_counts.get(1, 0)
    diseased_count = health_counts.get(0, 0)
    
    # Plant distribution
    cursor.execute(SELECT plant, COUNT(*) FROM scans WHERE user_id = ? GROUP BY plant, (user_id,))
    plant_counts = dict(cursor.fetchall())
    
    # Disease distribution
    cursor.execute(SELECT disease, COUNT(*) FROM scans WHERE user_id = ? AND is_healthy = 0 GROUP BY disease ORDER BY COUNT(*) DESC, (user_id,))
    disease_counts = dict(cursor.fetchall())
    
    # Recent scans over time
    cursor.execute(SELECT DATE(timestamp) as scan_date, COUNT(*) FROM scans WHERE user_id = ? GROUP BY DATE(timestamp) ORDER BY scan_date ASC, (user_id,))
    timeline = cursor.fetchall()
    
    conn.close()
    return {
        total_scans: total_scans,
        healthy_count: healthy_count,
        diseased_count: diseased_count,
        plant_counts: plant_counts,
        disease_counts: disease_counts,
        timeline: timeline
    }
