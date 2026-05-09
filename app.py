from __future__ import annotations

import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/ayurai_model.joblib"))

app = FastAPI(title="AyurAI Chatbot API", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    dosha: str = Field(min_length=1, description="One of: vata, pitta, kapha")


class ChatResponse(BaseModel):
    response: str


def _load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Train it first with `python train_model.py`."
        )
    payload = joblib.load(MODEL_PATH)
    return payload["model"]


def _feature_text(message: str, dosha: str) -> str:
    return f"dosha:{dosha.strip().lower()} text:{message.strip().lower()}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    dosha = request.dosha.strip().lower()
    if dosha not in {"vata", "pitta", "kapha"}:
        raise HTTPException(status_code=400, detail="dosha must be one of: vata, pitta, kapha")

    try:
        model = _load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    prediction = model.predict([_feature_text(request.message, dosha)])[0]
    return ChatResponse(response=prediction)
