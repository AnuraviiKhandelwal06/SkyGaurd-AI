import re
with open('../skyguard/main_pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''        if not diag_res["is_anomalous"]:
            fault_label = "CLEAN"
            conf_prob = 0.98
        elif diag_res["diagnosis_type"] == "GENUINE_EXTREME_EVENT":
            fault_label = "GENUINE_EXTREME"
            conf_prob = 0.92
        elif edge_flags["missing_data"]:
            fault_label = "COMM_FAILURE"
            conf_prob = 0.98
        else:
            fault_label, conf_prob, class_probs = self.fault_classifier.classify(feat_vector)

        # Synchronize complete diagnosis dictionary with final fault_label verdict
        if fault_label in ["CLEAN", "NORMAL"]:
            diag_res["is_anomalous"] = False
            diag_res["diagnosis_type"] = "NORMAL"
            diag_res["root_cause"] = "Station telemetry operating normally within expected physical, temporal, and spatial bounds."
            diag_res["evidence_chain"] = ["All edge, temporal, physics, and spatial checks passed within normal bounds."]
            diag_res["severity_score"] = 0.0
        elif fault_label == "GENUINE_EXTREME":
            diag_res["diagnosis_type"] = "GENUINE_EXTREME_EVENT"
            diag_res["root_cause"] = "Genuine Extreme Meteorological Event confirmed by spatial neighbor consensus."
        elif fault_label == "COMM_FAILURE":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Communication Failure / Sensor Dropout (Missing NaN Telemetry)."
        elif fault_label == "SPIKE":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Isolated Sensor Spike Fault (Abrupt rate-of-change jump)."
        elif fault_label == "FROZEN":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Sensor Hardware Freeze / Flatline Fault."
        elif fault_label == "DRIFT":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Sensor Calibration Drift."
        elif fault_label == "INCONSISTENT":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Psychrometric Physical Inconsistency (Dew Point Deficit)."'''

new_block = '''        if not diag_res["is_anomalous"]:
            fault_label = "CLEAN"
            conf_prob = 0.98
        elif diag_res["diagnosis_type"] == "GENUINE_EXTREME_EVENT":
            fault_label = "GENUINE_EXTREME"
            conf_prob = 0.92
        elif edge_flags["missing_data"]:
            fault_label = "COMM_FAILURE"
            conf_prob = 0.98
        else:
            fault_label, conf_prob, class_probs = self.fault_classifier.classify(feat_vector)
            # SAFETY NET: If Counterfactual detected a fault but XGBoost failed to map it
            if fault_label in ["CLEAN", "NORMAL", "GENUINE_EXTREME"]:
                fault_label = "UNKNOWN_FAULT"

        # Synchronize complete diagnosis dictionary with final fault_label verdict
        if fault_label in ["CLEAN", "NORMAL"]:
            diag_res["is_anomalous"] = False
            diag_res["diagnosis_type"] = "NORMAL"
            diag_res["root_cause"] = "Station telemetry operating normally within expected physical, temporal, and spatial bounds."
            diag_res["evidence_chain"] = ["All edge, temporal, physics, and spatial checks passed within normal bounds."]
            diag_res["severity_score"] = 0.0
        elif fault_label == "GENUINE_EXTREME":
            diag_res["diagnosis_type"] = "GENUINE_EXTREME_EVENT"
            diag_res["root_cause"] = "Genuine Extreme Meteorological Event confirmed by spatial neighbor consensus."
        elif fault_label == "COMM_FAILURE":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Communication Failure / Sensor Dropout (Missing NaN Telemetry)."
        elif fault_label == "SPIKE":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Isolated Sensor Spike Fault (Abrupt rate-of-change jump)."
        elif fault_label == "FROZEN":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Sensor Hardware Freeze / Flatline Fault."
        elif fault_label == "DRIFT":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Sensor Calibration Drift."
        elif fault_label == "INCONSISTENT":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Psychrometric Physical Inconsistency (Dew Point Deficit)."
        elif fault_label == "UNKNOWN_FAULT":
            diag_res["diagnosis_type"] = "SENSOR_FAULT"
            diag_res["root_cause"] = "Unspecified Sensor Fault (Failed XGBoost Classification)."'''

content = content.replace(old_block, new_block)
with open('../skyguard/main_pipeline.py', 'w', encoding='utf-8') as f:
    f.write(content)
