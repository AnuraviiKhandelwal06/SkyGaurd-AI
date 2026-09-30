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

print("=== MOCKING A SINGLE STATION SPIKE ===")
def mocked_fetch(lat, lon):
    # Depending on lat/lon, return different temp
    if abs(lat - 30.25) < 0.1: # AWS-002 is at 30.25, 74.25? Actually let's just use a global counter
        pass
    pass

count = 0
def mocked_fetch_counter(lat, lon):
    global count
    count += 1
    if count == 1: # AWS-002
        return {
            "time": "2036-01-01T15:00:00",
            "temperature": 99.0, # massive spike
            "humidity": 80.0,
            "pressure": 1010.0
        }
    else:
        return {
            "time": "2036-01-01T15:00:00",
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
