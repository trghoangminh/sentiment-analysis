# System Architecture & Design

This document details the architectural decisions, component interactions, and structural flow of the **Multi-lingual Sentiment Analysis** platform.

## 1. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph "External Clients"
        UI[Frontend UI / Browsers]
        POSTMAN[API Consumers / Postman]
    end

    subgraph "Dockerized Environment (Self-Hosted)"
        API[FastAPI (Core MLOps Service)\nPort: 8080]
        MLFLOW[MLflow Tracking Server\nPort: 5001]
        PROM[Prometheus Scraper\nPort: 9091]
        GRAF[Grafana Dashboard\nPort: 3001]
        
        UI -->|HTTP POST /predict| API
        POSTMAN -->|HTTP POST /predict| API
        
        API -.->|Log metrics & experiments| MLFLOW
        PROM -->|Scrape /metrics endpoint| API
        GRAF -->|Read Time-series Data| PROM
    end
    
    subgraph "Data & Weights (Mounted Volumes)"
        MODELS[(saved_models/)]
        DB[(mlruns/)]
    end

    API -->|Load Weights| MODELS
    MLFLOW -->|Read/Write Artifacts| DB
    
    classDef service fill:#f9f,stroke:#333,stroke-width:2px;
    class API,MLFLOW,PROM,GRAF service;
```

## 2. Component Description

1. **FastAPI Application (`app/main.py`)**: The system's heart. It exposes RESTful APIs for inference. It directly wraps the PyTorch/HuggingFace model for evaluating strings in real-time.
2. **ML Engine (`ml_engine/`)**: Scripts decoupled from the API infrastructure for data processing, offline training pipelines, and dataset shuffling.
3. **MLflow Tracking Server**: Stores metadata regarding model runs, accuracy, F1-Scores, and manages dynamic versioning of weights.
4. **Prometheus & Grafana**: A sidecar observability stack that monitors API requests, ensuring the model's latency stays within defined limits and alerting engineering teams in case of inference failures.

## 3. Data Flow Process

### Inference Flow
1. **Input**: A JSON payload containing `{ "text": "This UI is terrible" }` arrives at the Edge boundary.
2. **Preprocessing**: The Router strips HTML, trims whitespaces, and normalizes encodings.
3. **Tokenization**: The input is passed to the RoBERTa AutoTokenizer.
4. **Prediction**: The mapped tensors flow into the PyTorch inference graph.
5. **Output**: The API maps the predicted Logits back to human-readable labels (Positive/Negative/Neutral) returning HTTP 200.

### Training Flow
1. Data Engineers drop updated CSVs strictly formatted inside `/data/`.
2. The trigger `python3 train.py` executes.
3. The dataset is chunked, evaluated through an Epoch loop, and metrics (Loss) are continuously streamed to MLflow.
4. Upon successful completion, the `best_model.pt` replaces the old file inside `/saved_models/`. It is immediately ready for deployment.

## 4. Trade-off Analysis & Architecture Justifications

> [!TIP]
> **Why Self-Hosted vs. Cloud Integration?**
> Given the heavy compute requirements (a 1GB Core DL Model loading tensors into memory), purchasing equivalent Managed Cloud VMs (AWS EC2 GPU Instances / AWS SageMaker) is financially unviable for an experimental phase. Self-hosting utilizing GitHub Action's hybrid Runner maximizes local resources at no additional cost.

> [!NOTE]
> **Why Docker Compose vs. Kubernetes?**
> Kubernetes offers extreme horizontal scalability and rolling updates. However, it introduces an administrative overhead known as the "k8s tax". For a Single-Node architecture focused on serving a single NLP task, Docker Compose achieves 95% of the operational resilience while keeping deployment semantics simple.

> [!TIP]
> **Why Single-Service Model Wrapping vs. Microservices?**
> The model loading operations occur directly inside the FastAPI environment (Monolithic service). If the platform scales to support hundreds of varying tasks (Object Detection, OCR, Text-to-Speech), breaking the ML nodes down into Microservices communicating over gRPC would be optimal. Currently, avoiding network I/O serialization improves inference speed.
