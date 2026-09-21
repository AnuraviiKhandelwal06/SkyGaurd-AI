from sqlalchemy.orm import Session
from app.models.sensor_reading import SensorReading
from app.schemas.sensor_reading import ReadingCreate


def store_reading(db: Session, data: ReadingCreate) -> SensorReading:
    reading = SensorReading(**data.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading