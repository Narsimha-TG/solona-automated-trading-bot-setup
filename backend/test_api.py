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
    assert "pnl" in data
    assert "win_rate" in data
    assert "active_trades" in data

def test_execute_trade_success():
    payload = {
        "symbol": "SOL/USDC",
        "side": "buy",
        "price": 150.0,
        "quantity": 5.0
    }
    response = client.post("/api/trade/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Trade executed"
    assert data["data"]["symbol"] == "SOL/USDC"
    assert data["data"]["status"] == "filled"

def test_get_positions():
    response = client.get("/api/positions")
    assert response.status_code == 200
    assert "positions" in response.json()
    assert "balance" in response.json()

def test_update_config():
    payload = {"max_slippage": 0.01, "leverage": 2}
    response = client.post("/api/config/update", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Configuration updated"
    assert response.json()["new_params"] == payload