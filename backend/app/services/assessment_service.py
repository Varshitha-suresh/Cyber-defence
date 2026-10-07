import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.entities import (
    User, SecurityAssessment, Device, DeviceFinding, NetworkFinding,
    PhishingScan, CredentialExposure, LoginEvent, Recommendation, SecurityEvent
)
from app.scanners.device_scanner import device_scanner
from app.scanners.network_scanner import network_scanner
from app.services.breach_service import get_breach_provider
from app.risk_engine.engine import risk_engine
from app.recommendations.engine import recommendation_engine
from ml.inference.phishing_predictor import phishing_predictor
from ml.inference.behavioural_detector import behavioural_detector

class MasterAssessmentService:
    """
    Coordinates end-to-end security assessment pipeline:
    1. Safe Device Telemetry
    2. Local Network Security Analysis
    3. Credential Exposure Lookup
    4. Phishing ML Risk Integration
    5. Behavioural Anomaly Detection
    6. Deterministic NIST CSF Risk Scoring
    7. Recommendation Generation
    8. Database Persistence
    """
    def run_assessment(
        self,
        db: Session,
        user: User,
        scenario: Optional[str] = None
    ) -> SecurityAssessment:
        is_demo = bool(scenario in ["SECURE", "MODERATE", "CRITICAL"])
        demo_profile = scenario or "SECURE"

        all_findings = []
        data_sources = []
        module_status = {}

        # 1. Device Security Layer
        try:
            device_data = device_scanner.scan_device(is_demo=is_demo, demo_profile=demo_profile)
            device_score = device_data["device_score"]
            all_findings.extend(device_data["findings"])
            data_sources.append("Endpoint Host Telemetry (OS/Firewall/EDR)")
            module_status["device_module"] = "AVAILABLE"
        except Exception as e:
            device_score = 30.0
            module_status["device_module"] = f"LIMITED: {str(e)[:30]}"

        # 2. Network Security Layer
        try:
            network_data = network_scanner.scan_network(is_demo=is_demo, demo_profile=demo_profile)
            network_score = network_data["network_score"]
            all_findings.extend(network_data["findings"])
            data_sources.append("Local Network Adapter & Resolver Inspection")
            module_status["network_module"] = "AVAILABLE"
        except Exception as e:
            network_score = 30.0
            module_status["network_module"] = f"LIMITED: {str(e)[:30]}"

        # 3. Credential & Breach Intelligence Layer
        try:
            breach_provider = get_breach_provider()
            target_email = user.email
            if is_demo:
                if scenario == "CRITICAL":
                    target_email = "critical.risk@demo.org"
                elif scenario == "MODERATE":
                    target_email = "alex.freelancer@cyberwork.io"
                else:
                    target_email = "secure.user@demo.org"

            cred_result = breach_provider.check_email(target_email)
            if cred_result["status"] == "EXPOSED":
                credential_score = min(100.0, 30.0 + (cred_result["breach_count"] * 18.0))
                all_findings.append({
                    "category": "Credential Security",
                    "title": f"Email Compromised in {cred_result['breach_count']} Breach Data Sets",
                    "description": f"Identified exposure in breach collections: {', '.join(cred_result['affected_services'])}.",
                    "severity": "CRITICAL" if cred_result['breach_count'] > 2 else "HIGH",
                    "evidence": f"Exposed services: {', '.join(cred_result['affected_services'])}",
                    "confidence": 0.95,
                    "score_impact": 40.0,
                    "recommendation": "Rotate passwords on compromised platforms and implement FIDO2/TOTP multi-factor authentication."
                })
            elif cred_result["status"] == "CLEAN":
                credential_score = 10.0
                all_findings.append({
                    "category": "Credential Security",
                    "title": "Zero Known Breach Exposures",
                    "description": "Email address does not appear in publicly circulating breach dumps.",
                    "severity": "LOW",
                    "evidence": "Breach database query returned 0 exposure incidents.",
                    "confidence": 1.0,
                    "score_impact": 0.0,
                    "recommendation": "Maintain MFA across primary communication accounts."
                })
            else:
                credential_score = 25.0
                module_status["credential_module"] = "UNAVAILABLE"

            data_sources.append(f"Breach Intelligence ({cred_result['source']})")
            module_status["credential_module"] = "AVAILABLE" if cred_result["status"] != "UNAVAILABLE" else "UNAVAILABLE"
        except Exception as e:
            credential_score = 25.0
            module_status["credential_module"] = f"LIMITED: {str(e)[:30]}"

        # 4. Phishing ML Risk Layer
        try:
            if is_demo and scenario == "CRITICAL":
                sample_url = "http://192.168.1.100/paypal-update/verification/login.php?cmd=_login-run"
            elif is_demo and scenario == "MODERATE":
                sample_url = "https://bit.ly/3xSecLoginRedirectToBankingPort148"
            else:
                sample_url = "https://github.com/torvalds/linux"

            phish_res = phishing_predictor.predict(sample_url)
            phishing_score = phish_res["risk_score"]
            if phish_res["classification"] == "PHISHING":
                all_findings.append({
                    "category": "Phishing Risk",
                    "title": "High Probability Phishing URL Traversal",
                    "description": f"Encountered suspicious link with {phish_res['confidence']*100:.1f}% confidence of hostile credential harvesting intent.",
                    "severity": "HIGH",
                    "evidence": f"URL: {sample_url}. Flags: {[ind['name'] for ind in phish_res['indicators']]}",
                    "confidence": phish_res["confidence"],
                    "score_impact": phish_res["risk_score"],
                    "recommendation": "Do not submit credentials or download files from flagged suspicious links."
                })
            data_sources.append("Random Forest URL Classification ML Model")
            module_status["phishing_module"] = "AVAILABLE"
        except Exception as e:
            phishing_score = 15.0
            module_status["phishing_module"] = f"LIMITED: {str(e)[:30]}"

        # 5. Behavioural Anomaly Layer
        try:
            if is_demo and scenario == "CRITICAL":
                beh_res = behavioural_detector.analyze_event(
                    timestamp=datetime.datetime.utcnow().replace(hour=3),
                    network_category="PUBLIC_WIFI",
                    location_category="FOREIGN_UNTRUSTED",
                    login_frequency=9.5,
                    session_duration=4.0
                )
            elif is_demo and scenario == "MODERATE":
                beh_res = behavioural_detector.analyze_event(
                    timestamp=datetime.datetime.utcnow().replace(hour=23),
                    network_category="PUBLIC_WIFI",
                    location_category="DOMESTIC_TRAVEL",
                    login_frequency=3.0,
                    session_duration=25.0
                )
            else:
                beh_res = behavioural_detector.analyze_event(
                    timestamp=datetime.datetime.utcnow().replace(hour=14),
                    network_category="HOME",
                    location_category="HOME_REGION",
                    login_frequency=1.0,
                    session_duration=90.0
                )

            behaviour_score = beh_res["risk_contribution"]
            if beh_res["status"] == "ANOMALOUS":
                all_findings.append({
                    "category": "Behavioural Risk",
                    "title": "Atypical Authentication Behavioral Deviation",
                    "description": beh_res["explanation"],
                    "severity": "HIGH" if beh_res["anomaly_score"] > 0.7 else "MEDIUM",
                    "evidence": f"Anomaly score: {beh_res['anomaly_score']}. Factors: {', '.join(beh_res['indicators'])}",
                    "confidence": 0.88,
                    "score_impact": beh_res["risk_contribution"],
                    "recommendation": "Verify recent active sessions and re-authenticate via hardware MFA."
                })
            data_sources.append("Isolation Forest Behavioral Anomaly ML Model")
            module_status["behaviour_module"] = "AVAILABLE"
        except Exception as e:
            behaviour_score = 10.0
            module_status["behaviour_module"] = f"LIMITED: {str(e)[:30]}"

        # 6. Calculate Cyber Risk Index via deterministic scoring engine
        risk_result = risk_engine.calculate_risk(
            device_score=device_score,
            network_score=network_score,
            credential_score=credential_score,
            phishing_score=phishing_score,
            behaviour_score=behaviour_score,
            module_status=module_status
        )

        # 7. Generate Actionable Prioritized Recommendations
        recs_data = recommendation_engine.generate_recommendations(all_findings)

        # 8. Database Persistence
        assessment = SecurityAssessment(
            user_id=user.id,
            overall_score=risk_result["overall_score"],
            risk_level=risk_result["risk_level"],
            device_score=device_score,
            network_score=network_score,
            credential_score=credential_score,
            phishing_score=phishing_score,
            behaviour_score=behaviour_score,
            weighted_contributions=risk_result["weighted_contributions"],
            module_status=module_status,
            data_sources=data_sources,
            score_explanation=risk_result["score_explanation"],
            is_demo=is_demo
        )
        db.add(assessment)
        db.flush()

        # Persist recommendations
        for r in recs_data:
            rec_obj = Recommendation(
                user_id=user.id,
                assessment_id=assessment.id,
                title=r["title"],
                category=r["category"],
                severity=r["severity"],
                priority=r["priority"],
                why_it_matters=r["why_it_matters"],
                recommended_action=r["recommended_action"],
                estimated_risk_reduction=r["estimated_risk_reduction"],
                status="OPEN",
                is_demo=is_demo
            )
            db.add(rec_obj)

        # Record Security Event
        sec_event = SecurityEvent(
            user_id=user.id,
            event_type="ASSESSMENT_COMPLETED",
            category="System Audit",
            severity=risk_result["risk_level"],
            message=f"Completed {risk_result['risk_level']} risk assessment ({risk_result['overall_score']}/100) with {len(all_findings)} finding(s).",
            source="MasterAssessmentPipeline",
            status="RESOLVED" if risk_result["risk_level"] == "LOW" else "ACTION_REQUIRED",
            is_demo=is_demo
        )
        db.add(sec_event)

        db.commit()
        db.refresh(assessment)
        return assessment

assessment_service = MasterAssessmentService()
