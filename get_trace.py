import sqlite3
import json

conn = sqlite3.connect('backend/skyguard.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''
    SELECT r.id, r.station_id, r.temperature, r.humidity, r.pressure,
           a.fault_type, a.anomaly_score, a.status,
           c.corrected_value
    FROM readings r
    JOIN anomalies a ON a.reading_id = r.id
    LEFT JOIN corrections c ON c.anomaly_id = a.id
    ORDER BY r.timestamp DESC LIMIT 1
''')
row = c.fetchone()
if row:
    print(dict(row))
else:
    print("No anomaly reading found.")
conn.close()
