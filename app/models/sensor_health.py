from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class SensorHealth(Base):
    __tablename__ = "sensor_health"

    id = Column(Integer, primary_key=True, index=True)

    station_code = Column(
        String,
        ForeignKey("stations.station_code"),
        index=True,
        nullable=False
    )

    health_status = Column(
        String,
        default="healthy"
    )

    health_score = Column(Float, default=100.0)

    last_anomaly_score = Column(Float, default=0.0)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )