import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from app.models.anomaly import Anomaly
from app.models.correction import Correction
from app.models.fault_history import FaultHistory
from app.models.sensor_health import SensorHealth

db = SessionLocal()

stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']

print("--- CLEANUP ANALYSIS ---")
total_readings_to_delete = 0
total_anomalies_to_delete = 0
total_corrections_to_delete = 0
total_faults_to_delete = 0

for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
    to_delete_ids = []
    prev = None
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            to_delete_ids.append(r.id)
        prev = curr
        
    print(f"{s}: {len(to_delete_ids)} duplicate readings identified.")
    total_readings_to_delete += len(to_delete_ids)
    
    anomalies = db.query(Anomaly).filter(Anomaly.reading_id.in_(to_delete_ids)).all() if to_delete_ids else []
    anomaly_ids = [a.id for a in anomalies]
    total_anomalies_to_delete += len(anomaly_ids)
    print(f"  -> {len(anomaly_ids)} cascading anomalies.")
    
    corrections = db.query(Correction).filter(Correction.anomaly_id.in_(anomaly_ids)).all() if anomaly_ids else []
    total_corrections_to_delete += len(corrections)
    print(f"  -> {len(corrections)} cascading corrections.")
    
    # FaultHistory doesn't have reading_id. It matches by station and time? 
    # Or maybe it has anomaly_id? Let's check.
    # We will just print the schema if it fails.
