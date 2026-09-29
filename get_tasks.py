import sys
import os
import datetime
import math
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
from app.models.correction import Correction
from app.models.station import Station

db = SessionLocal()

# -----------------
# Task 1
# -----------------
print("=== TASK 1: REAL vs TEST TABLE ===")
readings_340_390 = db.query(Reading).filter(Reading.id >= 340, Reading.id <= 390).all()
cutoff = datetime.datetime.fromisoformat('2026-09-28T15:00:00')

test_ids = set()
for r in readings_340_390:
    # Classification logic:
    # If timestamp >= 2026-09-28 15:00:00 UTC (i.e. test rows we injected) -> TEST
    # OR if it's 348..363 (we know these were injected during tests)
    is_test = "REAL"
    ev = "Timestamp < 15:00 UTC"
    if r.timestamp >= cutoff:
        is_test = "TEST"
        ev = "Timestamp >= 15:00 UTC (Future Mock)"
        test_ids.add(r.id)
    if r.id in range(348, 364):
        is_test = "TEST"
        ev = "Known test mock range (348-363)"
        test_ids.add(r.id)
        
    print(f"{r.id:3} | {r.station_id:7} | {r.timestamp} | {r.source.name:15} | T:{r.temperature:5.1f} P:{r.pressure:6.1f} H:{r.humidity:4.1f} | {is_test:4} ({ev})")

print("\n--- Reading Counts (Station x Source) ---")
counts = {}
for r in db.query(Reading).all():
    k = (r.station_id, r.source.name)
    counts[k] = counts.get(k, 0) + 1
for k, v in sorted(counts.items()):
    print(f"Station: {k[0]:7} | Source: {k[1]:15} | Count: {v}")

# -----------------
# Task 3
# -----------------
print("\n=== TASK 3: AWS-002 PRESSURE ===")
aws002_readings = db.query(Reading).filter(Reading.station_id == 'AWS-002').order_by(Reading.timestamp).all()
for r in aws002_readings:
    print(f"{r.id:3} | {r.timestamp} | {r.source.name:15} | P:{r.pressure:6.1f}")

# -----------------
# Task 4
# -----------------
print("\n=== TASK 4: HAVERSINE DISTANCES ===")
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

stations = db.query(Station).filter(Station.station_id.in_(['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005'])).all()
st_dict = {s.station_id: (s.latitude, s.longitude) for s in stations}
st_ids = sorted(st_dict.keys())
for i in range(len(st_ids)):
    for j in range(i+1, len(st_ids)):
        s1, s2 = st_ids[i], st_ids[j]
        dist = haversine(st_dict[s1][0], st_dict[s1][1], st_dict[s2][0], st_dict[s2][1])
        print(f"{s1} to {s2}: {dist:.1f} km")

# -----------------
# Task 6
# -----------------
print("\n=== TASK 6: CLEANUP PLAN ===")
test_reading_ids = set()
for r in db.query(Reading).all():
    if r.timestamp >= cutoff or r.id in range(348, 364):
        test_reading_ids.add(r.id)

# Find duplicates
duplicate_reading_ids = set()
for s_id in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    rs = db.query(Reading).filter(Reading.station_id == s_id).order_by(Reading.timestamp).all()
    prev = None
    for r in rs:
        curr = (r.temperature, r.pressure, r.humidity)
        if prev == curr:
            duplicate_reading_ids.add(r.id)
        prev = curr

for s_id in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    s_rs = db.query(Reading).filter(Reading.station_id == s_id).all()
    s_ids = {r.id for r in s_rs}
    
    t_only = (test_reading_ids & s_ids) - duplicate_reading_ids
    d_only = (duplicate_reading_ids & s_ids) - test_reading_ids
    overlap = (test_reading_ids & duplicate_reading_ids & s_ids)
    to_delete = (test_reading_ids | duplicate_reading_ids) & s_ids
    
    anoms = db.query(Anomaly).filter(Anomaly.reading_id.in_(to_delete)).all()
    anom_ids = {a.id for a in anoms}
    corrs = db.query(Correction).filter(Correction.anomaly_id.in_(anom_ids)).all()
    
    print(f"{s_id}: Test_Only={len(t_only)} | Dup_Only={len(d_only)} | Overlap={len(overlap)} | "
          f"Total_Delete={len(to_delete)} | Casc_Anom={len(anoms)} | Casc_Corr={len(corrs)}")

# Anomalies on NORMAL readings among remaining
to_delete_all = test_reading_ids | duplicate_reading_ids
remaining = [r for r in db.query(Reading).all() if r.id not in to_delete_all]
rem_ids = {r.id for r in remaining}

remaining_anoms = db.query(Anomaly).filter(Anomaly.reading_id.in_(rem_ids)).all()
normal_anoms = [a for a in remaining_anoms if a.fault_type is None]
print(f"\nRemaining readings: {len(rem_ids)}")
print(f"Anomalies on NORMAL readings among remaining: {len(normal_anoms)}")

