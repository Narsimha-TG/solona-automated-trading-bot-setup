from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Solona Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: str = None
    title: str
    status: str
    score: float
    timestamp: str = None
    demo_payload: dict

# In-memory storage
db = [
    {"id": "1", "title": "Initial Strategy", "status": "active", "score": 98.5, "timestamp": "2023-10-27T10:00:00Z", "demo_payload": {"volatility": 0.02}}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_trades": 150, "win_rate": 0.68, "data": db}

@app.post("/api/reviews")
def create_review(review: Review):
    review.id = str(uuid.uuid4())
    review.timestamp = datetime.utcnow().isoformat()
    db.append(review.dict())
    return review

@app.get("/api/demo/stream")
def get_demo_stream():
    return {"stream": "active", "data": db[-1] if db else {}}
