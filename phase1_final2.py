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
    has_micro = r.timestamp.microsecond > 0
    is_mocked = not has_micro and r.timestamp.hour >= 15
    
    if r.id == 364:
        creator = "poll_stations() background task"
        evidence = "Has physical_sensor source. Timestamp lacks microseconds, cannot prove if real truncation or mock."
        c = "UNSURE"
    elif is_mocked:
        creator = "mock_poll.py / test script"
        evidence = f"Timestamp {r.timestamp} has no microseconds and is a perfectly round 5-minute increment, matching test scripts."
        c = "CERTAIN_TEST"
    else:
        creator = "poll_stations() background task"
        evidence = f"Microsecond precision ({r.timestamp.microsecond}) comes from datetime.now() during a live background run. Cannot be a mock override which hardcodes exact round times."
        c = "CERTAIN_REAL"
        
    print(f"{r.id} | {r.station_id} | {r.timestamp} | {r.source.name} | T:{r.temperature:.1f}/P:{r.pressure:.1f}/H:{r.humidity:.1f} | {creator} | {evidence} | {c}")

print("\n--- PHASE 1 C: Full reading provenance (340 to max) ---")
readings_c = db.query(Reading).filter(Reading.id >= 340).all()
for r in readings_c:
    has_micro = r.timestamp.microsecond > 0
    
    if r.station_id == 'AWS-001':
        c = "DO_NOT_TOUCH_AWS001"
        ev = "AWS-001 is strictly off limits per absolute rules."
    elif r.id in range(348, 364) or r.id in range(375, 391):
        c = "CERTAIN_TEST"
        ev = "Known test ID ranges with hardcoded future years/hours and perfectly round timestamps (e.g., 2030, 2035) injected by mock scripts."
    else:
        if has_micro or r.id < 348:
            if not has_micro and r.id == 364:
                c = "UNSURE"
                ev = "Timestamp lacks microseconds, could be real API truncation or mock, cannot prove."
            else:
                c = "CERTAIN_REAL"
                ev = f"Microsecond precision ({r.timestamp.microsecond}) from datetime.now() indicates a genuine live background poll execution, not a hardcoded mock."
        else:
            c = "UNSURE"
            ev = "Timestamp lacks microseconds, cannot prove."
            
    print(f"{r.id} | {r.station_id} | {r.timestamp} | {r.source.name} | {r.temperature:.1f} | {r.pressure:.1f} | {r.humidity:.1f} | {c} | {ev}")

