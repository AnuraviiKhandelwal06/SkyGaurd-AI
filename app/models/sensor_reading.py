from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String, ForeignKey("stations.station_code"), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    rainfall = Column(Float, default=0)
    quality_status = Column(String, default="ok")
    created_at = Column(DateTime(timezone=True), server_default=func.now())