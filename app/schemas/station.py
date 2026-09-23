from typing import Optional

from pydantic import BaseModel, ConfigDict


class StationCreate(BaseModel):
    station_code: str
    station_name: str
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None


class StationResponse(StationCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)