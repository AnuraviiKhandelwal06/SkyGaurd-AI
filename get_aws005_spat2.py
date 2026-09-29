import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import logging
from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

logging.getLogger().setLevel(logging.ERROR)
db = SessionLocal()
test_reading_ids = [348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]
stations = ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']
pipeline = SkyGuardPipeline()

readings = db.query(Reading).filter(Reading.station_id.in_(stations), ~Reading.id.in_(test_reading_ids)).order_by(Reading.timestamp).all()
distinct = []
prev = {s: None for s in stations}
for r in readings:
    curr = (r.temperature, r.pressure, r.humidity)
    if prev[r.station_id] != curr:
        distinct.append(r)
    prev[r.station_id] = curr

distinct.sort(key=lambda r: r.timestamp)

histories = {s: [] for s in stations}
for r in distinct:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    neighbors = {}
    for ns in stations:
        if ns != r.station_id and len(histories[ns]) > 0:
            neighbors[ns] = histories[ns][-1]
            
    if r.station_id == 'AWS-005' and r.timestamp.isoformat() == '2026-09-28T14:30:27.641750':
        pipeline.recent_history = histories[r.station_id]
        diag = pipeline.process_reading(rd, neighbors)
        print("\nDiag output:")
        print(diag)
        break
        
    histories[r.station_id].append(rd)
    if len(histories[r.station_id]) > 24:
        histories[r.station_id].pop(0)

