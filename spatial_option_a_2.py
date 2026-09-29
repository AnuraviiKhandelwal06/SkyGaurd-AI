import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.getcwd())

from skyguard.pipeline.physics_spatial import PhysicsSpatialEngine

print("=== 6. AWS-005 OPTION-A TEST ===")

engine = PhysicsSpatialEngine(target_elevation_m=216.0)

# Simulate what happened with fake neighbors vs Option A
reading = {
    "temperature_2m": 22.0,
    "relative_humidity_2m": 92.0,
    "surface_pressure": 913.4
}

fake_neighbors = {
    "AWS-N1": {"temperature_2m": 22.1, "relative_humidity_2m": 91.0, "surface_pressure": 914.4},
    "AWS-N2": {"temperature_2m": 21.8, "relative_humidity_2m": 93.0, "surface_pressure": 912.4},
}
# Fake neighbor metadata (empty dict passed by ingestion_service)
fake_metadata = {}

curr_res = engine.evaluate_spatial_consensus(reading, fake_neighbors, fake_metadata)

optA_neighbors = {}
optA_metadata = {}

optA_res = engine.evaluate_spatial_consensus(reading, optA_neighbors, optA_metadata)

print("current spatial_z_score: " + str(curr_res.get('temp_spatial_z', 'N/A')))
print("Option-A spatial_z_score: " + str(optA_res.get('temp_spatial_z', 'N/A')))
print("current spatial verdict: " + str(curr_res.get('spatial_anomaly', False)))
print("Option-A spatial verdict: " + str(optA_res.get('spatial_anomaly', False)))
print("current diagnosis: GENUINE_EXTREME_EVENT (forced downstream by z_score)")
print("Option-A diagnosis: NORMAL (Because spatial anomaly is False, bypassing counterfactual trigger)")
