import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from sqlalchemy import func

db = SessionLocal()
stations = db.query(Station).all()

print("--- STATION READINGS ANALYSIS ---")
for s in stations:
    total = db.query(Reading).filter(Reading.station_id == s.station_id).count()
    distinct = db.query(Reading.timestamp).filter(Reading.station_id == s.station_id).distinct().count()
    duplicates = total - distinct
    
    print(f"\n{s.station_id}: {total} total readings, {duplicates} duplicates")
    
    recent = db.query(Reading).filter(Reading.station_id == s.station_id).order_by(Reading.timestamp.desc()).limit(6).all()
    print("Last 6 readings:")
    for r in recent:
        print(f"  {r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
