import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

# Ignore AWS-001 completely
target = readings[readings['station_id'] != 'AWS-001']

# Let's see DUPLICATES in target (same station_id and timestamp)
target_sorted = target.sort_values('id')
dupes_mask = target_sorted.duplicated(subset=['station_id', 'timestamp'], keep='first')
dupes = target_sorted[dupes_mask]
print("DUPLICATE_ONLY count:", len(dupes))

# Let's see TEST_ONLY in target
# Based on provenance: source == 'weather_api' maybe? Or generated from manual runs.
# Previously I might have classified them by some specific timestamps or source values.
# Let's count how many have timestamp > '2026-09-28' (future/test mock rows)
# Wait, some test mock rows might have '2026-09-27' but were generated manually.
# "source is hardcoded physical_sensor but IDs 364..374 are weather_api"
# Let's check source values in target.
print("Target sources:")
print(target['source'].value_counts(dropna=False))

# What if we delete all target rows where source == 'weather_api'?
weather_api_target = target[target['source'] == 'weather_api']
print("weather_api in target count:", len(weather_api_target))

# What if the 142 rows = weather_api (some number) + duplicates?
# Let's print out the categories.
