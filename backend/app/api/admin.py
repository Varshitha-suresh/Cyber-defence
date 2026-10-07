from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import User, SecurityEvent, Device
from app.security.dependencies import get_current_user
import platform
import os
import ctypes

router = APIRouter(prefix="/admin", tags=["Security Team"])

@router.get("/critical-events")
def get_critical_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # In a real app, verify if current_user has admin/secops role.
    events = db.query(SecurityEvent).filter(SecurityEvent.severity.in_(["HIGH", "CRITICAL"])).order_by(SecurityEvent.timestamp.desc()).limit(50).all()
    return events

@router.post("/intervene/block-domain")
def block_domain(domain: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Simulates blocking a domain at the OS level (e.g., via hosts file) for demonstration."""
    try:
        # NOTE: Modifying the actual hosts file requires admin privileges.
        # For the sake of the project demo, we will simulate this by logging the action.
        
        # If running on Windows with admin rights, this would be:
        # hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        # with open(hosts_path, "a") as f:
        #     f.write(f"\n127.0.0.1 {domain} # Blocked by Cyber Defence SecOps")
        
        # Register a security event
        event = SecurityEvent(
            user_id=current_user.id,
            event_type="SECOPS_INTERVENTION",
            severity="HIGH",
            description=f"Security team forcefully blocked malicious domain: {domain}",
            source="Admin Portal",
            resolved=True
        )
        db.add(event)
        db.commit()
        return {"status": "success", "message": f"Domain {domain} successfully blocked network-wide."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/intervene/lock-device")
def lock_device(device_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Simulates sending a lock command to a remote device."""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
        
    event = SecurityEvent(
        user_id=current_user.id,
        event_type="DEVICE_LOCKED",
        severity="CRITICAL",
        description=f"Security team remotely locked device {device.hostname} due to critical compromise.",
        source="Admin Portal",
        resolved=True
    )
    db.add(event)
    db.commit()
    return {"status": "success", "message": f"Lock command dispatched to device {device.hostname}."}
