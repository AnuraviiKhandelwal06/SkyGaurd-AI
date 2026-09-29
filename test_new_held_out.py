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

# We will generate a base history centered around Jaipur (34C, 970 hPa, RH 40%)
def generate_jaipur_history():
    df = generate_dummy_training_data(24)
    df['temperature_2m'] = df['temperature_2m'] - 25.0 + 34.0
    df['surface_pressure'] = df['surface_pressure'] - 1015.0 + 970.0
    df['pressure_msl'] = df['surface_pressure'] + 20.0
    df['relative_humidity_2m'] = 40.0 + np.random.normal(0, 2.0, 24)
    return df

base_df = generate_jaipur_history()

def evaluate_case(temp_jump, rh_jump, is_freeze, expected, true_class=""):
    # Reset state to clean Jaipur baseline!
    pipeline.recent_history = base_df.to_dict('records')
    
    last = pipeline.recent_history[-1]
    now = datetime.datetime.now().isoformat()
    
    # Small realistic noise for target
    t_noise = np.random.normal(0, 0.2)
    rh_noise = np.random.normal(0, 0.5)
    sp_noise = np.random.normal(0, 0.2)
    
    # Add one more history point if not freeze, to ensure noise doesn't trigger flatline on history
    pipeline.recent_history[-1]['surface_pressure'] += np.random.normal(0, 0.1)
    pipeline.recent_history[-2]['surface_pressure'] += np.random.normal(0, 0.1)
    
    if is_freeze:
        # Create identical 4 static readings for freeze test
        sp_frozen = last['surface_pressure']
        t_frozen = last['temperature_2m']
        rh_frozen = last['relative_humidity_2m']
        pipeline.recent_history = pipeline.recent_history[:-3]
        for _ in range(3):
            pipeline.recent_history.append({
                'time': datetime.datetime.now().isoformat(),
                'temperature_2m': t_frozen,
                'relative_humidity_2m': rh_frozen,
                'surface_pressure': sp_frozen,
                'pressure_msl': sp_frozen + 20.0,
                'station_id': 'JAIPUR_AWS'
            })
        target_t = t_frozen
        target_rh = rh_frozen
        target_sp = sp_frozen
    else:
        target_t = float(last['temperature_2m']) + temp_jump + t_noise
        target_rh = float(last['relative_humidity_2m']) + rh_jump + rh_noise
        target_sp = float(last['surface_pressure']) + sp_noise
    
    reading = {
        'time': now,
        'temperature_2m': target_t,
        'relative_humidity_2m': target_rh,
        'surface_pressure': target_sp,
        'pressure_msl': target_sp + 20.0,
        'station_id': 'JAIPUR_AWS'
    }
    
    # Neighbors also get small realistic noise!
    # If genuine extreme, neighbors get the SAME jump + noise. 
    # If it's a sensor fault (spike), neighbors DO NOT get the jump.
    neighbors_jump = temp_jump if expected == "Warning" else 0.0
    
    neighbors = {}
    for i in range(1, 4):
        n_t_noise = np.random.normal(0, 0.2)
        n_rh_noise = np.random.normal(0, 0.5)
        n_sp_noise = np.random.normal(0, 0.2)
        neighbors[f'AWS-{i}'] = {
            'temperature_2m': float(last['temperature_2m']) + neighbors_jump + n_t_noise,
            'relative_humidity_2m': float(last['relative_humidity_2m']) + (rh_jump if expected == "Warning" else 0.0) + n_rh_noise,
            'surface_pressure': float(last['surface_pressure']) + n_sp_noise,
            'pressure_msl': float(last['surface_pressure']) + n_sp_noise + 20.0
        }
    
    master = pipeline.process_reading(reading, neighbors)
    ftype = master["diagnosis"]["diagnosis_type"]
    
    if ftype == "NORMAL": final_status = "Healthy"
    elif ftype == "GENUINE_EXTREME_EVENT": final_status = "Warning"
    else: final_status = "Faulty"
    
    return true_class, expected, final_status

np.random.seed(42)
results = []

# 1. Healthy Cases (10)
for _ in range(10):
    results.append(evaluate_case(0, 0, False, "Healthy", "NORMAL"))

# 2. Genuine Extreme Weather Cases (10)
for _ in range(10):
    jump = np.random.uniform(10, 15) * np.random.choice([-1, 1])
    results.append(evaluate_case(jump, 0, False, "Warning", "GENUINE_EXTREME"))

# 3. Faulty Cases (30 across classes)
# Spikes (10)
for _ in range(5): results.append(evaluate_case(np.random.uniform(7, 12), 0, False, "Faulty", "SPIKE"))
for _ in range(5): results.append(evaluate_case(-np.random.uniform(7, 12), 0, False, "Faulty", "SPIKE"))

# Drift (10) - Simulated by shifting target slowly away from neighbors
# evaluate_case doesn't do temporal drift well in one step, so we'll just do a small temp_jump where neighbors=0
for _ in range(10):
    # Small jump but enough to trigger spatial deviation if neighbors stay
    results.append(evaluate_case(np.random.uniform(2, 4) * np.random.choice([-1, 1]), 0, False, "Faulty", "DRIFT"))

# Freeze (10)
for _ in range(10): results.append(evaluate_case(0, 0, True, "Faulty", "FROZEN"))

# Flatline Test Case (As requested in STEP 2)
print("--- FLATLINE INFORMATIONAL TEST ---")
_, _, status = evaluate_case(0, 0, True, "Faulty", "FROZEN")
print(f"Flatline Test Result: {status}")
print("-----------------------------------\n")

print(f"{'Class':<20} | {'Expected':<15} | {'Predicted (Final Status)':<25} | Match")
print("-" * 75)

fp = 0
healthy_count = 0
faulty_total = 0
faulty_correct = 0

confusion = {}

for cls, exp, act in results:
    match = "YES" if exp == act else "NO"
    # print(f"{cls:<20} | {exp:<15} | {act:<25} | {match}")
    
    if cls not in confusion:
        confusion[cls] = {'Healthy': 0, 'Warning': 0, 'Faulty': 0}
    confusion[cls][act] += 1
    
    if exp == "Healthy":
        healthy_count += 1
        if act != "Healthy": fp += 1
    elif exp == "Faulty":
        faulty_total += 1
        if act == "Faulty": faulty_correct += 1

for cls, preds in confusion.items():
    print(f"Class: {cls:<16} => Preds: {preds}")

if healthy_count > 0:
    print(f"\nHealthy False Positive Rate: {fp}/{healthy_count} ({(fp/healthy_count)*100:.1f}%)")
if faulty_total > 0:
    print(f"Faulty Recall: {faulty_correct}/{faulty_total} ({(faulty_correct/faulty_total)*100:.1f}%)")
