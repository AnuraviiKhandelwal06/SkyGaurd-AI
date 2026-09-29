import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.path.join(os.getcwd(), 'skyguard'))
import logging
logging.getLogger().setLevel(logging.ERROR)

from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

db = SessionLocal()

# Get 5 consecutive real readings for AWS-003 (skip tests > 2026-09-28 15:00)
import datetime
cutoff = datetime.datetime.fromisoformat('2026-09-28T15:00:00')
readings = db.query(Reading).filter(Reading.station_id == 'AWS-003', Reading.timestamp < cutoff).order_by(Reading.timestamp).all()

# Distinct them
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

print("--- 2. HISTORY IN LIVE PATH (AWS-003) ---")

for r in target_readings:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    # (a) Empty history
    pipeline.recent_history = []
    diag_empty = pipeline.process_reading(rd, {})
    v_empty = diag_empty.get("anomaly_type")
    
    # (b) Loaded history from DB
    # Simulate DB load: get up to 24 before this reading
    past = [x for x in distinct_readings if x.timestamp <= r.timestamp][-24:]
    hist = []
    for pr in past:
        hist.append({
            "time": pr.timestamp.isoformat(),
            "temperature_2m": pr.temperature,
            "relative_humidity_2m": pr.humidity,
            "surface_pressure": pr.pressure,
            "pressure_msl": pr.pressure + 20,
            "station_id": pr.station_id
        })
    pipeline.recent_history = hist
    diag_loaded = pipeline.process_reading(rd, {})
    v_loaded = diag_loaded.get("anomaly_type")
    
    print(f"Time:{r.timestamp} T:{r.temperature} | Empty Hist -> {v_empty} | Loaded Hist -> {v_loaded}")

