import sys
import os
import json
from datetime import datetime, timedelta
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import app.services.ingestion_service as ig
from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
print("=== DEDUPE TEST ===")
# We have 2038 rows. We will try to insert a 2026 row (which is NOT the latest but already exists)
# Let's see if it skips.
# We will use AWS-002.
# 1. same timestamp -> skipped (we'll use 2026-09-28T16:00:00 which exists in DB)
print("TEST 1: same timestamp (already in DB but not the latest because 2038 exists)")
ig.fetch_weather_api = lambda lat, lon: {
    "time": "2026-09-28T16:00:00",
    "temperature": 27.0, "humidity": 80.0, "pressure": 1010.0
}
ig.poll_stations()

# 2. later timestamp -> inserted (e.g. 2026-09-28T16:15:00)
print("\nTEST 2: later timestamp -> inserted")
ig.fetch_weather_api = lambda lat, lon: {
    "time": "2026-09-28T16:15:00",
    "temperature": 27.0, "humidity": 80.0, "pressure": 1010.0
}
ig.poll_stations()

# Verify Test 2 inserted
r = db.query(Reading).filter(Reading.timestamp == datetime.fromisoformat("2026-09-28T16:15:00")).first()
if r: print("TEST 2: Inserted successfully")

# 3. future-dated row already present -> a real duplicate is still skipped.
# Test 1 actually demonstrated this since 2038 is present, but let's do 2038 directly.
print("\nTEST 3: future-dated row already present -> skipped")
ig.fetch_weather_api = lambda lat, lon: {
    "time": "2038-01-01T15:00:00",
    "temperature": 27.0, "humidity": 80.0, "pressure": 1010.0
}
ig.poll_stations()

