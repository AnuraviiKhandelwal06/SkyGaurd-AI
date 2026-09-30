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

try:
    total_to_delete_readings = []
    for s in stations:
        readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
        prev = None
        for r in readings:
            curr = (r.temperature, r.pressure, r.humidity)
            if prev == curr:
                total_to_delete_readings.append(r)
            prev = curr
            
    dupe_ids = [r.id for r in total_to_delete_readings]
    anomalies = db.query(Anomaly).filter(Anomaly.reading_id.in_(dupe_ids)).all() if dupe_ids else []
    anomaly_ids = [a.id for a in anomalies]
    corrections = db.query(Correction).filter(Correction.anomaly_id.in_(anomaly_ids)).all() if anomaly_ids else []
    
    r_count = len(total_to_delete_readings)
    a_count = len(anomalies)
    c_count = len(corrections)
    
    print(f"Attempting delete: {r_count} readings, {a_count} anomalies, {c_count} corrections")
    
    if r_count != 115 or a_count != 15 or c_count != 6:
        print("Count mismatch! Rolling back.")
        db.rollback()
    else:
        # DO NOT DO IT IF MISMATCH
        pass
except Exception as e:
    db.rollback()
    print("Error:", e)
