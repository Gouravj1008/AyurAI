from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAINING_DATA_PATH = Path("data/training_data.json")


def _feature_text(message: str, dosha: str) -> str:
    return f"dosha:{dosha.strip().lower()} text:{message.strip().lower()}"


def _load_training_samples() -> list[dict[str, str]]:
    with TRAINING_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def train_and_save_model(output_path: Path) -> Path:
    training_samples = _load_training_samples()
    features = [_feature_text(item["message"], item["dosha"]) for item in training_samples]
    responses = [item["response"] for item in training_samples]
    unique_responses = list(dict.fromkeys(responses))
    class_to_response = dict(enumerate(unique_responses))
    response_to_class = {response: idx for idx, response in class_to_response.items()}
    labels = [response_to_class[item["response"]] for item in training_samples]

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000)),  # Higher iteration limit avoids convergence warnings.
        ]
    )
    model.fit(features, labels)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "class_to_response": class_to_response}, output_path)
    return output_path


if __name__ == "__main__":
    destination = Path("models/ayurai_model.joblib")
    saved_at = train_and_save_model(destination)
    print(f"Model trained and saved at: {saved_at}")
