from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.station import Station
from app.models.sensor_reading import SensorReading
from app.models.sensor_health import SensorHealth
from app.models.anomaly import Anomaly

from app.schemas.dashboard import (
    DashboardResponse,
)

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    total_stations = db.query(Station).count()
    
    # Calculate health stats
    all_health = db.query(SensorHealth).all()
    healthy = sum(1 for h in all_health if h.health_status == "healthy")
    warning = sum(1 for h in all_health if h.health_status == "warning")
    faulty = sum(1 for h in all_health if h.health_status == "critical")
    
    active_anomalies = db.query(Anomaly).order_by(Anomaly.timestamp.desc()).limit(20).all()
    
    stations = db.query(Station).all()
    station_data = []
    for s in stations:
        station_data.append({
            "station_code": s.station_code,
            "station_name": s.station_name,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "status": s.status
        })

    return {
        "summary": {
            "total_stations": total_stations,
            "healthy_stations": healthy,
            "warning_stations": warning,
            "faulty_stations": faulty,
            "active_anomalies_count": len(active_anomalies)
        },
        "stations": station_data,
        "recent_anomalies": [
            {
                "station_code": a.station_code,
                "timestamp": a.timestamp,
                "diagnosis": a.diagnosis,
                "severity": a.anomaly_score
            } for a in active_anomalies
        ]
    }



@router.get(
    "/{station_code}",
    response_model=DashboardResponse
)
def get_dashboard(
    station_code: str,
    db: Session = Depends(get_db)
):
    # -------------------------
    # Station
    # -------------------------

    station = (
        db.query(Station)
        .filter(
            Station.station_code == station_code
        )
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail=f"Station '{station_code}' not found"
        )

    # -------------------------
    # Latest reading
    # -------------------------

    latest_reading = (
        db.query(SensorReading)
        .filter(
            SensorReading.station_code == station_code
        )
        .order_by(
            SensorReading.timestamp.desc()
        )
        .first()
    )

    latest_reading_data = None

    if latest_reading:
        latest_reading_data = {
            "station_code": station_code,
            "timestamp": latest_reading.timestamp,
            "temperature": latest_reading.temperature,
            "pressure": latest_reading.pressure,
            "humidity": latest_reading.humidity,
            "rainfall": latest_reading.rainfall,
            "quality_status": latest_reading.quality_status,
        }

    # -------------------------
    # Sensor health
    # -------------------------

    sensor_health = (
        db.query(SensorHealth)
        .filter(
            SensorHealth.station_code == station_code
        )
        .first()
    )

    sensor_health_data = None

    if sensor_health:
        sensor_health_data = {
            "station_code": sensor_health.station_code,
            "health_status": sensor_health.health_status,
            "health_score": sensor_health.health_score,
            "last_anomaly_score": sensor_health.last_anomaly_score,
            "updated_at": sensor_health.updated_at,
        }

    # -------------------------
    # Recent anomalies
    # -------------------------

    recent_anomalies = (
        db.query(Anomaly)
        .filter(
            Anomaly.station_code == station_code
        )
        .order_by(
            Anomaly.timestamp.desc()
        )
        .limit(10)
        .all()
    )

    anomaly_data = [
        {
            "id": anomaly.id,
            "station_code": anomaly.station_code,
            "reading_id": anomaly.reading_id,
            "timestamp": anomaly.timestamp,
            "anomaly_score": anomaly.anomaly_score,
            "diagnosis": anomaly.diagnosis,
            "confidence": anomaly.confidence,
            "reason": anomaly.reason,
        }
        for anomaly in recent_anomalies
    ]

    # -------------------------
    # Summary
    # -------------------------

    reading_count = (
        db.query(SensorReading)
        .filter(
            SensorReading.station_code == station_code
        )
        .count()
    )

    anomaly_count = (
        db.query(Anomaly)
        .filter(
            Anomaly.station_code == station_code
        )
        .count()
    )

    return {
        "station": {
            "station_code": station.station_code,
            "station_name": station.station_name,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "elevation": station.elevation,
            "state": station.state,
            "district": station.district,
            "status": station.status,
        },

        "latest_reading": latest_reading_data,

        "sensor_health": sensor_health_data,

        "recent_anomalies": anomaly_data,

        "summary": {
            "anomaly_count": anomaly_count,
            "reading_count": reading_count,
        },
    }