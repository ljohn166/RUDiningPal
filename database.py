#puts food combos in SQL db
import sqlite3
import json
from datetime import datetime, date
from typing import List, Dict, Optional
import hashlib

DB_NAME = "dining_combos.db"

def init_db():
    """Initialize the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS combinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dining_hall TEXT NOT NULL,
            meal_time TEXT NOT NULL,
            date TEXT NOT NULL,
            preferences_hash TEXT NOT NULL,
            combinations_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(dining_hall, meal_time, date, preferences_hash)
        )
    """)
    
    conn.commit()
    conn.close()

def get_preference_hash(preferences: List[str]) -> str:
    """Create a hash from preferences for database lookup"""
    sorted_prefs = sorted(preferences) if preferences else []
    pref_string = ",".join(sorted_prefs)
    return hashlib.md5(pref_string.encode()).hexdigest()

def get_combinations(
    dining_hall: str, 
    meal_time: str, 
    date_obj: date, 
    preferences: List[str]
) -> Optional[List[Dict]]:
    """Retrieve cached combinations from database"""
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    date_str = date_obj.isoformat()
    pref_hash = get_preference_hash(preferences)
    
    cursor.execute("""
        SELECT combinations_json FROM combinations
        WHERE dining_hall = ? AND meal_time = ? AND date = ? AND preferences_hash = ?
    """, (dining_hall, meal_time, date_str, pref_hash))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])
    return None

def save_combinations(
    dining_hall: str,
    meal_time: str,
    date_obj: date,
    preferences: List[str],
    combinations: List[Dict]
):
    """Save combinations to database"""
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    date_str = date_obj.isoformat()
    pref_hash = get_preference_hash(preferences)
    combinations_json = json.dumps(combinations)
    
    cursor.execute("""
        INSERT OR REPLACE INTO combinations 
        (dining_hall, meal_time, date, preferences_hash, combinations_json)
        VALUES (?, ?, ?, ?, ?)
    """, (dining_hall, meal_time, date_str, pref_hash, combinations_json))
    
    conn.commit()
    conn.close()

def cleanup_old_combinations():
    """Delete combinations older than today"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    today = datetime.now().date().isoformat()
    
    cursor.execute("DELETE FROM combinations WHERE date < ?", (today,))
    
    conn.commit()
    conn.close()