from sqlalchemy.orm import Session

from app.models.sensor_health import SensorHealth


def update_sensor_health(
    db: Session,
    station_code: str,
    anomaly_score: float,
    ml_result: dict = None
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
    
    sensor_health = ml_result.get("sensor_health", {}) if ml_result else {}
    if isinstance(sensor_health, dict) and "health_score_pct" in sensor_health:
        health.health_score = sensor_health["health_score_pct"]
        if health.health_score >= 80:
            health.health_status = "healthy"
        elif health.health_score >= 50:
            health.health_status = "warning"
        else:
            health.health_status = "critical"
    else:
        # Fallback if ML doesn't provide health_score_pct
        if anomaly_score >= 8.0:
            health.health_status = "critical"
            health.health_score = 20.0
        elif anomaly_score >= 5.0:
            health.health_status = "warning"
            health.health_score = 60.0
        else:
            health.health_status = "healthy"
            health.health_score = 100.0

    db.flush()

    return health

    return health