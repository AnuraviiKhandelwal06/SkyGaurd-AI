import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

target = readings[readings['station_id'] != 'AWS-001']

weather_api_target = target[target['source'] == 'weather_api']
print("weather_api in target (TEST_ONLY):", len(weather_api_target))

# Duplicates in target
target_phys = target[target['source'] == 'physical_sensor']
target_phys_sorted = target_phys.sort_values('id')
dupes_mask = target_phys_sorted.duplicated(subset=['station_id', 'timestamp'], keep='first')
dupes_target = target_phys_sorted[dupes_mask]
print("DUPLICATE_ONLY in target (physical_sensor):", len(dupes_target))

print("Total =", len(weather_api_target) + len(dupes_target))
