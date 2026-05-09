from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


TRAINING_SAMPLES = [
    {"message": "I feel dry skin and anxiety", "dosha": "vata", "response": "For Vata imbalance, prefer warm cooked meals, sesame oil massage, and regular sleep timings."},
    {"message": "I have irregular digestion and bloating", "dosha": "vata", "response": "For Vata digestion issues, use warm soups, ginger tea, and avoid cold/raw foods."},
    {"message": "I feel acidity and anger", "dosha": "pitta", "response": "For Pitta imbalance, choose cooling foods like cucumber, coconut water, and avoid spicy meals."},
    {"message": "I get skin rashes in summer", "dosha": "pitta", "response": "For Pitta skin irritation, stay cool, hydrate well, and include aloe vera and bitter vegetables."},
    {"message": "I feel heavy and sleepy", "dosha": "kapha", "response": "For Kapha imbalance, prefer light spicy meals, regular exercise, and avoid daytime naps."},
    {"message": "I have slow metabolism and congestion", "dosha": "kapha", "response": "For Kapha congestion, take warm herbal teas, reduce dairy, and keep active daily."},
    {"message": "How should I eat daily", "dosha": "vata", "response": "Vata routine: warm and grounding meals on a fixed schedule with gentle evening wind-down."},
    {"message": "How should I eat daily", "dosha": "pitta", "response": "Pitta routine: cooling, less spicy meals and enough hydration during the day."},
    {"message": "How should I eat daily", "dosha": "kapha", "response": "Kapha routine: light breakfast, warming spices, and avoid overeating at night."},
]


def _feature_text(message: str, dosha: str) -> str:
    return f"dosha:{dosha.strip().lower()} text:{message.strip().lower()}"


def train_and_save_model(output_path: Path) -> Path:
    features = [_feature_text(item["message"], item["dosha"]) for item in TRAINING_SAMPLES]
    labels = [item["response"] for item in TRAINING_SAMPLES]

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(features, labels)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model}, output_path)
    return output_path


if __name__ == "__main__":
    destination = Path("models/ayurai_model.joblib")
    saved_at = train_and_save_model(destination)
    print(f"Model trained and saved at: {saved_at}")
