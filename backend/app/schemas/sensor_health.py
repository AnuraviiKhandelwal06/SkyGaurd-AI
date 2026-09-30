from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict

class SensorHealthResponse(BaseModel):
    station_id: str
    fleet_health_score: float | None
    mtbf_days: int | None
    last_calculated: datetime | None
    degradation_trend: List[Dict[str, Any]] | None

    model_config = ConfigDict(from_attributes=True)
