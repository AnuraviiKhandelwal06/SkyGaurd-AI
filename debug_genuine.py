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

def debug_genuine(jump):
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    reading = {
        'time': now,
        'temperature_2m': float(last['temperature_2m']) + jump,
        'relative_humidity_2m': float(last['relative_humidity_2m']),
        'surface_pressure': float(last['surface_pressure']),
        'pressure_msl': float(last['surface_pressure']) + 20.0,
        'station_id': 'TEST_AWS'
    }
    
    neighbors = {
        'AWS-1': {'temperature_2m': float(last['temperature_2m']) + jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
        'AWS-2': {'temperature_2m': float(last['temperature_2m']) + jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
    }
    
    master = pipeline.process_reading(reading, neighbors)
    diag = master["diagnosis"]
    print(f"Jump: {jump:.2f} -> Type: {diag['diagnosis_type']}, Root Cause: {diag['root_cause']}")

np.random.seed(42)
for _ in range(5):
    jump = np.random.uniform(10, 15) * np.random.choice([-1, 1])
    debug_genuine(jump)
