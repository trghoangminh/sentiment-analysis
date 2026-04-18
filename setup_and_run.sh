#!/bin/bash

# Dừng kịch bản ngay lập tức nếu có bất kỳ lệnh nào bị lỗi
set -e

echo "🚀 Bắt đầu cài đặt dự án Multi-lingual Sentiment Analysis..."

# Ép biến môi trường PATH hiển thị Docker trên một số dòng máy Mac chặn PATH
export PATH=$PATH:/Applications/Docker.app/Contents/Resources/bin:/usr/local/bin

# 1. Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Lỗi: Không tìm thấy 'docker'. Vui lòng cài đặt Docker Desktop để chạy hệ thống MLOps."
    exit 1
fi

# 2. Khởi tạo Virtual Environment (Dành cho việc dev/train model local)
echo "📦 Bước 1: Khởi tạo Virtual Environment (venv_dl)..."
if [ ! -d "venv_dl" ]; then
    python3 -m venv venv_dl
    echo "✅ Đã tạo môi trường venv_dl."
else
    echo "✅ Môi trường venv_dl đã tồn tại."
fi

# 3. Kích hoạt môi trường và cài thư viện
echo "📥 Bước 2: Cài đặt các thư viện Python cần thiết..."
source venv_dl/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Cài đặt thư viện hoàn tất!"

# 4. Khởi chạy Hệ thống Tracking MLFlow
echo "🐳 Bước 3: Khởi chạy MLFlow Tracking Server..."
docker compose down || true
docker compose up -d mlflow
echo "⏳ Đang đợi MLFlow khởi động..."
sleep 5

# 5. Huấn luyện Mô hình
echo "🧠 Bước 4: Khởi chạy quy trình Training Model (Ghi nhận vào MLFlow)..."
export MLFLOW_TRACKING_URI="http://localhost:5001"
# Ép Python bỏ qua cài đặt Proxy của máy tính/VPN khi kết nối nội bộ
export no_proxy="localhost,127.0.0.1,::1"
export NO_PROXY="localhost,127.0.0.1,::1"
python3 ml_engine/train.py
echo "✅ Huấn luyện hoàn tất! Model đã được lưu vào /saved_models"

# 6. Kiểm thử tự động
echo "🧪 Bước 5: Chạy quy trình Kiểm thử (Unit/Integration Tests)..."
export PYTHONPATH=./
pytest tests/
echo "✅ Kiểm thử thành công!"

# 7. Khởi chạy toàn bộ hệ thống Deployment & Monitoring
echo "🚀 Bước 6: Đưa Model lên Production (FastAPI), React UI và bật Giám sát (Grafana/Prometheus)..."
docker compose up --build -d api frontend prometheus grafana

echo ""
echo "========================================================="
echo "🎉 HỆ THỐNG MLOps ĐÃ HOẠT ĐỘNG TOÀN DIỆN!"
echo "========================================================="
echo "🌐 React Web UI:         http://localhost:4000"
echo "🌐 API Server (Swagger): http://localhost:8080/docs"
echo "📈 Grafana Dashboard:    http://localhost:3001 (User/Pass: admin)"
echo "🧪 MLFlow Tracking:      http://localhost:5001"
echo "⚙️  Prometheus Metrics:   http://localhost:9091"
echo "========================================================="
echo ""
echo "💡 Để dừng toàn bộ hệ thống, hãy gõ: docker compose down"
