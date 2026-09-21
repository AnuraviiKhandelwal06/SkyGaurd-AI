from typing import Optional
from pydantic import BaseModel


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

    class Config:
        from_attributes = True