import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.path.join(os.getcwd(), 'skyguard'))
import logging
logging.getLogger().setLevel(logging.ERROR)

from app.core.database import SessionLocal
from app.models.station import Station
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

db = SessionLocal()

stations = db.query(Station).filter(Station.station_id != 'AWS-002').all()
neighbor_data = {}
for s in stations[:3]:
    r = db.query(Reading).filter(Reading.station_id == s.station_id).order_by(Reading.timestamp.desc()).first()
    if r:
        neighbor_data[s.station_id] = {
            "temperature_2m": r.temperature,
            "relative_humidity_2m": r.humidity,
            "surface_pressure": r.pressure,
            "pressure_msl": r.pressure,
            "time": r.timestamp.isoformat()
        }

pipeline = SkyGuardPipeline()
if os.path.exists("skyguard/models/classifier.pkl"):
    pipeline.fault_classifier.load("skyguard/models/classifier.pkl")
    pipeline.temporal_ai.load("skyguard/models/temporal")

rd = {
    "time": "2040-01-01T15:00:00",
    "temperature_2m": -100.0,
    "relative_humidity_2m": 80.0,
    "surface_pressure": 1010.0,
    "pressure_msl": 1030.0,
    "station_id": "AWS-002"
}

old_classify = pipeline.fault_classifier.classify

def patched_classify(feature_vector):
    label, conf, prob_dict = old_classify(feature_vector)
    print("--- RAW CLASSIFIER OUTPUT ---")
    print(f"fault_label: {label}")
    print(f"confidence: {conf:.4f}")
    print(f"class_probabilities: {prob_dict}")
    return label, conf, prob_dict

pipeline.fault_classifier.classify = patched_classify
pipeline.recent_history = []
try:
    diag = pipeline.process_reading(rd, neighbor_readings=neighbor_data)
except Exception as e:
    print(e)
