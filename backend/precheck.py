import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']

print("--- PRECHECK: DUPLICATE COUNT ---")
total_duplicates = 0
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
    duplicates = 0
    prev = None
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            duplicates += 1
        prev = curr
    print(f"{s}: {duplicates} duplicates")
    total_duplicates += duplicates

print(f"Total duplicates remaining: {total_duplicates}")
