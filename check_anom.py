import sqlite3
import pandas as pd
conn = sqlite3.connect('backend/skyguard.db')
df = pd.read_sql("SELECT r.timestamp, r.temperature, a.fault_type, a.status, a.anomaly_score FROM readings r LEFT JOIN anomalies a ON r.id = a.reading_id WHERE r.station_id = 'AWS-002' ORDER BY r.timestamp DESC LIMIT 3", conn)
print(df.to_string())
