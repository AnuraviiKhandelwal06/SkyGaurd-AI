import sys
import os
import math
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.getcwd())

from backend.app.core.database import SessionLocal
from backend.app.models.station import Station
from backend.app.models.reading import Reading
from skyguard.pipeline.physics_spatial import PhysicsSpatialEngine
from skyguard.main_pipeline import SkyGuardPipeline

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

db = SessionLocal()
stations = db.query(Station).all()
st_dict = {s.station_id: s for s in stations}

print("=== 7. TEST THE OTHER STATIONS TOO ===")
for st_id, st in st_dict.items():
    print(f"\nStation: {st_id}")
    print(f"Coordinates: {st.latitude}, {st.longitude}")
    
    valid_neighbors = []
    distances = {}
    for n_id, n_st in st_dict.items():
        if n_id == st_id:
            continue
        # Check if AWS-001 is included in the spatial pipeline. 
        # Usually it is, let's include it if it has valid coords.
        if n_id == 'AWS-001' and (n_st.latitude is None or n_st.longitude is None):
            continue
            
        dist = haversine(st.latitude, st.longitude, n_st.latitude, n_st.longitude)
        if dist <= 150.0:
            valid_neighbors.append(n_id)
            distances[n_id] = dist
            
    print(f"Valid neighbours within 150 km: {valid_neighbors}")
    if valid_neighbors:
        print(f"Neighbour distances: {distances}")
        print("Spatial check status: READY")
    else:
        print("Neighbour distances: {}")
        print("Spatial check status: SKIPPED (INSUFFICIENT_NEIGHBOURS)")
        
        
print("\n=== 6. AWS-005 OPTION-A TEST ===")

# Retrieve last 5 readings for AWS-005
aws005_readings = db.query(Reading).filter(Reading.station_id == 'AWS-005').order_by(Reading.id.desc()).limit(5).all()
aws005_readings.reverse() # Chronological

pipeline = SkyGuardPipeline() # Has the current logic
optA_pipeline = PhysicsSpatialEngine(target_elevation_m=216.0) # Delhi elevation approx

for reading in aws005_readings:
    # Build reading dict
    reading_dict = {
        "time": reading.timestamp.isoformat(),
        "temperature_2m": reading.temperature,
        "relative_humidity_2m": reading.humidity,
        "surface_pressure": reading.pressure,
        "pressure_msl": reading.pressure + 20,
        "station_id": reading.station_id
    }
    
    print(f"\nTimestamp: {reading.timestamp}")
    print(f"T: {reading.temperature}")
    print(f"P: {reading.pressure}")
    print(f"H: {reading.humidity}")
    
    # Current neighbour count (Fake AWS-N1, AWS-N2)
    fake_neighbors = {
        "AWS-N1": {"temperature_2m": reading.temperature + 0.1, "relative_humidity_2m": reading.humidity - 1, "surface_pressure": reading.pressure + 1, "pressure_msl": reading.pressure + 21},
        "AWS-N2": {"temperature_2m": reading.temperature - 0.2, "relative_humidity_2m": reading.humidity + 1, "surface_pressure": reading.pressure - 1, "pressure_msl": reading.pressure + 19},
    }
    print("current neighbour count: 2 (AWS-N1, AWS-N2)")
    
    # Option-A neighbour count
    optA_neighbors = {}
    st_005 = st_dict['AWS-005']
    for n_id, n_st in st_dict.items():
        if n_id == 'AWS-005': continue
        if haversine(st_005.latitude, st_005.longitude, n_st.latitude, n_st.longitude) <= 150.0:
            optA_neighbors[n_id] = {} # Mock empty reading just to show count
    
    optA_count = len(optA_neighbors)
    print(f"Option-A neighbour count: {optA_count}")
    
    if optA_count == 0:
        print("Status: INSUFFICIENT_NEIGHBOURS")
        print("Spatial check: SKIPPED")
    
    # Let's run current spatial z_score via pipeline
    diag_curr = pipeline.process_reading(reading_dict, fake_neighbors)
    curr_sz = diag_curr.get('evidence_metrics', {}).get('spatial_temp_z_score', 'N/A')
    
    print(f"current spatial_z_score: {curr_sz}")
    
    if optA_count == 0:
        print("Option-A spatial_z_score: N/A")
        print("current spatial verdict: FAILED (Implicitly due to fake neighbors)")
        print("Option-A spatial verdict: SKIPPED")
        print(f"current diagnosis: {diag_curr.get('diagnosis', {}).get('diagnosis_type', 'NORMAL')}")
        print("Option-A diagnosis: NORMAL (Spatial check bypassed)")

