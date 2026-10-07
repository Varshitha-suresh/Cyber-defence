from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database.session import get_db
from app.models.entities import User, Recommendation
from app.security.dependencies import get_current_user
from app.schemas.all_schemas import RecommendationResponse, RecommendationUpdate

router = APIRouter(prefix="/recommendations", tags=["Remediation Recommendations"])

@router.get("", response_model=List[RecommendationResponse])
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recs = db.query(Recommendation)\
        .filter(Recommendation.user_id == current_user.id)\
        .order_by(Recommendation.priority.asc(), Recommendation.created_at.desc())\
        .all()
    return recs

@router.patch("/{id}", response_model=RecommendationResponse)
def update_recommendation_status(
    id: str,
    update: RecommendationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(Recommendation.id == id, Recommendation.user_id == current_user.id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    rec.status = update.status
    if update.status == "RESOLVED":
        rec.resolved_at = datetime.utcnow()
    else:
        rec.resolved_at = None

    db.commit()
    db.refresh(rec)
    return rec
