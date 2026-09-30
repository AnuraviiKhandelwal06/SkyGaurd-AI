import os
import re

file_path = 'backend/app/services/ingestion_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace PRIMARY_SENSOR_URL
content = re.sub(r'PRIMARY_SENSOR_URL = "[^"]+"\n', '', content)

old_fetch = '''def fetch_primary_sensor():
    response = httpx.get(PRIMARY_SENSOR_URL, timeout=10.0)
    response.raise_for_status()
    return response.json()'''

new_fetch = '''import csv
CSV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/College_station_Data.csv"))
STATE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/csv_state.txt"))

def fetch_csv_row():
    idx = 0
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r") as f:
                idx = int(f.read().strip())
        except ValueError:
            pass
            
    if not os.path.exists(CSV_FILE_PATH):
        raise FileNotFoundError(f"CSV file not found at {CSV_FILE_PATH}")
        
    with open(CSV_FILE_PATH, "r") as f:
        reader = list(csv.DictReader(f))
        
    if not reader:
        raise ValueError("CSV is empty")
        
    if idx >= len(reader):
        logger.info(f"Reached end of CSV ({len(reader)} rows). Looping back to row 0.")
        print(f"Reached end of CSV ({len(reader)} rows). Looping back to row 0.")
        idx = 0
        
    row = reader[idx]
    
    with open(STATE_FILE_PATH, "w") as f:
        f.write(str(idx + 1))
        
    print(f"Consumed CSV Row {idx}: Temp={row['Temperature_C']} Hum={row['Humidity']} Press={row['Pressure_Hpa']}")
    logger.info(f"Consumed CSV Row {idx}: Temp={row['Temperature_C']} Hum={row['Humidity']} Press={row['Pressure_Hpa']}")
        
    return {
        "temperature": float(row["Temperature_C"]),
        "humidity": float(row["Humidity"]),
        "pressure": float(row["Pressure_Hpa"])
    }'''

content = content.replace(old_fetch, new_fetch)
content = content.replace('fetch_primary_sensor()', 'fetch_csv_row()')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated ingestion_service.py")
