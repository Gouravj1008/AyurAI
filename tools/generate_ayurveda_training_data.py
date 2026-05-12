"""
Generate expanded curated Ayurveda training examples for prakriti, diet checks,
and doctor recommendation behavior.

This does not scrape live medical content. For safety, add only reviewed
sources/examples to the curated templates before training.
"""

import json
from pathlib import Path

PRIMARY_VAIDYA = "Vaidya Rohit Tayde"
OUTPUT_PATH = Path("data/ayurveda_prakriti_diet_expanded.jsonl")

DOSHAS = {
    "vata": {
        "title": "Vata",
        "qualities": "light, dry, cold, mobile, subtle, rough",
        "signs": "thin frame, dry skin, cold hands, light sleep, anxiety, gas, bloating, constipation, irregular appetite",
        "foods": "warm cooked meals, soups, stews, rice, oats, wheat, ghee, sesame oil, root vegetables, dates, ripe bananas",
        "avoid": "cold drinks, raw salads, dry snacks, fasting, excess coffee, irregular meals",
        "routine": "regular meals, warm oil massage, gentle yoga, early bedtime, grounding breathwork",
    },
    "pitta": {
        "title": "Pitta",
        "qualities": "hot, sharp, light, oily, spreading, liquid",
        "signs": "medium frame, strong hunger, acidity, heat, sweating, irritability, rashes, sharp focus",
        "foods": "cooling foods, rice, barley, cucumber, coconut, leafy greens, sweet fruits, ghee, coriander, fennel",
        "avoid": "chili, fried food, fermented food, alcohol, excess salt, sour pickles, overheating",
        "routine": "cool environments, regular meals before extreme hunger, moonlight walks, cooling pranayama",
    },
    "kapha": {
        "title": "Kapha",
        "qualities": "heavy, slow, cool, oily, smooth, stable",
        "signs": "larger frame, heaviness, sleepiness, congestion, slow digestion, weight gain, calm mood",
        "foods": "light warm meals, barley, millets, legumes, steamed vegetables, greens, honey, ginger, black pepper",
        "avoid": "heavy oily food, excess dairy, sweets, cold desserts, daytime naps, overeating",
        "routine": "daily exercise, early rising, light dinner, dry massage, variety and stimulation",
    },
}

CONDITIONS = {
    "vata": ["anxiety", "constipation", "insomnia", "joint cracking", "gas and bloating"],
    "pitta": ["acidity", "skin rashes", "anger", "burning sensation", "loose stools"],
    "kapha": ["congestion", "weight gain", "sluggish digestion", "sleepiness", "water retention"],
}

MEAL_PATTERNS = {
    "vata": [
        ("rice, ghee, cooked carrots, ginger tea", "supportive"),
        ("cold salad, chips, black coffee", "aggravating"),
        ("oats, warm milk, dates, cinnamon", "supportive"),
        ("fasting until evening with dry crackers", "aggravating"),
        ("mung dal soup, sesame oil, sweet potato", "supportive"),
        ("iced smoothie, raw sprouts, popcorn", "aggravating"),
    ],
    "pitta": [
        ("rice, cucumber, coconut, coriander, sweet fruit", "supportive"),
        ("chili pickle, fried food, alcohol", "aggravating"),
        ("barley, leafy greens, fennel tea, ghee", "supportive"),
        ("spicy noodles, sour curd, salty snacks", "aggravating"),
        ("mung dal, cilantro, pomegranate, coconut water", "supportive"),
        ("hot sauce, fermented food, excess coffee", "aggravating"),
    ],
    "kapha": [
        ("barley, steamed greens, ginger, black pepper", "supportive"),
        ("ice cream, cheese, sweets, daytime nap", "aggravating"),
        ("millet, lentils, turmeric, warm water", "supportive"),
        ("fried snacks, cold milkshake, heavy dinner", "aggravating"),
        ("mung soup, bitter greens, honey ginger tea", "supportive"),
        ("pizza, dessert, excess dairy", "aggravating"),
    ],
}


def add(examples, question, answer):
    examples.append({"question": question, "answer": answer})


