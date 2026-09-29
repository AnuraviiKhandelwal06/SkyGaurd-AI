import sys

with open('backend/app/api/routes/predict.py', 'r') as f:
    content = f.read()

override_block = '''    diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
    out_fault = diag.get("anomaly_type")

    # Force state for testing
    if force_state == "GENUINE":
        diag_type = "GENUINE_EXTREME_EVENT"
        out_fault = "GENUINE_EXTREME"
    elif force_state == "FAULT":
        diag_type = "SENSOR_FAULT"
        out_fault = "Spike"
        # Mock the correction so it is inserted into the DB
        diag["corrected_telemetry"] = {
            "needs_correction": True,
            "temperature_2m": 30.0,
            "relative_humidity_2m": 50.0,
            "surface_pressure": 1000.0,
            "reconstruction_confidence_pct": 95.0,
            "imputation_method": "IDW_SPATIAL_MOCK"
        }
    elif force_state == "NORMAL":
        diag_type = "NORMAL"
        out_fault = "CLEAN"'''

content = content.replace(
    '''    diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
    out_fault = diag.get("anomaly_type")

    # Force state for testing
    if force_state == "GENUINE":
        diag_type = "GENUINE_EXTREME_EVENT"
        out_fault = "GENUINE_EXTREME"
    elif force_state == "FAULT":
        diag_type = "SENSOR_FAULT"
        out_fault = "Spike"
    elif force_state == "NORMAL":
        diag_type = "NORMAL"
        out_fault = "CLEAN"''',
    override_block
)

with open('backend/app/api/routes/predict.py', 'w') as f:
    f.write(content)
