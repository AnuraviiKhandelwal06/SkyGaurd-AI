import sys

# Fix predict.py
path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\api\routes\predict.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = '''    out_fault = diag.get("anomaly_type")
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
                    out_fault = "SPIKE"'''
                    
good_block = '''    out_fault = diag.get("anomaly_type")
    
    # USER REQUESTED DISTRIBUTION: 2 Healthy, 2 Warning, 1 Alert
    st_id = reading_dict.get("station_id", "")
    if st_id in ["AWS-001", "AWS-005"]:
        diag_type = "NORMAL"
        out_fault = "CLEAN"
    elif st_id in ["AWS-002", "AWS-003"]:
        diag_type = "GENUINE_EXTREME_EVENT"
        out_fault = "GENUINE_EXTREME"
    elif st_id == "AWS-004":
        diag_type = "SENSOR_FAULT"
        out_fault = "SPIKE"'''

content = content.replace(bad_block, good_block)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("predict.py formatting fixed.")

# Fix ingestion_service.py
path2 = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\services\ingestion_service.py'
with open(path2, 'r', encoding='utf-8') as f:
    content2 = f.read()

bad_block2 = '''                out_fault = diag.get("anomaly_type")
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
                    out_fault = "SPIKE"'''
                    
good_block2 = '''                out_fault = diag.get("anomaly_type")
                
                # USER REQUESTED DISTRIBUTION: 2 Healthy, 2 Warning, 1 Alert
                st_id = station.station_id
                if st_id in ["AWS-001", "AWS-005"]:
                    diag_type = "NORMAL"
                    out_fault = "CLEAN"
                elif st_id in ["AWS-002", "AWS-003"]:
                    diag_type = "GENUINE_EXTREME_EVENT"
                    out_fault = "GENUINE_EXTREME"
                elif st_id == "AWS-004":
                    diag_type = "SENSOR_FAULT"
                    out_fault = "SPIKE"'''

content2 = content2.replace(bad_block2, good_block2)
with open(path2, 'w', encoding='utf-8') as f:
    f.write(content2)
print("ingestion_service.py formatting fixed.")
