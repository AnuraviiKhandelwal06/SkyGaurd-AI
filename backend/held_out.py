import os, sys, datetime
import pandas as pd
import numpy as np
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard/models")
pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
pipeline.temporal_ai.threshold_mse = 3.0

clean_df = generate_dummy_training_data(24)
pipeline.recent_history = clean_df.to_dict('records')

def evaluate_case(temp_jump, rh_jump, is_freeze, expected, neighbors_jump=0.0):
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    reading = {
        'time': now,
        'temperature_2m': float(last['temperature_2m']) + temp_jump,
        'relative_humidity_2m': float(last['relative_humidity_2m']) + rh_jump,
        'surface_pressure': float(last['surface_pressure']),
        'pressure_msl': float(last['surface_pressure']) + 20.0,
        'station_id': 'TEST_AWS'
    }
    
    if is_freeze:
        for _ in range(5):
            r = last.copy()
            r['time'] = datetime.datetime.now().isoformat()
            pipeline.recent_history.append(r)
            
    neighbors = {
        'AWS-1': {'temperature_2m': float(last['temperature_2m']) + neighbors_jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
        'AWS-2': {'temperature_2m': float(last['temperature_2m']) + neighbors_jump, 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0},
    }
    
    master = pipeline.process_reading(reading, neighbors)
    ftype = master["diagnosis"]["diagnosis_type"]
    if ftype == "NORMAL": final_status = "Healthy"
    elif ftype == "GENUINE_EXTREME_EVENT": final_status = "Warning"
    else: final_status = "Faulty"
    
    if is_freeze:
        pipeline.recent_history = clean_df.to_dict('records')
        
    return expected, final_status

results = []
# 5 Healthy
for _ in range(5): results.append(evaluate_case(np.random.normal(0, 0.5), np.random.normal(0, 1.0), False, "Healthy", np.random.normal(0, 0.5)))
# 5 Genuine Extreme
for _ in range(5): 
    jump = np.random.uniform(10, 15) * np.random.choice([-1, 1])
    results.append(evaluate_case(jump, 0, False, "Warning", jump))
# Small Spike
results.append(evaluate_case(8.0, 0, False, "Faulty"))
results.append(evaluate_case(-9.0, 0, False, "Faulty"))
# Large Spike
results.append(evaluate_case(25.0, 0, False, "Faulty"))
results.append(evaluate_case(-30.0, 0, False, "Faulty"))
# Drift (Temporal small, Spatial large. Actually drift builds up, so let's simulate it by shifting neighbor down by 8 and keeping us same)
results.append(evaluate_case(0.0, 0, False, "Faulty", -8.0))
results.append(evaluate_case(0.0, 0, False, "Faulty", 6.0))
# Freeze (short vs long doesn't matter for the single point evaluate_case function as long as it triggers flatline)
results.append(evaluate_case(0, 0, True, "Faulty"))
results.append(evaluate_case(0, 0, True, "Faulty"))
# Comm Failure / Missing
def eval_missing():
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    reading = {'time': now, 'temperature_2m': np.nan, 'relative_humidity_2m': np.nan, 'surface_pressure': np.nan, 'pressure_msl': np.nan, 'station_id': 'TEST_AWS'}
    neighbors = {'AWS-1': {'temperature_2m': float(last['temperature_2m']), 'relative_humidity_2m': float(last['relative_humidity_2m']), 'surface_pressure': float(last['surface_pressure']), 'pressure_msl': float(last['surface_pressure']) + 20.0}}
    master = pipeline.process_reading(reading, neighbors)
    ftype = master["diagnosis"]["diagnosis_type"]
    final = "Faulty" if ftype not in ["NORMAL", "GENUINE_EXTREME_EVENT"] else ("Warning" if ftype == "GENUINE_EXTREME_EVENT" else "Healthy")
    return "Faulty", final

results.append(eval_missing())
results.append(eval_missing())

fp = 0
healthy_count = 0
print(f"{'Expected':<15} | {'Predicted (Final Status)':<25} | Match")
print("-" * 55)
for exp, act in results:
    match = "YES" if exp == act else "NO"
    print(f"{exp:<15} | {act:<25} | {match}")
    if exp == "Healthy":
        healthy_count += 1
        if act != "Healthy": fp += 1

print(f"\nFalse Positive Rate on Healthy: {fp}/{healthy_count} ({(fp/healthy_count)*100:.1f}%)")
