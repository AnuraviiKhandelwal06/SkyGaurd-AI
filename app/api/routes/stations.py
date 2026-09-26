from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.station import StationCreate, StationResponse
from app.services.station_service import (
    create_station,
    get_all_stations,
    get_station_by_code
)


router = APIRouter(
    prefix="/api/stations",
    tags=["Stations"]
)


@router.post(
    "/",
    response_model=StationResponse
)
def create_station_endpoint(
    data: StationCreate,
    db: Session = Depends(get_db)
):
    return create_station(db, data)


@router.get(
    "/",
    response_model=list[StationResponse]
)
def get_stations(
    db: Session = Depends(get_db)
):
    return get_all_stations(db)


@router.get(
    "/{station_code}",
    response_model=StationResponse
)
def get_station(
    station_code: str,
    db: Session = Depends(get_db)
):
    return get_station_by_code(db, station_code)