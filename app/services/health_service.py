from sqlalchemy.orm import Session

from app.models.sensor_health import SensorHealth


def update_sensor_health(
    db: Session,
    station_code: str,
    anomaly_score: float
) -> SensorHealth:

    health = (
        db.query(SensorHealth)
        .filter(
            SensorHealth.station_code == station_code
        )
        .first()
    )

    if not health:
        health = SensorHealth(
            station_code=station_code
        )
        db.add(health)

    health.last_anomaly_score = anomaly_score

    # Temporary health logic.
    # Final thresholds should come from the ML/diagnosis design.
    if anomaly_score >= 0.8:
        health.health_status = "critical"
        health.health_score = 20.0

    elif anomaly_score >= 0.5:
        health.health_status = "warning"
        health.health_score = 60.0

    else:
        health.health_status = "healthy"
        health.health_score = 100.0

    db.commit()
    db.refresh(health)

    return health