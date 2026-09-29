import json
import pandas as pd
import numpy as np
import sys

sys.path.insert(0, r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project')
from skyguard.main_pipeline import SkyGuardPipeline

def build_history(base_temp, count=24):
    history = []
    for i in range(count):
        history.append({
            "time": f"2023-01-01T{i:02d}:00",
            "temperature_2m": base_temp + np.sin(i/24.0*np.pi)*5,
            "relative_humidity_2m": 50.0,
            "surface_pressure": 1000.0,
            "pressure_msl": 1020.0
        })
    return history

pipeline = SkyGuardPipeline()
train_df = pd.DataFrame(build_history(30.0, 100))
pipeline.temporal_ai.fit(train_df, epochs=1)
pipeline.neighbor_metadata = {
    "N1": {"distance_km": 10.0, "corr_temp": 0.95}
}

neighbors = {
    "N1": {"temperature_2m": 30.0, "relative_humidity_2m": 50.0, "surface_pressure": 1000.0}
}

pipeline.recent_history = build_history(30.0, 24)
last_t = pipeline.recent_history[-1]["temperature_2m"]
current = {
    "time": "2023-01-02T00:00",
    "temperature_2m": last_t,
    "relative_humidity_2m": 50.0,
    "surface_pressure": 1000.0,
    "pressure_msl": 1020.0
}
out = pipeline.process_reading(current, neighbors)
print(json.dumps(out["diagnosis"], indent=2))
print(json.dumps(out["evidence_metrics"], indent=2))
