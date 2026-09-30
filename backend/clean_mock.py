import sys
import os
import json
from datetime import datetime, timezone, timedelta
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station
from app.models.station import StationStatus
from skyguard.main_pipeline import SkyGuardPipeline
import app.services.ingestion_service as ig

db = SessionLocal()
# Clean up just for a pristine test block
# We will use 2030-01-01 to ensure it's at the absolute top of the DB
print("=== MOCK TEST A: Same timestamp twice ===")
mock_response_1 = {
    "time": "2030-01-01T15:00:00",
    "temperature": 27.0,
    "humidity": 80.0,
    "pressure": 1010.0
}
ig.fetch_weather_api = lambda lat, lon: mock_response_1
print("--- First poll ---")
ig.poll_stations()

print("--- Second poll with identical timestamp ---")
ig.poll_stations()

print("\n=== MOCK TEST B: 4 different timestamps with small changes ===")
changes = [
    (0.1, -0.5, 0.2),
    (-0.2, 0.3, -0.1),
    (0.15, -0.2, 0.1),
    (-0.05, 0.1, -0.2)
]
for i, c in enumerate(changes):
    dt = (datetime(2030, 1, 1, 15, 0, 0) + timedelta(minutes=(i+1)*15)).isoformat()
    mock_resp = {
        "time": dt,
        "temperature": 27.0 + c[0],
        "humidity": 80.0 + c[1],
        "pressure": 1010.0 + c[2]
    }
    ig.fetch_weather_api = lambda lat, lon, r=mock_resp: r
    print(f"\n--- Polling {dt} ---")
    ig.poll_stations()
