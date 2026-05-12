"""
Build a structured Ayurveda dosha Q&A dataset from user-provided prompts.
"""

from __future__ import annotations

import json
from pathlib import Path

OUTPUT_PATH = Path("data/ayurveda_dosha_user_questions.jsonl")


QUESTION_BLOCK = [
    # Basic Vata
    "What is Vata dosha in Ayurveda?",
    "What are the symptoms of high Vata?",
    "How can I balance Vata naturally?",
    "Which foods increase Vata?",
    "What foods are good for Vata body type?",
    "Is cold weather bad for Vata?",
    "Can anxiety be related to Vata imbalance?",
    "Best morning routine for Vata dosha?",
    "Which oils are best for Vata massage?",
    "What exercises suit Vata people?",
    # Basic Pitta
    "What is Pitta dosha?",
    "Signs of excess Pitta in the body?",
    "Which foods cool down Pitta?",
    "Can spicy food increase Pitta?",
    "Why do I feel angry quickly according to Ayurveda?",
    "Best drinks for Pitta balance?",
    "Is summer season harmful for Pitta?",
    "Can acidity be caused by Pitta imbalance?",
    "Which yoga is best for Pitta?",
    "What fruits are best for Pitta?",
    # Basic Kapha
    "What is Kapha dosha?",
    "Symptoms of Kapha imbalance?",
    "Which foods reduce Kapha?",
    "Can laziness be related to Kapha?",
    "Best exercises for Kapha body type?",
    "Does dairy increase Kapha?",
    "Which spices help balance Kapha?",
    "Is weight gain related to Kapha imbalance?",
    "Best detox for Kapha dosha?",
    "Morning habits for Kapha people?",
    # Diet
    "Which Ayurvedic diet is best for digestion?",
    "What foods should I avoid at night?",
    "Can Ayurveda help with bloating?",
    "Which fruits should not be mixed?",
    "Is drinking cold water harmful in Ayurveda?",
    "Best Ayurvedic breakfast for energy?",
    "What is sattvic food?",
    "Difference between rajasic and tamasic food?",
    "Can Ayurveda help improve gut health?",
    "Which herbs improve metabolism?",
    "Best warm foods for Vata?",
    "Can dry foods increase Vata?",
    "Is fasting good for Vata?",
    "Which cooling herbs reduce Pitta?",
    "Is coffee bad for Pitta?",
    "Best summer diet for Pitta?",
    "Can sugar increase Kapha?",
    "Is intermittent fasting good for Kapha?",
    "Best low-fat Ayurvedic foods?",
    # Remedies
    "Home remedy for acidity in Ayurveda?",
    "Natural remedy for cough according to Ayurveda?",
    "How to improve digestion naturally?",
    "Ayurvedic remedy for stress?",
    "Home remedy for constipation?",
    "Best herbal tea for immunity?",
    "How to improve sleep naturally?",
    "Remedy for sore throat using kitchen ingredients?",
    "Ayurvedic drink for detox?",
    "Which spices reduce inflammation?",
    "Best oils for dry skin in Vata?",
    "Ayurvedic remedy for anxiety and restlessness?",
    "Herbal remedies for joint pain due to Vata?",
    "Cooling remedies for body heat?",
    "Natural remedy for skin rashes?",
    "Ayurvedic treatment for acidity?",
    "Home remedy for mucus and congestion?",
    "Ayurvedic remedy for slow metabolism?",
    "Herbs for reducing water retention?",
    # Intermediate
    "How do seasons affect doshas?",
    "What is Prakriti in Ayurveda?",
    "Difference between Prakriti and Vikriti?",
    "How to identify my dosha type?",
    "Which dosha controls digestion?",
    "What causes dosha imbalance?",
    "Ayurvedic daily routine for overall balance?",
    "How does sleep affect doshas?",
    "Which emotions are linked to each dosha?",
    "Can doshas change over time?",
    # Advanced
    "Explain Vata subdoshas with functions.",
    "What are the five types of Pitta?",
    "Explain Kapha subdoshas in detail.",
    "How does Agni relate to dosha balance?",
    "What is Ama and how is it formed?",
    "Relationship between gut health and doshas?",
    "How does Ayurveda explain mental health?",
    "Ayurvedic view on circadian rhythm?",
    "Panchakarma for each dosha?",
    "Difference between Sama and Nirama conditions?",
    # Conversational
    "I feel too much body heat, what should I eat?",
    "Why am I always anxious and overthinking?",
    "Suggest a Kapha-reducing breakfast.",
    "My digestion feels weak after eating.",
    "Which Ayurvedic tea is best for stress?",
    "I have dry skin and constipation together.",
    "Can Ayurveda help with sleep issues?",
    "I feel lazy and heavy all day.",
    "What should I eat in summer for Pitta?",
    "Suggest a daily Ayurvedic routine.",
]


