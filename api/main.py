import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, BertForSequenceClassification
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import torch
from torch.nn.functional import sigmoid

# Cargar variables de entorno
load_dotenv()

# Leer orígenes permitidos desde .env
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo desde Hugging Face Hub
MODEL_PATH = "ZAMORAPJ/feeltrack-model"
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model.eval()

emotion_labels = [model.config.id2label[i] for i in range(model.config.num_labels)]

label_translations = {
    "admiration": "admiración", "amusement": "diversión", "anger": "ira", "annoyance": "molestia",
    "approval": "aprobación", "caring": "cuidado", "confusion": "confusión", "curiosity": "curiosidad",
    "desire": "deseo", "disappointment": "decepción", "disapproval": "desaprobación", "disgust": "asco",
    "embarrassment": "vergüenza", "excitement": "emoción", "fear": "miedo", "gratitude": "gratitud",
    "grief": "duelo", "joy": "alegría", "love": "amor", "nervousness": "nerviosismo",
    "neutral": "neutral", "optimism": "optimismo", "pride": "orgullo", "realization": "reconocimiento",
    "relief": "alivio", "remorse": "arrepentimiento", "sadness": "tristeza", "surprise": "sorpresa"
}

class BatchInput(BaseModel):
    texts: List[str]

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API de clasificación de emociones lista"}

@app.post("/classify")
def classify_emotion(payload: BatchInput):
    texts = payload.texts
    if not texts:
        return {"error": "Lista vacía"}

    encoded = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        logits = model(**encoded).logits
        probs = sigmoid(logits).cpu().numpy()

    results = []
    threshold = 0.5
    for i, prob_row in enumerate(probs):
        predicted_indices = [j for j, p in enumerate(prob_row) if p > threshold]
        predicted_labels = [emotion_labels[j] for j in predicted_indices]
        translated_labels = [label_translations.get(label, label) for label in predicted_labels]
        prob_dict = {
            emotion_labels[j]: round(float(prob_row[j]), 4)
            for j in predicted_indices
        }

        results.append({
            "input": texts[i],
            "predicted_labels": predicted_labels,
            "translated_labels": translated_labels,
            "probabilities": prob_dict
        })

    return {"results": results}

@app.get("/stats")
def label_statistics():
    training_distribution = {
        "neutral": 31446,
        "approval": 13235,
        "annoyance": 10024,
        "admiration": 9912,
        "disapproval": 8399,
        "realization": 7248,
        "disappointment": 6656,
        "curiosity": 6203,
        "optimism": 6199,
        "joy": 5688,
        "anger": 5644,
        "confusion": 5311,
        "gratitude": 5288,
        "amusement": 5180,
        "sadness": 4667,
        "love": 4347,
        "excitement": 4335,
        "caring": 4330,
        "disgust": 4053,
        "surprise": 3823,
        "desire": 2838,
        "fear": 2136,
        "embarrassment": 2003,
        "remorse": 1663,
        "nervousness": 1556,
        "pride": 1127,
        "relief": 1085,
        "grief": 558
    }

    translated = {
        label_translations[k]: v for k, v in training_distribution.items()
    }

    return {
        "training_distribution_en": training_distribution,
        "training_distribution_es": translated,
        "note": "Estas cantidades reflejan el número de ejemplos por emoción durante el entrenamiento. Algunas emociones pueden estar subrepresentadas."
    }