import os, sys
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.anomaly import Anomaly
from app.models.correction import Correction
db = SessionLocal()

print("Any correction rows linked to Warning or Healthy anomalies?")
res = db.query(Correction).join(Anomaly).filter(Anomaly.status.in_(["warning", "resolved"])).all()
if len(res) == 0:
    print("None found.")
else:
    for c in res:
        print(f"Correction ID: {c.id}, Anomaly Status: {c.anomaly.status}")
