from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.anomaly import Anomaly
from app.schemas.anomaly import AnomalyResponse


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomalies"]
)


@router.get(
    "/{station_code}",
    response_model=list[AnomalyResponse]
)
def get_station_anomalies(
    station_code: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(Anomaly)
        .filter(
            Anomaly.station_code == station_code
        )
        .order_by(Anomaly.timestamp.desc())
        .limit(200)
        .all()
    )