import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''
    SELECT a.status, a.fault_type, COUNT(c.id) as correction_count
    FROM anomalies a
    LEFT JOIN corrections c ON c.anomaly_id = a.id
    GROUP BY a.status, a.fault_type
''')
for row in c.fetchall():
    print(dict(row))
conn.close()
