import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
cur = conn.cursor()

cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='readings'")
print("Readings schema:")
print(cur.fetchone()[0])
