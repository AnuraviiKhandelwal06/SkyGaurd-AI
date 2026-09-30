from sqlalchemy.orm import Session
from app.models.anomaly import Anomaly
from datetime import datetime

def store_anomaly(
    db: Session,
    station_id: str,
    reading_id: int,
    reading_timestamp: datetime,
    anomaly_score: float,
    fault_type: str,
    status: str,
    temporal_evidence: dict,
    physical_consistency: dict,
    spatial_evidence: dict
) -> Anomaly:

    anomaly = Anomaly(
        station_id=station_id,
        reading_id=reading_id,
        reading_timestamp=reading_timestamp,
        detected_at=datetime.utcnow(),
        anomaly_score=anomaly_score,
        fault_type=fault_type,
        status=status,
        temporal_evidence=temporal_evidence,
        physical_consistency=physical_consistency,
        spatial_evidence=spatial_evidence
    )

    db.add(anomaly)
    db.commit()
    db.refresh(anomaly)

    return anomaly
