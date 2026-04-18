from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
import os
from prometheus_fastapi_instrumentator import Instrumentator

# Ensure parent directory is in path so we can import ml_engine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ml_engine.predict import sentiment_model

from app.database import init_db, get_db, PredictionRecord
from fastapi import Depends
from sqlalchemy.orm import Session
import redis
import json
import time

redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://redis:6379/0"), decode_responses=True)

app = FastAPI(
    title="Transformer Sentiment Analysis API",
    description="Multi-lingual Sentiment API with latency tracking.",
    version="2.0.0"
)

# Allow React Frontend Port 4000 to hit this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for demo/local purposes. In production, list explicitly.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument the app for Prometheus
Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
def on_startup():
    print("Initializing Database...")
    init_db()

# Pydantic schemas for request/response validation
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=2, description="The text to analyze")

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    latency_ms: float

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "DL Sentiment Analysis API is running."}

@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest, db: Session = Depends(get_db)):
    try:
        start_cache_time = time.time()
        
        # 1. Check Redis Cache First
        cache_key = f"sentiment:{request.text}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            result = json.loads(cached_result)
            latency = round((time.time() - start_cache_time) * 1000, 2)
            # Override latency to show pure Redis speed (usually ~1ms)
            return SentimentResponse(sentiment=result["sentiment"], confidence=result["confidence"], latency_ms=latency)

        # 2. Cache Miss: Run Inference Model
        sentiment, confidence, latency = sentiment_model.predict(request.text)
        
        # 3. Store in Postgres DB
        record = PredictionRecord(
            text=request.text,
            sentiment=sentiment,
            confidence=confidence,
            latency_ms=latency
        )
        db.add(record)
        db.commit()

        # 4. Save to Redis Cache (persists indefinitely for this demo)
        redis_client.set(cache_key, json.dumps({"sentiment": sentiment, "confidence": confidence}))
        
        return SentimentResponse(sentiment=sentiment, confidence=confidence, latency_ms=latency)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during DL prediction.")
