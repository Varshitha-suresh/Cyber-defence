from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.entities import User, PhishingScan
from app.security.dependencies import get_current_user
from ml.inference.phishing_predictor import phishing_predictor
from app.schemas.all_schemas import PhishingRequest, PhishingResponse

router = APIRouter(prefix="/phishing", tags=["Phishing ML Analyzer"])

@router.post("/analyze", response_model=PhishingResponse)
def analyze_phishing_url(
    req: PhishingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prediction = phishing_predictor.predict(req.url)

    # Persist the scan audit
    scan_record = PhishingScan(
        user_id=current_user.id,
        url=req.url,
        classification=prediction["classification"],
        phishing_probability=prediction["phishing_probability"],
        risk_score=prediction["risk_score"],
        confidence=prediction["confidence"],
        indicators=prediction["indicators"],
        model_name=prediction["model_name"],
        model_version=prediction["model_version"]
    )
    db.add(scan_record)
    db.commit()

    return prediction

@router.get("/history", response_model=List[PhishingResponse])
def get_phishing_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scans = db.query(PhishingScan)\
        .filter(PhishingScan.user_id == current_user.id)\
        .order_by(PhishingScan.created_at.desc())\
        .limit(20)\
        .all()
    
    return [
        {
            "url": s.url,
            "classification": s.classification,
            "phishing_probability": s.phishing_probability,
            "risk_score": s.risk_score,
            "confidence": s.confidence,
            "indicators": s.indicators or [],
            "model_name": s.model_name,
            "model_version": s.model_version,
            "prediction_timestamp": s.created_at
        }
        for s in scans
    ]
