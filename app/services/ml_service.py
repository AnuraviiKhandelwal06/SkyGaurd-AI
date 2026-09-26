def run_anomaly_detection(reading: dict) -> dict:
    """
    Temporary ML service.

    This is only for backend integration testing.
    The actual LSTM model will replace this later.
    """

    # Temporary test condition
    if reading["temperature"] > 50:
        return {
            "anomaly_detected": True,
            "anomaly_score": 0.95,
            "model_status": "test"
        }

    return {
        "anomaly_detected": False,
        "anomaly_score": 0.0,
        "model_status": "test"
    }