from transformers import pipeline
import time
import os

class SentimentModelDL:
    def __init__(self):
        # We use a massive robust multi-lingual model trained on millions of Twitter texts.
        # It natively supports English, Vietnamese, and many other languages.
        # It predicts 3 classes: positive, neutral, negative
        # Check if we have fine-tuned a custom model
        custom_model_dir = "saved_models/sarcasm_model"
        if os.path.exists(custom_model_dir):
            model_name = custom_model_dir
            print(f"Loading CUSTOM FINE-TUNED model from {model_name}...")
        else:
            model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
            print(f"Loading BASE pre-trained model {model_name}...")
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model=model_name,
                tokenizer=model_name,
                device=-1 # Default to CPU to ensure it runs immediately across machines. If mac supports MPS, we could dynamically detect.
            )
            print("DL Model successfully loaded.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.analyzer = None

    def predict(self, text: str):
        if not self.analyzer:
            raise ValueError("DL Model is not loaded. Check internet connection or cache.")
        
        start_time = time.time()
        # pipeline output format: [{'label': 'positive', 'score': 0.99}]
        result = self.analyzer(text)[0]
        end_time = time.time()

        latency_ms = round((end_time - start_time) * 1000, 2)
        
        # Mapping Huggingface labels to our format
        raw_label = result['label'].lower()
        confidence = result['score'] * 100
        
        if raw_label == "positive":
            sentiment = "Positive"
        elif raw_label == "negative":
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return sentiment, confidence, latency_ms

sentiment_model = SentimentModelDL()
