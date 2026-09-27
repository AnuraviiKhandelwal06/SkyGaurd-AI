import math
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.station import Station
from app.models.sensor_reading import SensorReading

_pipeline = None

def init_ml_pipeline():
    global _pipeline
    try:
        from skyguard.main_pipeline import SkyGuardPipeline
        print("Initializing SkyGuard Pipeline...")
        _pipeline = SkyGuardPipeline()
        # Initialize with a dummy dataframe to satisfy xgboost/scaler requirements if there's no pre-trained model on disk
        import pandas as pd
        _dummy_df = pd.DataFrame([{
            "time": "2023-01-01 00:00:00",
            "temperature_2m": 25.0,
            "relative_humidity_2m": 50.0,
            "surface_pressure": 1000.0,
            "pressure_msl": 1000.0,
            "is_anomaly": 0
        }] * 30)
        _pipeline.fit(_dummy_df)
        print("SkyGuard Pipeline Initialized.")
    except Exception as e:
        print(f"Failed to initialize ML pipeline: {e}")
        _pipeline = None
        raise e  # Fail fast on startup

def get_neighbors(db: Session, station: Station):
    if station.latitude is None or station.longitude is None:
        return None
    
    # Simple Euclidean distance for neighbors (bounding box could be better but this is sufficient)
    stations = db.query(Station).filter(Station.id != station.id, Station.latitude.isnot(None), Station.longitude.isnot(None)).all()
    
    neighbors = []
    for s in stations:
        dist = math.sqrt((s.latitude - station.latitude)**2 + (s.longitude - station.longitude)**2)
        neighbors.append((dist, s))
    
    # Sort by distance and take top 3
    neighbors.sort(key=lambda x: x[0])
    top_neighbors = [n[1] for n in neighbors[:3]]
    
    neighbor_readings = {}
    for n in top_neighbors:
        latest_reading = db.query(SensorReading).filter(SensorReading.station_code == n.station_code).order_by(SensorReading.timestamp.desc()).first()
        if latest_reading:
            timestamp = latest_reading.timestamp
            if isinstance(timestamp, datetime):
                timestamp = timestamp.isoformat()
            neighbor_readings[n.station_code] = {
                "temperature_2m": latest_reading.temperature,
                "relative_humidity_2m": latest_reading.humidity,
                "surface_pressure": latest_reading.pressure,
                "pressure_msl": latest_reading.pressure_msl or latest_reading.pressure,
                "time": timestamp
            }
    
    return neighbor_readings if neighbor_readings else None

def run_anomaly_detection(reading: dict, db: Session = None, station: Station = None) -> dict:
    if _pipeline is None:
        raise RuntimeError("ML Pipeline not available")

    timestamp = reading.get("timestamp")
    if isinstance(timestamp, datetime):
        timestamp = timestamp.isoformat()

    ml_payload = {
        "temperature_2m": reading.get("temperature"),
        "relative_humidity_2m": reading.get("humidity"),
        "surface_pressure": reading.get("pressure"),
        "pressure_msl": reading.get("pressure_msl") or reading.get("pressure"),
        "time": timestamp
    }
    
    neighbor_data = None
    if db and station:
        neighbor_data = get_neighbors(db, station)

    try:
        ml_result = _pipeline.process_reading(ml_payload, neighbor_readings=neighbor_data)
        return ml_result
    except Exception as e:
        raise e