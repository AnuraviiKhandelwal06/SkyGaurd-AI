from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SensorHealthResponse(BaseModel):
    station_code: str
    health_status: str
    health_score: float
    last_anomaly_score: float
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)