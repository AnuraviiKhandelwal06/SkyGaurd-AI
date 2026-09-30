import os, sys, json
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
import datetime
import pandas as pd
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
    
    edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
    hist_df = pd.DataFrame(pipeline.recent_history + [reading])
    temporal = pipeline.temporal_ai.evaluate_window(hist_df)
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})
    
    diag_res = pipeline.counterfactual.diagnose(edge, temporal, physics, spatial)
    print("Counterfactual Verdict:", diag_res["diagnosis_type"])
    
    feat_vector = pipeline.fault_classifier.extract_features(reading, edge, temporal, physics, spatial, pipeline.recent_history)
    fault_label, conf, _ = pipeline.fault_classifier.classify(feat_vector)
    print("Classifier Verdict:", fault_label)
    
    master = pipeline.process_reading(reading, neighbors)
    print("Final Status:", master["diagnosis"]["diagnosis_type"])

run_case("Healthy", 25.0, 25.0)
run_case("Genuine Extreme Weather", 5.0, 5.0)
run_case("Sensor Spike", 60.0, 25.0)

