from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.reading import Reading
from app.schemas.reading import ReadingResponse

router = APIRouter(prefix="/readings", tags=["Readings"])

@router.get("/{station_id}", response_model=list[ReadingResponse])
def get_readings(station_id: str, db: Session = Depends(get_db)):
    return (
        db.query(Reading)
        .filter(Reading.station_id == station_id)
        .order_by(desc(Reading.timestamp))
        .limit(200)
        .all()
    )