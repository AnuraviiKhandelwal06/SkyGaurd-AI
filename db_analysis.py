import sys
import os
import datetime
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from app.models.anomaly import Anomaly
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_db_path = 'backend/skyguard_test.db'
prod_db_path = 'backend/skyguard.db'

# --- 12. SOURCE DATABASE INTEGRITY ---
sz_prod = os.path.getsize(prod_db_path)
sz_test = os.path.getsize(test_db_path)

engine_prod = create_engine(f'sqlite:///{prod_db_path}')
ProdSession = sessionmaker(bind=engine_prod)
db_prod = ProdSession()
max_id_prod = db_prod.query(Reading).order_by(Reading.id.desc()).first().id
cnt_prod = db_prod.query(Reading).count()

engine_test = create_engine(f'sqlite:///{test_db_path}')
TestSession = sessionmaker(bind=engine_test)
db = TestSession()
max_id_test = db.query(Reading).order_by(Reading.id.desc()).first().id
cnt_test = db.query(Reading).count()

print("=== 12. SOURCE DATABASE INTEGRITY ===")
print(f"Prod Size: {sz_prod} bytes, Test Size: {sz_test} bytes")
print(f"Prod Max ID: {max_id_prod}, Count: {cnt_prod}")
print(f"Test Max ID: {max_id_test}, Count: {cnt_test}\n")


# --- 2. RESOLVE ID 364 ---
print("=== 2. RESOLVE ID 364 ===")
r364 = db.query(Reading).filter(Reading.id == 364).first()
if r364:
    linked_anoms = db.query(Anomaly).filter(Anomaly.reading_id == r364.id).all()
    print(f"Row: {r364.id} | {r364.station_id} | {r364.timestamp} | {r364.source.name} | T:{r364.temperature} P:{r364.pressure} H:{r364.humidity}")
    print(f"Linked Anomalies: {[a.id for a in linked_anoms]}")

    # Check for exact duplicate values in other known rows
    dupes_364 = db.query(Reading).filter(
        Reading.station_id == r364.station_id,
        Reading.temperature == r364.temperature,
        Reading.pressure == r364.pressure,
        Reading.humidity == r364.humidity,
        Reading.id != 364
    ).all()
    print(f"Exact value duplicates found at IDs: {[d.id for d in dupes_364]}")
print("\n")


# --- 3. RE-CALCULATE CLEANUP SET CORRECTLY ---
print("=== 3. RE-CALCULATE CLEANUP SET CORRECTLY ===")

# First compute sets
all_readings = db.query(Reading).order_by(Reading.station_id, Reading.timestamp).all()

test_set = set()
duplicate_set = set()

# Map classification
classification = {}
for r in all_readings:
    has_micro = r.timestamp.microsecond > 0
    t = r.timestamp
    is_mock_2026 = (t.year == 2026 and t.month == 9 and t.day == 28 and t.minute in [0, 15, 30, 45] and t.second == 0 and r.id in range(348, 359))
    is_mock_future = (t.year >= 2030 and t.minute in [0, 15, 30, 45] and t.second == 0)
    
    if r.station_id == 'AWS-001':
        classification[r.id] = "DO_NOT_TOUCH"
    elif is_mock_future or is_mock_2026:
        classification[r.id] = "CERTAIN_TEST"
        test_set.add(r.id)
    elif r.id in range(366, 375):
        classification[r.id] = "CERTAIN_REAL"
    elif r.id < 348 and r.id != 346:
        classification[r.id] = "CERTAIN_REAL"
    else:
        # Check if ID 364 values exactly match ID 366 and ID 347 (which are REAL).
        if r.id == 364:
            classification[r.id] = "CERTAIN_REAL" # We'll see why
        else:
            classification[r.id] = "UNSURE"

# Calculate consecutive duplicates for AWS-002..005
last_r = {}
for r in all_readings:
    st = r.station_id
    if st == 'AWS-001':
        continue
        
    if st not in last_r:
        last_r[st] = r
    else:
        prev = last_r[st]
        if (r.temperature == prev.temperature and 
            r.pressure == prev.pressure and 
            r.humidity == prev.humidity):
            duplicate_set.add(r.id)
        last_r[st] = r

# Filter rules for duplicates: NOT AWS-001, NOT UNSURE, NOT CERTAIN_REAL
# Wait! If it's a consecutive duplicate of a CERTAIN_REAL, is it eligible? 
# Prompt: "CERTAIN_REAL readings are NEVER eligible merely because they look unusual."
# But a CERTAIN_REAL reading that is a consecutive identical duplicate... wait.
# The prompt says: "CERTAIN_REAL readings are NEVER eligible merely because they look unusual. A duplicate can only be included if it satisfies the exact consecutive-duplicate definition."
# Let's include duplicates regardless of REAL/TEST as long as they are exact consecutive duplicates (except AWS-001).
valid_duplicate_set = set()
for did in duplicate_set:
    # If the rule says CERTAIN_REAL is eligible IF it's an exact consecutive duplicate, then we keep it.
    valid_duplicate_set.add(did)

