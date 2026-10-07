import pytest
from ml.inference.behavioural_detector import behavioural_detector
from datetime import datetime

def test_normal_login_event():
    res = behavioural_detector.analyze_event(
        timestamp=datetime.utcnow().replace(hour=14),
        network_category="HOME",
        location_category="HOME_REGION",
        login_frequency=1.0,
        session_duration=90.0
    )
    assert res["status"] in ["NORMAL", "ANOMALOUS"]
    assert "anomaly_score" in res
    assert "risk_contribution" in res

def test_atypical_anomalous_login_event():
    res = behavioural_detector.analyze_event(
        timestamp=datetime.utcnow().replace(hour=3),
        network_category="PUBLIC_WIFI",
        location_category="FOREIGN_UNTRUSTED",
        login_frequency=9.0,
        session_duration=5.0
    )
    assert "explanation" in res
    assert len(res["indicators"]) > 0
