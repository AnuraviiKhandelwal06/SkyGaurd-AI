import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from app.models.anomaly import Anomaly
from app.models.correction import Correction

db = SessionLocal()
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']

print("--- A.2 RECOUNT LIVE ---")
total_dupes = 0
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
    to_delete = []
    prev = None
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            to_delete.append(r)
        prev = curr
        
    dupe_ids = [r.id for r in to_delete]
    anomalies = db.query(Anomaly).filter(Anomaly.reading_id.in_(dupe_ids)).all() if dupe_ids else []
    anomaly_ids = [a.id for a in anomalies]
    corrections = db.query(Correction).filter(Correction.anomaly_id.in_(anomaly_ids)).all() if anomaly_ids else []
    
    print(f"{s}: {len(to_delete)} readings, {len(anomalies)} anomalies, {len(corrections)} corrections")
    total_dupes += len(to_delete)
    
    if s == 'AWS-002' and len(to_delete) >= 2:
        print("  Newest 2 AWS-002 duplicates:")
        for r in to_delete[-2:]:
            print(f"    ID: {r.id}, Timestamp: {r.timestamp}")
            
print(f"Total readings to delete: {total_dupes}")
