with open('app/services/ingestion_service.py', 'w', encoding='utf-8') as f:
    f.write('''import logging
from datetime import datetime, timezone
import httpx
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.station import Station, StationStatus
from app.models.reading import Reading, ReadingSource
from app.models.anomaly import Anomaly, FaultType, AnomalyStatus
from app.models.correction import Correction
from app.models.health import SensorHealth
from app.models.history import FaultHistory
import sys
import os

logger = logging.getLogger(__name__)

PRIMARY_SENSOR_URL = "http://localhost:9999/api/sensor"

def fetch_primary_sensor():
    response = httpx.get(PRIMARY_SENSOR_URL, timeout=10.0)
    response.raise_for_status()
    return response.json()

def poll_stations():
    db: Session = SessionLocal()
    try:
        stations = db.query(Station).filter(Station.status != StationStatus.faulty).all()
        now = datetime.now(timezone.utc)
        
        # Load ML Pipeline
        try:
            from skyguard.main_pipeline import SkyGuardPipeline
            pipeline = SkyGuardPipeline()
        except ImportError as e:
            logger.error(f"Failed to import SkyGuardPipeline: {e}")
            return
            
        for station in stations:
            if not station.is_primary:
                continue # Only poll primary sensor in this hardware integration
                
            try:
                data = fetch_primary_sensor()
                reading_data = {
                    "temperature": data.get("temperature"),
                    "humidity": data.get("humidity"),
                    "pressure": data.get("pressure")
                }
                
                if reading_data["temperature"] is None:
                    raise ValueError("Sensor returned no temperature")
                    
                reading = Reading(
                    station_id=station.station_id,
                    timestamp=now,
                    temperature=reading_data["temperature"],
                    humidity=reading_data["humidity"],
                    pressure=reading_data["pressure"] or 1013.25,
                    source=ReadingSource.physical_sensor
                )
                db.add(reading)
                db.commit()
                db.refresh(reading)
                
                reading_dict = {
                    "time": reading.timestamp.isoformat(),
                    "temperature_2m": reading.temperature,
                    "relative_humidity_2m": reading.humidity,
                    "surface_pressure": reading.pressure,
                    "pressure_msl": reading.pressure + 20,
                    "station_id": station.station_id
                }
                
                neighbors = {
                    "AWS-1": {"temperature_2m": 30.0, "relative_humidity_2m": 50, "surface_pressure": 1000, "pressure_msl": 1020},
                    "AWS-2": {"temperature_2m": 30.5, "relative_humidity_2m": 48, "surface_pressure": 1001, "pressure_msl": 1021},
                }
                
                diag = pipeline.process_reading(reading_dict, neighbors)
                
                diag_type = diag.get("diagnosis", {}).get("diagnosis_type", "NORMAL")
                out_fault = diag.get("anomaly_type")
                
                fault_type_enum = None
                if out_fault == "Spike": fault_type_enum = FaultType.Spike
                elif out_fault == "Frozen": fault_type_enum = FaultType.Frozen
                elif out_fault == "Drift": fault_type_enum = FaultType.Drift
                elif out_fault == "CommFailure": fault_type_enum = FaultType.CommFailure

                if diag_type == "NORMAL":
                    status_enum = AnomalyStatus.resolved
                    station_status_enum = StationStatus.healthy
                elif diag_type == "GENUINE_EXTREME_EVENT":
                    status_enum = AnomalyStatus.warning
                    station_status_enum = StationStatus.warning
                else:
                    status_enum = AnomalyStatus.critical
                    station_status_enum = StationStatus.faulty
                    
                station.status = station_status_enum
                db.commit()
                
                anomaly = Anomaly(
                    station_id=station.station_id,
                    reading_id=reading.id,
                    reading_timestamp=reading.timestamp,
                    detected_at=datetime.now(timezone.utc),
                    anomaly_score=diag.get('severity_score', 0.0),
                    fault_type=fault_type_enum,
                    status=status_enum,
                    temporal_evidence={"details": diag.get('evidence_metrics', {}).get("temporal_lstm_mse")},
                    physical_consistency={"details": diag.get('evidence_metrics', {}).get("physics_dew_point_c")},
                    spatial_evidence={"details": diag.get('evidence_metrics', {}).get("spatial_temp_z_score")}
                )
                db.add(anomaly)
                db.commit()
                db.refresh(anomaly)
                
                if status_enum == AnomalyStatus.critical:
                    ct = diag.get("corrected_telemetry", {})
                    if ct.get("needs_correction"):
                        correction = Correction(
                            anomaly_id=anomaly.id,
                            original_value=reading.temperature,
                            corrected_value=ct.get('temperature_2m'),
                            confidence=ct.get('reconstruction_confidence_pct', 90) / 100,
                            methodology={"method": ct.get('imputation_method')},
                            operator_decision="pending"
                        )
                        db.add(correction)
                        db.commit()
                        
                        fh = FaultHistory(
                            station_id=station.station_id,
                            component="Temperature Sensor",
                            action="imputed",
                            event_date=datetime.now(timezone.utc).date()
                        )
                        db.add(fh)
                        db.commit()
                        
                health = db.query(SensorHealth).filter(SensorHealth.station_id == station.station_id).first()
                if not health:
                    health = SensorHealth(station_id=station.station_id, fleet_health_score=100.0, mtbf_days=120)
                    db.add(health)
                
                sh = diag.get("sensor_health", {})
                health.fleet_health_score = sh.get("health_score_pct", 100.0)
                health.last_calculated = datetime.now(timezone.utc)
                db.commit()

            except Exception as e:
                logger.error(f"Error polling primary station {station.station_id}: {e}")
                db.rollback()
                continue
                
    except Exception as e:
        logger.error(f"Error in poll_stations job: {e}")
    finally:
        db.close()
''')
