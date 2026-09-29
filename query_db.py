import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
print('--- STATIONS ---')
print(pd.read_sql_query('SELECT station_id, status FROM stations', conn))
print('--- ANOMALIES ---')
print(pd.read_sql_query('SELECT id, station_id, status FROM anomalies ORDER BY detected_at DESC LIMIT 5', conn))
print('--- SENSOR_HEALTH ---')
print(pd.read_sql_query('SELECT station_id, fleet_health_score FROM sensor_health', conn))
conn.close()
