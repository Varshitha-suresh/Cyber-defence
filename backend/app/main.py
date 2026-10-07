from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.database.session import engine, Base
import app.models.entities  # Ensure models are loaded for schema creation

# API Routers
from app.api.auth import router as auth_router
from app.api.assessment import router as assessment_router
from app.api.device import router as device_router
from app.api.network import router as network_router
from app.api.phishing import router as phishing_router
from app.api.credentials import router as credentials_router
from app.api.behaviour import router as behaviour_router
from app.api.recommendations import router as recommendations_router
from app.api.security_events import router as security_events_router
from app.api.risk import router as risk_router
from app.api.system import router as system_router

# Setup logging
setup_logging()

# Auto-create tables on launch (guarantees schema integrity)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-driven cyber-risk assessment and defence-advisory platform for remote professionals.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits dev Vite client
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes under /api
app.include_router(auth_router, prefix="/api")
app.include_router(assessment_router, prefix="/api")
app.include_router(device_router, prefix="/api")
app.include_router(network_router, prefix="/api")
app.include_router(phishing_router, prefix="/api")
app.include_router(credentials_router, prefix="/api")
app.include_router(behaviour_router, prefix="/api")
app.include_router(recommendations_router, prefix="/api")
app.include_router(security_events_router, prefix="/api")
app.include_router(risk_router, prefix="/api")
app.include_router(system_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    logger.info("Cyber Defence System backend initialized and operational.")
