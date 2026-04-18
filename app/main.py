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
def predict_sentiment(request: SentimentRequest):
    try:
        sentiment, confidence, latency = sentiment_model.predict(request.text)
        return SentimentResponse(sentiment=sentiment, confidence=confidence, latency_ms=latency)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during DL prediction.")
