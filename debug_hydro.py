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
    
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    print(f"Jump: {temp_jump:.2f} Hydro Viol: {physics['hydrostatic_violation']} Residual: {physics['hydrostatic_residual_hpa']:.2f}")

np.random.seed(42)
evaluate_case(-13.93)
evaluate_case(14.0)
