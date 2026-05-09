from __future__ import annotations

import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/ayurai_model.joblib"))
MODEL = None
CLASS_TO_RESPONSE = {}
MODEL_LOAD_ERROR = None

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
    return payload["model"], payload.get("class_to_response", {})


def _feature_text(message: str, dosha: str) -> str:
    return f"dosha:{dosha.strip().lower()} text:{message.strip().lower()}"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.on_event("startup")
def load_model_on_startup() -> None:
    global MODEL, CLASS_TO_RESPONSE, MODEL_LOAD_ERROR
    try:
        MODEL, CLASS_TO_RESPONSE = _load_model()
        MODEL_LOAD_ERROR = None
    except FileNotFoundError as exc:
        MODEL = None
        CLASS_TO_RESPONSE = {}
        MODEL_LOAD_ERROR = str(exc)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    global MODEL, CLASS_TO_RESPONSE, MODEL_LOAD_ERROR
    dosha = request.dosha.strip().lower()
    if dosha not in {"vata", "pitta", "kapha"}:
        raise HTTPException(status_code=400, detail="dosha must be one of: vata, pitta, kapha")

    if MODEL is None:
        if MODEL_LOAD_ERROR is None:
            try:
                MODEL, CLASS_TO_RESPONSE = _load_model()
                MODEL_LOAD_ERROR = None
            except FileNotFoundError as exc:
                MODEL_LOAD_ERROR = str(exc)
        raise HTTPException(status_code=503, detail=MODEL_LOAD_ERROR)

    prediction_class = int(MODEL.predict([_feature_text(request.message, dosha)])[0])
    response = CLASS_TO_RESPONSE.get(prediction_class, "")
    return ChatResponse(response=response)
