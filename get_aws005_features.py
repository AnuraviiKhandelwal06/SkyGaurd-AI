import sys
import os
import datetime
import pandas as pd
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import logging
from app.core.database import SessionLocal
from app.models.reading import Reading
from skyguard.main_pipeline import SkyGuardPipeline

logging.getLogger().setLevel(logging.ERROR)
db = SessionLocal()
test_reading_ids = [348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390]
stations = ['AWS-005']
pipeline = SkyGuardPipeline()
if os.path.exists("skyguard/models/classifier.pkl"):
    pipeline.fault_classifier.load("skyguard/models/classifier.pkl")
    pipeline.temporal_ai.load("skyguard/models/temporal")

readings = db.query(Reading).filter(Reading.station_id == 'AWS-005', ~Reading.id.in_(test_reading_ids)).order_by(Reading.timestamp).all()
prev = None
distinct = []
for r in readings:
    curr = (r.temperature, r.pressure, r.humidity)
    if prev != curr:
        distinct.append(r)
    prev = curr

print("--- 5. AWS-005 LAST 10 ROWS AND FEATURES ---")
last_10 = distinct[-10:]
for r in last_10:
    print(f"Time:{r.timestamp} | T:{r.temperature:.1f} P:{r.pressure:.1f} H:{r.humidity:.1f}")

histories = []
for r in distinct:
    rd = {
        "time": r.timestamp.isoformat(),
        "temperature_2m": r.temperature,
        "relative_humidity_2m": r.humidity,
        "surface_pressure": r.pressure,
        "pressure_msl": r.pressure + 20,
        "station_id": r.station_id
    }
    
    pipeline.recent_history = histories.copy()
    
    # We only care about the last 10
    if r in last_10:
        window = histories + [rd]
        window_df = pd.DataFrame(window)
        # Just grab the features using feature_extractor
        f = pipeline.fault_classifier.feature_extractor.extract(window_df, pd.DataFrame([rd]))
        print(f"\n[Time: {r.timestamp}] Features:")
        print(f"  temp_variance: {f.get('temp_variance')}")
        print(f"  rolling_std_temp: {f.get('rolling_std_temp')}")
        print(f"  diff_from_mean: {f.get('diff_from_mean')}")
        
    histories.append(rd)
    if len(histories) > 24:
        histories.pop(0)

