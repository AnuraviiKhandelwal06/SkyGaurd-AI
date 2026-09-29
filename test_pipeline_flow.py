import os, sys, json
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
import datetime
import pandas as pd
from app.api.routes.predict import generate_dummy_training_data

pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard", "models")
fc_loaded = pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
temp_loaded = pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))

# FORCE THRESHOLD TO 3.0 (same as in production API)
pipeline.temporal_ai.threshold_mse = 3.0

clean_df = generate_dummy_training_data(24)
pipeline.recent_history = clean_df.to_dict('records')

def run_case(name, temp, neighbors_temp, rh, press, apply_frozen=False):
    now = datetime.datetime.now().isoformat()
    
    reading = {
        'time': now,
        'temperature_2m': temp,
        'relative_humidity_2m': rh,
        'surface_pressure': press,
        'pressure_msl': press + 20.0,
        'station_id': 'TEST_AWS'
    }
    
    if apply_frozen:
        last = pipeline.recent_history[-1]
        reading['temperature_2m'] = last['temperature_2m']
        reading['relative_humidity_2m'] = last['relative_humidity_2m']
        reading['surface_pressure'] = last['surface_pressure']
        for _ in range(5):
            r = last.copy()
            r['time'] = datetime.datetime.now().isoformat()
            pipeline.recent_history.append(r)
            
    neighbors = {
        'AWS-1': {'temperature_2m': neighbors_temp, 'relative_humidity_2m': rh, 'surface_pressure': press, 'pressure_msl': press + 20.0},
        'AWS-2': {'temperature_2m': neighbors_temp, 'relative_humidity_2m': rh, 'surface_pressure': press, 'pressure_msl': press + 20.0},
    }
    
    edge = pipeline.edge_qc.process_reading(reading, pipeline.recent_history)
    hist_df = pd.DataFrame(pipeline.recent_history + [reading])
    temporal = pipeline.temporal_ai.evaluate_window(hist_df)
    physics = pipeline.physics_spatial.evaluate_physics(reading)
    spatial = pipeline.physics_spatial.evaluate_spatial_consensus(reading, neighbors, {})
    
    diag_res = pipeline.counterfactual.diagnose(edge, temporal, physics, spatial)
    cf_verdict = diag_res["diagnosis_type"]
    
    feat_vector = pipeline.fault_classifier.extract_features(reading, edge, temporal, physics, spatial, pipeline.recent_history)
    fault_label, conf, _ = pipeline.fault_classifier.classify(feat_vector)
    
    master = pipeline.process_reading(reading, neighbors)
    final_type = master["diagnosis"]["diagnosis_type"]
    
    if final_type == "NORMAL": final_status = "Healthy"
    elif final_type == "GENUINE_EXTREME_EVENT": final_status = "Warning"
    else: final_status = "Faulty"
    
    needs_corr = "Yes" if master["corrected_telemetry"]["needs_correction"] else "No"
    
    if apply_frozen:
        pipeline.recent_history = clean_df.to_dict('records')
        
    return f"{name:<25} | {cf_verdict:<25} | {fault_label:<20} | {final_status:<12} | {needs_corr}"

print(f"{'Scenario':<25} | {'Counterfactual Verdict':<25} | {'Classifier Verdict':<20} | {'Final Status':<12} | {'Correction?'}")
print("-" * 105)

last = clean_df.iloc[-1]
base_temp = float(last['temperature_2m'])
base_rh = float(last['relative_humidity_2m'])
base_press = float(last['surface_pressure'])

print(run_case("Healthy", base_temp, base_temp, base_rh, base_press))
print(run_case("Genuine Extreme Weather", base_temp - 15, base_temp - 15, base_rh, base_press))
print(run_case("Sensor Spike", base_temp + 35, base_temp, base_rh, base_press))
print(run_case("Sensor Drift", base_temp + 5, base_temp, base_rh, base_press))
print(run_case("Frozen Sensor", base_temp, base_temp, base_rh, base_press, apply_frozen=True))
