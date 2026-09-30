import shutil
import sqlite3
import datetime

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
src = 'skyguard.db'
dst = f'skyguard_backup_{timestamp}_precleanup.db'
shutil.copy2(src, dst)

conn = sqlite3.connect(dst)
cur = conn.cursor()
tables = ['stations', 'readings', 'anomalies', 'corrections', 'sensor_health', 'fault_history']
print(f"Backup created: {dst}")
print("Row counts:")
for t in tables:
    cur.execute(f"SELECT count(*) FROM {t}")
    print(f"  {t}: {cur.fetchone()[0]}")
conn.close()
