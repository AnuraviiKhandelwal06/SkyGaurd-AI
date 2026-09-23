from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.station import Station
from app.schemas.station import StationCreate


def create_station(
    db: Session,
    data: StationCreate
) -> Station:

    # Check if station already exists
    existing_station = (
        db.query(Station)
        .filter(
            Station.station_code == data.station_code
        )
        .first()
    )

    if existing_station:
        raise HTTPException(
            status_code=400,
            detail="Station already exists"
        )

    station = Station(
        **data.model_dump()
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station


def get_all_stations(
    db: Session
) -> list[Station]:

    return (
        db.query(Station)
        .order_by(Station.id)
        .all()
    )


def get_station_by_code(
    db: Session,
    station_code: str
) -> Station:

    station = (
        db.query(Station)
        .filter(
            Station.station_code == station_code
        )
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return station