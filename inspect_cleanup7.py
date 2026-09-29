import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings WHERE source = 'weather_api'", conn)

print("Total weather_api:", len(readings))

# Group by timestamp patterns?
print("Min timestamp:", readings['timestamp'].min())
print("Max timestamp:", readings['timestamp'].max())
