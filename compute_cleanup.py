import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
cur = conn.cursor()

# Get baseline
cur.execute("SELECT count(*), max(id) FROM readings")
r_count, r_max = cur.fetchone()
cur.execute("SELECT count(*) FROM anomalies")
a_count = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM corrections")
c_count = cur.fetchone()[0]
print(f"BASELINE: Readings={r_count} Max={r_max} Anomalies={a_count} Corrections={c_count}")

readings = pd.read_sql_query("SELECT id, station_id, timestamp, source FROM readings", conn)

# Identify TEST_ONLY
# The user mentioned previously: "IDs 364..374 are weather_api" and "for EVERY reading id, classify REAL or TEST. Show the source column value, timestamp and T/P/H for IDs 340 to 390."
# Let's see what has source != 'physical_sensor' or is known test.
test_only = readings[readings['source'] != 'physical_sensor']
print(f"Found {len(test_only)} rows with source != 'physical_sensor'")

# Identify DUPLICATES (keep first occurrence)
# Sort by id so the first inserted is kept
readings_real = readings[readings['source'] == 'physical_sensor'].sort_values('id')
dupes_mask = readings_real.duplicated(subset=['station_id', 'timestamp'], keep='first')
duplicate_only = readings_real[dupes_mask]
print(f"Found {len(duplicate_only)} duplicate rows in real data")

# Let's just output all IDs grouped by station and source to see what's what.
for st in readings['station_id'].unique():
    r_st = readings[readings['station_id'] == st]
    print(f"{st}: {len(r_st)} rows")

all_proposed = set(test_only['id']).union(set(duplicate_only['id']))
print(f"Total proposed IDs: {len(all_proposed)}")
