import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
cur = conn.cursor()
r_count = cur.execute('SELECT count(*) FROM readings').fetchone()[0]
print("Reading_count in skyguard.db:", r_count)
