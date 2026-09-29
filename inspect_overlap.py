import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT id, station_id, timestamp, source FROM readings ORDER BY id", conn)

# The user explicitly said:
# "TEST_ONLY count
# DUPLICATE_ONLY count
# OVERLAP count
# TOTAL = 142"

# So there is a category called OVERLAP!
# Let's find overlapping readings.
# What is OVERLAP? Maybe overlapping times across stations? No, overlap between physical_sensor and weather_api?
# Wait! "duplicate evidence where applicable"
# If a station has a reading at the same timestamp from physical_sensor and weather_api.
dupes_overlap = readings.duplicated(subset=['station_id', 'timestamp'], keep=False)
overlap_rows = readings[dupes_overlap]
print("Rows sharing station_id and timestamp:")
print(overlap_rows.sort_values(['station_id', 'timestamp']))
