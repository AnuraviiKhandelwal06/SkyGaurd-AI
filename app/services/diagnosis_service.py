from typing import Any


def diagnose_reading(
    reading: dict,
    ml_result: dict
) -> dict:
    """
    Extract diagnosis from ML result.
    """
    anomaly_detected = ml_result.get("is_anomaly", False)
    anomaly_score = ml_result.get("severity_score", 0.0)
    
    if not anomaly_detected:
        return {
            "diagnosis": "normal",
            "anomaly_score": anomaly_score,
            "confidence": 1.0,
            "reason": "No anomaly detected"
        }
    
    diag_dict = ml_result.get("diagnosis", {})
    expl_dict = ml_result.get("explainability", {})
    diag_type = diag_dict.get("diagnosis_type", "anomaly") if isinstance(diag_dict, dict) else "anomaly"
    reason_str = expl_dict.get("reason_string", "Anomaly detected by ML model") if isinstance(expl_dict, dict) else "Anomaly detected"
    
    return {
        "diagnosis": diag_type,
        "anomaly_score": anomaly_score,
        "confidence": ml_result.get("confidence_score", 1.0),
        "reason": reason_str
    }