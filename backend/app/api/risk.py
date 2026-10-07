from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, SecurityAssessment
from app.security.dependencies import get_current_user
from app.api.assessment import get_latest_assessment, get_assessment_history

router = APIRouter(prefix="/risk", tags=["Risk Information"])

@router.get("/current")
def get_current_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_latest_assessment(current_user=current_user, db=db)

@router.get("/history")
def get_historical_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_assessment_history(limit=20, current_user=current_user, db=db)
