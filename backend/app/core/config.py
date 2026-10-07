import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cyber Defence System for Remote Professionals"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./cyber_defence.db"
    
    # JWT & Auth
    JWT_SECRET: str = "super-secret-cyber-defence-jwt-key-change-in-production-min32chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Breach Intelligence Provider
    BREACH_API_URL: str = "https://haveibeenpwned.com/api/v3"
    BREACH_API_KEY: str = ""
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # Risk Scoring default weights
    WEIGHT_DEVICE: float = 0.25
    WEIGHT_NETWORK: float = 0.20
    WEIGHT_CREDENTIAL: float = 0.20
    WEIGHT_PHISHING: float = 0.20
    WEIGHT_BEHAVIOUR: float = 0.15

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
