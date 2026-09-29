import sqlite3
import pandas as pd
conn = sqlite3.connect('backend/skyguard.db')
df = pd.read_sql("SELECT * FROM readings WHERE station_id = 'AWS-001' ORDER BY timestamp DESC LIMIT 20", conn)
print(df.to_string())
