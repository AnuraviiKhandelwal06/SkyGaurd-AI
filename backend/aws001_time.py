import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
readings = db.query(Reading).filter(Reading.station_id == 'AWS-001', Reading.source == 'physical_sensor').order_by(Reading.timestamp).all()
if readings:
    print(f"First timestamp: {readings[0].timestamp}")
    print(f"Last timestamp: {readings[-1].timestamp}")
else:
    print("No physical_sensor readings found.")
