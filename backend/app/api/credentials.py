from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.entities import User, CredentialExposure
from app.security.dependencies import get_current_user
from app.services.breach_service import get_breach_provider
from app.schemas.all_schemas import CredentialCheckRequest, CredentialCheckResponse

router = APIRouter(prefix="/credentials", tags=["Credential Security"])

@router.post("/check", response_model=CredentialCheckResponse)
def check_credential_exposure(
    req: CredentialCheckRequest = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_email = req.email if (req and req.email) else current_user.email
    provider = get_breach_provider()
    res = provider.check_email(target_email)

    # Persist exposure check
    exposure = CredentialExposure(
        user_id=current_user.id,
        email=target_email,
        status=res["status"],
        breach_count=res["breach_count"],
        affected_services=res["affected_services"],
        source=res["source"],
        last_checked=datetime.utcnow()
    )
    db.add(exposure)
    db.commit()

    return res

@router.get("/status", response_model=CredentialCheckResponse)
def get_credential_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest = db.query(CredentialExposure)\
        .filter(CredentialExposure.user_id == current_user.id)\
        .order_by(CredentialExposure.last_checked.desc())\
        .first()

    if latest:
        return {
            "email": latest.email,
            "status": latest.status,
            "breach_count": latest.breach_count,
            "affected_services": latest.affected_services or [],
            "source": latest.source,
            "mfa_status": "SECURE" if latest.status == "CLEAN" else "HIGH_RISK",
            "recommended_actions": ["Rotate passwords and verify 2FA"],
            "last_checked": latest.last_checked
        }

    provider = get_breach_provider()
    return provider.check_email(current_user.email)
