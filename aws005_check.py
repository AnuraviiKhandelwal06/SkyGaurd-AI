import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.station import Station

db = SessionLocal()
readings = db.query(Reading).filter(Reading.station_id == 'AWS-005').order_by(Reading.timestamp).all()
print(f"Total readings for AWS-005: {len(readings)}")
print("First 10:")
for r in readings[:10]:
    print(f"  {r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
print("Last 10:")
for r in readings[-10:]:
    print(f"  {r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")
    
distinct_timestamps = len(set(r.timestamp for r in readings))
distinct_values = len(set((r.temperature, r.pressure, r.humidity) for r in readings))
print(f"Distinct timestamps: {distinct_timestamps}")
print(f"Distinct value triples: {distinct_values}")

print("\nLat/Lon:")
for s in db.query(Station).filter(Station.station_id.in_(['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005'])).all():
    print(f"{s.station_id}: {s.latitude}, {s.longitude}")

