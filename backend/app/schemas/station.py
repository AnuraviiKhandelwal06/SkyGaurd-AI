from typing import Optional
from datetime import date

from pydantic import BaseModel, ConfigDict
from app.models.station import StationStatus


class StationCreate(BaseModel):
    station_id: str
    location_name: str
    latitude: float
    longitude: float
    is_primary: bool = False
    active_since: Optional[date] = None
    status: StationStatus = StationStatus.healthy


class StationResponse(StationCreate):
    model_config = ConfigDict(from_attributes=True)
