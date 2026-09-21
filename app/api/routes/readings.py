
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sensor_reading import SensorReading
from app.schemas.sensor_reading import ReadingCreate, ReadingResponse
from app.services.ingestion_service import store_reading

router = APIRouter(prefix="/api/sensor-data", tags=["Sensor Data"])


@router.post("/upload", response_model=ReadingResponse)
def upload_reading(data: ReadingCreate, db: Session = Depends(get_db)):
    return store_reading(db, data)


@router.get("/{station_id}", response_model=list[ReadingResponse])
def get_readings(station_id: str, db: Session = Depends(get_db)):
    return (
        db.query(SensorReading)
        .filter(SensorReading.station_id == station_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(200)
        .all()
    )