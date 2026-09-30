from app.services.ingestion_service import poll_stations
from app.core.database import SessionLocal
from app.models.reading import Reading
import time

print("Starting Poll 1...")
poll_stations()

print("Starting Poll 2...")
poll_stations()

print("Starting Poll 3...")
poll_stations()

print("\nFetching DB Rows...")
db = SessionLocal()
readings = db.query(Reading).filter(Reading.station_id == 'AWS-001').order_by(Reading.timestamp.desc()).limit(3).all()
for r in reversed(readings):
    print(f"DB Row - ID: {r.id}, Temp: {r.temperature}, Hum: {r.humidity}, Press: {r.pressure}, Time: {r.timestamp}")
