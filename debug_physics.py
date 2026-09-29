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

def evaluate_case(temp_jump, rh_jump, is_freeze, expected, neighbors_jump=0.0):
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    reading = {
        'time': now,
        'temperature_2m': float(last['temperature_2m']) + temp_jump,
        'relative_humidity_2m': float(last['relative_humidity_2m']) + rh_jump,
        'surface_pressure': float(last['surface_pressure']),
        'pressure_msl': float(last['surface_pressure']) + 20.0,
        'station_id': 'TEST_AWS'
    }
            
    neighbors = {
        'AWS-1': {'temperature_2m': float(last['temperature_2m']) + neighbors_jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
        'AWS-2': {'temperature_2m': float(last['temperature_2m']) + neighbors_jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
    }
    
    edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
    hist_df = pd.DataFrame(pipeline.recent_history + [reading])
    temporal = pipeline.temporal_ai.evaluate_window(hist_df)
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})
    
    diag_res = pipeline.counterfactual.diagnose(edge, temporal, physics, spatial)
    
    print(f"Jump={temp_jump:.2f} CF={diag_res['diagnosis_type']} Temp={reading['temperature_2m']:.2f} DP={physics['dew_point_c']:.2f} DP_Viol={physics['dew_point_violation']}")

np.random.seed(42)
for _ in range(5): evaluate_case(np.random.normal(0, 0.5), np.random.normal(0, 1.0), False, "Healthy", np.random.normal(0, 0.5))

for _ in range(5): 
    jump = np.random.uniform(10, 15) * np.random.choice([-1, 1])
    evaluate_case(jump, 0, False, "Warning", jump)
