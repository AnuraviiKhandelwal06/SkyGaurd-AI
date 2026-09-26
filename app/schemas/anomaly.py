from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnomalyResponse(BaseModel):
    id: int
    station_code: str
    reading_id: int | None
    timestamp: datetime
    anomaly_score: float
    diagnosis: str
    confidence: float
    reason: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)