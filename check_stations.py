import sqlite3
import pandas as pd
conn = sqlite3.connect('backend/skyguard.db')
df = pd.read_sql("SELECT station_id, location_name FROM stations", conn)
print(df.to_string())
