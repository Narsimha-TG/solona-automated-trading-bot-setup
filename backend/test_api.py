import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_trades" in data
    assert isinstance(data["data"], list)

def test_create_review():
    payload = {
        "title": "Test Strategy",
        "status": "pending",
        "score": 95.0,
        "demo_payload": {"volatility": 0.05}
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Strategy"
    assert "id" in data
    assert "timestamp" in data

def test_get_demo_stream():
    response = client.get("/api/demo/stream")
    assert response.status_code == 200
    assert "stream" in response.json()