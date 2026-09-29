import sys
import os
import shutil
import datetime

sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Step 0: Copy DB and recount
src = 'backend/skyguard.db'
dst = 'backend/skyguard_test.db'
shutil.copy2(src, dst)

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from app.models.anomaly import Anomaly
from app.models.correction import Correction
from app.models.sensor_health import SensorHealth
from app.models.fault_history import FaultHistory

db = SessionLocal()
print("--- 0. ROW COUNTS ---")
for t, m in [('stations', Station), ('readings', Reading), ('anomalies', Anomaly), 
             ('corrections', Correction), ('sensor_health', SensorHealth), ('fault_history', FaultHistory)]:
    print(f"  {t}: {db.query(m).count()}")

print("\n--- 1. TEST ROWS ---")
now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
test_readings = db.query(Reading).filter(Reading.timestamp > now).all()

# anomaly 146
a146 = db.query(Anomaly).filter(Anomaly.id >= 134).all() # Just grab all recent ones

# Collect readings from anomalies if not already in test_readings
r_ids = {r.id for r in test_readings}
for a in a146:
    if a.reading_id not in r_ids:
        r = db.query(Reading).filter(Reading.id == a.reading_id).first()
        if r:
            test_readings.append(r)
            r_ids.add(r.id)

for r in test_readings:
    print(f"Reading ID:{r.id} | Station:{r.station_id} | Time:{r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
    anoms = db.query(Anomaly).filter(Anomaly.reading_id == r.id).all()
    for a in anoms:
        print(f"  -> Anomaly ID:{a.id} FaultType:{a.fault_type}")
        corrs = db.query(Correction).filter(Correction.anomaly_id == a.id).all()
        for c in corrs:
            print(f"    -> Correction ID:{c.id}")

