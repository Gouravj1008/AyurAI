from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field


MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/ayurai_model.joblib"))
VALID_DOSHAS = {"vata", "pitta", "kapha"}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    dosha: str = Field(min_length=1, description=f"One of: {', '.join(sorted(VALID_DOSHAS))}")


class ChatResponse(BaseModel):
    response: str


def _load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Train it first with `python train_model.py`."
        )
    payload = joblib.load(MODEL_PATH)
    return payload["model"], payload["class_to_response"]


def _feature_text(message: str, dosha: str) -> str:
    return f"dosha:{dosha.strip().lower()} text:{message.strip().lower()}"


@asynccontextmanager
async def lifespan(application: FastAPI):
    try:
        model, class_to_response = _load_model()
        application.state.model = model
        application.state.class_to_response = class_to_response
        application.state.model_load_error = None
    except FileNotFoundError as exc:
        application.state.model = None
        application.state.class_to_response = {}
        application.state.model_load_error = str(exc)
    yield


app = FastAPI(title="AyurAI Chatbot API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: Request, body: ChatRequest) -> ChatResponse:
    dosha = body.dosha.strip().lower()
    if dosha not in VALID_DOSHAS:
        raise HTTPException(status_code=400, detail="dosha must be one of: vata, pitta, kapha")

    if request.app.state.model is None:
        detail = request.app.state.model_load_error or "Model is unavailable."
        raise HTTPException(status_code=503, detail=detail)

    try:
        prediction_class = request.app.state.model.predict([_feature_text(body.message, dosha)])[0]
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response ({exc.__class__.__name__}).",
        ) from exc
    response = request.app.state.class_to_response.get(prediction_class)
    if response is None:
        raise HTTPException(
            status_code=500,
            detail=f"No response mapping found for prediction class {prediction_class}.",
        )
    return ChatResponse(response=response)
