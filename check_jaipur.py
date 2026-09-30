import sqlite3
import pandas as pd
conn = sqlite3.connect('backend/skyguard.db')
df = pd.read_sql("SELECT timestamp, temperature, humidity, pressure FROM readings WHERE station_id = 'AWS-002' ORDER BY timestamp DESC LIMIT 5", conn)
print(df.to_string())
