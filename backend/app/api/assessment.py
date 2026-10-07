from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.models.entities import User, SecurityAssessment, Recommendation
from app.security.dependencies import get_current_user
from app.services.assessment_service import assessment_service
from app.schemas.all_schemas import AssessmentRunRequest, AssessmentResponse

router = APIRouter(prefix="/assessment", tags=["Security Assessment"])

@router.post("/run", response_model=AssessmentResponse)
def run_security_assessment(
    req: AssessmentRunRequest = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    scenario = req.scenario if req else None
    assessment = assessment_service.run_assessment(db=db, user=current_user, scenario=scenario)

    # Format response
    recs = db.query(Recommendation).filter(Recommendation.assessment_id == assessment.id).all()
    category_scores = {
        "device_security": assessment.device_score,
        "network_security": assessment.network_score,
        "credential_security": assessment.credential_score,
        "phishing_risk": assessment.phishing_score,
        "behavioural_risk": assessment.behaviour_score
    }

    return {
        "id": assessment.id,
        "user_id": assessment.user_id,
        "overall_score": assessment.overall_score,
        "risk_level": assessment.risk_level,
        "category_scores": category_scores,
        "weighted_contributions": assessment.weighted_contributions or {},
        "score_explanation": assessment.score_explanation or "",
        "findings": [],
        "recommendations": recs,
        "data_sources": assessment.data_sources or [],
        "module_status": assessment.module_status or {},
        "is_demo": assessment.is_demo,
        "created_at": assessment.created_at
    }

@router.get("/latest", response_model=Optional[AssessmentResponse])
def get_latest_assessment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(SecurityAssessment)\
        .filter(SecurityAssessment.user_id == current_user.id)\
        .order_by(SecurityAssessment.created_at.desc())\
        .first()

    if not assessment:
        return None

    recs = db.query(Recommendation).filter(Recommendation.assessment_id == assessment.id).all()
    category_scores = {
        "device_security": assessment.device_score,
        "network_security": assessment.network_score,
        "credential_security": assessment.credential_score,
        "phishing_risk": assessment.phishing_score,
        "behavioural_risk": assessment.behaviour_score
    }

    return {
        "id": assessment.id,
        "user_id": assessment.user_id,
        "overall_score": assessment.overall_score,
        "risk_level": assessment.risk_level,
        "category_scores": category_scores,
        "weighted_contributions": assessment.weighted_contributions or {},
        "score_explanation": assessment.score_explanation or "",
        "findings": [],
        "recommendations": recs,
        "data_sources": assessment.data_sources or [],
        "module_status": assessment.module_status or {},
        "is_demo": assessment.is_demo,
        "created_at": assessment.created_at
    }

@router.get("/history", response_model=List[AssessmentResponse])
def get_assessment_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessments = db.query(SecurityAssessment)\
        .filter(SecurityAssessment.user_id == current_user.id)\
        .order_by(SecurityAssessment.created_at.desc())\
        .limit(limit)\
        .all()

    response = []
    for a in assessments:
        recs = db.query(Recommendation).filter(Recommendation.assessment_id == a.id).all()
        response.append({
            "id": a.id,
            "user_id": a.user_id,
            "overall_score": a.overall_score,
            "risk_level": a.risk_level,
            "category_scores": {
                "device_security": a.device_score,
                "network_security": a.network_score,
                "credential_security": a.credential_score,
                "phishing_risk": a.phishing_score,
                "behavioural_risk": a.behaviour_score
            },
            "weighted_contributions": a.weighted_contributions or {},
            "score_explanation": a.score_explanation or "",
            "findings": [],
            "recommendations": recs,
            "data_sources": a.data_sources or [],
            "module_status": a.module_status or {},
            "is_demo": a.is_demo,
            "created_at": a.created_at
        })
    return response

@router.get("/{id}", response_model=AssessmentResponse)
def get_assessment_by_id(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    a = db.query(SecurityAssessment).filter(SecurityAssessment.id == id, SecurityAssessment.user_id == current_user.id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    recs = db.query(Recommendation).filter(Recommendation.assessment_id == a.id).all()
    return {
        "id": a.id,
        "user_id": a.user_id,
        "overall_score": a.overall_score,
        "risk_level": a.risk_level,
        "category_scores": {
            "device_security": a.device_score,
            "network_security": a.network_score,
            "credential_security": a.credential_score,
            "phishing_risk": a.phishing_score,
            "behavioural_risk": a.behaviour_score
        },
        "weighted_contributions": a.weighted_contributions or {},
        "score_explanation": a.score_explanation or "",
        "findings": [],
        "recommendations": recs,
        "data_sources": a.data_sources or [],
        "module_status": a.module_status or {},
        "is_demo": a.is_demo,
        "created_at": a.created_at
    }
