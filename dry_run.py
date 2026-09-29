import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.path.join(os.getcwd(), 'skyguard'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from app.models.anomaly import Anomaly
from app.models.correction import Correction
from skyguard.main_pipeline import SkyGuardPipeline
import logging

logging.getLogger().setLevel(logging.ERROR)

db = SessionLocal()
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']

all_readings = []
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s).order_by(Reading.timestamp).all()
    prev = None
    distinct_readings = []
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev != curr:
            distinct_readings.append(r)
        prev = curr
    all_readings.extend(distinct_readings)

all_readings.sort(key=lambda r: r.timestamp)

pipeline = SkyGuardPipeline()
if os.path.exists("skyguard/models/classifier.pkl"):
    pipeline.fault_classifier.load_model("skyguard/models/classifier.pkl")
    pipeline.temporal_ai.load_model("skyguard/models/temporal_sklearn.pkl")

histories = {s: [] for s in stations}
verdicts = {s: [] for s in stations}

print("--- B. DRY RUN RECOMPUTE ---")
for r in all_readings:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    neighbors = {}
    for ns in stations:
        if ns != r.station_id and len(histories[ns]) > 0:
            neighbors[ns] = histories[ns][-1]
            
    pipeline.recent_history = histories[r.station_id].copy()
    diag = pipeline.process_reading(rd, neighbors)
    
    histories[r.station_id].append(rd)
    if len(histories[r.station_id]) > 24:
        histories[r.station_id].pop(0)
        
    diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
    out_fault = diag.get("anomaly_type")
    
    if diag_type == "NORMAL":
        status = "healthy"
    elif diag_type == "GENUINE_EXTREME_EVENT":
        status = "warning"
    else:
        status = "faulty"
        
    verdicts[r.station_id].append((diag_type, out_fault, status))

for s in stations:
    print(f"\n{s}:")
    print("  Last 5 Verdicts:")
    for v in verdicts[s][-5:]:
        print(f"    CF:{v[0]} | CLF:{v[1]} -> {v[2]}")
    final_status = verdicts[s][-1][2] if verdicts[s] else "unknown"
    print(f"  Proposed final status: {final_status}")

print("\n--- STALE ROWS ---")
stale_anomalies = db.query(Anomaly).filter(Anomaly.fault_type == None).all()
print(f"Stale anomalies (fault_type=None): {len(stale_anomalies)}")

stale_corrections = []
corrections = db.query(Correction).all()
for c in corrections:
    st_status = c.anomaly.reading.station.status.value
    if st_status in ['healthy', 'warning']:
        stale_corrections.append(c)
print(f"Stale corrections (on healthy/warning stations): {len(stale_corrections)}")

