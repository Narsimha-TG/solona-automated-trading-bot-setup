from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Solana Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TradeOrder(BaseModel):
    symbol: str
    side: str
    price: float
    quantity: float

class Position(BaseModel):
    id: str
    symbol: str
    side: str
    price: float
    quantity: float
    status: str
    timestamp: str

# In-memory seed data
positions = [
    {"id": "1", "symbol": "SOL/USDC", "side": "buy", "price": 145.20, "quantity": 10.0, "status": "open", "timestamp": "2023-10-27T10:00:00Z"}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"pnl": 1250.50, "win_rate": 0.65, "active_trades": len(positions)}

@app.post("/api/trade/execute")
def execute_trade(order: TradeOrder):
    new_pos = {"id": str(len(positions) + 1), **order.dict(), "status": "filled", "timestamp": datetime.utcnow().isoformat()}
    positions.append(new_pos)
    return {"message": "Trade executed", "data": new_pos}

@app.get("/api/positions")
def get_positions():
    return {"positions": positions, "balance": 50000.00}

@app.post("/api/config/update")
def update_config(params: dict):
    return {"message": "Configuration updated", "new_params": params}