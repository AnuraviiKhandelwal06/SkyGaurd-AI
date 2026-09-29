import sys

paths = [
    r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\services\ingestion_service.py',
    r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\api\routes\predict.py'
]

old_override = '''                # USER REQUESTED DISTRIBUTION: 2 Healthy, 2 Warning, 1 Alert
                station_id = station.station_id
                if station_id in ["AWS-001", "AWS-005"]:
                    diag_type = "NORMAL"
                    out_fault = "CLEAN"
                elif station_id in ["AWS-002", "AWS-003"]:
                    diag_type = "GENUINE_EXTREME_EVENT"
                    out_fault = "GENUINE_EXTREME"
                elif station_id == "AWS-004":
                    diag_type = "SENSOR_FAULT"
                    out_fault = "SPIKE"'''
                    
old_override_2 = '''    # ---------------------------------------------------------
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

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_override in content:
        content = content.replace(old_override, '')
    if old_override_2 in content:
        content = content.replace(old_override_2, '')
        
    # Now replace the jumps
    content = content.replace('reading_data["temperature"] += 15.2', 'reading_data["temperature"] += 4.5')
    content = content.replace('reading_data["temperature"] -= 12.0', 'reading_data["temperature"] -= 4.5')
    
    # ensure AWS-004 always spikes so we reliably get a Faulty 
    if 'if random.random() < 0.5:\n                              reading_data["temperature"] += 35.0' in content:
        content = content.replace('if random.random() < 0.5:\n                              reading_data["temperature"] += 35.0', 'reading_data["temperature"] += 35.0')
    elif 'if random.random() < 0.5:\n                            reading_data["temperature"] += 35.0' in content:
        content = content.replace('if random.random() < 0.5:\n                            reading_data["temperature"] += 35.0', 'reading_data["temperature"] += 35.0')

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {p}")
