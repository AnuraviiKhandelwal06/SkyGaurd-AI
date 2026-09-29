import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

# 1. Duplicates
readings_sorted = readings.sort_values('id')
dupes_mask = readings_sorted.duplicated(subset=['station_id', 'timestamp'], keep='first')
duplicate_ids = set(readings_sorted[dupes_mask]['id'])

# 2. Test Only (Future timestamps? Or specific patterns?)
# The user mentioned "timestamp later than current UTC now (including the 2030-01-01 row, IDs 357, 358)"
# Let's check rows with timestamp > '2026-09-28' or something.
# Also, maybe specific values like T=99.0? Or maybe there's a specific timestamp threshold?
now_utc_approx = '2025' # Let's see all timestamps
print(readings['timestamp'].max())
print(readings['timestamp'].min())

# Let's inspect IDs 340 to 390
print(readings[(readings['id'] >= 340) & (readings['id'] <= 390)][['id', 'station_id', 'timestamp', 'source', 'temperature', 'humidity', 'pressure']])

