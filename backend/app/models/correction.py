import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class OperatorDecision(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    manual_review = "manual_review"

class Correction(Base):
    __tablename__ = "corrections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    anomaly_id = Column(Integer, ForeignKey("anomalies.id"), nullable=False)
    original_value = Column(Float)
    corrected_value = Column(Float)
    confidence = Column(Float)
    methodology = Column(JSON) # jsonb or text[]
    operator_decision = Column(Enum(OperatorDecision), default=OperatorDecision.pending)

    anomaly = relationship("Anomaly", back_populates="correction")
