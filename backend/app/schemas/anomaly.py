from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, ConfigDict
from app.models.anomaly import FaultType, AnomalyStatus

class AnomalyResponse(BaseModel):
    id: int
    station_id: str
    reading_id: int
    reading_timestamp: datetime
    detected_at: datetime
    anomaly_score: float | None
    fault_type: FaultType | None
    status: AnomalyStatus | None
    
    temporal_evidence: Dict[str, Any]
    physical_consistency: Dict[str, Any]
    spatial_evidence: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)