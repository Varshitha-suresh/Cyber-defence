import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_system_status():
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "phishing_classifier" in data
    assert "anomaly_detector" in data

def test_login_flow():
    # Login with pre-seeded demo user
    response = client.post("/api/auth/login", json={
        "email": "alex.freelancer@cyberwork.io",
        "password": "CyberDefense2026!"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # Access protected profile
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "alex.freelancer@cyberwork.io"

def test_assessment_run_pipeline():
    # Login
    auth_resp = client.post("/api/auth/login", json={
        "email": "alex.freelancer@cyberwork.io",
        "password": "CyberDefense2026!"
    })
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Run assessment
    assess_resp = client.post("/api/assessment/run", json={"scenario": "MODERATE"}, headers=headers)
    assert assess_resp.status_code == 200
    res = assess_resp.json()
    assert "overall_score" in res
    assert "risk_level" in res
    assert "recommendations" in res
    assert res["overall_score"] > 0
