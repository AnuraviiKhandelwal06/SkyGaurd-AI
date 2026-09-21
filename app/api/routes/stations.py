from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.station import Station
from app.schemas.station import StationCreate, StationResponse

router = APIRouter(prefix="/api/stations", tags=["Stations"])


@router.post("/", response_model=StationResponse)
def create_station(data: StationCreate, db: Session = Depends(get_db)):
    if db.query(Station).filter(Station.station_code == data.station_code).first():
        raise HTTPException(status_code=400, detail="Station already exists")
    station = Station(**data.model_dump())
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


@router.get("/", response_model=list[StationResponse])
def get_stations(db: Session = Depends(get_db)):
    return db.query(Station).all()


@router.get("/{station_code}", response_model=StationResponse)
def get_station(station_code: str, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.station_code == station_code).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station