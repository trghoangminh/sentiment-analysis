# 🧠 Diptronic Multi-lingual Sentiment Analysis

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/badge/Transformers-HuggingFace-orange" alt="Transformers">
</div>

<br>

Dự án **Phân tích Sắc thái Ngôn ngữ (Sentiment Analysis)** ứng dụng Học Sâu (Deep Learning) và các mô hình ngôn ngữ lớn Transformer, được tối ưu hóa đặc biệt cho dữ liệu văn bản trên mạng xã hội (Sarcasm, Slang) hỗ trợ đa ngôn ngữ bao gồm **Tiếng Việt và Tiếng Anh**.

Hệ thống được phát triển dựa trên kiến trúc **XLM-RoBERTa** tinh chỉnh (fine-tuned) từ Đại học Cardiff, tích hợp khả năng **Tự Huấn luyện (Fine-Tuning Pipeline)** trực tiếp cho phép mô hình liên tục cập nhật và thích nghi với các từ ngữ, câu cú hoặc xu hướng mới.

---

## ✨ Tính năng Nổi bật

- **Kiến trúc MLOps chuyên nghiệp**: Cấu trúc phân tách rõ ràng giữa Frontend UI, Backend API và Machine Learning Engine. Dễ dàng triển khai thành các vi dịch vụ (Microservices).
- **API Bất đồng bộ (Asynchronous) Tốc độ cao**: Xây dựng trên nền tảng cơ lõi **FastAPI** và Web Server Uvicorn cho phép xử lý hàng ngàn yêu cầu dự đoán với độ trễ cực thấp.
- **Hỗ trợ Đa ngôn ngữ (English & Vietnamese)**: Đánh giá cực kỳ chính xác sắc thái câu chữ, khả năng đọc hiểu các ngữ cảnh phức tạp: từ lóng, khen ngược, mỉa mai, nói giảm nói tránh.
- **Quy trình Huấn luyện Tự động**: Tích hợp sẵn Script để Fine-tune và Re-train mô hình với bộ dữ liệu tùy chỉnh.

## 🏗 Kiến trúc Dự án (Architecture)

Dự án áp dụng mô hình phân tách tầng lớp hiện đại:

```text
sentiment-analysis-dl/
├── app/                     # 🌐 Tầng Backend: Khởi tạo REST API bằng FastAPI (main.py)
├── ml_engine/               # 🧠 Tầng MLOps: Script dự đoán (predict.py) & huấn luyện (train.py)
├── frontend/                # 🎨 Tầng UI: Giao diện người dùng thuần HTML/CSS/JS (index.html)
├── data/                    # 📚 Tầng Dữ liệu: Chứa các file CSV để nạp vào quy trình huấn luyện
├── saved_models/            # 📦 Tầng Lưu trữ: Nơi lưu trữ bộ trọng số (Weights) sau khi training
└── requirements.txt         # ⚙️ Danh sách thư viện và dependencies cài đặt
```

## 🚀 Hướng dẫn Cài đặt (Getting Started)

### 1. Yêu cầu hệ thống
* Python 3.9 trở lên
* Git

### 2. Cài đặt chi tiết

Khởi động Terminal và trỏ vào thư mục chứa code của bạn:
```bash
cd /Users/trghoangminh/Desktop/sentiment-analysis-dl
```

**Bước 2.1: Tạo môi trường ảo (Virtual Environment) để cô lập thư viện**
```bash
python3 -m venv venv_dl
source venv_dl/bin/activate  # Đối với macOS/Linux
# venv_dl\Scripts\activate   # Đối với Windows
```

**Bước 2.2: Tải và cài đặt các thư viện lõi ML**
```bash
pip install -r requirements.txt
```
*(Lưu ý: Quá trình cài đặt PyTorch và HuggingFace Transformers có thể mất 1-2 phút tùy thuộc vào tốc độ mạng, do bộ thư viện DL khá nặng).*

**Bước 2.3: Khởi động Web API & Backend**
```bash
uvicorn app.main:app --port 8001 --reload
```
Hoàn tất! Hãy mở trình duyệt Web và truy cập: **[http://127.0.0.1:8001](http://127.0.0.1:8001)** để trải nghiệm giao diện người dùng.

🔗 **Tài liệu API Tự động (Swagger UI)** sẽ khả dụng tại: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 🐳 Khởi chạy Hệ thống MLOps Giám sát (End-to-End Stack)

Hệ thống đã được nâng cấp lên kiến trúc giám sát toàn diện chạy độc lập từng phần bằng Docker. Để trải nghiệm và debug từng hệ thống một cách tuần tự, thực hiện các lệnh sau:

**1. Khởi chạy MLFlow Tracking Server**
Chạy MLFlow trước để chuẩn bị hệ thống lưu trữ log khi model tiến hành train.
```bash
docker compose up -d mlflow
```
👉 *Kiểm tra Dashboard quản lý Model tại: http://localhost:5001*

**2. Khởi chạy Core Backend (FastAPI)**
Model sẽ được tải lên và sẵn sàng phục vụ các API Endpoint.
```bash
docker compose up -d api
```
👉 *Kiểm tra Swagger API tại: http://localhost:8000/docs*

**3. Khởi chạy Prometheus Scraper**
Chạy bộ thu thập dữ liệu (Metrics) từ máy chủ API FastAPI.
```bash
docker compose up -d prometheus
```
👉 *Kiểm tra trạng thái quét Metrics tại: http://localhost:9091/targets*

**4. Khởi chạy Grafana Visualizer**
Kết nối giao diện biểu đồ với Prometheus.
```bash
docker compose up -d grafana
```
👉 *Truy cập: http://localhost:3001 (User: `admin` / Password: `admin`)*

*(Mẹo: Bạn có thể bật cùng lúc toàn bộ hệ thống bằng lệnh `docker compose up --build -d`)*

---

## 🛠 Hướng dẫn Tự Huấn luyện (Fine-Tuning Pipeline)

Dù Transformer Models đã được cấu trúc tốt, nhưng do ngôn ngữ thay đổi liên tục, mô hình cần được học lại (Fine-tune) để nắm bắt biến thể GenZe hoặc các từ khoá hot trend. Bạn có thể tự cho AI đi học theo luồng sau:

**1. Cập nhật Dataset Mạng xã hội:**
- Mở file `data/processed/sarcasm_dataset.csv`.
- Cập nhật thêm các câu bạn cần AI đánh giá với cấu trúc phân cách bởi dấu phẩy `text,label`:
   - `0`: Tiêu cực (Negative)
   - `1`: Trung tính (Neutral)
   - `2`: Tích cực (Positive)

**2. Khởi chạy luồng Train:**
Thực thi lệnh Python để mô hình tự học:
```bash
python3 ml_engine/train.py
```
*(Mô hình sẽ tiến hành training, check loss và tự lưu phiên bản có F1-Score/Accuracy cao nhất).*

**3. Tích hợp Mô hình mới lên App:**
- File mô hình (hàng trăm MB) sẽ được sinh ra ở `saved_models/sarcasm_model`.
- Thoát và Khởi động lại FastAPI WebServer, mô hình mới sẽ tự động được Push lên Production và API có thể nhận dạng các từ mới bạn vừa thêm ngay lập tức.

---

## 📝 Giấy phép (License)
Dự án được phân phối dưới giấy phép **MIT License**. Bạn có toàn quyền sử dụng thương mại, tinh chỉnh và phân phối.
