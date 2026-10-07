import pytest
from app.risk_engine.engine import RiskScoringEngine

def test_risk_scoring_bands():
    engine = RiskScoringEngine()
    
    # 1. Clean secure inputs should be LOW risk (< 25)
    low_res = engine.calculate_risk(10, 10, 10, 5, 5)
    assert low_res["risk_level"] == "LOW"
    assert low_res["overall_score"] < 25.0
    
    # 2. Critical vulnerabilities should be CRITICAL (> 75)
    crit_res = engine.calculate_risk(90, 85, 95, 90, 80)
    assert crit_res["risk_level"] == "CRITICAL"
    assert crit_res["overall_score"] >= 75.0
    
    # 3. Weights sum to 100%
    total_w = engine.w_device + engine.w_network + engine.w_credential + engine.w_phishing + engine.w_behaviour
    assert round(total_w, 2) == 1.0

def test_risk_explanation_contains_drivers():
    engine = RiskScoringEngine()
    res = engine.calculate_risk(80, 10, 10, 10, 10)
    assert "Device Security" in res["top_risks"]
    assert "Overall Cyber Risk Index" in res["score_explanation"]
