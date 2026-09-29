import os
import sys
import datetime
import pandas as pd
import numpy as np
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from skyguard.main_pipeline import SkyGuardPipeline
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "skyguard/models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))

def generate_jaipur_history():
    df = generate_dummy_training_data(24)
    df['temperature_2m'] = df['temperature_2m'] - 25.0 + 34.0
    df['surface_pressure'] = df['surface_pressure'] - 1015.0 + 970.0
    df['pressure_msl'] = df['surface_pressure'] + 20.0
    df['relative_humidity_2m'] = 40.0 + np.random.normal(0, 2.0, 24)
    return df

base_df = generate_jaipur_history()
pipeline.recent_history = base_df.to_dict('records')
last = pipeline.recent_history[-1]
now = datetime.datetime.now().isoformat()

t_noise = np.random.normal(0, 0.2)
rh_noise = np.random.normal(0, 0.5)
sp_noise = np.random.normal(0, 0.2)

reading = {
    'time': now,
    'temperature_2m': float(last['temperature_2m']) + t_noise,
    'relative_humidity_2m': float(last['relative_humidity_2m']) + rh_noise,
    'surface_pressure': float(last['surface_pressure']) + sp_noise,
    'pressure_msl': float(last['surface_pressure']) + sp_noise + 20.0,
    'station_id': 'JAIPUR_AWS'
}

hist_df = pd.DataFrame(pipeline.recent_history + [reading])
temporal = pipeline.temporal_ai.evaluate_window(hist_df)
print(temporal)
