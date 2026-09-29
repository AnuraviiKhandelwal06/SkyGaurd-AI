import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

# Let's find overlaps between physical_sensor and weather_api
phys = readings[readings['source'] == 'physical_sensor']
wapi = readings[readings['source'] == 'weather_api']

overlap = pd.merge(phys, wapi, on=['station_id', 'timestamp'], suffixes=('_phys', '_wapi'))
print("OVERLAP count:", len(overlap))
print(overlap[['station_id', 'timestamp']])

