import os, sys, datetime
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from skyguard.main_pipeline import SkyGuardPipeline
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "skyguard/models")
fc_loaded = pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
temp_loaded = pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
if not (fc_loaded and temp_loaded):
    print("FAILED TO LOAD MODELS", fc_loaded, temp_loaded)
    sys.exit(1)

pipeline.temporal_ai.threshold_mse = 3.0

clean_df = generate_dummy_training_data(24)
pipeline.recent_history = clean_df.to_dict('records')

def test_warning_case(temp_jump):
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    temp = float(last['temperature_2m']) + temp_jump
    rh = float(last['relative_humidity_2m'])
    sp = float(last['surface_pressure'])
    
    reading = {
        'time': now, 'temperature_2m': temp, 'relative_humidity_2m': rh, 
        'surface_pressure': sp, 'pressure_msl': sp + 20.0, 'station_id': 'TEST_AWS'
    }
    
    # Neighbors exactly match the test node (perfect agreement)
    neighbors = {
        'AWS-1': {'temperature_2m': temp, 'relative_humidity_2m': rh, 'surface_pressure': sp, 'pressure_msl': sp + 20.0},
        'AWS-2': {'temperature_2m': temp, 'relative_humidity_2m': rh, 'surface_pressure': sp, 'pressure_msl': sp + 20.0},
    }
    
    edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
    hist_df = pd.DataFrame(pipeline.recent_history + [reading])
    temporal = pipeline.temporal_ai.evaluate_window(hist_df)
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})
    
    diag_res = pipeline.counterfactual.diagnose(edge, temporal, physics, spatial)
    
    return {
        'temp_jump': temp_jump,
        'cf_verdict': diag_res['diagnosis_type'],
        'temp_z': spatial.get('temp_spatial_z', 0),
        'rh_z': spatial.get('rh_spatial_z', 0),
        'sp_z': spatial.get('sp_spatial_z', 0),
        'spatial_anomaly': spatial.get('spatial_anomaly'),
        'details': spatial.get('details', [])
    }

print(f"{'Jump':<8} | {'Verdict':<25} | {'TempZ':<8} | {'RH Z':<8} | {'SP Z':<8} | {'Spatial Anom':<15} | {'Details'}")
print("-" * 120)
np.random.seed(42)
for _ in range(5):
    jump = np.random.uniform(10, 15) * np.random.choice([-1, 1])
    res = test_warning_case(jump)
    print(f"{res['temp_jump']:<8.2f} | {res['cf_verdict']:<25} | {res['temp_z']:<8.2f} | {res['rh_z']:<8.2f} | {res['sp_z']:<8.2f} | {str(res['spatial_anomaly']):<15} | {res['details']}")
