from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User
from app.security.dependencies import get_current_user
from app.scanners.network_scanner import network_scanner
from app.schemas.all_schemas import NetworkScanResponse

router = APIRouter(prefix="/network", tags=["Network Security"])

@router.post("/scan", response_model=NetworkScanResponse)
def scan_network_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return network_scanner.scan_network(is_demo=False)

@router.get("/security", response_model=NetworkScanResponse)
def get_network_security(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return network_scanner.scan_network(is_demo=False)
