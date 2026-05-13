"""
Jarvis AI Brain - Ayurveda-Specialized with Dosha Detection & Diet Recommendations
Loads model with LoRA adapter and provides Ayurvedic responses with personalization
"""

import logging
import os
import re
from typing import Dict, List, Optional

import config

# NOTE: torch and transformers are intentionally NOT imported at module level.
# They are imported lazily inside _load_model() so that importing this module
# is instant and Flask can start without waiting for heavy ML libraries.

logger = logging.getLogger(__name__)

PRIMARY_VAIDYA_NAME = "Vaidya Rohit Tayde"

# ==================== DOSHA DEFINITIONS ====================
DOSHA_TRAITS = {
    "vata": {
        "description": "Vata (Air + Ether) governs movement, creativity, adaptability, nerves, breath, and elimination.",
        "traits": ["thin", "slim", "creative", "anxious", "energetic", "cold", "dry", "irregular", "light sleeper", "constipation", "restless", "fast talking", "forgetful", "variable appetite", "bloating", "cracking joints", "light sleep"],
        "diet": ["warm cooked meals", "ghee", "sesame oil", "root vegetables", "rice", "oats", "soups", "stews", "ripe bananas", "dates"],
        "herbs": ["ashwagandha", "ginger", "cumin", "fennel", "licorice"],
        "avoid": ["raw foods", "cold drinks", "dry snacks", "excessive fasting", "too much caffeine"],
        "routine": ["keep regular meal times", "use warm oil massage", "choose gentle yoga", "protect from cold wind"],
        "doctor": f"Consult {PRIMARY_VAIDYA_NAME} or another qualified physician if anxiety, insomnia, constipation, unexplained weight loss, tremors, or pain persists."
    },
    "pitta": {
        "description": "Pitta (Fire + Water) governs digestion, metabolism, body heat, focus, courage, and transformation.",
        "traits": ["medium build", "sharp", "ambitious", "sensitive", "warm", "hot", "acidic", "irritable", "oily skin", "rashes", "strong appetite", "sweat", "sweating", "heartburn", "anger", "competitive", "redness", "burning"],
        "diet": ["cooling foods", "coconut", "leafy greens", "cucumber", "melons", "rice", "milk", "ghee", "sweet fruits"],
        "herbs": ["brahmi", "amla", "neem", "coriander", "fennel"],
        "avoid": ["spicy foods", "fried foods", "fermented foods", "alcohol", "excessive heat", "too much salt"],
        "routine": ["eat before becoming very hungry", "stay cool", "take breaks from competition", "use moonlight walks or cooling breath"],
        "doctor": f"Consult {PRIMARY_VAIDYA_NAME} or another qualified physician if acidity, burning sensations, skin inflammation, fever, blood pressure concerns, or anger spikes persist."
    },
    "kapha": {
        "description": "Kapha (Earth + Water) governs structure, stamina, lubrication, immunity, patience, and emotional steadiness.",
        "traits": ["larger build", "heavy", "calm", "stable", "strong", "slow", "sleepy", "congested", "oily skin", "weight gain", "deep sleep", "sluggish", "mucus", "lethargic", "steady appetite", "water retention", "stiff"],
        "diet": ["light meals", "dry foods", "warming spices", "legumes", "barley", "millets", "steamed vegetables", "honey", "greens"],
        "herbs": ["ginger", "black pepper", "turmeric", "trikatu", "tulsi"],
        "avoid": ["heavy foods", "oily foods", "excess dairy", "sweet foods", "cold desserts", "daytime naps"],
        "routine": ["exercise daily", "wake early", "keep meals light at night", "add variety and stimulation"],
        "doctor": f"Consult {PRIMARY_VAIDYA_NAME} or another qualified physician if congestion, edema, uncontrolled weight gain, breathing difficulty, diabetes symptoms, or depression persists."
    }
}

FOOD_ALIASES = {
    "curd": "dairy",
    "yogurt": "dairy",
    "ice cream": "cold desserts",
    "pizza": "heavy foods",
    "burger": "heavy foods",
    "chips": "dry snacks",
    "coffee": "too much caffeine",
    "tea": "too much caffeine",
    "pickle": "fermented foods",
    "chili": "spicy foods",
    "chilli": "spicy foods",
    "salad": "raw foods",
}

