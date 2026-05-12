"""
Test fever & remedy responses for each dosha.

We test ONLY the rule-based routing (no ML model needed).
We import the data structures and manually construct a minimal brain.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# ── Import only the rule-based pieces (no torch / transformers) ──
from ai_brain_ayurveda import (
    DOSHA_REMEDIES,
    DOSHA_TRAITS,
    AYURVEDA_SCOPE_KEYWORDS,
    PRIMARY_VAIDYA_NAME,
)


# ── Minimal brain that uses the same logic but skips the model ──
class TestBrain:
    """Lightweight copy of AyurvedicBrain for testing rule-based routing."""

    def __init__(self):
        self.user_dosha = None

    def set_user_profile(self, dosha):
        if dosha and dosha.lower() in DOSHA_TRAITS:
            self.user_dosha = dosha.lower()

    def resolve_dosha(self, dosha=None, prompt=""):
        if dosha and dosha.lower() in DOSHA_TRAITS:
            return dosha.lower()
        return self.user_dosha

    def is_ayurveda_scope(self, prompt):
        text = prompt.lower()
        return any(kw in text for kw in AYURVEDA_SCOPE_KEYWORDS)

    def classify_request(self, prompt):
        text = prompt.lower()
        if any(t in text for t in ["doctor", "vaidya", "physician", "consult"]):
            return "doctor"
        if any(t in text for t in ["fever", "jwara", "cold", "cough", "sore throat", "flu", "infection"]):
            return "remedy_condition"
        if any(t in text for t in ["remedy", "remedies", "home remedy", "cure", "heal", "treatment", "medicine"]):
            return "remedy_general"
        if any(t in text for t in ["diet", "food", "meal", "eat"]):
            return "diet"
        if any(t in text for t in ["sleep", "stress", "routine", "yoga", "exercise", "meditation"]):
            return "routine"
        if any(t in text for t in ["digestion", "acidity", "gas", "bloating", "constipation", "appetite", "skin", "heat", "rash", "weight"]):
            return "condition"
        if any(t in text for t in ["dosha", "prakriti", "vata", "pitta", "kapha"]):
            return "dosha"
        if any(t in text for t in ["herb", "herbs"]):
            return "herb"
        return "general"

    def get_remedy(self, dosha, condition):
        dosha_lower = dosha.lower()
        condition_lower = condition.lower()
        key_map = {
            "fever": "fever", "jwara": "fever", "temperature": "fever",
            "cold": "cold", "flu": "cold", "runny nose": "cold",
            "cough": "cough",
            "acidity": "acidity", "acid": "acidity", "heartburn": "acidity",
            "sore throat": "sore_throat", "throat": "sore_throat",
            "constipation": "constipation",
        }
        remedy_key = None
        for term, key in key_map.items():
            if term in condition_lower:
                remedy_key = key
                break
        if remedy_key and dosha_lower in DOSHA_REMEDIES:
            return DOSHA_REMEDIES[dosha_lower].get(remedy_key)
        return None

    def suggest_vaidya(self):
        return PRIMARY_VAIDYA_NAME

    def respond(self, prompt, dosha=None):
        active_dosha = self.resolve_dosha(dosha)
        if not active_dosha:
            return "No dosha set."
        if not self.is_ayurveda_scope(prompt):
            return f"Out of scope. Your dosha is {active_dosha.upper()}."

        intent = self.classify_request(prompt)

        if intent == "remedy_condition":
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return (
                    f"For your **{active_dosha.upper()}** dosha:\n\n"
                    f"{remedy}\n\n"
                    f"**Important:** If symptoms persist beyond 2 days, consult {self.suggest_vaidya()}.\n"
                    f"Recommended Vaidya: {self.suggest_vaidya()}"
                )
            return f"General advice for {active_dosha.upper()} - rest and consult Vaidya."

        if intent == "remedy_general":
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return f"For {active_dosha.upper()}:\n{remedy}"
            info = DOSHA_TRAITS[active_dosha]
            return f"For {active_dosha.upper()}, herbs: {', '.join(info['herbs'])}."

        if intent == "condition":
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return f"For {active_dosha.upper()}:\n{remedy}"
            return f"Condition advice for {active_dosha.upper()}."

        return f"Intent={intent} for {active_dosha.upper()}."


def separator(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


# ──────────────────────────────────────────────────
brain = TestBrain()
passed = 0
total = 0

# 1. Fever remedies per dosha
separator("FEVER REMEDY TEST — All 3 Doshas")
for dosha in ["vata", "pitta", "kapha"]:
    brain.set_user_profile(dosha)
    response = brain.respond("fever medicine", dosha=dosha)
    total += 1
    print(f"\n--- {dosha.upper()} → 'fever medicine' ---")
    print(response[:500])
    assert "fever" in response.lower() or "jwara" in response.lower(), f"FAIL: {dosha}"
    print("✅ PASS")
    passed += 1

# 2. Cold / Cough per dosha
separator("COLD & COUGH REMEDY TEST")
for dosha in ["vata", "pitta", "kapha"]:
    brain.set_user_profile(dosha)
    for query in ["I have a cold", "cough remedy"]:
        response = brain.respond(query, dosha=dosha)
        total += 1
        print(f"\n--- {dosha.upper()} → '{query}' ---")
        print(response[:400])
        assert len(response) > 50, f"FAIL: {dosha}/{query}"
        print("✅ PASS")
        passed += 1

# 3. Acidity & Constipation per dosha
separator("ACIDITY & CONSTIPATION TEST")
for dosha in ["vata", "pitta", "kapha"]:
    brain.set_user_profile(dosha)
    for query in ["acidity problem", "constipation remedy"]:
        response = brain.respond(query, dosha=dosha)
        total += 1
        print(f"\n--- {dosha.upper()} → '{query}' ---")
        print(response[:400])
        assert len(response) > 50, f"FAIL: {dosha}/{query}"
        print("✅ PASS")
        passed += 1

# 4. Specific: "fever medication for pitta"
separator("SPECIFIC: 'fever medication for pitta'")
brain.set_user_profile("pitta")
response = brain.respond("fever medication for pitta", dosha="pitta")
total += 1
print(response)
assert "pitta" in response.lower(), "FAIL: no pitta ref"
assert "fever" in response.lower() or "jwara" in response.lower(), "FAIL: no fever content"
print("\n✅ PASS")
passed += 1

# 5. Out-of-scope rejection
separator("OUT-OF-SCOPE REJECTION")
brain.set_user_profile("kapha")
response = brain.respond("what is the capital of France", dosha="kapha")
total += 1
print(response)
assert "out of scope" in response.lower() or "scope" in response.lower(), "FAIL: not rejected"
print("✅ PASS")
passed += 1

# 6. All remedies exist in DOSHA_REMEDIES
separator("KNOWLEDGE BASE COMPLETENESS")
for dosha in ["vata", "pitta", "kapha"]:
    for condition in ["fever", "cold", "cough", "acidity", "sore_throat", "constipation"]:
        total += 1
        assert condition in DOSHA_REMEDIES[dosha], f"MISSING: {dosha}/{condition}"
        assert len(DOSHA_REMEDIES[dosha][condition]) > 50, f"TOO SHORT: {dosha}/{condition}"
        print(f"  ✅ {dosha.upper()} / {condition}")
        passed += 1

separator(f"ALL TESTS PASSED: {passed}/{total} ✅")
