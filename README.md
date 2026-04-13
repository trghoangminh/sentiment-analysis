# Diptronic Multi-lingual Sentiment Analysis (Deep Learning)

Đây là dự án Phân tích Sắc thái Ngôn ngữ (Sentiment Analysis) sử dụng Học Sâu (Deep Learning), đặc biệt tối ưu cho việc xử lý ngôn ngữ trên mạng xã hội (Sarcasm, Slang) ở cả **Tiếng Việt và Tiếng Anh**.

Hệ thống được xây dựng đè lên lõi Mạng nợ-ron `XLM-RoBERTa` tinh chỉnh bởi Đại học Cardiff, và có khả năng **Tự Huấn luyện (Fine-Tuning)** để "tiến hóa" thông minh hơn mỗi ngày.

## 🏗 Công nghệ sử dụng
- **Backend Framework:** `FastAPI` + `Uvicorn` (Siêu nhẹ, tốc độ cao)
- **Deep Learning Core:** `Transformers` (HuggingFace), `PyTorch`
- **Mô hình gốc (Base Model):** `cardiffnlp/twitter-xlm-roberta-base-sentiment`
- **Môi trường Web:** HTML/CSS thuần kết nối qua API Asynchronous.

## 🏗 Kiến trúc Dự án (MLOps Architecture)

Hệ thống được thiết kế theo chuẩn phân tách dịch vụ (Microservices Pattern) của các tập đoàn Công nghệ lớn:

```text
sentiment-analysis-dl/
├── app/                     # 🌐 Tầng Backend API: Chứa main.py định tuyến REST API (FastAPI).
├── ml_engine/               # 🧠 Tầng MLOps: Chứa Lõi phân tích (predict.py) & Lò luyện (train.py).
│   └── scripts/             # Kịch bản phụ trợ như máy nhân bản Data.
├── frontend/                # 🎨 Tầng Giao diện UI: Chứa HTML/CSS/JS (tách biệt hoàn toàn với AI).
├── data/                    # 📚 Tầng Dữ liệu: Nơi chứa File CSV để nạp vào Lò luyện.
├── saved_models/            # 📦 Tầng Lưu trữ Não: Nơi cất giữ file Tạ (Weights) sau khi học xong.
├── requirements.txt         # Thư viện môi trường
└── README.md
```

---

## 🛠 Hướng dẫn Cài đặt & Khởi động Dự án

Đầu tiên, hãy mở Terminal (trên Mac/Linux) và trỏ vào thư mục chứa code:
```bash
cd /Users/trghoangminh/Desktop/DDM/sentiment-analysis-dl
```

### Bước 1: Khởi tạo môi trường ảo (Virtual Environment)
```bash
python3 -m venv venv_dl
source venv_dl/bin/activate
```

### Bước 2: Cài đặt thư viện cốt lõi
```bash
pip install -r requirements.txt
```
*(Lưu ý: Quá trình cài đặt PyTorch và Transformers có thể tốn vài phút tùy mạng).*

### Bước 3: Khởi động Máy chủ Web API
```bash
uvicorn src.main:app --port 8001
```
Sau đó Mở trình duyệt Web lên và truy cập: **[http://127.0.0.1:8001](http://127.0.0.1:8001)**

---

## 🧠 Hướng dẫn Cày Level cho AI (Fine-Tuning)

Mặc dù Mô hình Tiêu chuẩn toàn cầu đã rất thông minh, nhưng đôi khi nó sẽ "ngơ" trước từ khóa Lóng (Slang) hoặc kiểu khen ngược (Sarcasm) đậm chất Việt Nam. Rất may mắn, bạn có thể TỰ DẠY LẠI nó chỉ trong 3 phút!

### Cách lấy dataset ra dạy AI:
1. Mở file `data/processed/sarcasm_dataset.csv`.
2. Gõ thêm các câu lóng bạn phân tích vào đó với cấu trúc `Câu chữ,Nhãn`.
   - `0`: Tiêu cực (Negative)
   - `1`: Trung tính (Neutral)
   - `2`: Tích cực (Positive)
3. Chạy lệnh Train:
   ```bash
   python3 ml_engine/train.py
   ```
4. Sau khoảng 1-2 phút, bộ Não AI mới của bạn sẽ đẻ ra tại thư mục `saved_models/sarcasm_model`.
5. Đóng máy chủ Web đang chạy ở (Bước 3) và chạy lệnh `uvicorn app.main:app --port 8001` lại để tải Cục Não Sát thủ này lên Web.

---

