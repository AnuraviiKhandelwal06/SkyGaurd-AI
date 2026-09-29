import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
from app.models.correction import Correction

db = SessionLocal()

test_reading_ids = list(range(348, 364)) + list(range(375, 391))
# Actually, wait, let's just query them
test_readings = db.query(Reading).filter(Reading.id.in_(test_reading_ids)).all()

test_r_ids = [r.id for r in test_readings]
anoms = db.query(Anomaly).filter(Anomaly.reading_id.in_(test_r_ids)).all()
test_a_ids = [a.id for a in anoms]
corrs = db.query(Correction).filter(Correction.anomaly_id.in_(test_a_ids)).all()
test_c_ids = [c.id for c in corrs]

print(f"TEST Reading IDs ({len(test_r_ids)}): {test_r_ids}")
print(f"Cascading Anomaly IDs ({len(test_a_ids)}): {test_a_ids}")
print(f"Cascading Correction IDs ({len(test_c_ids)}): {test_c_ids}")
