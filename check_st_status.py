import sqlite3
import pandas as pd
conn = sqlite3.connect('backend/skyguard.db')
df = pd.read_sql("SELECT station_id, status FROM stations WHERE station_id = 'AWS-002'", conn)
print(df.to_string())
