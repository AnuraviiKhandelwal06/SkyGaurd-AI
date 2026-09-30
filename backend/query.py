import sqlite3
conn = sqlite3.connect('C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/backend/skyguard.db')
c = conn.cursor()
c.execute("SELECT status, count(*) FROM stations GROUP BY status")
print('Stations:', c.fetchall())
c.execute("SELECT status, count(*) FROM anomalies GROUP BY status")
print('Anomalies:', c.fetchall())
c.execute("SELECT fault_type, count(*) FROM anomalies GROUP BY fault_type")
print('Faults:', c.fetchall())
