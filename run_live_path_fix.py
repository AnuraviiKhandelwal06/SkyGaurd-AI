import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.path.join(os.getcwd(), 'skyguard'))
import logging
logging.getLogger().setLevel(logging.ERROR)

from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline
import datetime

db = SessionLocal()

cutoff = datetime.datetime.fromisoformat('2026-09-28T15:00:00')
readings = db.query(Reading).filter(Reading.station_id == 'AWS-003', Reading.timestamp < cutoff).order_by(Reading.timestamp).all()

prev = None
distinct_readings = []
for r in readings:
    curr = (r.temperature, r.pressure, r.humidity)
    if prev != curr:
        distinct_readings.append(r)
    prev = curr

target_readings = distinct_readings[-5:]

pipeline = SkyGuardPipeline()
if os.path.exists("skyguard/models/classifier.pkl"):
    pipeline.fault_classifier.load("skyguard/models/classifier.pkl")
    pipeline.temporal_ai.load("skyguard/models/temporal")

print("--- 2. HISTORY WINDOW FIX (AWS-003) ---")

for r in target_readings:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    
    # OLD LOGIC: <= r.timestamp
    past_old = [x for x in distinct_readings if x.timestamp <= r.timestamp][-24:]
    hist_old = []
    for pr in past_old:
        hist_old.append({
            "time": pr.timestamp.isoformat(), "temperature_2m": pr.temperature,
            "relative_humidity_2m": pr.humidity, "surface_pressure": pr.pressure,
            "pressure_msl": pr.pressure + 20, "station_id": pr.station_id
        })
    pipeline.recent_history = hist_old
    diag_old = pipeline.process_reading(rd, {})
    v_old = diag_old.get("anomaly_type")
    if diag_old.get("diagnosis", {}).get("diagnosis_type") == "NORMAL": v_old = "CLEAN"
    
    # NEW LOGIC: < r.timestamp
    past_new = [x for x in distinct_readings if x.timestamp < r.timestamp][-23:]
    hist_new = []
    for pr in past_new:
        hist_new.append({
            "time": pr.timestamp.isoformat(), "temperature_2m": pr.temperature,
            "relative_humidity_2m": pr.humidity, "surface_pressure": pr.pressure,
            "pressure_msl": pr.pressure + 20, "station_id": pr.station_id
        })
    pipeline.recent_history = hist_new
    diag_new = pipeline.process_reading(rd, {})
    v_new = diag_new.get("anomaly_type")
    if diag_new.get("diagnosis", {}).get("diagnosis_type") == "NORMAL": v_new = "CLEAN"
    
    print(f"[{r.timestamp}] T:{r.temperature:.1f} P:{r.pressure:.1f} H:{r.humidity:.1f} | Old (Buggy) -> {v_old} | New (Fixed) -> {v_new}")

