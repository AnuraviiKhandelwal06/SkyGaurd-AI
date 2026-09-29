import sqlite3

db_path = 'backend/skyguard.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get a normal reading
cur.execute('''
    SELECT id, station_id, timestamp, temperature, humidity, pressure
    FROM readings 
    WHERE id NOT IN (SELECT reading_id FROM anomalies)
    LIMIT 1
''')
normal = cur.fetchone()
print("Normal candidate:", normal)

# Get an anomalous reading
cur.execute('''
    SELECT r.id, r.station_id, r.timestamp, r.temperature, r.humidity, r.pressure, a.fault_type
    FROM readings r
    JOIN anomalies a ON r.id = a.reading_id
    LIMIT 1
''')
anom = cur.fetchone()
print("Anomaly candidate:", anom)

conn.close()
