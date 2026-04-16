from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Instrument the app for Prometheus
Instrumentator().instrument(app).expose(app)

# Mount frontend folder for static assets if needed
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="static")

# Pydantic schemas for request/response validation
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=2, description="The text to analyze")

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    latency_ms: float

@app.get("/")
def serve_ui():
    html_path = os.path.join(BASE_DIR, "frontend", "index.html")
    return FileResponse(html_path)

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
