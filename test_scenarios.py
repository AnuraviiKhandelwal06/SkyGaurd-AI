import json
import pandas as pd
import numpy as np
import os
import sys

# Ensure correct path
sys.path.insert(0, r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project')

from skyguard.main_pipeline import SkyGuardPipeline

def build_history(base_temp, count=24):
    history = []
    for i in range(count):
        history.append({
            "time": f"2023-01-01T{i:02d}:00",
            "temperature_2m": base_temp + np.sin(i/24.0*np.pi)*5 + np.random.normal(0, 0.2),
            "relative_humidity_2m": 50.0,
            "surface_pressure": 1000.0,
            "pressure_msl": 1020.0
        })
    return history

pipeline = SkyGuardPipeline()
train_df = pd.DataFrame(build_history(30.0, 100))
pipeline.temporal_ai.fit(train_df, epochs=1)

neighbors = {
    "N1": {"temperature_2m": 30.0, "relative_humidity_2m": 50.0, "surface_pressure": 1000.0},
    "N2": {"temperature_2m": 30.5, "relative_humidity_2m": 51.0, "surface_pressure": 1001.0},
}
pipeline.neighbor_metadata = {
    "N1": {"distance_km": 10.0, "corr_temp": 0.95},
    "N2": {"distance_km": 15.0, "corr_temp": 0.90}
}

scenarios = [
    {"name": "Normal", "t_offset": 0.0, "expected_status": "Healthy"},
    {"name": "Genuine Jump (+4.5C)", "t_offset": 4.5, "expected_status": "Warning"},
    {"name": "Sensor Fault (+35C)", "t_offset": 35.0, "expected_status": "Faulty"},
    {"name": "Out-of-range (-100C)", "abs_temp": -100.0, "expected_status": "Faulty"},
    {"name": "Flatline", "flatline": True, "expected_status": "Faulty"}
]

print(f"{'Scenario':<25} | {'Expected':<15} | {'Actual Status':<15} | {'Fault Type':<20}")
print("-" * 85)

for sc in scenarios:
    pipeline.recent_history = build_history(30.0, 24)
    last_t = pipeline.recent_history[-1]["temperature_2m"]
    
    current = {
        "time": "2023-01-02T00:00",
        "temperature_2m": sc.get("abs_temp", last_t + sc.get("t_offset", 0.0)),
        "relative_humidity_2m": 50.0,
        "surface_pressure": 1000.0,
        "pressure_msl": 1020.0
    }
    
    if sc.get("flatline"):
        val = current["temperature_2m"]
        for i in range(1, 6):
            pipeline.recent_history[-i]["temperature_2m"] = val
            pipeline.recent_history[-i]["relative_humidity_2m"] = 50.0
            pipeline.recent_history[-i]["surface_pressure"] = 1000.0
    
    out = pipeline.process_reading(current, neighbors)
    status = out.get("status")
    print(f"{sc['name']:<25} | {sc['expected_status']:<15} | {str(status):<15} | {str(out.get('fault_type')):<20}")

print("\nTesting Cold Start...")
pipeline.recent_history = build_history(30.0, 2)
current = {
    "time": "2023-01-02T00:00",
    "temperature_2m": 30.0,
    "relative_humidity_2m": 50.0,
    "surface_pressure": 1000.0,
    "pressure_msl": 1020.0
}
out = pipeline.process_reading(current, neighbors)
print("Cold Start Test -> Status:", out.get("status"), "Fault Type:", out.get("fault_type"))
