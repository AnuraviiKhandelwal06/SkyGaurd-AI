import json
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project')
from skyguard.main_pipeline import SkyGuardPipeline

np.random.seed(42)

out_dir = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\public\demo-data'
os.makedirs(out_dir, exist_ok=True)

stations = [
    {"id": "AWS-001", "name": "Jaipur", "lat": 26.9124, "lng": 75.7873},
    {"id": "AWS-002", "name": "Jodhpur", "lat": 26.2389, "lng": 73.0243},
    {"id": "AWS-003", "name": "Udaipur", "lat": 24.5854, "lng": 73.7125},
    {"id": "AWS-004", "name": "Bikaner", "lat": 28.0229, "lng": 73.3119},
    {"id": "AWS-005", "name": "Kota", "lat": 25.2138, "lng": 75.8648}
]

intervals = 48 * 4
start_time = datetime(2026, 9, 28, 0, 0)
timestamps = [(start_time + timedelta(minutes=15*i)).isoformat() for i in range(intervals)]

raw_data = {s["id"]: [] for s in stations}
for i in range(intervals):
    base_temp = 25.0 + np.sin(i / (24*4) * 2 * np.pi) * 10
    base_rh = 60.0 + np.cos(i / (24*4) * 2 * np.pi) * 20
    for s in stations:
        raw_data[s["id"]].append({
            "time": timestamps[i],
            "temperature_2m": base_temp + np.random.normal(0, 0.5),
            "relative_humidity_2m": base_rh + np.random.normal(0, 1.0),
            "surface_pressure": 980.0 + np.random.normal(0, 0.5),
            "pressure_msl": 1000.0 + np.random.normal(0, 0.5)
        })

# Inject anomalies at specific points
raw_data["AWS-001"][150]["temperature_2m"] += 4.5
raw_data["AWS-001"][150]["relative_humidity_2m"] -= 10.0
raw_data["AWS-002"][160]["temperature_2m"] += 35.0

flat_t = raw_data["AWS-003"][100]["temperature_2m"]
flat_p = raw_data["AWS-003"][100]["surface_pressure"]
for i in range(100, 120):
    raw_data["AWS-003"][i]["temperature_2m"] = flat_t
    raw_data["AWS-003"][i]["surface_pressure"] = flat_p

pipelines = {}
for s in stations:
    p = SkyGuardPipeline()
    train_df = pd.DataFrame(raw_data[s["id"]][:100]) # train on first 100
    p.temporal_ai.fit(train_df, epochs=1)
    pipelines[s["id"]] = p

readings_out, anomalies_out, corrections_out, health_out = [], [], [], []

for i in range(intervals):
    step_neighbors = {s["id"]: raw_data[s["id"]][i] for s in stations}
        
    for s in stations:
        p = pipelines[s["id"]]
        current = raw_data[s["id"]][i]
        
        others = {k: v for k, v in step_neighbors.items() if k != s["id"]}
        p.neighbor_metadata = {k: {"distance_km": 50.0, "corr_temp": 0.9} for k in others.keys()}
        
        res = p.process_reading(current, others)
        
        readings_out.append({
            "station_id": s["id"],
            "timestamp": timestamps[i],
            "temperature": res["original_telemetry"]["temperature_2m"],
            "humidity": res["original_telemetry"]["relative_humidity_2m"],
            "pressure": res["original_telemetry"]["surface_pressure"]
        })
        
        if res.get("is_anomaly"):
            anomalies_out.append({
                "id": f"anom_{s['id']}_{i}",
                "station_id": s["id"],
                "timestamp": timestamps[i],
                "status": res["status"],
                "fault_type": res["fault_type"],
                "confidence": res["confidence_score"],
                "features": res["explainability"]["shap_attributions"],
                "root_cause": res["diagnosis"]["root_cause"]
            })
            if res["corrected_telemetry"]["needs_correction"]:
                corrections_out.append({
                    "id": f"corr_{s['id']}_{i}",
                    "anomaly_id": f"anom_{s['id']}_{i}",
                    "station_id": s["id"],
                    "timestamp": timestamps[i],
                    "original_temp": res["original_telemetry"]["temperature_2m"],
                    "corrected_temp": res["corrected_telemetry"]["temperature_2m"],
                    "method": res["corrected_telemetry"]["imputation_method"],
                    "status": "pending"
                })
        
        if i == intervals - 1:
            s["health"] = res["sensor_health"]
            s["status"] = res["status"]

final_stations = []
for s in stations:
    final_stations.append({
        "id": s["id"],
        "name": s["name"],
        "lat": s["lat"],
        "lng": s["lng"],
        "status": s["status"]
    })
    health_out.append({
        "station_id": s["id"],
        "health_score": s["health"]["health_score_pct"],
        "rul_days": s["health"]["estimated_rul_days"]
    })

analytics_out = {
    "total_readings": intervals * len(stations),
    "total_anomalies": len(anomalies_out),
    "active_faults": len([a for a in anomalies_out if a["status"] == "Faulty"]),
    "avg_health": float(np.mean([h["health_score"] for h in health_out]))
}

with open(os.path.join(out_dir, 'stations.json'), 'w') as f: json.dump(final_stations, f, indent=2)
with open(os.path.join(out_dir, 'readings.json'), 'w') as f: json.dump(readings_out, f, indent=2)
with open(os.path.join(out_dir, 'anomalies.json'), 'w') as f: json.dump(anomalies_out, f, indent=2)
with open(os.path.join(out_dir, 'corrections.json'), 'w') as f: json.dump(corrections_out, f, indent=2)
with open(os.path.join(out_dir, 'sensor_health.json'), 'w') as f: json.dump(health_out, f, indent=2)
with open(os.path.join(out_dir, 'analytics.json'), 'w') as f: json.dump(analytics_out, f, indent=2)

print("Demo data generated successfully.")
