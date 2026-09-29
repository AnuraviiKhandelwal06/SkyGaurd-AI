import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
cur = conn.cursor()

cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='anomalies'")
print("Anomalies schema:")
print(cur.fetchone()[0])

cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='corrections'")
print("\nCorrections schema:")
print(cur.fetchone()[0])

