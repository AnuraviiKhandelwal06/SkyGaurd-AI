import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()

print("--- IDs 364..374 ---")
readings = db.query(Reading).filter(Reading.id >= 364, Reading.id <= 374).all()
for r in readings:
    print(f"ID:{r.id} | Station:{r.station_id} | Source:{r.source} | Time:{r.timestamp}")

