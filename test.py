import sqlite3

DB_PATH = "geiger.db"


def read_all_readings():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT id, cps, timestamp FROM readings ORDER BY timestamp DESC"
        )

        rows = cursor.fetchall()

    return [
        {"id": r[0], "cps": r[1], "timestamp": r[2]}
        for r in rows
    ]

def clean_db(): 
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM readings;")
        conn.commit()


def test_read_all_readings():
    result = read_all_readings()
    assert result is not None
    assert isinstance(result[1], dict)
    clean_db()

