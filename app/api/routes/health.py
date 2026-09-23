from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sensor_health import SensorHealth
from app.schemas.sensor_health import SensorHealthResponse


router = APIRouter(
    prefix="/api/health",
    tags=["Sensor Health"]
)


@router.get(
    "/{station_code}",
    response_model=SensorHealthResponse
)
def get_sensor_health(
    station_code: str,
    db: Session = Depends(get_db)
):
    health = (
        db.query(SensorHealth)
        .filter(
            SensorHealth.station_code == station_code
        )
        .first()
    )

    if not health:
        raise HTTPException(
            status_code=404,
            detail="Sensor health record not found"
        )

    return health