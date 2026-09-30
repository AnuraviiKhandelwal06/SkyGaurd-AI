import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
readings = db.query(Reading).filter(Reading.station_id == 'AWS-002').order_by(Reading.timestamp.desc()).limit(10).all()
for r in readings:
    print(r.id, r.timestamp, r.temperature, r.humidity, r.pressure)
