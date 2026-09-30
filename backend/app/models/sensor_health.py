from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class SensorHealth(Base):
    __tablename__ = "sensor_health"

    station_id = Column(String, ForeignKey("stations.station_id"), primary_key=True)
    fleet_health_score = Column(Float)
    mtbf_days = Column(Integer)
    last_calculated = Column(DateTime(timezone=True))
    degradation_trend = Column(JSON) # [{month, health}]

    station = relationship("Station", back_populates="sensor_health")
