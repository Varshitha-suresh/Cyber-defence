from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.entities import User, SecurityEvent
from app.security.dependencies import get_current_user
from app.schemas.all_schemas import SecurityEventResponse

router = APIRouter(prefix="/security-events", tags=["Security Events"])

@router.get("", response_model=List[SecurityEventResponse])
def get_security_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    events = db.query(SecurityEvent)\
        .filter(SecurityEvent.user_id == current_user.id)\
        .order_by(SecurityEvent.timestamp.desc())\
        .limit(30)\
        .all()
    return events
