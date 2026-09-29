import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()

print("--- IDs 348..363 ---")
readings = db.query(Reading).filter(Reading.id >= 348, Reading.id <= 363).all()
for r in readings:
    print(f"ID:{r.id} | Station:{r.station_id} | Source:{r.source} | Time:{r.timestamp}")
