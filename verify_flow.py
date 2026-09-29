import requests
import sqlite3
import pandas as pd

# Fetch from DB
conn = sqlite3.connect('backend/skyguard.db')
db_stations = pd.read_sql_query("SELECT station_id, status FROM stations", conn).set_index('station_id')
db_anomalies = pd.read_sql_query('''
SELECT a.station_id, a.status as anom_status, c.id as corr_id 
FROM anomalies a 
LEFT JOIN corrections c ON a.id = c.anomaly_id 
GROUP BY a.station_id 
HAVING a.detected_at = MAX(a.detected_at)
''', conn).set_index('station_id')
conn.close()

# Fetch from API
resp = requests.get('http://localhost:8000/predict/all')
api_data = resp.json()

print(f"{'Station':<10} | {'DB Status':<12} | {'API Status':<12} | {'Overview Count':<14} | {'Live Stations':<14} | {'Correction?'}")
print("-" * 85)

for st in api_data:
    sid = st['station_id']
    api_status = st['status']
    db_status = db_stations.loc[sid, 'status'] if sid in db_stations.index else 'Unknown'
    
    if sid in db_anomalies.index:
        corr_id = db_anomalies.loc[sid, 'corr_id']
        has_corr = 'Yes' if not pd.isna(corr_id) else 'No'
    else:
        has_corr = 'No'
        
    # Overview logic: uses stations table
    ov_status = db_status.capitalize()
    
    # Live Stations uses API status
    ls_status = api_status
    
    print(f"{sid:<10} | {db_status:<12} | {api_status:<12} | {ov_status:<14} | {ls_status:<14} | {has_corr}")
