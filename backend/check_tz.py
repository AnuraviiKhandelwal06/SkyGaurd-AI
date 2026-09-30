import sys
import os
from datetime import datetime, timezone
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
last_reading = db.query(Reading).order_by(Reading.timestamp.desc()).first()
print("DB timestamp:", repr(last_reading.timestamp))
print("DB tzinfo:", last_reading.timestamp.tzinfo)
