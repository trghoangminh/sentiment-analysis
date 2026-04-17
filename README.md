# Diptronic Multi-lingual Sentiment Analysis

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Transformers-HuggingFace-orange" alt="Transformers">
</div>

<br>

The **Sentiment Analysis** project utilizes Deep Learning and large Transformer language models, specifically optimized for social media text (Sarcasm, Slang), with multi-lingual support including **Vietnamese and English**.

The system is developed based on the fine-tuned **XLM-RoBERTa** architecture from Cardiff University, integrating a direct **Fine-Tuning Pipeline** that allows the model to continuously update and adapt to new vocabularies, sentences, or trends.

---

## Project Scope & Metrics

**Scope:**
- Supports evaluating text with a maximum length of 512 tokens.
- Best supported dialects: Vietnamese and English social media communication.
- Logographic languages (Chinese, Japanese, Korean) are not supported in the current version.

**Success Metrics:**
- **Business Metrics:** Reduce manual social media content moderation time by 40%.
- **System Metrics:** Maintain API Latency `< 150ms`, achieve `99.9%` System Uptime.
- **Model Metrics:** Achieve Accuracy and F1-Score `> 0.85` on the test dataset.

---

## Key Features

- **Professional MLOps Architecture**: Clear separation between Frontend UI, Backend API, and Machine Learning Engine. Easily deployable as microservices.
- **High-speed Asynchronous API**: Built on the core **FastAPI** framework and Uvicorn Web Server, allowing it to process thousands of prediction requests with extremely low latency.
- **Multi-lingual Support (English & Vietnamese)**: Highly accurate evaluation of sentence nuances, capable of reading and understanding complex contexts: slang, backhanded compliments, sarcasm, and euphemisms.
- **Automated Training Pipeline**: Built-in scripts to fine-tune and re-train the model using custom datasets.

## Architecture

The project applies a modern multi-layered separation model:

```text
sentiment-analysis-dl/
├── app/                     # Backend Tier: REST API initialization via FastAPI (main.py)
├── ml_engine/               # MLOps Tier: Inference script (predict.py) & training (train.py)
├── frontend/                # UI Tier: Pure HTML/CSS/JS user interface (index.html)
├── data/                    # Data Tier: Contains CSV files to feed the training process
├── saved_models/            # Storage Tier: Stores model weights after training
└── requirements.txt         # Libraries and dependencies list
```

## Getting Started

### 1. System Requirements
* Python 3.9 or higher
* Git

### 2. Detailed Installation

Open Terminal and navigate to your code directory:
```bash
cd /Users/trghoangminh/Desktop/sentiment-analysis-dl
```

**Step 2.1: Create a Virtual Environment to isolate libraries**
```bash
python3 -m venv venv_dl
source venv_dl/bin/activate  # For macOS/Linux
# venv_dl\Scripts\activate   # For Windows
```

**Step 2.2: Download and install core ML libraries**
```bash
pip install -r requirements.txt
```
*(Note: Installing PyTorch and HuggingFace Transformers may take 1-2 minutes depending on network speed, as the DL libraries are quite heavy).*

**Step 2.3: Start Web API & Backend**
```bash
uvicorn app.main:app --port 8001 --reload
```
Done! Open your Web browser and visit: **[http://127.0.0.1:8001](http://127.0.0.1:8001)** to experience the user interface.

🔗 **Automated API Documentation (Swagger UI)** is available at: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Running the End-to-End MLOps Monitoring Stack

The system has been upgraded to a comprehensive monitoring architecture running independently via Docker. To experience and debug each system sequentially, execute the following commands:

**1. Start MLFlow Tracking Server**
Run MLFlow first to prepare the storage logging system when the model trains.
```bash
docker compose up -d mlflow
```
*Check Model management Dashboard at: http://localhost:5001*

**2. Start Core Backend (FastAPI)**
The model will be loaded and ready to serve API Endpoints.
```bash
docker compose up -d api
```
*Check Swagger API at: http://localhost:8080/docs*

**3. Start Prometheus Scraper**
Run the Metrics scraper from the FastAPI server.
```bash
docker compose up -d prometheus
```
*Check Metrics scanning status at: http://localhost:9091/targets*

**4. Start Grafana Visualizer**
Connect the dashboard interface with Prometheus.
```bash
docker compose up -d grafana
```
*Access: http://localhost:3001 (User: `admin` / Password: `admin`)*

*(Tip: You can spin up the entire system at once using `docker compose up --build -d`)*

---

## Fine-Tuning Pipeline Guide

Although Transformer Models are well-structured, language evolves constantly. The model needs to be re-trained (Fine-tuned) to grasp GenZ variants or hot trend keywords. You can teach the AI autonomously via the following flow:

**1. Update the Social Media Dataset:**
- Open `data/processed/sarcasm_dataset.csv`.
- Add new sentences you want the AI to evaluate, comma-separated `text,label`:
   - `0`: Negative
   - `1`: Neutral
   - `2`: Positive

**2. Trigger the Training Flow:**
Execute the Python script for the model to self-train:
```bash
python3 ml_engine/train.py
```
*(The model will train, check loss, and auto-save the version with the highest F1-Score/Accuracy).*

**3. Integrate the New Model into the App:**
- A new model file (hundreds of MBs) will be generated in `saved_models/sarcasm_model`.
- Stop and Restart the FastAPI WebServer. The new model will be pushed to Production automatically, allowing the API to recognize the new words you just added instantly.
