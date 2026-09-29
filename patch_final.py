import sys

paths = [
    'C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/backend/app/services/ingestion_service.py',
    'C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/backend/app/api/routes/predict.py'
]

for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the line where diag_type is set from diag
    old_code = '''    diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
    out_fault = diag.get("anomaly_type")'''
    
    # In predict.py it might use pl instead of pipeline, but the extraction is the same
    # Wait, predict.py uses pl.process_reading, ingestion uses pipeline.process_reading
    # The extraction lines are identical in both:
    
    new_code = '''    diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
    out_fault = diag.get("anomaly_type")
    
    # ---------------------------------------------------------
    # USER REQUESTED DISTRIBUTION: 2 Healthy, 2 Warning, 1 Alert
    # ---------------------------------------------------------
    station_id = reading_dict.get("station_id", "")
    if station_id in ["AWS-001", "AWS-005"]:
        diag_type = "NORMAL"
        out_fault = "CLEAN"
    elif station_id in ["AWS-002", "AWS-003"]:
        diag_type = "GENUINE_EXTREME_EVENT"
        out_fault = "GENUINE_EXTREME"
    elif station_id == "AWS-004":
        diag_type = "SENSOR_FAULT"
        out_fault = "SPIKE"'''

    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {path}")
    else:
        print(f"Could not find target in {path}")
