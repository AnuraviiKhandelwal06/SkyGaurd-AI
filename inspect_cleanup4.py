import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

print("Weather_api ids:")
print(readings[readings['source'] == 'weather_api']['id'].tolist())

