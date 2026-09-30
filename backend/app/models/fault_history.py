import enum
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class FaultAction(str, enum.Enum):
    replaced = "replaced"
    calibrated = "calibrated"
    reset = "reset"
    pending = "pending"
    scheduled = "scheduled"

class FaultHistory(Base):
    __tablename__ = "fault_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, ForeignKey("stations.station_id"), nullable=False)
    component = Column(String) # e.g. "Temp Sensor", "Comm Module"
    action = Column(Enum(FaultAction))
    event_date = Column(Date)

    station = relationship("Station", back_populates="fault_history")
