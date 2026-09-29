import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
import datetime

db = SessionLocal()
now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
for s in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    print(f"\n{s} Real Last 5:")
    readings = db.query(Reading).filter(Reading.station_id == s, Reading.timestamp < now).order_by(Reading.timestamp.desc()).limit(5).all()
    for r in reversed(readings):
        print(f"  {r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
