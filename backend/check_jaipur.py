import os, sys, datetime
import pandas as pd
import numpy as np
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard/models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
pipeline.temporal_ai.threshold_mse = 3.0

# 24h history at real Jaipur values
start = datetime.datetime.now() - datetime.timedelta(hours=24)
history = []
for i in range(24):
    history.append({
        'time': (start + datetime.timedelta(hours=i)).isoformat(),
        'temperature_2m': 34.0 + np.sin(i / 24.0) * 1.5,
        'relative_humidity_2m': 45.0 + np.cos(i / 24.0) * 2.0,
        'surface_pressure': 970.0 + np.sin(i / 12.0) * 1.0,
        'pressure_msl': 970.0 + np.sin(i / 12.0) * 1.0 + 20.0,
        'station_id': 'TEST_AWS'
    })
pipeline.recent_history = history

now = datetime.datetime.now().isoformat()
reading = {
    'time': now,
    'temperature_2m': 34.5,
    'relative_humidity_2m': 44.0,
    'surface_pressure': 970.5,
    'pressure_msl': 990.5,
    'station_id': 'TEST_AWS'
}
neighbors = {
    'AWS-1': {'temperature_2m': 34.5, 'relative_humidity_2m': 44.0, 'surface_pressure': 970.5, 'pressure_msl': 990.5},
    'AWS-2': {'temperature_2m': 34.5, 'relative_humidity_2m': 44.0, 'surface_pressure': 970.5, 'pressure_msl': 990.5},
}

master = pipeline.process_reading(reading, neighbors)
print("Final Status:", master["diagnosis"]["diagnosis_type"])
print("Evidence:", master["diagnosis"]["evidence_chain"])

