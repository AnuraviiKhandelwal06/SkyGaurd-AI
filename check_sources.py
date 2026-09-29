import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT id, station_id, timestamp, source FROM readings", conn)
print(readings['source'].value_counts(dropna=False))

# From previous logs, there were exactly 142 readings to be deleted.
# Let's find exactly which ones.
# Previously: "115 readings, 15 anomalies, 6 corrections." wait, if the total READING IDs to delete is 142...