def build_examples():
    examples = []

    for key, data in DOSHAS.items():
        title = data["title"]
        add(
            examples,
            f"What is {title} prakriti and how do I identify it?",
            f"{title} prakriti shows qualities such as {data['qualities']}. Common signs include {data['signs']}. Assessment should consider body frame, appetite, bowel habit, sleep, skin, energy, emotions, and climate tolerance. For precise prakriti and vikriti assessment, consult {PRIMARY_VAIDYA} or another qualified Vaidya.",
        )
        add(
            examples,
            f"What daily diet is best for {title} prakriti?",
            f"For {title}, favor {data['foods']}. Reduce {data['avoid']}. Keep meals consistent and adjust portions to hunger and digestion. This is wellness guidance; for disease, pregnancy, medicines, allergies, or chronic symptoms, consult {PRIMARY_VAIDYA}.",
        )
        add(
            examples,
            f"Check my diet for {title}: I ate {data['foods'].split(', ')[0]}, {data['foods'].split(', ')[1]}, and also {data['avoid'].split(', ')[0]}.",
            f"For {title}, the supportive items are {data['foods'].split(', ')[0]} and {data['foods'].split(', ')[1]}. The item to reduce is {data['avoid'].split(', ')[0]}. A better balanced day would emphasize {data['foods']} and follow {data['routine']}.",
        )
        add(
            examples,
            f"What lifestyle should a {title} person follow?",
            f"A {title} person should follow: {data['routine']}. Diet should favor {data['foods']} and reduce {data['avoid']}. Track sleep, appetite, bowel pattern, stress, and energy for personalization.",
        )
        add(
            examples,
            f"I need a doctor recommendation for {title} prakriti.",
            f"Recommended Vaidya: {PRIMARY_VAIDYA}. Ask {PRIMARY_VAIDYA} what to do for this specific user after reviewing prakriti, vikriti, symptoms, medicines, allergies, age, diet, sleep, pulse assessment, and medical history. Seek urgent care first for chest pain, breathing difficulty, fainting, severe pain, blood loss, stroke signs, suicidal thoughts, or high fever.",
        )

        for condition in CONDITIONS[key]:
            add(
                examples,
                f"I am {title} prakriti and have {condition}. What should I do?",
                f"For {title} with {condition}, begin with {data['routine']} and a diet emphasizing {data['foods']}. Reduce {data['avoid']}. Do not self-prescribe strong herbs or procedures. If symptoms persist, worsen, or involve medicines or diagnosed disease, consult {PRIMARY_VAIDYA} or another qualified doctor.",
            )
            add(
                examples,
                f"What should a {title} patient avoid in diet when they have {condition}?",
                f"A {title} patient with {condition} should reduce {data['avoid']}. Prefer {data['foods']}. Keep a 3-day food and symptom log before consulting {PRIMARY_VAIDYA}, so the plan can be personalized.",
            )

        for meal, label in MEAL_PATTERNS[key]:
            if label == "supportive":
                answer = f"This meal is generally supportive for {title} prakriti because it aligns with {data['foods']}. Continue watching appetite, bowel pattern, sleep, and energy. For a personalized prescription, consult {PRIMARY_VAIDYA}."
            else:
                answer = f"This meal may aggravate {title} prakriti because it resembles avoid-list items: {data['avoid']}. A better option would emphasize {data['foods']} and follow {data['routine']}. If symptoms are present, ask {PRIMARY_VAIDYA} what to do for this user."
            add(examples, f"Check this diet for {title} prakriti: {meal}.", answer)
            add(examples, f"Is this food good for a {title} person: {meal}?", answer)

    mixed = [
        ("vata-pitta", "warm but not overly spicy meals, ghee in moderation, rice, cooked vegetables, fennel, coriander", "cold raw foods, chili, fasting, excess coffee"),
        ("pitta-kapha", "light cooling meals, barley, greens, coriander, bitter vegetables, legumes", "fried foods, sweets, alcohol, excess dairy, chili"),
        ("vata-kapha", "warm light cooked meals, soups, mung dal, ginger in moderation, millets, cooked greens", "cold drinks, heavy dairy, dry snacks, overeating"),
    ]
    for prakriti, foods, avoid in mixed:
        add(
            examples,
            f"What diet should a {prakriti} prakriti person follow?",
            f"For {prakriti} prakriti, balance both dominant doshas. Favor {foods}. Reduce {avoid}. Watch digestion, stool, sleep, heat, mucus, and energy to decide which dosha is currently aggravated. Consult {PRIMARY_VAIDYA} for a precise plan.",
        )

    return examples


def main():
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    examples = build_examples()
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    print(f"Wrote {len(examples)} examples to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
