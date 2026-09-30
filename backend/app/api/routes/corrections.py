from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.correction import Correction, OperatorDecision
from app.models.anomaly import Anomaly, AnomalyStatus

router = APIRouter(prefix="/api/corrections", tags=["Corrections"])

class DecisionUpdate(BaseModel):
    decision: str

@router.patch("/{id}/decision")
def update_decision(id: int, payload: DecisionUpdate, db: Session = Depends(get_db)):
    correction = db.query(Correction).filter(Correction.id == id).first()
    if not correction:
        raise HTTPException(status_code=404, detail="Correction not found")
        
    if payload.decision == "accepted":
        correction.operator_decision = OperatorDecision.accepted
        anomaly = db.query(Anomaly).filter(Anomaly.id == correction.anomaly_id).first()
        if anomaly:
            anomaly.status = AnomalyStatus.resolved
    elif payload.decision == "rejected":
        correction.operator_decision = OperatorDecision.rejected
    elif payload.decision == "manual_review":
        # Maybe add manual_review to Enum if it doesn't exist, but we can store it or just reject for now.
        correction.operator_decision = "manual_review"
    else:
        raise HTTPException(status_code=400, detail="Invalid decision")

    db.commit()
    db.refresh(correction)
    return {
        "message": f"Correction {payload.decision}",
        "correction": {
            "id": correction.id,
            "operator_decision": correction.operator_decision
        }
    }
