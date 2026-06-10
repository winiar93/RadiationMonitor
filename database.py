import sqlite3
from datetime import datetime
from models import GeigerReading


DB_PATH = "geiger.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cps INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)


def save_reading(reading: GeigerReading):

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO readings (cps, timestamp) VALUES (?, ?)",
            (reading.cps, reading.timestamp.isoformat())
        )


def cleanup_old_rows():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM readings
            WHERE timestamp < datetime('now', '-24 hours')
        """)