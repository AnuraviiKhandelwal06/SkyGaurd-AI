from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from app.core.database import get_db
from app.models.station import Station
from app.models.anomaly import Anomaly
from app.models.sensor_health import SensorHealth
from app.models.reading import Reading
from app.schemas.dashboard import DashboardResponse

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_stations = db.query(Station).count()
    active_anomalies = db.query(Anomaly).filter(Anomaly.status.in_(["critical", "warning"])).count()
    
    # Calculate fleet health average
    avg_health_row = db.query(func.avg(SensorHealth.fleet_health_score)).first()
    fleet_health = avg_health_row[0] if avg_health_row and avg_health_row[0] is not None else 100.0

    return {
        "total_stations": total_stations,
        "active_anomalies": active_anomalies,
        "fleet_health": fleet_health
    }

@router.get("/analytics/trends")
def get_analytics_trends(db: Session = Depends(get_db)):
    # Group anomalies by day for the last 30 days
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    
    trends = db.query(
        func.date(Anomaly.detected_at).label("day"),
        func.count(Anomaly.id).label("count")
    ).filter(
        Anomaly.detected_at >= thirty_days_ago
    ).group_by(
        func.date(Anomaly.detected_at)
    ).order_by("day").all()

    return {
        "trends": [{"date": str(t.day), "anomalies_count": t.count} for t in trends]
    }

@router.get("/api/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    total_stations = db.query(Station).count()
    
    # Calculate health stats from single source of truth (Station)
    healthy = db.query(Station).filter(Station.status == "healthy").count()
    warning = db.query(Station).filter(Station.status == "warning").count()
    faulty = db.query(Station).filter(Station.status == "faulty").count()
    
    active_anomalies = db.query(Anomaly).order_by(Anomaly.detected_at.desc()).limit(20).all()
    
    stations = db.query(Station).all()
    station_data = []
    for s in stations:
        station_data.append({
            "station_id": s.station_id,
            "station_name": s.location_name,
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
            "active_anomalies_count": warning + faulty
        },
        "stations": station_data,
        "recent_anomalies": [
            {
                "station_id": a.station_id,
                "timestamp": a.detected_at,
                "diagnosis": a.fault_type,
                "severity": a.anomaly_score
            } for a in active_anomalies
        ]
    }
@router.get(
    "/api/dashboard/{station_id}",
    response_model=DashboardResponse
)
def get_dashboard(
    station_id: str,
    db: Session = Depends(get_db)
):
    # -------------------------
    # Station
    # -------------------------
    station = (
        db.query(Station)
        .filter(
            Station.station_id == station_id
        )
        .first()
    )
    if not station:
        raise HTTPException(
            status_code=404,
            detail=f"Station '{station_id}' not found"
        )
    # -------------------------
    # Latest reading
    # -------------------------
    latest_reading = (
        db.query(Reading)
        .filter(
            Reading.station_id == station_id
        )
        .order_by(
            Reading.timestamp.desc()
        )
        .first()
    )
    latest_reading_data = None
    if latest_reading:
        latest_reading_data = {
            "station_id": station_id,
            "timestamp": latest_reading.timestamp,
            "temperature": latest_reading.temperature,
            "pressure": latest_reading.pressure,
            "humidity": latest_reading.humidity,
            "rainfall": None,
            "quality_status": None,
        }
    # -------------------------
    # Sensor health
    # -------------------------
    sensor_health = (
        db.query(SensorHealth)
        .filter(
            SensorHealth.station_id == station_id
        )
        .first()
    )
    sensor_health_data = None
    if sensor_health:
        sensor_health_data = {
            "station_id": sensor_health.station_id,
            "health_status": "healthy" if sensor_health.fleet_health_score and sensor_health.fleet_health_score >= 80 else ("warning" if sensor_health.fleet_health_score and sensor_health.fleet_health_score >= 50 else "critical"),
            "health_score": sensor_health.fleet_health_score,
            "last_anomaly_score": 0.0,
            "updated_at": sensor_health.last_calculated,
        }
    # -------------------------
    # Recent anomalies
    # -------------------------
    recent_anomalies = (
        db.query(Anomaly)
        .filter(
            Anomaly.station_id == station_id
        )
        .order_by(
            Anomaly.detected_at.desc()
        )
        .limit(10)
        .all()
    )
    anomaly_data = [
        {
            "id": anomaly.id,
            "station_id": anomaly.station_id,
            "reading_id": anomaly.reading_id,
            "timestamp": anomaly.detected_at,
            "anomaly_score": anomaly.anomaly_score,
            "diagnosis": anomaly.fault_type,
            "confidence": 0.0,
            "reason": anomaly.status,
        }
        for anomaly in recent_anomalies
    ]
    # -------------------------
    # Summary
    # -------------------------
    reading_count = (
        db.query(Reading)
        .filter(
            Reading.station_id == station_id
        )
        .count()
    )
    anomaly_count = (
        db.query(Anomaly)
        .filter(
            Anomaly.station_id == station_id
        )
        .count()
    )
    return {
        "station": {
            "station_id": station.station_id,
            "station_name": station.location_name,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "elevation": None,
            "state": None,
            "district": None,
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

