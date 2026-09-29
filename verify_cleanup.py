import sqlite3

db_path = 'backend/skyguard.db'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

r = cur.execute('SELECT count(*) FROM readings').fetchone()[0]
a = cur.execute('SELECT count(*) FROM anomalies').fetchone()[0]
c = cur.execute('SELECT count(*) FROM corrections').fetchone()[0]

print(f"Readings: {r}")
print(f"Anomalies: {a}")
print(f"Corrections: {c}")
conn.close()
