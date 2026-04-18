# Diptronic Multi-lingual Sentiment Analysis (Enterprise MLOps)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white" alt="Docker">
</div>

<br>

The **Sentiment Analysis** project is an Enterprise-Grade Machine Learning Operations (MLOps) architecture utilizing Deep Learning Transformer models. It is specifically optimized to detect complex internet contexts such as **Sarcasm and Slang**, with native support for **Vietnamese and English**.

The core NLP engine is powered by the **CardiffNLP XLM-RoBERTa** architecture and integrates a full automated lifecycle including Model Serving, Redis Caching, Post-Inference Logging, and Data Drift Observability.

---

## 🏗 System Architecture (Microservices)

The project heavily relies on Docker Compose, deploying **11 interdependent containers** that ensure zero downtime and immense scalability:

1. **Frontend (`sentiment_react_ui` / Port: `4000`)**: Modern React JS Vite UI with Glassmorphism and Toast notifications.
2. **Backend API (`sentiment_dl_api` / Port: `8080`)**: Throttled FastAPI endpoint for Model inference and input sanitization (Gibberish filtering).
3. **Database (`sentiment_postgres` / Port: `5432`)**: Relational logging store persistently saving text, prediction labels, and confidences.
4. **Cache Store (`sentiment_redis` / Port: `6379`)**: In-memory caching providing 1ms ultra-low latency for duplicate queries.
5. **Model Registry (`sentiment_mlflow` / Port: `5000`)**: MLflow instance for experiment tracking and artifact versioning.
6. **Object Storage (`sentiment_minio` / Port: `9000`, `9001`)**: S3-compatible raw storage handling Git-ignored heavy `.bin` and `.pt` model weight files.
7. **Storage Sidecar (`sentiment_minio_bucket_creator`)**: Automated bucket initializer for MinIO.
8. **Drift Monitor (`sentiment_evidently_ui` / Port: `8001`)**: Evidently AI dashboard tracking production data deviation from baseline datasets.
9. **Metrics Scraper (`sentiment_prometheus` / Port: `9090`)**: Scraping system HTTP metrics from FastAPI.
10. **Visualizer (`sentiment_grafana` / Port: `3000`)**: Operational Dashboard for real-time monitoring.
11. **Alerting (`sentiment_alertmanager` / Port: `9093`)**: Telegram/Slack webhook router for 500/503 HTTP server crashes.

---

## 📂 Project Structure

```text
sentiment-analysis-dl/
├── app/                     # Backend Tier: FastAPI server with Redis/Postgres try-except blocks
├── ml_engine/               # Machine Learning Tier: CardiffNLP instantiation & Fine-tuning script
├── frontend/                # Presentation Tier: React/JSX source codebase
├── scripts/                 # Automation Tier: python scripts for Drift tracking extraction
├── prometheus/              # Monitoring Tier: scrape configs and alert triggers
├── .dockerignore            # Docker optimizations
├── docker-compose.yml       # Primary orchestration script coordinating all 11 nodes
└── requirements.txt         # Core dependencies
```

---

## 🚀 Quick Start (Production Sandbox)

### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Docker** and **Docker Desktop** (or Docker Engine)
* **Git**

### 2. Stand Up the Architecture

The beauty of this architecture is its isolated Docker networks. You do not need to install Python locally.

```bash
# Clone and enter the project
cd /Users/trghoangminh/Desktop/sentiment-analysis-dl

# Build and start all 11 containers concurrently
docker compose up --build -d
```

### 3. Service Access Panel

Once the deployment completes, the services will be ready at:

| Service | Address | Credentials / Usage |
| :--- | :--- | :--- |
| **User Interface (Web)** | [http://localhost:4000](http://localhost:4000) | Main App |
| **FastAPI Swagger Docs** | [http://localhost:8080/docs](http://localhost:8080/docs) | Developer API Sandbox |
| **Grafana Dashboards** | [http://localhost:3000](http://localhost:3000) | User: `admin` / Pass: `admin` |
| **MLflow Registry** | [http://localhost:5000](http://localhost:5000) | Track Training iterations |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | User: `minioadmin` / Pass: `minioadmin` |
| **PostgreSQL Database** | `localhost:5432` | User: `sentiment_user` / Pass: `sentiment_pass` / DB: `sentiment_db` |
| **Evidently Drift UI** | [http://localhost:8001](http://localhost:8001) | Baseline vs Production reporting |

---

## 🔄 Retraining & Fine-Tuning Pipeline

When AI drifts due to new local slangs or sarcasm evolutions, follow these steps to trigger a local Fine-Tuning run tracking under MLOps:

1. **Supply Custom Data**: Place your labeled records into `data/processed/sarcasm_dataset.csv`.
2. **Execute Trainer**: Run the trainer locally pointing to MLflow (assuming Python is installed locally):
   ```bash
   python3 ml_engine/train.py
   ```
3. **Automated Registration**: The script uses `AdamW` and `CrossEntropyLoss` via the HuggingFace `Trainer` module, pushes hyperparams to **MLflow (Port 5000)**, saves the `.bin` to **MinIO**, and exports the model locally to `saved_models/sarcasm_model`.
4. **Hot Reload**: The `api` container dynamically prioritizes models found in `saved_models/` without breaking underlying code. Restart the container to switch AI brains.
   ```bash
   docker compose restart api
   ```
