from sqlalchemy.orm import Session

from app.models.anomaly import Anomaly


def store_anomaly(
    db: Session,
    station_code: str,
    reading_id: int | None,
    timestamp,
    diagnosis_result: dict
) -> Anomaly:

    anomaly = Anomaly(
        station_code=station_code,
        reading_id=reading_id,
        timestamp=timestamp,
        anomaly_score=diagnosis_result["anomaly_score"],
        diagnosis=diagnosis_result["diagnosis"],
        confidence=diagnosis_result["confidence"],
        reason=diagnosis_result["reason"]
    )

    db.add(anomaly)
    db.commit()
    db.refresh(anomaly)

    return anomaly