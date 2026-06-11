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
            (reading.cps, reading.timestamp.isoformat()),
        )


def cleanup_old_rows():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            DELETE FROM readings
            WHERE timestamp < datetime('now', '-24 hours')
        """)


def get_recent_readings(limit: int | None = None, hours: int | None = None, ma_window: int = 8):
    with sqlite3.connect(DB_PATH) as conn:
        inner = f"""
            SELECT *,
                   AVG(cps) OVER (
                       ORDER BY timestamp
                       ROWS BETWEEN {ma_window - 1} PRECEDING AND CURRENT ROW
                   ) AS cps_ma
            FROM readings
        """
        if hours:
            inner += f" WHERE timestamp >= datetime('now', '-{hours} hours')"

        query = f"SELECT * FROM ({inner}) ORDER BY timestamp DESC"

        if limit:
            query += f" LIMIT {limit}"

        query = f"SELECT * FROM ({query}) ORDER BY timestamp ASC"

        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
