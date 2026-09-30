from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.schemas.anomaly import AnomalyResponse
from app.models.anomaly import Anomaly

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])

@router.get("/", response_model=list[AnomalyResponse])
def get_anomalies(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    anomalies = db.query(Anomaly).order_by(desc(Anomaly.detected_at)).offset(skip).limit(limit).all()
    # NFR: Every anomaly response must include non-empty temporal_evidence, physical_consistency, and spatial_evidence fields
    # Ensure they are returned properly (they are JSONB in model, default dict)
    
    return anomalies