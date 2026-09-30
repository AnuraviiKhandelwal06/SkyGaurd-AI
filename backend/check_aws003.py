import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
station_id = 'AWS-003'
past = db.query(Reading).filter(Reading.station_id == station_id).order_by(Reading.timestamp.desc()).limit(5).all()
for r in past:
    print(r.timestamp, r.temperature, r.humidity, r.pressure)
