import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
# Delete readings from the future
cur = conn.cursor()
cur.execute("DELETE FROM readings WHERE timestamp > '2027-01-01'")
deleted_readings = cur.rowcount
cur.execute("DELETE FROM anomalies WHERE reading_timestamp > '2027-01-01'")
deleted_anomalies = cur.rowcount
conn.commit()
conn.close()

print(f"Deleted {deleted_readings} rogue future readings.")
print(f"Deleted {deleted_anomalies} rogue future anomalies.")
