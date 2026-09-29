import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

dupes = readings[readings.duplicated(subset=['station_id', 'timestamp'], keep=False)]
print("Total rows involved in duplicates:", len(dupes))
print("Unique timestamps involved:", len(dupes[['station_id', 'timestamp']].drop_duplicates()))

