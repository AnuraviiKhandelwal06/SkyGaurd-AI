from sqlalchemy.orm import Session
from app.models.sensor_health import SensorHealth
from datetime import datetime

def update_sensor_health(
    db: Session,
    station_id: str,
    anomaly_score: float
) -> SensorHealth:

    health = (
        db.query(SensorHealth)
        .filter(
            SensorHealth.station_id == station_id
        )
        .first()
    )

    if not health:
        health = SensorHealth(
            station_id=station_id,
            fleet_health_score=100.0,
            mtbf_days=365
        )
        db.add(health)

    # Temporary health logic mapping anomaly_score (0-100) to health
    # In SkyGuard, score is usually 0-100.
    if anomaly_score >= 80:
        health.fleet_health_score = max(0.0, health.fleet_health_score - 10.0)
    elif anomaly_score >= 50:
        health.fleet_health_score = max(0.0, health.fleet_health_score - 2.0)
    else:
        health.fleet_health_score = min(100.0, health.fleet_health_score + 1.0)
        
    health.last_calculated = datetime.utcnow()

    db.commit()
    db.refresh(health)

    return health
