import sqlite3
conn = sqlite3.connect('backend/skyguard_backup_20260928_1940.db')
c = conn.cursor()
for table in ['readings', 'anomalies', 'corrections', 'stations']:
    c.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {c.fetchone()[0]}")
conn.close()
