import sqlite3
import os

# Delete state file
state_file = 'backend/data/csv_state.txt'
if os.path.exists(state_file):
    os.remove(state_file)

# Clear readings for AWS-001
conn = sqlite3.connect('backend/skyguard.db')
conn.execute("DELETE FROM readings WHERE station_id = 'AWS-001'")
conn.execute("DELETE FROM anomalies WHERE station_id = 'AWS-001'")
conn.commit()
conn.close()
print("Cleaned up!")
