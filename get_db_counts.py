import sqlite3
import os

db_path = 'backend/skyguard.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = ["stations", "readings", "anomalies", "corrections", "sensor_health", "fault_history"]
    for t in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            count = cursor.fetchone()[0]
            print(f"{t}: {count} rows")
        except sqlite3.OperationalError:
            print(f"{t}: TABLE DOES NOT EXIST")
    conn.close()
