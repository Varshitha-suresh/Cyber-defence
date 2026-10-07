import os
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from app.core.config import settings

class BreachIntelligenceProvider(ABC):
    """
    Abstract Base Class for Credential/Breach Intelligence.
    Never collects or stores passwords.
    Only checks registered email against known credential exposures.
    """
    @abstractmethod
    def check_email(self, email: str) -> Dict[str, Any]:
        pass

class ExternalBreachProvider(BreachIntelligenceProvider):
    """
    Queries real external breach-intelligence API (e.g. HIBP v3) using secure environment key.
    Handles rate limits, network timeouts, and returns UNAVAILABLE when credentials/network fail.
    """
    def __init__(self, api_url: str = settings.BREACH_API_URL, api_key: str = settings.BREACH_API_KEY):
        self.api_url = api_url
        self.api_key = api_key

    def check_email(self, email: str) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "status": "UNAVAILABLE",
                "email": email,
                "breach_count": 0,
                "affected_services": [],
                "source": "ExternalBreachProvider (No API key configured)",
                "mfa_status": "UNKNOWN",
                "recommended_actions": ["Configure BREACH_API_KEY or use DemoBreachProvider."],
                "last_checked": datetime.utcnow()
            }

        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "CyberDefenceSystem-RemotePro/1.0"
        }
        url = f"{self.api_url}/breachedaccount/{email}?truncateResponse=false"

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                breaches = resp.json()
                services = [b.get("Name", "Unknown") for b in breaches]
                return {
                    "status": "EXPOSED",
                    "email": email,
                    "breach_count": len(services),
                    "affected_services": services,
                    "source": "ExternalBreachProvider (Verified)",
                    "mfa_status": "CRITICAL_ACTION_REQUIRED",
                    "recommended_actions": [
                        "Change passwords immediately on all affected services.",
                        "Enforce hardware/app-based MFA (FIDO2 or TOTP).",
                        "Never reuse credentials across corporate and personal accounts."
                    ],
                    "last_checked": datetime.utcnow()
                }
            elif resp.status_code == 404:
                return {
                    "status": "CLEAN",
                    "email": email,
                    "breach_count": 0,
                    "affected_services": [],
                    "source": "ExternalBreachProvider (Verified)",
                    "mfa_status": "HEALTHY",
                    "recommended_actions": ["Maintain proactive password rotation and continuous monitoring."],
                    "last_checked": datetime.utcnow()
                }
            else:
                return {
                    "status": "UNAVAILABLE",
                    "email": email,
                    "breach_count": 0,
                    "affected_services": [],
                    "source": f"ExternalBreachProvider (HTTP {resp.status_code})",
                    "mfa_status": "UNKNOWN",
                    "recommended_actions": ["External breach provider returned non-200 status."],
                    "last_checked": datetime.utcnow()
                }
        except Exception as e:
            return {
                "status": "UNAVAILABLE",
                "email": email,
                "breach_count": 0,
                "affected_services": [],
                "source": f"ExternalBreachProvider (Error: {str(e)[:40]})",
                "mfa_status": "UNKNOWN",
                "recommended_actions": ["External API network unreachable."],
                "last_checked": datetime.utcnow()
            }


class DemoBreachProvider(BreachIntelligenceProvider):
    """
    Academic Demonstration Provider with realistic known breach corpora.
    Clearly labeled as demonstration data.
    """
    KNOWN_EXPOSURES = {
        "alex.freelancer@cyberwork.io": {
            "status": "EXPOSED",
            "breaches": ["LinkedIn (2021 Scraping)", "Canva (2019 Breach)", "Dropbox (2016 Legacy)"]
        },
        "critical.risk@demo.org": {
            "status": "EXPOSED",
            "breaches": ["Adobe Systems (2013)", "Collection #1 (2019)", "Verifications.io", "Exploit.in Combo"]
        },
        "secure.user@demo.org": {
            "status": "CLEAN",
            "breaches": []
        }
    }

    def check_email(self, email: str) -> Dict[str, Any]:
        email_clean = email.strip().lower()
        if email_clean in self.KNOWN_EXPOSURES:
            data = self.KNOWN_EXPOSURES[email_clean]
            if data["status"] == "EXPOSED":
                return {
                    "status": "EXPOSED",
                    "email": email,
                    "breach_count": len(data["breaches"]),
                    "affected_services": data["breaches"],
                    "source": "DemoBreachProvider (Synthetic Academic Corpus)",
                    "mfa_status": "HIGH_RISK",
                    "recommended_actions": [
                        "Change password immediately for all flagged breached platforms.",
                        "Deploy unique 16+ character passwords via a password manager.",
                        "Enforce Authenticator App (TOTP) or Security Key on email and cloud accounts."
                    ],
                    "last_checked": datetime.utcnow()
                }
            else:
                return {
                    "status": "CLEAN",
                    "email": email,
                    "breach_count": 0,
                    "affected_services": [],
                    "source": "DemoBreachProvider (Synthetic Academic Corpus)",
                    "mfa_status": "SECURE",
                    "recommended_actions": ["No public compromise records found. Continue good credential hygiene."],
                    "last_checked": datetime.utcnow()
                }

        # For any unspecified email, deterministic hash-based clean check or realistic low risk
        return {
            "status": "CLEAN",
            "email": email,
            "breach_count": 0,
            "affected_services": [],
            "source": "DemoBreachProvider (Zero Known Hits)",
            "mfa_status": "SECURE",
            "recommended_actions": ["Enable MFA on all primary email and code repository accounts."],
            "last_checked": datetime.utcnow()
        }

def get_breach_provider() -> BreachIntelligenceProvider:
    if settings.BREACH_API_KEY:
        return ExternalBreachProvider()
    return DemoBreachProvider()
