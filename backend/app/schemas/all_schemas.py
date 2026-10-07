import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any

# Token & Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    professional_type: str = "Remote Employee"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    professional_type: Optional[str] = None
    telemetry_consent: Optional[bool] = None
    mfa_enabled: Optional[bool] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    professional_type: str
    mfa_enabled: bool
    telemetry_consent: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Finding Schema
class FindingSchema(BaseModel):
    id: Optional[str] = None
    category: str
    title: str
    description: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    evidence: Optional[str] = None
    confidence: float = 1.0
    score_impact: float = 0.0
    recommendation: Optional[str] = None
    is_demo: bool = False

# Recommendation Schema
class RecommendationResponse(BaseModel):
    id: str
    title: str
    category: str
    severity: str
    priority: int
    why_it_matters: str
    recommended_action: str
    estimated_risk_reduction: float
    status: str
    is_demo: bool
    created_at: datetime.datetime
    resolved_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class RecommendationUpdate(BaseModel):
    status: str  # OPEN, IN PROGRESS, RESOLVED

# Phishing Analyzer Schemas
class PhishingRequest(BaseModel):
    url: str

class PhishingIndicator(BaseModel):
    name: str
    description: str
    detected: bool
    severity: str

class PhishingResponse(BaseModel):
    url: str
    classification: str  # LEGITIMATE, PHISHING
    phishing_probability: float
    risk_score: float
    confidence: float
    indicators: List[Dict[str, Any]]
    model_name: str
    model_version: str
    prediction_timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

# Credential Exposure Schemas
class CredentialCheckRequest(BaseModel):
    email: Optional[EmailStr] = None

class CredentialCheckResponse(BaseModel):
    email: str
    status: str  # CLEAN, EXPOSED, UNAVAILABLE
    breach_count: int
    affected_services: List[str]
    source: str
    mfa_status: str
    recommended_actions: List[str]
    last_checked: datetime.datetime

# Behavioural Anomaly Schemas
class LoginEventCreate(BaseModel):
    device_id: str
    network_category: str  # HOME, PUBLIC_WIFI, VPN, CORPORATE, UNKNOWN
    location_category: str = "HOME_REGION"
    login_frequency: float = 1.0
    session_duration: float = 60.0

class BehaviourAnalysisResponse(BaseModel):
    status: str  # NORMAL, ANOMALOUS
    anomaly_score: float
    risk_contribution: float
    explanation: str
    indicators: List[str]
    model_version: str

# Device & Network Schemas
class DeviceScanResponse(BaseModel):
    device_name: str
    os: str
    os_version: str
    patch_status: str
    firewall_status: str
    antivirus_status: str
    disk_encryption_status: str
    browser_extension_count: int
    findings: List[FindingSchema]
    device_score: float

class NetworkScanResponse(BaseModel):
    network_type: str
    wifi_security: str
    local_ip: str
    dns_servers: List[str]
    gateway: str
    exposure_indicators: List[str]
    findings: List[FindingSchema]
    network_score: float

# Master Assessment Schemas
class AssessmentRunRequest(BaseModel):
    scenario: Optional[str] = None  # None, "SECURE", "MODERATE", "CRITICAL"

class AssessmentResponse(BaseModel):
    id: str
    user_id: str
    overall_score: float
    risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    category_scores: Dict[str, float]
    weighted_contributions: Dict[str, float]
    score_explanation: str
    findings: List[FindingSchema]
    recommendations: List[RecommendationResponse]
    data_sources: List[str]
    module_status: Dict[str, str]
    is_demo: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Security Event Schema
class SecurityEventResponse(BaseModel):
    id: str
    event_type: str
    category: str
    severity: str
    message: str
    source: str
    status: str
    is_demo: bool
    timestamp: datetime.datetime

    class Config:
        from_attributes = True
