from datetime import datetime
from pydantic import BaseModel


class ReadingCreate(BaseModel):
    station_id: str
    timestamp: datetime
    temperature: float
    pressure: float
    humidity: float
    rainfall: float = 0


class ReadingResponse(ReadingCreate):
    id: int
    quality_status: str

    class Config:
        from_attributes = True