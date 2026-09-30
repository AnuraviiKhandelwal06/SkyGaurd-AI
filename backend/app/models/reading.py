import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class ReadingSource(str, enum.Enum):
    physical_sensor = "physical_sensor"
    weather_api = "weather_api"

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, ForeignKey("stations.station_id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, ) # Part of PK for TimescaleDB hypertable if needed, but Timescale can just use timestamp as partition key. Usually TimescaleDB doesn't require timestamp in PK unless unique constraint across time. Wait, typically it's just id as PK and timestamp as partition key. Wait, Timescale requires partition key to be part of primary key if there's a unique/primary constraint, but we can just let `id` and `timestamp` be PK or drop PK on `id` and use `(id, timestamp)` as PK.
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    source = Column(Enum(ReadingSource))

    station = relationship("Station", back_populates="readings")
    anomaly = relationship("Anomaly", back_populates="reading", uselist=False, cascade="all, delete")
