import os
import sys
import datetime
from sqlalchemy.orm import Session

# Setup python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(parent_dir, "backend"))
sys.path.insert(0, parent_dir)

from app.database.session import SessionLocal, Base, engine
from app.models.entities import (
    User, Device, SecurityAssessment, DeviceFinding, NetworkFinding,
    PhishingScan, CredentialExposure, LoginEvent, Recommendation, SecurityEvent
)
from app.security.auth import get_password_hash

def seed_database():
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if already seeded
        existing_user = db.query(User).filter(User.email == "alex.freelancer@cyberwork.io").first()
        if existing_user:
            print("Database already contains demo user. Refreshing demo scenarios...")
            return

        print("Seeding academic demonstration accounts and scenarios...")

        # 1. Primary Demo User
        demo_user = User(
            name="Alex Rivera",
            email="alex.freelancer@cyberwork.io",
            hashed_password=get_password_hash("CyberDefense2026!"),
            professional_type="Freelancer",
            mfa_enabled=False,
            telemetry_consent=True
        )
        db.add(demo_user)
        db.flush()

        # 2. Registered Work Device
        device = Device(
            user_id=demo_user.id,
            device_name="ALEX-DELL-XPS-FREELANCE",
            os="Windows 11 Pro",
            os_version="23H2 (Build 22631)",
            hostname="alex-dev-node",
            is_current_device=True,
            last_scanned=datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        )
        db.add(device)
        db.flush()

        # 3. Baseline Security Assessment (Score: 42.5 - MODERATE)
        assessment = SecurityAssessment(
            user_id=demo_user.id,
            overall_score=42.5,
            risk_level="MODERATE",
            device_score=40.0,
            network_score=45.0,
            credential_score=55.0,
            phishing_score=35.0,
            behaviour_score=32.0,
            weighted_contributions={
                "device_security": 10.0,
                "network_security": 9.0,
                "credential_security": 11.0,
                "phishing_risk": 7.0,
                "behavioural_risk": 5.5
            },
            module_status={
                "device_module": "AVAILABLE",
                "network_module": "AVAILABLE",
                "credential_module": "AVAILABLE",
                "phishing_module": "AVAILABLE",
                "behaviour_module": "AVAILABLE"
            },
            data_sources=[
                "Endpoint Host Telemetry (OS/Firewall/EDR)",
                "Local Network Adapter & Resolver Inspection",
                "Breach Intelligence (DemoBreachProvider)",
                "Random Forest URL Classification ML Model",
                "Isolation Forest Behavioral Anomaly ML Model"
            ],
            score_explanation="Overall Cyber Risk Index is 42.5/100 (MODERATE). Credential exposures and unencrypted DNS resolvers represent the largest contributors.",
            is_demo=True,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        )
        db.add(assessment)
        db.flush()

        # Historical Assessment 7 days ago (Score: 68.0 - HIGH) to show trend
        hist_assessment = SecurityAssessment(
            user_id=demo_user.id,
            overall_score=68.0,
            risk_level="HIGH",
            device_score=75.0,
            network_score=70.0,
            credential_score=75.0,
            phishing_score=60.0,
            behaviour_score=50.0,
            weighted_contributions={
                "device_security": 18.7,
                "network_security": 14.0,
                "credential_security": 15.0,
                "phishing_risk": 12.0,
                "behavioural_risk": 8.3
            },
            module_status={"all": "AVAILABLE"},
            data_sources=["Full Telemetry Stack"],
            score_explanation="Initial baseline assessment before firewall remediation.",
            is_demo=True,
            created_at=datetime.datetime.utcnow() - datetime.timedelta(days=7)
        )
        db.add(hist_assessment)
        db.flush()

        # 4. Actionable Recommendations
        recs = [
            Recommendation(
                user_id=demo_user.id,
                assessment_id=assessment.id,
                title="Remediate: Turn On Multi-Factor Authentication",
                category="Credential Security",
                severity="HIGH",
                priority=1,
                why_it_matters="Email found in 3 known historical breach collections (LinkedIn, Canva, Dropbox).",
                recommended_action="Enable app-based authenticator (TOTP) or FIDO2 hardware key immediately.",
                estimated_risk_reduction=12.0,
                status="OPEN",
                is_demo=True
            ),
            Recommendation(
                user_id=demo_user.id,
                assessment_id=assessment.id,
                title="Remediate: Configure Encrypted DNS (DoH/DoT)",
                category="Network Security",
                severity="MEDIUM",
                priority=2,
                why_it_matters="ISP cleartext DNS resolver is currently leaking remote client query domains.",
                recommended_action="Switch DNS resolver to Cloudflare 1.1.1.1 or Quad9 with DNS-over-HTTPS in browser.",
                estimated_risk_reduction=8.0,
                status="OPEN",
                is_demo=True
            ),
            Recommendation(
                user_id=demo_user.id,
                assessment_id=assessment.id,
                title="Remediate: Apply Cumulative OS Security Updates",
                category="Device Security",
                severity="MEDIUM",
                priority=3,
                why_it_matters="System missing latest cumulative security rollups.",
                recommended_action="Run Windows Update and perform restart during non-work hours.",
                estimated_risk_reduction=10.0,
                status="IN PROGRESS",
                is_demo=True
            )
        ]
        for r in recs:
            db.add(r)

        # 5. Phishing Scans History
        scans = [
            PhishingScan(
                user_id=demo_user.id,
                url="http://192.168.1.100/paypal-update/verification/login.php?cmd=_login-run",
                classification="PHISHING",
                phishing_probability=0.96,
                risk_score=96.0,
                confidence=0.96,
                indicators=[
                    {"name": "Raw IP Hostname", "description": "Numeric IP destination bypassing DNS checks", "severity": "CRITICAL"},
                    {"name": "Targeted Brand Impersonation", "description": "Contains paypal keyword in path", "severity": "HIGH"}
                ],
                is_demo=True
            ),
            PhishingScan(
                user_id=demo_user.id,
                url="https://github.com/torvalds/linux",
                classification="LEGITIMATE",
                phishing_probability=0.03,
                risk_score=3.0,
                confidence=0.97,
                indicators=[],
                is_demo=True
            )
        ]
        for s in scans:
            db.add(s)

        # 6. Login Events
        logins = [
            LoginEvent(
                user_id=demo_user.id,
                device_id="ALEX-DELL-XPS-FREELANCE",
                network_category="HOME",
                location_category="HOME_REGION",
                login_frequency=1.2,
                session_duration=120.0,
                is_anomalous=False,
                anomaly_score=0.12,
                risk_contribution=3.0,
                explanation="Standard daytime authentication from home office subnet.",
                is_demo=True
            ),
            LoginEvent(
                user_id=demo_user.id,
                device_id="UNKNOWN-MAC-DEV",
                network_category="PUBLIC_WIFI",
                location_category="DOMESTIC_TRAVEL",
                login_frequency=3.8,
                session_duration=22.0,
                is_anomalous=True,
                anomaly_score=0.68,
                risk_contribution=45.0,
                explanation="Late night login from untrusted public Wi-Fi on unfamiliar device footprint.",
                is_demo=True
            )
        ]
        for l in logins:
            db.add(l)

        # 7. Security Events Log
        events = [
            SecurityEvent(
                user_id=demo_user.id,
                event_type="BREACH_EXPOSURE_DETECTED",
                category="Credential Security",
                severity="HIGH",
                message="Credential monitoring alert: email found in circulating credential stuffing dumps.",
                source="DemoBreachProvider",
                status="ACTION_REQUIRED",
                is_demo=True
            ),
            SecurityEvent(
                user_id=demo_user.id,
                event_type="UNUSUAL_LOGIN_DETECTED",
                category="Behavioural Risk",
                severity="MEDIUM",
                message="Anomalous login flagged by Isolation Forest detector from Public Wi-Fi.",
                source="IsolationForest",
                status="NEW",
                is_demo=True
            ),
            SecurityEvent(
                user_id=demo_user.id,
                event_type="ASSESSMENT_COMPLETED",
                category="System Audit",
                severity="MODERATE",
                message="Scheduled Cyber Risk Index evaluation calculated at 42.5/100 (MODERATE).",
                source="MasterAssessmentPipeline",
                status="RESOLVED",
                is_demo=True
            )
        ]
        for ev in events:
            db.add(ev)

        db.commit()
        print("Database seed successfully executed! Default credentials:")
        print("Email: alex.freelancer@cyberwork.io")
        print("Password: CyberDefense2026!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
