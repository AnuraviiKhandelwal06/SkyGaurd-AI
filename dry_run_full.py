import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import logging
from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

logging.getLogger().setLevel(logging.ERROR)
db = SessionLocal()

# TEST IDs to exclude
test_reading_ids = [348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]

stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']
pipeline = SkyGuardPipeline()
if os.path.exists("skyguard/models/classifier.pkl"):
    pipeline.fault_classifier.load("skyguard/models/classifier.pkl")
    pipeline.temporal_ai.load("skyguard/models/temporal")

all_readings = []
for s in stations:
    readings = db.query(Reading).filter(Reading.station_id == s, ~Reading.id.in_(test_reading_ids)).order_by(Reading.timestamp).all()
    prev = None
    distinct_readings = []
    for r in readings:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev != curr:
            distinct_readings.append(r)
        prev = curr
    all_readings.extend(distinct_readings)

all_readings.sort(key=lambda r: r.timestamp)

histories = {s: [] for s in stations}
verdicts = {s: [] for s in stations}

print("--- 4. DRY RUN RECOMPUTE ---")
for r in all_readings:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    
    # Warm up: only process through diag if history >= 24?
    # Actually, the prompt says "warm up with the earliest 24 readings, then feed AWS-002..005 chronologically together."
    # We just feed them all chronologically. The pipeline naturally warms up (evaluates but maybe lacks history).
    # We will just evaluate them all chronologically, and only print the last 5.
    
    neighbors = {}
    for ns in stations:
        if ns != r.station_id and len(histories[ns]) > 0:
            neighbors[ns] = histories[ns][-1]
            
    pipeline.recent_history = histories[r.station_id].copy()
    diag = pipeline.process_reading(rd, neighbor_readings=neighbors)
    
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
        
    verdicts[r.station_id].append((r.timestamp, r.temperature, r.pressure, r.humidity, diag_type, out_fault, status))

for s in stations:
    print(f"\n{s}:")
    print("  Last 5 Verdicts:")
    for v in verdicts[s][-5:]:
        # v: timestamp, T, P, H, CF, CLF, status
        print(f"    [{v[0]}] T:{v[1]:.1f} P:{v[2]:.1f} H:{v[3]:.1f} | CF:{v[4]} | CLF:{v[5]} -> {v[6]}")
    final_status = verdicts[s][-1][6] if verdicts[s] else "unknown"
    print(f"  Proposed final status: {final_status}")

