from fastapi import HTTPException

from app.schemas.sensor_reading import ReadingCreate


def preprocess_reading(data: ReadingCreate) -> dict:
    """
    Validate and prepare a sensor reading for further processing.
    """

    # Humidity must be between 0 and 100 percent
    if not 0 <= data.humidity <= 100:
        raise HTTPException(
            status_code=422,
            detail="Humidity must be between 0 and 100"
        )

    # Rainfall cannot be negative
    if data.rainfall < 0:
        raise HTTPException(
            status_code=422,
            detail="Rainfall cannot be negative"
        )

    # Basic temperature sanity check
    if not -90 <= data.temperature <= 60:
        raise HTTPException(
            status_code=422,
            detail="Temperature value is outside the allowed range"
        )

    # Basic pressure sanity check
    if not 800 <= data.pressure <= 1100:
        raise HTTPException(
            status_code=422,
            detail="Pressure value is outside the allowed range"
        )

    return {
        "station_code": data.station_code,
        "timestamp": data.timestamp,
        "temperature": data.temperature,
        "pressure": data.pressure,
        "humidity": data.humidity,
        "rainfall": data.rainfall,
    }