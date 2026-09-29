import sqlite3

db_path = 'backend/skyguard.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('''
    SELECT r.id, r.station_id, r.timestamp, r.temperature, r.humidity, r.pressure, a.fault_type, a.status
    FROM readings r
    JOIN anomalies a ON r.id = a.reading_id
    WHERE a.fault_type IS NOT NULL
    LIMIT 3
''')
for row in cur.fetchall():
    print(row)

conn.close()
