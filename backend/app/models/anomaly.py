import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class FaultType(str, enum.Enum):
    Spike = "Spike"
    Frozen = "Frozen"
    Drift = "Drift"
    CommFailure = "CommFailure"
    MissingData = "MissingData"

class AnomalyStatus(str, enum.Enum):
    critical = "critical"
    warning = "warning"
    genuine_event = "genuine_event"
    resolved = "resolved"

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, ForeignKey("stations.station_id"), nullable=False)
    
    reading_id = Column(Integer, nullable=False)
    reading_timestamp = Column(DateTime(timezone=True), nullable=False)
    
    detected_at = Column(DateTime(timezone=True), nullable=False)
    anomaly_score = Column(Float) # 0-100
    fault_type = Column(Enum(FaultType), nullable=True)
    status = Column(Enum(AnomalyStatus))
    
    temporal_evidence = Column(JSON, nullable=False, default=dict)
    physical_consistency = Column(JSON, nullable=False, default=dict)
    spatial_evidence = Column(JSON, nullable=False, default=dict)

    station = relationship("Station", back_populates="anomalies")
    reading = relationship("Reading", back_populates="anomaly")
    correction = relationship("Correction", back_populates="anomaly", uselist=False, cascade="all, delete")

    __table_args__ = (
        ForeignKeyConstraint(
            ['reading_id', 'reading_timestamp'],
            ['readings.id', 'readings.timestamp'],
        ),
    )
