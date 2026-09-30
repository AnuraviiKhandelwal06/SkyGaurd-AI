import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
import app.services.ingestion_service as ig
import logging
logging.getLogger().setLevel(logging.ERROR)

db = SessionLocal()

print("=== MOCKING A REAL FAULT ===")
count = 0
def mocked_fetch_counter(lat, lon):
    global count
    count += 1
    if count == 1: # AWS-002
        return {
            "time": "2038-01-01T15:00:00",
            "temperature": -100.0, # massive negative spike
            "humidity": 80.0,
            "pressure": 1010.0
        }
    else:
        return {
            "time": "2038-01-01T15:00:00",
            "temperature": 27.0,
            "humidity": 80.0,
            "pressure": 1010.0
        }

ig.fetch_weather_api = mocked_fetch_counter
ig.poll_stations()

new_anomaly = db.query(Anomaly).order_by(Anomaly.id.desc()).first()
if new_anomaly:
    print(f"New Anomaly ID: {new_anomaly.id}")
    print(f"Fault Type: {new_anomaly.fault_type}")
