import sqlite3
import pandas as pd
conn = sqlite3.connect('skyguard.db')
print("--- Stale Anomalies ---")
query = "SELECT id, reading_id, station_id, fault_type, detected_at FROM anomalies WHERE fault_type IN ('Unknown Fault', 'Clean', '') OR fault_type IS NULL LIMIT 5"
df = pd.read_sql_query(query, conn)
print(df)

print("\n--- Stations with Unknown/Stale Status ---")
df_st = pd.read_sql_query("SELECT station_id, status FROM stations LIMIT 5", conn)
print(df_st)
conn.close()
