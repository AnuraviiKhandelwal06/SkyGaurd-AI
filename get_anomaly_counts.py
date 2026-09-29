import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly

db = SessionLocal()

cutoff = datetime.datetime.fromisoformat('2026-09-28T15:00:00')

# anomalies belonging to readings whose verdict was NORMAL
# "fault_type=None" means the classifier mapped it to None or it wasn't a fault.
# But "verdict was NORMAL" implies we should look at the Anomaly rows where fault_type is None.
anoms = db.query(Anomaly).all()

normal_anoms = [a for a in anoms if a.fault_type is None]
print(f"Total anomalies with fault_type=None: {len(normal_anoms)}")

real_anoms = []
test_anoms = []
for a in normal_anoms:
    r = db.query(Reading).filter(Reading.id == a.reading_id).first()
    if r:
        if r.timestamp > cutoff:
            test_anoms.append(a)
        else:
            real_anoms.append(a)

print(f"  REAL readings (fault_type=None): {len(real_anoms)}")
print(f"  TEST readings (fault_type=None): {len(test_anoms)}")

