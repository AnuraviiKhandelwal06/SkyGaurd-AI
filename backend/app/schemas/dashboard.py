from datetime import datetime

from pydantic import BaseModel


class DashboardStation(BaseModel):
    station_id: str
    station_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    elevation: float | None = None
    state: str | None = None
    district: str | None = None
    status: str


class DashboardReading(BaseModel):
    station_id: str
    timestamp: datetime
    temperature: float | None = None
    pressure: float | None = None
    humidity: float | None = None
    rainfall: float | None = None
    quality_status: str | None = None


class DashboardHealth(BaseModel):
    station_id: str
    health_status: str
    health_score: float
    last_anomaly_score: float
    updated_at: datetime | None = None


class DashboardAnomaly(BaseModel):
    id: int
    station_id: str
    reading_id: int | None = None
    timestamp: datetime
    anomaly_score: float
    diagnosis: str | None = None
    confidence: float
    reason: str | None = None


class DashboardSummary(BaseModel):
    anomaly_count: int
    reading_count: int


class DashboardResponse(BaseModel):
    station: DashboardStation
    latest_reading: DashboardReading | None = None
    sensor_health: DashboardHealth | None = None
    recent_anomalies: list[DashboardAnomaly]
    summary: DashboardSummary
