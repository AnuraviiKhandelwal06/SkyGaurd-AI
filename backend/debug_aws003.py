import sys
import os
import pandas as pd
import json

sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

db = SessionLocal()
pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard/models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))

station_id = 'AWS-003'
past_readings = db.query(Reading).filter(Reading.station_id == station_id).order_by(Reading.timestamp.desc()).limit(24).all()
past_readings.reverse()

hist = []
for r in past_readings:
    hist.append({
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": station_id
    })

pipeline.recent_history = hist

reading = hist[-1].copy()
# simulate next reading slightly changed
reading['temperature_2m'] += 0.1
reading['time'] = "2026-09-28T20:00:00"

neighbors = {
    "AWS-N1": {"temperature_2m": reading['temperature_2m'] + 0.1, "relative_humidity_2m": reading['relative_humidity_2m'] - 1, "surface_pressure": reading['surface_pressure'] + 1, "pressure_msl": reading['pressure_msl'] + 21},
    "AWS-N2": {"temperature_2m": reading['temperature_2m'] - 0.2, "relative_humidity_2m": reading['relative_humidity_2m'] + 1, "surface_pressure": reading['surface_pressure'] - 1, "pressure_msl": reading['pressure_msl'] + 19},
}

diag = pipeline.process_reading(reading, neighbors)
print(json.dumps(diag['diagnosis'], indent=2))
