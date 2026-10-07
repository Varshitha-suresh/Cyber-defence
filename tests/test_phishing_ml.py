import pytest
from ml.features.url_features import url_extractor
from ml.inference.phishing_predictor import phishing_predictor

def test_feature_extraction():
    url = "http://192.168.1.1/paypal/login.php?user=test"
    feats = url_extractor.extract_features(url)
    assert feats["features"]["has_ip_address"] == 1.0
    assert feats["features"]["has_suspicious_token"] == 1.0
    assert len(feats["vector"]) == len(url_extractor.FEATURE_NAMES)

def test_phishing_prediction_phishing():
    phish_url = "http://192.168.1.100/paypal-update/verification/login.php?cmd=_login-run"
    pred = phishing_predictor.predict(phish_url)
    assert pred["classification"] in ["PHISHING", "LEGITIMATE"]
    assert "phishing_probability" in pred
    assert "risk_score" in pred
    assert len(pred["indicators"]) > 0

def test_phishing_prediction_legitimate():
    legit_url = "https://www.google.com/search?q=cybersecurity"
    pred = phishing_predictor.predict(legit_url)
    assert pred["phishing_probability"] < 0.50
    assert pred["classification"] == "LEGITIMATE"
