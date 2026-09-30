import os, sys, json
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
import datetime
import pandas as pd
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard", "models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
clean_df = generate_dummy_training_data(24)
pipeline.recent_history = clean_df.to_dict('records')

temp = clean_df.iloc[-1]['temperature_2m']
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
    'AWS-1': {'temperature_2m': temp, 'relative_humidity_2m': 50.0, 'surface_pressure': 1000.0, 'pressure_msl': 1020.0}
}

edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
hist_df = pd.DataFrame(pipeline.recent_history + [reading])
temporal = pipeline.temporal_ai.evaluate_window(hist_df)
physics = pipeline.physics_spatial.evaluate_physics(reading)
spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})

print("Edge:", edge)
print("Temporal is_anomaly:", temporal.get("is_temporal_anomaly"), "MSE:", temporal.get("lstm_mse"))
print("Physics:", physics)
print("Spatial:", spatial)
