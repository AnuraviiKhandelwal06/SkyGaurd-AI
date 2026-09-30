import enum
from sqlalchemy import Column, String, Float, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class StationStatus(str, enum.Enum):
    healthy = "healthy"
    warning = "warning"
    faulty = "faulty"

class Station(Base):
    __tablename__ = "stations"

    station_id = Column(String, primary_key=True)
    location_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_primary = Column(Boolean, default=False)
    active_since = Column(Date)
    status = Column(Enum(StationStatus))

    readings = relationship("Reading", back_populates="station", cascade="all, delete")
    anomalies = relationship("Anomaly", back_populates="station", cascade="all, delete")
    sensor_health = relationship("SensorHealth", back_populates="station", uselist=False, cascade="all, delete")
    fault_history = relationship("FaultHistory", back_populates="station", cascade="all, delete")
