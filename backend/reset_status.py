import sqlite3

conn = sqlite3.connect('skyguard.db')
c = conn.cursor()
c.execute("UPDATE stations SET status = 'healthy'")
conn.commit()
conn.close()
print("Reset station status to healthy.")
