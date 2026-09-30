import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station

db = SessionLocal()
stations = db.query(Station).all()

print("--- STATION READINGS ANALYSIS ---")
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s.station_id).order_by(Reading.timestamp).all()
    duplicates = 0
    prev = None
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            duplicates += 1
        prev = curr
        
    total = len(readings)
    print(f"\n{s.station_id}: {total} total readings, {duplicates} sequential duplicates")
    
    recent = readings[-6:]
    print("Last 6 readings:")
    for r in reversed(recent):
        print(f"  {r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
