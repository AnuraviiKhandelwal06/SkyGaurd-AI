import sqlite3
conn = sqlite3.connect('skyguard.db')
cur = conn.cursor()
cur.execute("SELECT station_id, event_date, action FROM fault_history")
for row in cur.fetchall():
    print(row)
