import os, sys, datetime
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from skyguard.main_pipeline import SkyGuardPipeline
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "skyguard/models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
pipeline.temporal_ai.threshold_mse = 3.0

clean_df = generate_dummy_training_data(24)
pipeline.recent_history = clean_df.to_dict('records')

def evaluate_case(temp_jump):
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    reading = {
        'time': now,
        'temperature_2m': float(last['temperature_2m']) + temp_jump,
        'relative_humidity_2m': float(last['relative_humidity_2m']),
        'surface_pressure': float(last['surface_pressure']),
        'pressure_msl': float(last['surface_pressure']) + 20.0,
        'station_id': 'TEST_AWS'
    }
            
    neighbors = {
        'AWS-1': reading.copy(),
        'AWS-2': reading.copy(),
    }
    
    edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
    hist_df = pd.DataFrame(pipeline.recent_history + [reading])
    temporal = pipeline.temporal_ai.evaluate_window(hist_df)
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})
    
    print(f"Jump {temp_jump:.2f}")
    print(f"Edge: {edge}")
    print(f"Temporal: {temporal}")
    print(f"Physics: {physics}")
    print(f"Spatial: {spatial}")
    
    diag_res = pipeline.counterfactual.diagnose(edge, temporal, physics, spatial)
    print(f"CF Diagnosis: {diag_res['diagnosis_type']}")
    print("-" * 50)

np.random.seed(42)
for _ in range(5):
    # Skip the healthy jumps to advance RNG state exactly like held_out.py
    np.random.normal(0, 0.5)
    np.random.normal(0, 1.0)
    np.random.normal(0, 0.5)

evaluate_case(-13.93)
