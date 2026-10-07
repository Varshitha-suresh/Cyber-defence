from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User
from app.security.dependencies import get_current_user
from app.scanners.device_scanner import device_scanner
from app.schemas.all_schemas import DeviceScanResponse

router = APIRouter(prefix="/device", tags=["Device Security"])

@router.post("/scan", response_model=DeviceScanResponse)
def scan_device_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = device_scanner.scan_device(is_demo=False)
    return result

@router.get("/security", response_model=DeviceScanResponse)
def get_device_security(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return device_scanner.scan_device(is_demo=False)
