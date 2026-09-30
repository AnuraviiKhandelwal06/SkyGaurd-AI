import os, sys
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.station import Station

db = SessionLocal()
print("--- BEFORE ---")
for s in db.query(Station).all():
    print(f"{s.station_id}: {s.latitude}, {s.longitude}, name: {s.location_name}")

aws1 = db.query(Station).filter(Station.station_id == 'AWS-001').first()
if aws1:
    aws1.latitude = 30.25
    aws1.longitude = 74.25
    db.commit()

print("--- AFTER ---")
for s in db.query(Station).all():
    print(f"{s.station_id}: {s.latitude}, {s.longitude}, name: {s.location_name}")
