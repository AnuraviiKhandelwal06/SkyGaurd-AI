import os
import sys
import pandas as pd
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()
for s in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    count = db.query(Reading).filter(Reading.station_id == s).count()
    print(f"{s}: {count} readings in DB")
