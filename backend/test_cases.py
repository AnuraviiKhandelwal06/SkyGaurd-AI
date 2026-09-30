import os, sys, json
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
import datetime
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
train_df = generate_dummy_training_data()
pipeline.fit(train_df)
pipeline.temporal_ai.threshold_mse = 3.0
pipeline.recent_history = train_df.to_dict('records')[-24:]

def run_case(name, temp, neighbors_temp):
    print(f"\n--- {name} ---")
    now = datetime.datetime.now().isoformat()
    reading = {
        'time': now,
        'temperature_2m': temp,
        'relative_humidity_2m': 50.0,
        'surface_pressure': 1000.0,
        'pressure_msl': 1020.0,
        'station_id': 'TEST_AWS'
    }
    neighbors = {
        'AWS-1': {'temperature_2m': neighbors_temp, 'relative_humidity_2m': 50.0, 'surface_pressure': 1000.0, 'pressure_msl': 1020.0},
        'AWS-2': {'temperature_2m': neighbors_temp, 'relative_humidity_2m': 50.0, 'surface_pressure': 1000.0, 'pressure_msl': 1020.0},
    }
    
    # We want to peek inside the pipeline. Let's run it step by step to see the clash
    edge = pipeline.edge_qc.check_bounds(reading)
    # fake temporal history
    temporal = pipeline.temporal_ai.evaluate(reading, pipeline.recent_history)
    physics = pipeline.physics_spatial.check_physics(reading, 189)
    spatial = pipeline.physics_spatial.check_spatial_consensus(reading, neighbors)
    
    diag_res = pipeline.counterfactual_diagnoser.diagnose(edge, temporal, physics, spatial)
    print("Counterfactual Diagnosis:", diag_res["diagnosis_type"])
    
    feat_vector = pipeline.fault_classifier.extract_features(reading, edge, temporal, physics, spatial, pipeline.recent_history)
    fault_label, conf, _ = pipeline.fault_classifier.classify(feat_vector)
    print("Classifier Verdict:", fault_label)
    
    # Run full process to get final status
    master = pipeline.process_reading(reading, neighbors)
    print("Final Status:", master["diagnosis"]["diagnosis_type"], "- Root Cause:", master["diagnosis"]["root_cause"])

# 1. Healthy (Temp = 25.0)
run_case("Healthy", 25.0, 25.0)

# 2. Genuine Extreme Weather (Temp drops to 5.0, Neighbors also drop to 5.0)
run_case("Genuine Extreme Weather", 5.0, 5.0)

# 3. Sensor Spike (Temp jumps to 60.0, Neighbors stay at 25.0)
run_case("Sensor Spike", 60.0, 25.0)

