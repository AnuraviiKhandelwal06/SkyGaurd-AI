import os

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\main_pipeline.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the routing logic
bad_routing_start = '        if not diag_res["is_anomalous"]:'
bad_routing_end = '        # 6. SHAP Explainability'

import re
pattern = re.compile(re.escape(bad_routing_start) + '.*?' + re.escape(bad_routing_end), re.DOTALL)

good_routing = '''        # --- ROUTING FIX (Phase 1) ---
        # 1. Final Status comes strictly from Stage 4 (Counterfactual)
        diag_type = diag_res["diagnosis_type"]
        if not diag_res["is_anomalous"] or diag_type == "NORMAL":
            status = "Healthy"
            fault_type = "CLEAN"
            conf_prob = 0.98
        elif diag_type == "GENUINE_EXTREME_EVENT":
            status = "Warning"
            fault_type = "GENUINE_EXTREME"
            conf_prob = diag_res.get("confidence_score", 0.92)
        elif diag_type == "UNCONFIRMED_ANOMALY":
            status = "Warning"
            fault_type = "UNCONFIRMED_ANOMALY"
            conf_prob = diag_res.get("confidence_score", 0.50)
        else:
            status = "Faulty"
            
            # 2. Only if Faulty, we trust Stage 5 to classify the EXACT fault type.
            if edge_flags["missing_data"]:
                fault_type = "COMM_FAILURE"
                conf_prob = 0.98
            else:
                fault_label, conf_prob, class_probs = self.fault_classifier.classify(feat_vector)
                
                if fault_label in ["CLEAN", "NORMAL", "GENUINE_EXTREME"]:
                    fault_type = "UNKNOWN_FAULT" # Safety net
                else:
                    fault_type = fault_label

        # Synchronize diag_res root cause
        if status == "Faulty":
            if fault_type == "SPIKE":
                diag_res["root_cause"] = "Isolated Sensor Spike Fault (Abrupt rate-of-change jump)."
            elif fault_type == "FROZEN":
                diag_res["root_cause"] = "Sensor Hardware Freeze / Flatline Fault."
            elif fault_type == "DRIFT":
                diag_res["root_cause"] = "Sensor Calibration Drift."
            elif fault_type == "INCONSISTENT":
                diag_res["root_cause"] = "Psychrometric Physical Inconsistency (Dew Point Deficit)."
            elif fault_type == "COMM_FAILURE":
                diag_res["root_cause"] = "Communication Failure / Sensor Dropout (Missing NaN Telemetry)."
            elif fault_type == "UNKNOWN_FAULT":
                diag_res["root_cause"] = "Unspecified Sensor Fault (Failed XGBoost Classification)."

        # 6. SHAP Explainability'''

content = pattern.sub(good_routing, content)

# Also fix the master output to include status and fault_type correctly
output_pattern = r'"is_anomaly": bool\(fault_label not in \["CLEAN", "NORMAL"\]\),\s*"anomaly_type": str\(fault_label\),'
good_output = '''"status": status,
            "is_anomaly": (status != "Healthy"),
            "anomaly_type": str(fault_type),
            "fault_type": str(fault_type),'''
content = re.sub(output_pattern, good_output, content)

# Fix explain, heal, and health calls to use fault_type instead of fault_label
content = content.replace('fault_label, conf_prob', 'fault_type, conf_prob')
content = content.replace('fault_label not in', 'fault_type not in')
content = content.replace('fault_label=', 'fault_type=')
content = content.replace('spatial_res, fault_label', 'spatial_res, fault_type')


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("main_pipeline patched successfully")
