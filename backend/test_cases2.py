import os, sys, json
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
import datetime
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
    
    master = pipeline.process_reading(reading, neighbors)
    print("Classifier Verdict:", master["anomaly_type"])
    print("Final Status:", master["diagnosis"]["diagnosis_type"])

run_case("Healthy", 25.0, 25.0)
run_case("Genuine Extreme Weather", 5.0, 5.0)
run_case("Sensor Spike", 60.0, 25.0)

