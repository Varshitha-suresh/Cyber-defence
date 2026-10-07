from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.session import get_db
from app.models.entities import User, LoginEvent
from app.security.dependencies import get_current_user
from ml.inference.behavioural_detector import behavioural_detector
from app.schemas.all_schemas import LoginEventCreate, BehaviourAnalysisResponse

router = APIRouter(prefix="/behaviour", tags=["Behavioural Security"])

@router.post("/analyze", response_model=BehaviourAnalysisResponse)
def analyze_behavioural_event(
    evt: LoginEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = behavioural_detector.analyze_event(
        timestamp=datetime.utcnow(),
        device_id=evt.device_id,
        network_category=evt.network_category,
        location_category=evt.location_category,
        login_frequency=evt.login_frequency,
        session_duration=evt.session_duration
    )

    # Persist login event
    record = LoginEvent(
        user_id=current_user.id,
        device_id=evt.device_id,
        network_category=evt.network_category,
        location_category=evt.location_category,
        login_frequency=evt.login_frequency,
        session_duration=evt.session_duration,
        is_anomalous=bool(analysis["status"] == "ANOMALOUS"),
        anomaly_score=analysis["anomaly_score"],
        risk_contribution=analysis["risk_contribution"],
        explanation=analysis["explanation"]
    )
    db.add(record)
    db.commit()

    return analysis

@router.get("/history")
def get_behaviour_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(LoginEvent)\
        .filter(LoginEvent.user_id == current_user.id)\
        .order_by(LoginEvent.timestamp.desc())\
        .limit(20)\
        .all()
    
    return [
        {
            "id": e.id,
            "device_id": e.device_id,
            "network_category": e.network_category,
            "location_category": e.location_category,
            "login_frequency": e.login_frequency,
            "session_duration": e.session_duration,
            "is_anomalous": e.is_anomalous,
            "anomaly_score": e.anomaly_score,
            "explanation": e.explanation,
            "timestamp": e.timestamp
        }
        for e in events
    ]