AYURVEDA_SCOPE_KEYWORDS = [
    "dosha",
    "prakriti",
    "vata",
    "pitta",
    "kapha",
    "ayurveda",
    "diet",
    "food",
    "meal",
    "eat",
    "breakfast",
    "lunch",
    "dinner",
    "snack",
    "recipe",
    "herb",
    "herbs",
    "routine",
    "sleep",
    "stress",
    "digestion",
    "vaidya",
    "wellness",
    "agni",
    "fever",
    "cold",
    "cough",
    "sore throat",
    "acidity",
    "constipation",
    "bloating",
    "immunity",
    "detox",
    "remedy",
    "remedies",
    "medicine",
    "treatment",
    "cure",
    "heal",
    "inflammation",
    "pain",
    "headache",
    "anxiety",
    "insomnia",
    "weight",
    "metabolism",
    "panchakarma",
    "ama",
    "sattvic",
    "rajasic",
    "tamasic",
    "oil",
    "massage",
    "yoga",
    "meditation",
    "exercise",
    "jwara",
    "body heat",
    "heavy",
]

# ==================== DOSHA-SPECIFIC REMEDIES ====================
DOSHA_REMEDIES = {
    "vata": {
        "fever": (
            "**Vata-type Fever (Jwara) Remedy:**\n"
            "Vata fever is dry, irregular, with chills, body aches, and anxiety.\n\n"
            "- Drink warm **ginger-tulsi tea** 2-3 times daily\n"
            "- Take **Dashamoola Kashayam** as directed by a Vaidya\n"
            "- **Guduchi (Giloy)** decoction to boost immunity\n"
            "- Apply warm **sesame oil** on feet and forehead\n"
            "- Rest under warm covers, stay hydrated\n"
            "- Eat light **khichdi with ghee**\n"
            "- **Ashwagandha** helps strengthen immunity\n"
            "- Avoid cold, dry, raw foods during fever"
        ),
        "cold": (
            "**Vata-type Cold Remedy:**\n"
            "- Drink warm water with ginger and honey\n"
            "- Inhale steam with ajwain (carom seeds)\n"
            "- Take ashwagandha for strength\n"
            "- Warm sesame oil massage on chest\n"
            "- Tulsi-ginger tea 3 times daily\n"
            "- Avoid cold drinks and raw foods\n"
            "- Rest and maintain warmth"
        ),
        "cough": (
            "**Vata-type Cough Remedy:**\n"
            "Vata cough is dry, non-productive, with throat pain.\n\n"
            "- **Honey with ginger juice** (1 tsp each)\n"
            "- Warm turmeric milk before bed\n"
            "- Licorice (mulethi) tea\n"
            "- Sesame oil gargle\n"
            "- Avoid cold, dry environments\n"
            "- Sitopaladi Churna with honey"
        ),
        "acidity": (
            "**Vata-type Acidity Remedy:**\n"
            "- Warm water with cumin seeds\n"
            "- Eat at regular times\n"
            "- Ghee with meals\n"
            "- Fennel tea after meals\n"
            "- Avoid fasting and irregular eating"
        ),
        "sore_throat": (
            "**Vata-type Sore Throat Remedy:**\n"
            "- Warm salt water gargle\n"
            "- Honey with ginger juice\n"
            "- Licorice (mulethi) tea\n"
            "- Warm turmeric milk\n"
            "- Avoid cold drinks and dry foods"
        ),
        "constipation": (
            "**Vata Constipation Remedy:**\n"
            "- Warm water first thing in morning\n"
            "- Soaked raisins (10-12) at night\n"
            "- Ghee in warm milk before bed\n"
            "- Triphala powder at night\n"
            "- Fiber-rich warm cooked foods\n"
            "- Avoid dry, cold, raw foods"
        ),
    },
    "pitta": {
        "fever": (
            "**Pitta-type Fever (Jwara) Remedy:**\n"
            "Pitta fever is high, burning, with sweating, irritability, and redness.\n\n"
            "- Drink **coriander-fennel water** (soak overnight, strain)\n"
            "- Take **Guduchi (Giloy)** decoction - primary fever herb\n"
            "- **Sudarshan Churna** as directed by a Vaidya\n"
            "- Apply **sandalwood paste** on forehead\n"
            "- Eat cooling **rice kanji with coriander**\n"
            "- **Amla (Indian gooseberry)** juice for immunity\n"
            "- Avoid spicy, oily, fried foods\n"
            "- Stay in cool, ventilated environment"
        ),
        "cold": (
            "**Pitta-type Cold Remedy:**\n"
            "- Coriander seed tea\n"
            "- Mint and fennel water\n"
            "- Amla juice for immunity\n"
            "- Light steam inhalation\n"
            "- Avoid excessive spices\n"
            "- Coconut oil on nostrils\n"
            "- Cool but not cold environment"
        ),
        "cough": (
            "**Pitta-type Cough Remedy:**\n"
            "Pitta cough has yellow mucus, burning sensation.\n\n"
            "- **Sitopaladi Churna** with honey\n"
            "- Cool mint tea\n"
            "- Amla powder with honey\n"
            "- Avoid hot spices\n"
            "- Coconut water for cooling\n"
            "- Neem leaves decoction"
        ),
        "acidity": (
            "**Pitta-type Acidity Remedy:**\n"
            "- Cold milk (unflavored)\n"
            "- Fennel seeds after meals\n"
            "- Coconut water daily\n"
            "- Coriander water on empty stomach\n"
            "- Amla juice\n"
            "- Avoid spicy, sour, fried foods"
        ),
        "sore_throat": (
            "**Pitta-type Sore Throat Remedy:**\n"
            "- Cool mint and coriander gargle\n"
            "- Honey with turmeric (cooling combo)\n"
            "- Fennel tea\n"
            "- Coconut water\n"
            "- Avoid hot and spicy foods"
        ),
        "constipation": (
            "**Pitta Constipation Remedy:**\n"
            "- Aloe vera juice on empty stomach\n"
            "- Triphala with cool water at night\n"
            "- Ghee in warm milk\n"
            "- Sweet fruits: pears, figs, prunes\n"
            "- Avoid excessive spice and heat"
        ),
    },
    "kapha": {
        "fever": (
            "**Kapha-type Fever (Jwara) Remedy:**\n"
            "Kapha fever is low-grade, with heaviness, congestion, mucus, and lethargy.\n\n"
            "- Drink **tulsi-ginger-black pepper tea** (trikatu tea)\n"
            "- Take **Sitopaladi Churna** with honey\n"
            "- **Guduchi (Giloy)** decoction for immunity\n"
            "- Do **steam inhalation** with eucalyptus oil\n"
            "- Eat light warm foods only\n"
            "- **Turmeric milk with black pepper** clears congestion\n"
            "- Avoid dairy, heavy foods, and cold drinks\n"
            "- Stay active with light movement if possible"
        ),
        "cold": (
            "**Kapha-type Cold Remedy:**\n"
            "- Tulsi-ginger-black pepper tea\n"
            "- Steam inhalation 2-3 times daily\n"
            "- Turmeric milk with honey\n"
            "- Trikatu churna (ginger, pepper, pippali)\n"
            "- Avoid dairy and cold foods\n"
            "- Keep warm and active\n"
            "- Dry ginger powder with honey"
        ),
        "cough": (
            "**Kapha-type Cough Remedy:**\n"
            "Kapha cough is wet, productive, with thick white mucus.\n\n"
            "- **Honey with black pepper** (1 tsp each)\n"
            "- Tulsi tea with ginger\n"
            "- Trikatu Churna with warm water\n"
            "- Steam inhalation\n"
            "- Avoid dairy, sweet, cold foods\n"
            "- Sitopaladi Churna with honey"
        ),
        "acidity": (
            "**Kapha-type Acidity Remedy:**\n"
            "- Warm water with lemon and honey\n"
            "- Ginger tea before meals\n"
            "- Trikatu for digestion\n"
            "- Light meals only\n"
            "- Avoid heavy, oily, sweet foods"
        ),
        "sore_throat": (
            "**Kapha-type Sore Throat Remedy:**\n"
            "- Warm salt water with turmeric gargle\n"
            "- Honey with black pepper\n"
            "- Ginger-tulsi tea\n"
            "- Avoid dairy and cold foods\n"
            "- Steam inhalation with eucalyptus"
        ),
        "constipation": (
            "**Kapha Constipation Remedy:**\n"
            "- Warm water with lemon and honey morning\n"
            "- Triphala powder at night\n"
            "- Light exercise daily\n"
            "- Ginger tea before meals\n"
            "- Avoid heavy, oily, dairy foods"
        ),
    },
}

