from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ReadingCreate(BaseModel):
    station_code: str
    timestamp: datetime
    temperature: float = Field(..., ge=-100, le=100)
    pressure: float = Field(..., ge=800, le=1200)
    pressure_msl: float | None = Field(None, ge=800, le=1200)
    humidity: float = Field(..., ge=0, le=100)
    rainfall: float = Field(0, ge=0)


class ReadingResponse(ReadingCreate):
    id: int
    quality_status: str

    model_config = ConfigDict(from_attributes=True)