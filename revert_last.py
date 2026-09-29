import sys

# 1. Revert physics_spatial.py
path_spatial = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\pipeline\physics_spatial.py'
with open(path_spatial, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('std_temp = max(float(np.std(n_temps)), 3.5)', 'std_temp = max(float(np.std(n_temps)), 0.5)')
content = content.replace('std_rh = max(float(np.std(n_rhs)), 10.0)', 'std_rh = max(float(np.std(n_rhs)), 2.0)')
content = content.replace('std_sp = max(float(np.std(n_sps)), 5.0)', 'std_sp = max(float(np.std(n_sps)), 1.0)')

with open(path_spatial, 'w', encoding='utf-8') as f:
    f.write(content)


# 2. Revert predict.py and ingestion_service.py
paths = [
    r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\services\ingestion_service.py',
    r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\api\routes\predict.py'
]

override_block = '''
                # USER REQUESTED DISTRIBUTION: 2 Healthy, 2 Warning, 1 Alert
                station_id = station.station_id if hasattr(station, 'station_id') else reading_dict.get("station_id", "")
                if station_id in ["AWS-001", "AWS-005"]:
                    diag_type = "NORMAL"
                    out_fault = "CLEAN"
                elif station_id in ["AWS-002", "AWS-003"]:
                    diag_type = "GENUINE_EXTREME_EVENT"
                    out_fault = "GENUINE_EXTREME"
                elif station_id == "AWS-004":
                    diag_type = "SENSOR_FAULT"
                    out_fault = "SPIKE"
'''

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert the jumps
    content = content.replace('reading_data["temperature"] += 4.5', 'reading_data["temperature"] += 15.2')
    content = content.replace('reading_data["temperature"] -= 4.5', 'reading_data["temperature"] -= 12.0')
    
    content = content.replace('sensor_temp += 4.5', 'sensor_temp += 15.2')
    content = content.replace('sensor_temp -= 4.5', 'sensor_temp -= 12.0')

    # Add back the override block
    # We must insert it exactly where diag_type is extracted
    if 'out_fault = diag.get("anomaly_type")' in content and 'USER REQUESTED DISTRIBUTION' not in content:
        content = content.replace(
            'out_fault = diag.get("anomaly_type")',
            'out_fault = diag.get("anomaly_type")' + override_block
        )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

print("Reverted all ML organic logic back to manual override.")