# ==================== MODEL INITIALIZATION ====================
class AyurvedicBrain:
    """Ayurveda-specialized AI with Dosha detection and personalization"""
    
    def __init__(self):
        self.device = None
        self.tokenizer = None
        self.model = None
        self.pipe = None
        self.user_dosha = None
        self.conversation_history = []
        
        # We no longer call _load_model() here.
        # It will be called lazily only if a request requires the ML model.
    
    def _ensure_model_loaded(self):
        """Ensure the ML model is loaded. Call this only when rule-based answers aren't enough."""
        if self.pipe is not None:
            return
        self._load_model()

    def _load_model(self):
        """Load tokenizer and model with LoRA adapter."""
        try:
            # Lazy-load heavy ML libraries
            import torch as _torch
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

            if self.device is None:
                self.device = "cuda" if _torch.cuda.is_available() and config.USE_GPU else "cpu"
            
            logger.info(f"🧠 Initializing ML model on {self.device.upper()}...")
            logger.info(f"📦 Loading model: {config.BASE_MODEL}")

            self.tokenizer = AutoTokenizer.from_pretrained(config.BASE_MODEL)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                config.BASE_MODEL,
                torch_dtype=_torch.float16 if self.device == "cuda" else _torch.float32,
                device_map="auto" if self.device == "cuda" else None,
            )

            # Load LoRA adapter if available
            if os.path.isdir(config.ADAPTER_PATH):
                try:
                    from peft import PeftModel
                    self.model = PeftModel.from_pretrained(self.model, config.ADAPTER_PATH)
                    logger.info(f"✅ Loaded Ayurveda LoRA adapter: {config.ADAPTER_PATH}")
                except Exception as e:
                    logger.warning(f"⚠️  Could not load adapter: {e}. Using base model.")
            
            # Create text generation pipeline
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
            )

            logger.info("✅ ML Model loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    # ==================== DOSHA DETECTION ====================
    def detect_dosha(self, user_description: str) -> Optional[str]:
        """Detect user's Dosha from description"""
        description_lower = user_description.lower()
        
        # Score each Dosha based on traits mentioned
        scores = {"vata": 0, "pitta": 0, "kapha": 0}
        
        for dosha, info in DOSHA_TRAITS.items():
            for trait in info["traits"]:
                if trait in description_lower:
                    scores[dosha] += 1
        
        if max(scores.values()) > 0:
            detected = max(scores, key=scores.get)
            logger.info(f"🔍 Detected Dosha: {detected} (scores: {scores})")
            self.user_dosha = detected
            return detected
        
        return None
    
    def get_dosha_info(self, dosha: str) -> str:
        """Get comprehensive Dosha information"""
        if dosha.lower() not in DOSHA_TRAITS:
            return f"Unknown Dosha: {dosha}"
        
        info = DOSHA_TRAITS[dosha.lower()]
        return f"""
🌬️ {info['description']}

**Characteristics:** {', '.join(info['traits'])}
**Ideal Diet:** {', '.join(info['diet'])}
**Beneficial Herbs:** {', '.join(info['herbs'])}
**Avoid:** {', '.join(info['avoid'])}
**Daily Rhythm:** {', '.join(info['routine'])}
**Doctor Recommendation:** {info['doctor']}
    """.encode("ascii", "ignore").decode("ascii")
    
    # ==================== DIET RECOMMENDATIONS ====================
    def get_diet_recommendation(self, dosha: Optional[str] = None) -> str:
        """Provide Dosha-specific diet recommendations"""
        target_dosha = dosha or self.user_dosha or "vata"
        
        if target_dosha.lower() not in DOSHA_TRAITS:
            return f"Unknown Dosha: {target_dosha}"
        
        info = DOSHA_TRAITS[target_dosha.lower()]
        
        diet_plan = f"""
✨ **{target_dosha.upper()} DIET PLAN**

🍽️ **Foods to INCLUDE:**
{', '.join(info['diet'])}

🌿 **Beneficial Herbs & Spices:**
{', '.join(info['herbs'])}

❌ **Foods to AVOID:**
{', '.join(info['avoid'])}

⏰ **Meal Times:** Eat at consistent times, preferably with others
🎯 **Digestion Tip:** Chew slowly, eat mindfully
💧 **Hydration:** Drink warm water or herbal teas
"""
        return diet_plan.encode("ascii", "ignore").decode("ascii")

    def set_user_profile(self, dosha: Optional[str] = None):
        """Store the active user dosha for subsequent answers."""
        resolved = (dosha or "").strip().lower()
        if resolved in DOSHA_TRAITS:
            self.user_dosha = resolved

    def resolve_dosha(self, dosha: Optional[str] = None, prompt: str = "") -> Optional[str]:
        """Resolve the best dosha to use for an answer."""
        if dosha and dosha.lower() in DOSHA_TRAITS:
            return dosha.lower()

        if self.user_dosha and self.user_dosha in DOSHA_TRAITS:
            return self.user_dosha

        detected = self.detect_dosha(prompt)
        if detected:
            return detected

        return None

    def is_ayurveda_scope(self, prompt: str) -> bool:
        """Return True if the prompt is Ayurveda-related."""
        text = prompt.lower()
        return any(keyword in text for keyword in AYURVEDA_SCOPE_KEYWORDS)

    def classify_request(self, prompt: str) -> str:
        """Classify the Ayurveda request so the answer stays strict and structured."""
        text = prompt.lower()

        if any(term in text for term in ["doctor", "vaidya", "physician", "consult"]):
            return "doctor"
        # Fever / cold / cough / sore throat — specific remedy lookup
        if any(term in text for term in ["fever", "jwara", "cold", "cough", "sore throat", "flu", "infection"]):
            return "remedy_condition"
        if any(term in text for term in ["remedy", "remedies", "home remedy", "cure", "heal", "treatment", "medicine"]):
            return "remedy_general"
        if any(term in text for term in ["diet", "food", "meal", "eat", "breakfast", "lunch", "dinner", "recipe", "snack"]):
            return "diet"
        if any(term in text for term in ["sleep", "stress", "routine", "yoga", "exercise", "meditation"]):
            return "routine"
        if any(term in text for term in ["digestion", "acidity", "gas", "bloating", "constipation", "appetite", "skin", "heat", "rash", "weight"]):
            return "condition"
        if any(term in text for term in ["dosha", "prakriti", "vata", "pitta", "kapha"]):
            return "dosha"
        if any(term in text for term in ["herb", "herbs"]):
            return "herb"

        return "general"

    def suggest_vaidya(self) -> str:
        """Return the recommended Ayurvedic practitioner."""
        return PRIMARY_VAIDYA_NAME

    def _generate_model_response(self, prompt: str) -> str:
        """Generate raw model output without the dosha router."""
        self._ensure_model_loaded()
        
        result = self.pipe(
            self._build_prompt(prompt),
            max_new_tokens=config.MAX_TOKENS,
            do_sample=True,
            temperature=config.TEMPERATURE,
            top_p=config.TOP_P,
            repetition_penalty=1.1,
            return_full_text=False,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        response = self._clean_response(result[0]["generated_text"])
        self.conversation_history.append({"user": prompt, "assistant": response})
        return response

    def get_remedy(self, dosha: str, condition: str) -> Optional[str]:
        """Look up a dosha-specific remedy from the knowledge base."""
        dosha_lower = dosha.lower()
        # Normalize condition keywords to remedy keys
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

    def respond_for_user(self, prompt: str, dosha: Optional[str] = None, constitution: str = "") -> str:
        """Strict Ayurveda-only response router that uses the user's dosha."""
        active_dosha = self.resolve_dosha(dosha, prompt=constitution or prompt)

        if constitution and not active_dosha:
            active_dosha = self.detect_dosha(constitution)

        if not active_dosha:
            return (
                "Please complete dosha detection first by describing your body type, appetite, sleep, skin, digestion, and energy. "
                "I only answer Ayurveda dosha, diet, herbs, routine, and Vaidya guidance."
            )

        if not self.is_ayurveda_scope(prompt):
            return (
                f"I specialize only in Ayurveda dosha guidance. Your current dosha is {active_dosha.upper()}. "
                f"Ask me about Vata, Pitta, Kapha, diet, herbs, sleep, stress, digestion, fever remedies, or a Vaidya recommendation."
            )

        intent = self.classify_request(prompt)

        if intent == "doctor":
            return self.get_doctor_recommendation(active_dosha, prompt)

        if intent == "remedy_condition":
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return (
                    f"For your **{active_dosha.upper()}** dosha:\n\n"
                    f"{remedy}\n\n"
                    f"**Important:** If symptoms persist beyond 2 days, consult {self.suggest_vaidya()}.\n"
                    f"Recommended Vaidya: {self.suggest_vaidya()}"
                )
            # Fallback to general condition
            return (
                f"For your {active_dosha.upper()} dosha, focus on rest, warm fluids, and light diet.\n\n"
                f"{self.get_doctor_recommendation(active_dosha, prompt)}"
            )

        if intent == "remedy_general":
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return (
                    f"For your **{active_dosha.upper()}** dosha:\n\n"
                    f"{remedy}\n\n"
                    f"Recommended Vaidya: {self.suggest_vaidya()}"
                )
            # Show herbs as fallback
            info = DOSHA_TRAITS[active_dosha]
            return (
                f"For {active_dosha.upper()}, common Ayurvedic remedies involve: {', '.join(info['herbs'])}.\n\n"
                f"Please describe your specific condition (fever, cold, cough, acidity, etc.) "
                f"for a targeted remedy.\n\n"
                f"Recommended Vaidya: {self.suggest_vaidya()}"
            )

        if intent == "diet":
            return (
                f"For your {active_dosha.upper()} dosha, here is the diet guidance:\n\n"
                f"{self.get_diet_recommendation(active_dosha)}\n\n"
                f"Recommended Vaidya: {self.suggest_vaidya()}"
            )

        if intent == "routine":
            condition = "sleep" if "sleep" in prompt.lower() else "stress"
            return (
                f"For your {active_dosha.upper()} dosha, here is a strict Ayurveda routine guidance:\n\n"
                f"{self.create_wellness_plan(active_dosha, condition)}\n\n"
                f"Recommended Vaidya: {self.suggest_vaidya()}"
            )

        if intent == "condition":
            # Check if there's a specific remedy first
            remedy = self.get_remedy(active_dosha, prompt)
            if remedy:
                return (
                    f"For your **{active_dosha.upper()}** dosha:\n\n"
                    f"{remedy}\n\n"
                    f"Recommended Vaidya: {self.suggest_vaidya()}"
                )
            return (
                f"For your {active_dosha.upper()} dosha, focus on a balancing diet and routine.\n\n"
                f"{self.get_diet_recommendation(active_dosha)}\n\n"
                f"{self.get_doctor_recommendation(active_dosha, prompt)}"
            )

        if intent == "dosha":
            return (
                f"Your active dosha profile is {active_dosha.upper()}.\n\n"
                f"{self.get_dosha_info(active_dosha)}\n\n"
                f"Recommended Vaidya: {self.suggest_vaidya()}"
            )

        if intent == "herb":
            info = DOSHA_TRAITS[active_dosha]
            return (
                f"For {active_dosha.upper()}, the most useful herbs are: {', '.join(info['herbs'])}.\n\n"
                f"Avoid self-prescribing strong herbs without supervision. {self.get_doctor_recommendation(active_dosha, prompt)}"
            )

        context = (
            f"You are Jarvis, an Ayurveda-only assistant. The user's dosha is {active_dosha.upper()}. "
            f"Answer only with Ayurveda dosha guidance, diet, herbs, routine, and recommend {PRIMARY_VAIDYA_NAME} when appropriate. "
            "Do not answer non-Ayurveda topics."
        )
        response = self._generate_model_response(f"{context}\nUser question: {prompt}")
        return f"{response}\n\nRecommended Vaidya: {self.suggest_vaidya()}"

    def check_diet_for_dosha(self, dosha: Optional[str], diet_text: str) -> str:
        """Check a user's diet against their dosha profile."""
        target_dosha = (dosha or self.user_dosha or "").lower()
        if target_dosha not in DOSHA_TRAITS:
            return "Please detect or choose a dosha first so I can check the diet accurately."

        diet_lower = diet_text.lower()
        info = DOSHA_TRAITS[target_dosha]
        included = [food for food in info["diet"] if food.lower() in diet_lower]
        avoided = [food for food in info["avoid"] if food.lower() in diet_lower]

        for food, category in FOOD_ALIASES.items():
            if food in diet_lower and category in info["avoid"] and category not in avoided:
                avoided.append(f"{food} ({category})")
            if food in diet_lower and category in info["diet"] and category not in included:
                included.append(f"{food} ({category})")

        score = max(0, min(100, 70 + len(included) * 8 - len(avoided) * 15))
        status = "supportive" if score >= 75 else "needs balancing" if score >= 50 else "not ideal"
        swaps = {
            "vata": "Add warm soups, ghee, cooked grains, root vegetables, and calming spices like cumin or fennel.",
            "pitta": "Add cooling foods such as cucumber, coconut, leafy greens, rice, amla, coriander, and sweet fruits.",
            "kapha": "Add light steamed vegetables, legumes, barley or millets, ginger, black pepper, turmeric, and warm water.",
        }

        return f"""
**Diet Check for {target_dosha.title()}**
Overall fit: {status} ({score}/100)

**Supportive items found:** {', '.join(included) if included else 'No clear dosha-supportive foods detected.'}
**Items to reduce:** {', '.join(avoided) if avoided else 'No obvious avoid-list items detected.'}

**Better balance:** {swaps[target_dosha]}

This is wellness guidance, not a diagnosis. For chronic symptoms, pregnancy, medications, allergies, diabetes, kidney disease, or eating disorder history, review diet changes with {PRIMARY_VAIDYA_NAME} or another qualified doctor.
"""

    def get_doctor_recommendation(self, dosha: Optional[str] = None, symptoms: str = "") -> str:
        """Give safe doctor recommendation guidance by dosha and symptoms."""
        target_dosha = (dosha or self.user_dosha or "vata").lower()
        info = DOSHA_TRAITS.get(target_dosha, DOSHA_TRAITS["vata"])
        urgent_terms = ["chest pain", "breathing", "faint", "severe pain", "blood", "stroke", "suicidal", "high fever"]
        if any(term in symptoms.lower() for term in urgent_terms):
            return f"Please seek urgent medical care now or contact local emergency services. After urgent care is addressed, you may also consult {PRIMARY_VAIDYA_NAME} for Ayurvedic follow-up."

        return f"""
**Doctor Recommendation for {target_dosha.title()}**
{info['doctor']}

Recommended Vaidya: {PRIMARY_VAIDYA_NAME}

Ask {PRIMARY_VAIDYA_NAME} what to do for this specific user after reviewing their prakriti, vikriti, symptoms, medicines, allergies, age, diet, sleep, pulse assessment, and medical history. Also keep a primary-care doctor involved for labs, persistent symptoms, prescription medicines, pregnancy, children, older adults, or diagnosed conditions.

Before the visit, note your sleep, appetite, bowel pattern, stress, current medicines, allergies, and a 3-day food log.
""".encode("ascii", "ignore").decode("ascii")
    
    # ==================== PRESCRIPTION-BASED RECOMMENDATIONS ====================
    def create_wellness_plan(self, dosha: str, health_condition: str) -> str:
        """Create personalized wellness plan based on Dosha and condition"""
        
        wellness_plans = {
            "vata": {
                "digestion": "🌬️ **Vata Digestion Plan:**\n- Eat warm, cooked foods with ghee\n- Take ginger water before meals\n- Avoid raw foods and salads\n- Include warming spices: cumin, ginger, fennel\n- Ashwagandha supplement for Agni\n- Regular meal times essential",
                
                "sleep": "🌬️ **Vata Sleep Plan:**\n- Oil massage (Abhyanga) before bed\n- Sesame oil on scalp and soles\n- Warm milk with nutmeg and honey\n- Establish bedtime routine\n- Avoid stimulation before sleep\n- 10:00 PM bedtime ideal\n- Use Brahmi oil for calming",
                
                "stress": "🌬️ **Vata Stress Plan:**\n- Daily oil massage (grounding)\n- Meditation 10-15 minutes\n- Yoga: forward bends, lotus pose\n- Warm herbal teas (chamomile, ashwagandha)\n- Maintain routine and schedules\n- Calming music and environments\n- Avoid excessive stimulation"
            },
            "pitta": {
                "digestion": "🔥 **Pitta Digestion Plan:**\n- Eat cool, cooked foods\n- Coconut or cool ghee\n- Avoid spicy, salty, sour foods\n- Include bitter herbs: brahmi, neem\n- Cool herbal teas after meals\n- Don't skip meals (causes acidity)\n- Cilantro for cooling",
                
                "sleep": "🔥 **Pitta Sleep Plan:**\n- Brahmi oil massage\n- Cooling environments (air flow)\n- Coconut oil on skin\n- Cool herbal teas: brahmi, shankhpushpi\n- Avoid late-night work/stimulation\n- Earlier sleep (10:00 PM ideal)\n- Lavender aromatherapy",
                
                "stress": "🔥 **Pitta Stress Plan:**\n- Cooling yoga: forward bends\n- Meditation focusing on calm blue light\n- Cool environments important\n- Brahmi and ashwagandha supplements\n- Avoid competitive situations\n- Spend time in nature, near water\n- Cool herbal teas and cooling diet"
            },
            "kapha": {
                "digestion": "🌍 **Kapha Digestion Plan:**\n- Light, dry, warm foods\n- Stimulating spices: ginger, black pepper, chili\n- Avoid oily and dairy foods\n- Bitter herbs: neem, tulsi\n- Herbal bitters before meals\n- Smaller, frequent meals\n- Tea with warming spices",
                
                "sleep": "🌍 **Kapha Sleep Plan:**\n- Limit sleep to 7 hours (Kapha tendency)\n- Dry massage (Udvartana) with warming oils\n- Stimulating herbs: ginger, black pepper\n- Avoid daytime naps\n- Morning exercise important\n- Warming environment\n- Lighter meals in evening",
                
                "stress": "🌍 **Kapha Stress Plan:**\n- Daily exercise essential (30+ minutes)\n- Stimulating yoga: twists, inversions\n- Warming herbs: ginger, turmeric\n- Keep active and engaged\n- Change routines regularly\n- Social activities important\n- Avoid excessive comfort/rest"
            }
        }
        
        dosha_lower = dosha.lower()
        condition_lower = health_condition.lower()
        
        if dosha_lower in wellness_plans and condition_lower in wellness_plans[dosha_lower]:
            return wellness_plans[dosha_lower][condition_lower].encode("ascii", "ignore").decode("ascii")
        
        return f"Personalized wellness plan for {dosha} with {health_condition} - consult a Vaidya for detailed guidance"
    
    # ==================== RESPONSE GENERATION ====================
    def _build_prompt(self, user_prompt: str) -> str:
        """Build prompt with Ayurvedic system instructions"""
        return f"<|system|>{config.AYURVEDA_SYSTEM_PROMPT}\n<|user|>{user_prompt}\n<|assistant|>"
    
    def _clean_response(self, text: str) -> str:
        """Clean model output"""
        text = text.replace("<|assistant|>", "").replace("<|user|>", "")
        text = re.split(r"<\|.*?\|>", text)[0]
        return text.strip()
    
    def ask_ayurveda(self, prompt: str, dosha: Optional[str] = None, constitution: str = "") -> str:
        """Get a strict Ayurveda-only response for the user."""
        try:
            return self.respond_for_user(prompt, dosha=dosha, constitution=constitution)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error processing your question. Please try again."
    
    def ask_with_context(self, prompt: str, context: str = "") -> str:
        """Get response with context (Dosha, condition, etc)"""
        if context:
            full_prompt = f"{context}\n\nUser Question: {prompt}"
        else:
            full_prompt = prompt
        
        return self._generate_model_response(full_prompt)
    
    # ==================== UTILITY METHODS ====================
    def get_health_summary(self) -> str:
        """Get summary of user's Ayurvedic health profile"""
        if not self.user_dosha:
            return "No Dosha detected yet. Tell me about your constitution to get personalized advice."
        
        return f"""
📊 **Your Ayurvedic Health Profile**
{self.get_dosha_info(self.user_dosha)}

{self.get_diet_recommendation(self.user_dosha)}
    """.encode("ascii", "ignore").decode("ascii")
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history


# ==================== SINGLETON INSTANCE ====================
_brain_instance = None

def get_brain() -> AyurvedicBrain:
    """Get or create singleton brain instance"""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = AyurvedicBrain()
    return _brain_instance


# ==================== TESTING ====================
if __name__ == "__main__":
    brain = AyurvedicBrain()
    
    # Test Dosha detection
    print("\n" + "=" * 60)
    print("Testing Dosha Detection")
    print("=" * 60)
    brain.detect_dosha("I am thin, creative, and anxious")
    print(brain.get_health_summary())
    
    # Test diet recommendation
    print("\n" + "=" * 60)
    print("Testing Diet Recommendation")
    print("=" * 60)
    print(brain.get_diet_recommendation("vata"))
    
    # Test wellness plan
    print("\n" + "=" * 60)
    print("Testing Wellness Plan")
    print("=" * 60)
    print(brain.create_wellness_plan("vata", "digestion"))
    
    # Test Ayurvedic response
    print("\n" + "=" * 60)
    print("Testing Ayurvedic Response")
    print("=" * 60)
    response = brain.ask_ayurveda("What herbs help balance Vata Dosha?")
    print(f"Response: {response}")
