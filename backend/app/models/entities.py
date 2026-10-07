import datetime
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    professional_type = Column(String(100), default="Remote Employee")  # Remote Employee, Freelancer, Contractor, Gig Worker, Other
    mfa_enabled = Column(Boolean, default=False)
    telemetry_consent = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("SecurityAssessment", back_populates="user", cascade="all, delete-orphan")
    login_events = relationship("LoginEvent", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    security_events = relationship("SecurityEvent", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class Device(Base):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    device_name = Column(String(255), nullable=False)
    os = Column(String(100), nullable=False)
    os_version = Column(String(100))
    hostname = Column(String(255))
    is_current_device = Column(Boolean, default=True)
    last_scanned = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="devices")
    findings = relationship("DeviceFinding", back_populates="device", cascade="all, delete-orphan")


class SecurityAssessment(Base):
    __tablename__ = "security_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    overall_score = Column(Float, nullable=False)  # 0 to 100
    risk_level = Column(String(50), nullable=False)  # LOW, MODERATE, HIGH, CRITICAL
    
    # Sub-scores
    device_score = Column(Float, nullable=False)
    network_score = Column(Float, nullable=False)
    credential_score = Column(Float, nullable=False)
    phishing_score = Column(Float, nullable=False)
    behaviour_score = Column(Float, nullable=False)

    weighted_contributions = Column(JSON, default=dict)
    module_status = Column(JSON, default=dict)
    data_sources = Column(JSON, default=list)
    score_explanation = Column(Text)
    is_demo = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user = relationship("User", back_populates="assessments")
    recommendations = relationship("Recommendation", back_populates="assessment", cascade="all, delete-orphan")


class DeviceFinding(Base):
    __tablename__ = "device_findings"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    device_id = Column(String(36), ForeignKey("devices.id"), nullable=True, index=True)
    assessment_id = Column(String(36), ForeignKey("security_assessments.id"), nullable=True, index=True)
    category = Column(String(100), default="Device Security")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    evidence = Column(Text)
    confidence = Column(Float, default=1.0)
    score_impact = Column(Float, default=0.0)
    recommendation = Column(Text)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    device = relationship("Device", back_populates="findings")


class NetworkFinding(Base):
    __tablename__ = "network_findings"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    assessment_id = Column(String(36), ForeignKey("security_assessments.id"), nullable=True, index=True)
    category = Column(String(100), default="Network Security")
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)
    evidence = Column(Text)
    confidence = Column(Float, default=1.0)
    score_impact = Column(Float, default=0.0)
    recommendation = Column(Text)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PhishingScan(Base):
    __tablename__ = "phishing_scans"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    assessment_id = Column(String(36), ForeignKey("security_assessments.id"), nullable=True, index=True)
    url = Column(Text, nullable=False)
    classification = Column(String(50), nullable=False)  # LEGITIMATE, PHISHING
    phishing_probability = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    indicators = Column(JSON, default=list)
    model_name = Column(String(100), default="RandomForest_URL_Classifier")
    model_version = Column(String(50), default="1.0.0")
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CredentialExposure(Base):
    __tablename__ = "credential_exposures"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    status = Column(String(50), nullable=False)  # CLEAN, EXPOSED, UNAVAILABLE
    breach_count = Column(Integer, default=0)
    affected_services = Column(JSON, default=list)
    source = Column(String(100), default="DemoBreachProvider")
    last_checked = Column(DateTime, default=datetime.datetime.utcnow)
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class LoginEvent(Base):
    __tablename__ = "login_events"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    device_id = Column(String(100), nullable=False)
    network_category = Column(String(100), nullable=False)  # HOME, PUBLIC_WIFI, VPN, CORPORATE, UNKNOWN
    location_category = Column(String(100), default="HOME_REGION")
    login_frequency = Column(Float, default=1.0)  # logins in last 24h
    session_duration = Column(Float, default=60.0)  # minutes
    is_anomalous = Column(Boolean, default=False)
    anomaly_score = Column(Float, default=0.0)
    risk_contribution = Column(Float, default=0.0)
    explanation = Column(Text)
    is_demo = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user = relationship("User", back_populates="login_events")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    assessment_id = Column(String(36), ForeignKey("security_assessments.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    priority = Column(Integer, default=1)  # 1 is highest priority
    why_it_matters = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    estimated_risk_reduction = Column(Float, default=5.0)
    status = Column(String(50), default="OPEN")  # OPEN, IN PROGRESS, RESOLVED
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="recommendations")
    assessment = relationship("SecurityAssessment", back_populates="recommendations")


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    source = Column(String(100), default="System")
    status = Column(String(50), default="NEW")
    is_demo = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    user = relationship("User", back_populates="security_events")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