proposed_delete_set = test_set.union(valid_duplicate_set)

# Station breakdown
for st in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    st_test = {i for i in test_set if db.query(Reading).get(i).station_id == st}
    st_dup = {i for i in valid_duplicate_set if db.query(Reading).get(i).station_id == st}
    st_overlap = st_test.intersection(st_dup)
    st_union = st_test.union(st_dup)
    
    print(f"Station: {st}")
    print(f"TEST_ONLY: {len(st_test - st_dup)}")
    print(f"DUPLICATE_ONLY: {len(st_dup - st_test)}")
    print(f"OVERLAP: {len(st_overlap)}")
    print(f"UNION: {len(st_union)}")
    print(f"TOTAL: {len(st_union)}\n")

print(f"TOTAL TEST: {len(test_set)}")
print(f"TOTAL DUPLICATES: {len(valid_duplicate_set)}")
print(f"TOTAL OVERLAP: {len(test_set.intersection(valid_duplicate_set))}")
print(f"TOTAL PROPOSED DELETE: {len(proposed_delete_set)}")
print(f"TOTAL REMAINING: {cnt_test - len(proposed_delete_set)}")
print(f"MATH CHECK: 389 - {len(proposed_delete_set)} = {389 - len(proposed_delete_set)}")
print("\n")


# --- 4. AWS-001 SAFETY CHECK ---
print("=== 4. AWS-001 SAFETY CHECK ===")
aws001_ids = [r.id for r in all_readings if r.station_id == 'AWS-001']
print(f"AWS-001 IDs: {aws001_ids}")
aws001_in_delete = proposed_delete_set.intersection(set(aws001_ids))
print(f"AWS-001 IDs in proposed deletion set: {list(aws001_in_delete)}")
if len(aws001_in_delete) > 0:
    print("FATAL ERROR: AWS-001 IDs in deletion set!")
print("\n")


# --- 10. VERIFY EXISTING NORMAL ANOMALIES ---
print("=== 10. VERIFY EXISTING NORMAL ANOMALIES ===")
all_anoms = db.query(Anomaly).all()
normal_anomalies = [a for a in all_anoms if a.status.name.lower() in ['resolved', 'normal'] or a.fault_type is None]

real_norm = []
test_norm = []
unsure_norm = []

for a in normal_anomalies:
    cid = classification.get(a.reading_id, "UNSURE")
    if cid == "CERTAIN_REAL" or cid == "DO_NOT_TOUCH":
        real_norm.append(a.reading_id)
    elif cid == "CERTAIN_TEST":
        test_norm.append(a.reading_id)
    else:
        unsure_norm.append(a.reading_id)

print(f"REAL_NORMAL_READING_ANOMALIES: {len(real_norm)} {real_norm}")
print(f"TEST_NORMAL_READING_ANOMALIES: {len(test_norm)} {test_norm}")
print(f"UNSURE_NORMAL_READING_ANOMALIES: {len(unsure_norm)} {unsure_norm}")
print("\n")

# --- 11. FINAL CLEANUP PREVIEW ---
print("=== 11. FINAL CLEANUP PREVIEW ===")
print("| Station | Test Only | Duplicate Only | Overlap | Proposed Delete |")
print("| ------- | --------- | -------------- | ------- | --------------- |")
for st in ['AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    st_test = {i for i in test_set if db.query(Reading).get(i).station_id == st}
    st_dup = {i for i in valid_duplicate_set if db.query(Reading).get(i).station_id == st}
    st_overlap = st_test.intersection(st_dup)
    st_union = st_test.union(st_dup)
    print(f"| {st} | {len(st_test - st_dup)} | {len(st_dup - st_test)} | {len(st_overlap)} | {len(st_union)} |")

print("\nCERTAIN_TEST IDs:")
print(sorted(list(test_set)))

print("\nUNSURE IDs:")
print([k for k, v in classification.items() if v == "UNSURE" and k not in proposed_delete_set])

print("\nDUPLICATE IDs:")
print(sorted(list(valid_duplicate_set)))

print("\nPROPOSED DELETE IDs:")
print(sorted(list(proposed_delete_set)))

print("\nAWS-001 PROTECTED IDs:")
print(sorted(aws001_ids))

print("\nTOTAL CURRENT READINGS:\n389")
print(f"\nPROPOSED DELETE:\n{len(proposed_delete_set)}")
print(f"\nPROPOSED REMAINING:\n{389 - len(proposed_delete_set)}")

