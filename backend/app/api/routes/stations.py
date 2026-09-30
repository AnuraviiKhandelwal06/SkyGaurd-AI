from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.station import Station
from app.schemas.station import StationResponse

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("/", response_model=list[StationResponse])
def get_stations(db: Session = Depends(get_db)):
    return db.query(Station).all()

@router.get("/{station_id}", response_model=StationResponse)
def get_station(station_id: str, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.station_id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station