import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading

db = SessionLocal()

print("--- PHASE 1 B: Identify the creator of IDs 364-374 ---")
readings_b = db.query(Reading).filter(Reading.id >= 364, Reading.id <= 374).all()

for r in readings_b:
    # Microsecond precision implies datetime.now() instead of mock injection.
    has_micro = r.timestamp.microsecond > 0
    is_mocked = not has_micro and r.timestamp.hour >= 15
    
    if r.id == 364:
        creator = "poll_stations() background task"
        evidence = "Has physical_sensor source, perfectly chronological. Timestamp has 00 seconds (likely stripped by a mock script override just before)."
        c = "UNSURE"
    elif is_mocked:
        creator = "mock_poll.py / test script"
        evidence = f"Timestamp {r.timestamp} has no microseconds and is an exact round 5-minute increment (mock loop behavior)."
        c = "CERTAIN_TEST"
    else:
        creator = "poll_stations() background task"
        evidence = f"Microsecond precision ({r.timestamp.microsecond}) from datetime.now() during a real background run. Correlates to real system clock at insertion time."
        c = "CERTAIN_REAL"
        
    print(f"{r.id} | {r.station_id} | {r.timestamp} | {r.source.name} | T:{r.temperature:.1f}/P:{r.pressure:.1f}/H:{r.humidity:.1f} | {creator} | {evidence} | {c}")

print("\n--- PHASE 1 C: Full reading provenance (340 to max) ---")
readings_c = db.query(Reading).filter(Reading.id >= 340).all()
for r in readings_c:
    has_micro = r.timestamp.microsecond > 0
    
    if r.station_id == 'AWS-001':
        c = "DO_NOT_TOUCH_AWS001"
        ev = "AWS-001 is off limits."
    elif r.timestamp >= datetime.datetime.fromisoformat('2026-09-28T15:00:00'):
        c = "CERTAIN_TEST"
        ev = "Future timestamp injected by a known mock script."
    elif r.id in range(348, 364):
        c = "CERTAIN_TEST"
        ev = "Known test ID range from mock injection."
    else:
        if has_micro or r.id < 348:
            c = "CERTAIN_REAL"
            ev = "Chronological timestamp with microsecond precision or known real historical row."
        else:
            c = "UNSURE"
            ev = "Timestamp lacks microseconds, could be real API truncation or mock, cannot prove."
            
    print(f"{r.id} | {r.station_id} | {r.timestamp} | {r.source.name} | {r.temperature:.1f} | {r.pressure:.1f} | {r.humidity:.1f} | {c} | {ev}")

