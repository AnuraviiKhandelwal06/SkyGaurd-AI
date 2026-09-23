from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReadingCreate(BaseModel):
    station_code: str
    timestamp: datetime
    temperature: float
    pressure: float
    humidity: float
    rainfall: float = 0


class ReadingResponse(ReadingCreate):
    id: int
    quality_status: str

    model_config = ConfigDict(from_attributes=True)