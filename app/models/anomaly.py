from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)

    station_code = Column(
        String,
        ForeignKey("stations.station_code"),
        index=True,
        nullable=False
    )

    reading_id = Column(
        Integer,
        ForeignKey("sensor_readings.id"),
        nullable=True
    )

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False
    )

    anomaly_score = Column(Float, default=0.0)

    diagnosis = Column(
        String,
        default="requires_diagnosis"
    )

    confidence = Column(Float, default=0.0)

    reason = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )