import os, sys
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly

db = SessionLocal()
r = db.query(Reading).filter(Reading.id == 275).first()
if r:
    print(f"Before delete: Reading 275 exists (Temp: {r.temperature}, Station: {r.station_id})")
    a = db.query(Anomaly).filter(Anomaly.reading_id == 275).first()
    if a:
        print(f"Before delete: Anomaly {a.id} exists for reading 275")
        db.delete(a)
    db.delete(r)
    db.commit()
    print("Deleted.")
else:
    print("Reading 275 not found.")
