from typing import Any


def diagnose_reading(
    reading: dict,
    ml_result: dict
) -> dict:
    """
    Determine whether an ML-detected anomaly requires
    further diagnosis.

    Physics and spatial validation will be added later.
    """

    anomaly_detected = ml_result.get(
        "anomaly_detected",
        False
    )

    anomaly_score = ml_result.get(
        "anomaly_score",
        0.0
    )

    # No anomaly detected
    if not anomaly_detected:
        return {
            "diagnosis": "normal",
            "anomaly_score": anomaly_score,
            "confidence": 1.0,
            "reason": "No anomaly detected by ML model"
        }

    # Temporary state.
    # Do NOT classify this as a sensor fault yet.
    return {
        "diagnosis": "requires_diagnosis",
        "anomaly_score": anomaly_score,
        "confidence": 0.0,
        "reason": "Anomaly detected; physics and spatial validation required"
    }