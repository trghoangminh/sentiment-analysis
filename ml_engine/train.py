import os
import torch
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import numpy as np
import evaluate

def train():
    print("--- Khởi động lò luyện AI (Fine-Tuning) ---")
    
    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    output_model_dir = "saved_models/sarcasm_model"
    data_path = "data/processed/sarcasm_dataset.csv"

    if not os.path.exists(data_path):
        print(f"Không tìm thấy {data_path}. Vui lòng tạo tệp dữ liệu!")
        return

    print("1. Đang nạp Dữ liệu từ file CSV...")
    df = pd.read_csv(data_path)
    # Lọc dữ liệu lỗi (nếu có)
    df = df.dropna()
    
    # Ép kiểu cho chắc chắn
    df['text'] = df['text'].astype(str)
    df['label'] = df['label'].astype(int)

    # Chuyển Dataframe Pandas thành định dạng HuggingFace Dataset
    hf_dataset = Dataset.from_pandas(df)
    
    # Chia tập train/test (chỉ để đánh giá, vì data ít nên lấy 10% test)
    split_dataset = hf_dataset.train_test_split(test_size=0.1, seed=42)
    train_data = split_dataset['train']
    eval_data = split_dataset['test']

    print(f"2. Đang tải Tokenizer & Bộ Não Gốc ({model_name})...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Hàm xử lý Tokenize
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    print("3. Đang cắt nhỏ từ vựng (Tokenization)...")
    tokenized_train = train_data.map(tokenize_function, batched=True)
    tokenized_eval = eval_data.map(tokenize_function, batched=True)

    # Model for sequence classification uses 3 labels
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

    print("4. Đang thiết lập Môi trường Huấn Luyện...")
    # Vì mình train trên CPU/Mac, thiết lập siêu nhỏ để chạy lẹ
    training_args = TrainingArguments(
        output_dir='saved_models/checkpoints', # Nơi lưu các bản nháp (Checkpoints) tự động
        num_train_epochs=2,           # Giảm số dòng để máy chạy lẹ hơn đối với Data lớn
        per_device_train_batch_size=4,# Batch size nhỏ để khỏi báo RAM
        per_device_eval_batch_size=4,
        warmup_steps=0,
        weight_decay=0.01,
        eval_strategy="epoch",  
        save_strategy="epoch",
        logging_dir='./logs',
        logging_steps=2,
    )

    metric = evaluate.load("accuracy")
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        compute_metrics=compute_metrics,
    )

    print("5. BẮT ĐẦU HUẤN LUYỆN (Quá trình này tùy Mac có thể tốn 1 - 3 phút)...")
    trainer.train()

    print(f"6. LƯU BỘ TẠ MỚI: {output_model_dir}")
    # Lưu lại bộ tạ (Weights) & Tokenizer để mốt xài
    model.save_pretrained(output_model_dir)
    tokenizer.save_pretrained(output_model_dir)
    print("--- Train xong! Bây giờ quay lại model.py để nạp não mới nhé ---")

if __name__ == "__main__":
    train()
