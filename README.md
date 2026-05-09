# AyurAI

Ayurveda based chatbot that answers according to the user's dosha (`vata`, `pitta`, `kapha`).

## Train the model

```bash
pip install -r requirements.txt
python train_model.py
```

This creates `models/ayurai_model.joblib`.
Training examples are stored in `data/training_data.json`, so you can edit and retrain.

## Run locally with trained model

```bash
uvicorn app:app --reload
```

API endpoints:
- `GET /health`
- `POST /chat`

Example request:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"I feel acidity and anger", "dosha":"pitta"}'
```

## Deploy with trained model (Docker)

```bash
docker build -t ayurai .
docker run -p 8000:8000 ayurai
```

The Docker image trains the model during build and serves the API with the trained model.
