import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.fault_history import FaultHistory

db = SessionLocal()
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']

total_to_delete_readings = []
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
    prev = None
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            total_to_delete_readings.append(r)
        prev = curr

print("--- FAULT HISTORY MATCHING DELETED READINGS ---")
count = 0
for r in total_to_delete_readings:
    fhs = db.query(FaultHistory).filter(
        FaultHistory.station_id == r.station_id,
        FaultHistory.event_date == r.timestamp.date()
    ).all()
    for fh in fhs:
        print(f"Station: {fh.station_id}, Date: {fh.event_date}, Action: {fh.action}")
        count += 1
print(f"Total matching fault_history rows: {count}")
