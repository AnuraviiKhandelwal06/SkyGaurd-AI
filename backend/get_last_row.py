import os, sys, json
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
readings = db.query(Reading).order_by(Reading.timestamp.desc()).limit(1).all()
for r in readings:
    print(f"Reading ID: {r.id}, Station: {r.station_id}, Temp: {r.temperature}, Time: {r.timestamp}")
