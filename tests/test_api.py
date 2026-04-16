import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "DL Sentiment Analysis API is running."}

def test_predict_sentiment_positive():
    response = client.post(
        "/predict",
        json={"text": "I absolutely love this new tool! It's fantastic."}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "confidence" in data
    assert "latency_ms" in data
    # Note: Depending on the model loaded, the prediction might be different,
    # but the structure must be present.

def test_predict_sentiment_invalid_input():
    # Length validation failure
    response = client.post(
        "/predict",
        json={"text": "a"}
    )
    assert response.status_code == 422
