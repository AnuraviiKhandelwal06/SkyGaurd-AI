from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.reading import ReadingSource

class ReadingResponse(BaseModel):
    id: int
    station_id: str
    timestamp: datetime
    temperature: float | None
    humidity: float | None
    pressure: float | None
    source: ReadingSource | None

    model_config = ConfigDict(from_attributes=True)
