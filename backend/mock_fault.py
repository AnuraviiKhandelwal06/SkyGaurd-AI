import sys
import os
import json
from datetime import datetime, timezone, timedelta
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
from app.models.station import StationStatus
import app.services.ingestion_service as ig
import logging
logging.getLogger().setLevel(logging.ERROR)

db = SessionLocal()

print("=== MOCKING A FAULT TO CHECK fault_type ===")
mock_resp = {
    "time": "2035-01-01T15:00:00",
    "temperature": 99.0, # massive spike
    "humidity": 80.0,
    "pressure": 1010.0
}
ig.fetch_weather_api = lambda lat, lon: mock_resp
# Limit stations to AWS-002 to be fast
def custom_query():
    from app.models.station import Station
    return db.query(Station).filter(Station.station_id == 'AWS-002').all()
    
stations = custom_query()
ig.poll_stations()

new_anomaly = db.query(Anomaly).order_by(Anomaly.id.desc()).first()
if new_anomaly:
    print(f"New Anomaly ID: {new_anomaly.id}")
    print(f"Fault Type: {new_anomaly.fault_type}")
    print(f"Description: {new_anomaly.description}")
