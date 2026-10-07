from typing import Dict, Any, List
from app.core.config import settings

class RiskScoringEngine:
    """
    Deterministic, explainable scoring engine aligned with NIST CSF.
    Produces Cyber Risk Index (0-100) with classifications:
    0-24: LOW
    25-49: MODERATE
    50-74: HIGH
    75-100: CRITICAL
    """
    def __init__(
        self,
        weight_device: float = settings.WEIGHT_DEVICE,
        weight_network: float = settings.WEIGHT_NETWORK,
        weight_credential: float = settings.WEIGHT_CREDENTIAL,
        weight_phishing: float = settings.WEIGHT_PHISHING,
        weight_behaviour: float = settings.WEIGHT_BEHAVIOUR
    ):
        self.w_device = weight_device
        self.w_network = weight_network
        self.w_credential = weight_credential
        self.w_phishing = weight_phishing
        self.w_behaviour = weight_behaviour

    def calculate_risk(
        self,
        device_score: float,
        network_score: float,
        credential_score: float,
        phishing_score: float,
        behaviour_score: float,
        module_status: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Calculates the Cyber Risk Index based on normalized category risk scores (0-100).
        0 means completely secure, 100 means extreme vulnerability/risk.
        """
        # Clamp inputs between 0 and 100
        d_val = max(0.0, min(100.0, float(device_score)))
        n_val = max(0.0, min(100.0, float(network_score)))
        c_val = max(0.0, min(100.0, float(credential_score)))
        p_val = max(0.0, min(100.0, float(phishing_score)))
        b_val = max(0.0, min(100.0, float(behaviour_score)))

        # Weighted calculation
        c_device = d_val * self.w_device
        c_network = n_val * self.w_network
        c_credential = c_val * self.w_credential
        c_phishing = p_val * self.w_phishing
        c_behaviour = b_val * self.w_behaviour

        overall_score = round(c_device + c_network + c_credential + c_phishing + c_behaviour, 1)

        # Risk Classification Bands
        if overall_score < 25.0:
            risk_level = "LOW"
        elif overall_score < 50.0:
            risk_level = "MODERATE"
        elif overall_score < 75.0:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        # Explainable breakdown
        category_scores = {
            "device_security": d_val,
            "network_security": n_val,
            "credential_security": c_val,
            "phishing_risk": p_val,
            "behavioural_risk": b_val
        }

        weighted_contributions = {
            "device_security": round(c_device, 1),
            "network_security": round(c_network, 1),
            "credential_security": round(c_credential, 1),
            "phishing_risk": round(c_phishing, 1),
            "behavioural_risk": round(c_behaviour, 1)
        }

        # Identify top risk drivers
        sorted_drivers = sorted(weighted_contributions.items(), key=lambda item: item[1], reverse=True)
        top_risks = [k.replace("_", " ").title() for k, v in sorted_drivers if v > 5.0]

        explanation = (
            f"Overall Cyber Risk Index is {overall_score}/100 ({risk_level}). "
            f"Calculated via weighted formula: Device ({self.w_device*100}%: {c_device:.1f}pts), "
            f"Network ({self.w_network*100}%: {c_network:.1f}pts), "
            f"Credential ({self.w_credential*100}%: {c_credential:.1f}pts), "
            f"Phishing ({self.w_phishing*100}%: {c_phishing:.1f}pts), and "
            f"Behavioural ({self.w_behaviour*100}%: {c_behaviour:.1f}pts). "
            f"Primary risk drivers: {', '.join(top_risks) if top_risks else 'None detected'}."
        )

        return {
            "overall_score": overall_score,
            "risk_level": risk_level,
            "category_scores": category_scores,
            "weighted_contributions": weighted_contributions,
            "top_risks": top_risks,
            "score_explanation": explanation
        }

risk_engine = RiskScoringEngine()
