import shutil
import sqlite3
import datetime
import os
import csv

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
src = 'skyguard.db'
dst = f'skyguard_backup_{timestamp}_precleanup2.db'
shutil.copy2(src, dst)

conn = sqlite3.connect(dst)
cur = conn.cursor()
tables = ['stations', 'readings', 'anomalies', 'corrections', 'sensor_health', 'fault_history']
print(f"Backup created: {dst}")
print("Row counts:")
for t in tables:
    cur.execute(f"SELECT count(*) FROM {t}")
    print(f"  {t}: {cur.fetchone()[0]}")

export_dir = f"cleanup_exports_{timestamp}"
os.makedirs(export_dir, exist_ok=True)

# Identify rows to delete (AWS-002..005)
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']
to_delete_readings = []
for s in stations:
    cur.execute("SELECT * FROM readings WHERE station_id = ? ORDER BY timestamp", (s,))
    rows = cur.fetchall()
    prev = None
    for row in rows:
        # row: id(0), station_id(1), timestamp(2), temperature(3), humidity(4), pressure(5)
        curr = (row[3], row[5], row[4]) # T, P, H
        if prev == curr:
            to_delete_readings.append(row)
        prev = curr

reading_ids = [str(r[0]) for r in to_delete_readings]
if reading_ids:
    q = ",".join(reading_ids)
    cur.execute(f"SELECT * FROM anomalies WHERE reading_id IN ({q})")
    to_delete_anomalies = cur.fetchall()
    
    anomaly_ids = [str(a[0]) for a in to_delete_anomalies]
    to_delete_corrections = []
    if anomaly_ids:
        aq = ",".join(anomaly_ids)
        cur.execute(f"SELECT * FROM corrections WHERE anomaly_id IN ({aq})")
        to_delete_corrections = cur.fetchall()
else:
    to_delete_anomalies = []
    to_delete_corrections = []

def write_csv(filename, table_name, data):
    cur.execute(f"PRAGMA table_info({table_name})")
    headers = [col[1] for col in cur.fetchall()]
    path = os.path.join(export_dir, filename)
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Exported {len(data)} rows to {path}")

write_csv("readings_to_delete.csv", "readings", to_delete_readings)
write_csv("anomalies_to_delete.csv", "anomalies", to_delete_anomalies)
write_csv("corrections_to_delete.csv", "corrections", to_delete_corrections)

conn.close()
