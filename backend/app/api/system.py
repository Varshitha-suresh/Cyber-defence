import platform
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db
from app.core.config import settings
from ml.inference.phishing_predictor import phishing_predictor
from ml.inference.behavioural_detector import behavioural_detector

router = APIRouter(tags=["System & Status"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@router.get("/system/status")
def system_status(db: Session = Depends(get_db)):
    # 1. Database check
    db_status = "ERROR"
    try:
        db.execute(text("SELECT 1"))
        db_status = "CONNECTED"
    except Exception:
        db_status = "ERROR"

    # 2. Phishing Model
    phish_status = "READY" if (phishing_predictor.model is not None) else "NOT READY (HEURISTIC FALLBACK)"

    # 3. Anomaly Model
    anom_status = "READY" if (behavioural_detector.model is not None) else "NOT READY"

    # 4. Breach Intelligence
    breach_status = "CONNECTED (Live HIBP API)" if settings.BREACH_API_KEY else "CONNECTED (Academic Demo Corpus)"

    # 5. Telemetry
    os_name = platform.system()
    device_col = "AVAILABLE" if os_name in ["Windows", "Linux", "Darwin"] else "LIMITED"
    net_col = "AVAILABLE" if os_name in ["Windows", "Linux"] else "LIMITED"

    return {
        "database": db_status,
        "ml_model_overall": "READY" if (phish_status == "READY" and anom_status == "READY") else "DEGRADED",
        "phishing_classifier": phish_status,
        "anomaly_detector": anom_status,
        "breach_api": breach_status,
        "device_collector": device_col,
        "network_collector": net_col,
        "platform_os": os_name,
        "environment": settings.ENVIRONMENT
    }
