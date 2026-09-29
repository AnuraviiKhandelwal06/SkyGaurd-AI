import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
from app.models.correction import Correction

db = SessionLocal()

print("--- 1. REAL vs TEST ---")
readings = db.query(Reading).filter(Reading.id >= 340, Reading.id <= 390).all()
for r in readings:
    print(f"ID:{r.id} | Source:{r.source} | Time:{r.timestamp} | T:{r.temperature} P:{r.pressure} H:{r.humidity}")

# Determine TEST vs REAL. Test rows are the ones generated from my mocks.
# My mocks generated rows starting at ID 352? Or 358?
# Let's just fetch all test readings based on what we see.