def classify_dosha(question: str) -> str:
    q = question.lower()
    if "vata" in q or "anxiety" in q or "dry skin" in q or "constipation" in q:
        return "vata"
    if "pitta" in q or "acidity" in q or "heat" in q or "rashes" in q:
        return "pitta"
    if "kapha" in q or "mucus" in q or "lazy" in q or "weight gain" in q:
        return "kapha"
    return "vata"


def classify_category(question: str) -> str:
    q = question.lower()
    if "food" in q or "diet" in q or "breakfast" in q or "drink" in q or "eat" in q:
        return "diet"
    if "herb" in q or "tea" in q or "spices" in q or "oil" in q:
        return "herbs"
    if "remedy" in q or "detox" in q or "treatment" in q or "relat" in q:
        return "remedies"
    if "what is" in q or "explain" in q or "difference" in q or "dosha" in q:
        return "dosha"
    return "consultation"


def classify_difficulty(question: str) -> str:
    q = question.lower()
    if "subdosha" in q or "panchakarma" in q or "sama" in q or "nirama" in q or "agni" in q or "ama" in q:
        return "advanced"
    if "prakriti" in q or "vikriti" in q or "seasons" in q or "identify my dosha" in q:
        return "intermediate"
    return "basic"


def build_answer(question: str, dosha: str, category: str) -> str:
    base = {
        "vata": "This pattern suggests Vata imbalance. Favor warm cooked meals, regular routine, sesame oil massage, gentle yoga, and early sleep.",
        "pitta": "This pattern suggests Pitta aggravation. Use cooling foods, reduce chili/fried foods, hydrate well, and avoid excess heat.",
        "kapha": "This pattern suggests Kapha aggravation. Prefer light warm meals, spices like ginger/black pepper, daily exercise, and avoid heavy cold foods.",
    }[dosha]

    if category == "diet":
        extra = "Diet focus: choose dosha-specific foods, avoid triggers, and keep meal timing consistent."
    elif category == "herbs":
        extra = "Herb focus: use dosha-appropriate herbs in moderate amounts and seek Vaidya guidance for long-term use."
    elif category == "remedies":
        extra = "Home remedy focus: use gentle kitchen remedies, monitor response, and seek care if symptoms persist."
    elif category == "dosha":
        extra = "Dosha focus: assess prakriti/vikriti with symptoms, digestion, sleep, and seasonal response."
    else:
        extra = "Consultation focus: for persistent, severe, or chronic symptoms, consult a qualified Vaidya for personalized care."

    return f"{base} {extra}"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for question in QUESTION_BLOCK:
        dosha = classify_dosha(question)
        category = classify_category(question)
        difficulty = classify_difficulty(question)
        rows.append(
            {
                "question": question,
                "answer": build_answer(question, dosha, category),
                "category": category,
                "dosha": dosha,
                "difficulty": difficulty,
                "source": "user-provided-dosha-questions",
            }
        )

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
