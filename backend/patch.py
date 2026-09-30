import sys
path = 'C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/backend/app/services/ingestion_service.py'
with open(path, 'r') as f:
    content = f.read()

old_code = '''            try:
                if reading_data.get("temperature") is None:'''

new_code = '''            try:
                # -------------------------------------------------------------
                # INJECT SYNTHETIC ANOMALIES/WARNINGS AS DEFINED EARLIER
                # This ensures the dashboard sees Warning/Faulty/Anomalies
                # -------------------------------------------------------------
                import random
                if reading_data and station.station_id == "AWS-002":
                    # Drift Fault -> Faulty
                    reading_data["temperature"] += 15.2
                elif reading_data and station.station_id == "AWS-003":
                    # Genuine Event -> Warning
                    reading_data["temperature"] += 12.0
                elif reading_data and station.station_id == "AWS-004":
                    # Spike Fault -> Faulty
                    if random.random() < 0.5:
                        reading_data["temperature"] += 35.0
                
                if reading_data.get("temperature") is None:'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, 'w') as f:
        f.write(content)
    print("Patched ingestion_service.py successfully!")
else:
    print("Could not find the insertion point.")
