import sys
import os
import json
sys.path.append('C:\\Users\\aj132\\OneDrive\\Desktop\\Anvi SIH Project')

from skyguard.main_pipeline import SkyGuardPipeline

# Initialize Pipeline
pipeline = SkyGuardPipeline()
model_dir = 'C:\\Users\\aj132\\OneDrive\\Desktop\\Anvi SIH Project\\skyguard\\models'
fc_path = os.path.join(model_dir, 'classifier.pkl')
temp_path = os.path.join(model_dir, 'temporal')

pipeline.fault_classifier.load(fc_path)
pipeline.temporal_ai.load(temp_path)

# Prepare input data
reading_dict = {
    "time": "2026-09-29T19:00:00",
    "temperature_2m": 32.0,
    "relative_humidity_2m": 20.0,
    "surface_pressure": 800.0,
    "pressure_msl": 820.0,
    "station_id": "AWS-001"
}

# Assume neighbors are normal (e.g., around 1010 hPa)
neighbors = {
    "Neighbor1": {
        "temperature_2m": 31.0,
        "relative_humidity_2m": 25.0,
        "surface_pressure": 1010.0,
        "pressure_msl": 1030.0
    }
}
pipeline.neighbor_metadata = {
    "Neighbor1": {"distance_km": 10.0, "corr_temp": 1.0}
}

# Run pipeline
result = pipeline.process_reading(reading_dict, neighbors)
print(json.dumps(result, indent=2))
