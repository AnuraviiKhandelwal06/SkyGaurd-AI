import os
import sys
sys.path.insert(0, r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project')
from skyguard.main_pipeline import SkyGuardPipeline
pl = SkyGuardPipeline()

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_training_data(hours=100):
    start = datetime.now() - timedelta(hours=hours)
    data = []
    for i in range(hours):
        data.append({
            'time': (start + timedelta(hours=i)).isoformat(),
            'temperature_2m': 25.0 + np.sin(i / 24.0) * 5 + np.random.normal(0, 0.5),
            'relative_humidity_2m': 50.0 + np.cos(i / 24.0) * 10 + np.random.normal(0, 1.0),
            'surface_pressure': 1013.0 + np.sin(i / 12.0) * 2 + np.random.normal(0, 0.5),
            'pressure_msl': 1013.0 + np.sin(i / 12.0) * 2 + 21.1 + np.random.normal(0, 0.5),
            'anomaly_type': 'CLEAN'
        })
    return pd.DataFrame(data)

import os
model_dir = 'C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/skyguard/models'
if os.path.exists(model_dir):
    pl.fault_classifier.load(os.path.join(model_dir, 'classifier.pkl'))
    pl.temporal_ai.load(os.path.join(model_dir, 'temporal'))
else:
    train_df = generate_dummy_training_data()
    pl.fit(train_df)

pl.recent_history = generate_dummy_training_data().to_dict('records')[-24:]

reading = {
    'time': '2024-01-01T10:00:00',
    'temperature_2m': 65.0,
    'relative_humidity_2m': 50.0,
    'surface_pressure': 1000.0,
    'pressure_msl': 1020.0,
    'station_id': 'AWS-004'
}
neighbors = {
    'AWS-1': {'temperature_2m': 30.0, 'relative_humidity_2m': 50, 'surface_pressure': 1000, 'pressure_msl': 1020},
}
res = pl.process_reading(reading, neighbors)
print('diag_type:', res['diagnosis']['diagnosis_type'])
print('fault_label:', res['anomaly_type'])
