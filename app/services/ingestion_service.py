from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.station import Station
from app.models.sensor_reading import SensorReading
from app.schemas.sensor_reading import ReadingCreate

from app.services.preprocessing_service import preprocess_reading
from app.services.ml_service import run_anomaly_detection
from app.services.health_service import update_sensor_health
from app.services.diagnosis_service import diagnose_reading
from app.services.anomaly_service import store_anomaly


def store_reading(
    db: Session,
    data: ReadingCreate
) -> SensorReading:

    # Step 1: Check that the station exists
    station = (
        db.query(Station)
        .filter(
            Station.station_code == data.station_code
        )
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail=f"Station '{data.station_code}' not found"
        )

    # Step 2: Preprocess the incoming sensor data
    processed_data = preprocess_reading(data)

    # Step 3: Run ML anomaly detection
    ml_result = run_anomaly_detection(
        processed_data
    )

    # Step 4: Diagnose the ML result
    diagnosis_result = diagnose_reading(
        reading=processed_data,
        ml_result=ml_result
    )

    # Step 5: Create the sensor reading
    reading = SensorReading(
        **processed_data
    )

    if ml_result["anomaly_detected"]:
        reading.quality_status = "anomaly"
    else:
        reading.quality_status = "ok"

    # Save reading first so we get reading.id
    db.add(reading)
    db.commit()
    db.refresh(reading)

    # Step 6: Update sensor health
    update_sensor_health(
        db=db,
        station_code=data.station_code,
        anomaly_score=ml_result["anomaly_score"]
    )

    # Step 7: Store anomaly/diagnosis only if an anomaly was detected
    if ml_result["anomaly_detected"]:
        store_anomaly(
            db=db,
            station_code=data.station_code,
            reading_id=reading.id,
            timestamp=data.timestamp,
            diagnosis_result=diagnosis_result
        )

    return reading