"""
Ayurveda-Specialized LoRA Training Pipeline - DOSHA-SPECIFIC VERSION
Trains model with strict focus on Dosha diet, symptoms, and remedies
"""

import json
import logging
import os
import random
import inspect
from collections import defaultdict

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model

import config

# ==================== COMPREHENSIVE DOSHA DATA ====================
DOSHA_SPECIFIC_DATA = {
    "vata": {
        "symptoms": ["anxiety and worry", "dry skin", "constipation", "irregular digestion",
                    "low energy and fatigue", "poor sleep", "scattered mind", "cold body",
                    "weak immunity", "joint pain and cracking", "irregular appetite"],
        "diet": ["warm cooked foods", "sesame oil", "ghee", "warm milk", "mung beans", "rice", 
                "wheat", "root vegetables", "dates and raisins", "warm herbal teas"],
        "herbs": ["Ashwagandha", "Brahmi", "Sesame oil", "Shatavari", "Ginger"],
        "remedies": ["Daily oil massage with sesame oil", "Warm baths", "Regular sleep schedule"],
        "lifestyle": ["Establish daily routine", "Regular meal times", "Early sleep"]
    },
    "pitta": {
        "symptoms": ["excessive heat and burning", "inflamed skin and rashes", "excessive sweating",
                    "anger and irritability", "sharp hunger", "loose stools and diarrhea"],
        "diet": ["cool foods", "coconut oil", "coconut milk", "sweet fruits", "leafy greens", 
                "barley", "rice", "cool water", "herbal cooling teas", "melons"],
        "herbs": ["Brahmi", "Ashwagandha", "Sankhapushpi", "Shatavari", "Turmeric"],
        "remedies": ["Cool coconut oil massage", "Brahmi oil on scalp", "Cool baths"],
        "lifestyle": ["Avoid excessive heat", "Cool environments preferred", "Calm social interactions"]
    },
    "kapha": {
        "symptoms": ["sluggishness and lethargy", "weight gain", "heaviness", "slow digestion",
                    "congestion and mucus", "sweet cravings", "water retention"],
        "diet": ["light and dry foods", "warming spices", "beans and legumes", "barley and rye",
                "bitter greens", "stimulating foods", "black pepper", "ginger and chili"],
        "herbs": ["Ginger", "Black Pepper", "Turmeric", "Cumin", "Triphala"],
        "remedies": ["Daily dry massage (Udvartana)", "Stimulating exercise", "Regular movement"],
        "lifestyle": ["Regular exercise essential", "Avoid excessive rest", "Early rising"]
    }
}

ALLOWED_CATEGORIES = {
    "diet", "herbs", "remedies", "consultation", "dosha",
    "homeremedy", "remedy", "routine", "advanced", "conversational",
}
STRICT_DOMAIN_TERMS = {
    "dosha", "vata", "pitta", "kapha", "prakriti", "vikriti",
    "diet", "food", "meal", "herb", "herbs", "remedy", "remedies",
    "consult", "consultation", "vaidya", "ayurveda",
    "fever", "cold", "cough", "acidity", "constipation", "immunity",
    "detox", "sleep", "stress", "digestion", "bloating", "inflammation",
    "sore throat", "agni", "ama", "panchakarma", "sattvic", "yoga",
    "meditation", "exercise", "routine", "breakfast", "weight",
}

LOW_MEMORY_MODE = True
ONLY_THREE_DOSHAS = {"vata", "pitta", "kapha", "general"}

# ==================== SIMPLE DATASET CLASS ====================
class SimpleTextDataset(torch.utils.data.Dataset):
    """Custom dataset without TextDataset dependency"""
    def __init__(self, examples, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = examples
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        ex = self.examples[idx]
        text = f"Q: {ex.get('question', '')}\nA: {ex.get('answer', '')}"
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": encoding["input_ids"].squeeze(),
        }

# ==================== GENERATE TRAINING DATA ====================
def generate_dosha_training_data():
    """Generate comprehensive dosha-specific Q&A training data"""
    training_data = []
    
    for dosha, data in DOSHA_SPECIFIC_DATA.items():
        # Dosha profile
        training_data.append({
            "question": f"What are the characteristics of {dosha} dosha?",
            "answer": f"The {dosha} dosha is characterized by: {', '.join(data['symptoms'][:3])}.",
            "dosha": dosha, "category": "dosha"
        })
        
        # Diet
        training_data.append({
            "question": f"What foods should a {dosha} person eat?",
            "answer": f"A {dosha} person should eat: {', '.join(data['diet'][:5])}.",
            "dosha": dosha, "category": "diet"
        })
        
        # Herbs
        training_data.append({
            "question": f"Which herbs are beneficial for {dosha} dosha?",
            "answer": f"Top herbs for {dosha}: {', '.join(data['herbs'])}.",
            "dosha": dosha, "category": "herbs"
        })
        
        # Remedies
        training_data.append({
            "question": f"How should a {dosha} person manage their health?",
            "answer": f"For {dosha} wellness: {', '.join(data['remedies'])}.",
            "dosha": dosha, "category": "remedies"
        })
        
        # Consultation
        training_data.append({
            "question": f"When should a {dosha} person consult an Ayurveda doctor?",
            "answer": "Consult a qualified Vaidya for persistent symptoms, chronic disease, medicine interactions, pregnancy, severe pain, or unresolved digestive and sleep issues. Dosha-specific guidance must be personalized.",
            "dosha": dosha, "category": "consultation"
        })

        # Symptom-led diet + herb + remedy + consult advice
        for symptom in data["symptoms"]:
            training_data.append({
                "question": f"I have {symptom}. What should I do?",
                "answer": (
                    f"This may indicate {dosha} aggravation. Favor {', '.join(data['diet'][:4])}, "
                    f"use herbs such as {', '.join(data['herbs'][:3])}, and follow {', '.join(data['remedies'][:2])}. "
                    "If symptoms persist or worsen, consult a qualified Vaidya."
                ),
                "dosha": dosha, "category": "consultation"
            })

        # Extra domain-focused permutations for better coverage
        for food in data["diet"]:
            training_data.append({
                "question": f"Is {food} good for {dosha} dosha?",
                "answer": f"For {dosha}, {food} can be useful when combined with a balanced dosha-friendly meal plan and regular routine.",
                "dosha": dosha, "category": "diet"
            })

        for herb in data["herbs"]:
            training_data.append({
                "question": f"How is {herb} used for {dosha} balance?",
                "answer": f"{herb} is commonly used in Ayurveda for {dosha} support. Use under proper guidance with dosha-specific diet and routine.",
                "dosha": dosha, "category": "herbs"
            })
    
    return training_data


def is_in_allowed_domain(example):
    """Keep only strict domain examples requested by user."""
    category = str(example.get("category", "")).strip().lower()
    if category and category not in ALLOWED_CATEGORIES:
        return False

    combined = f"{example.get('question', '')} {example.get('answer', '')}".lower()
    return any(term in combined for term in STRICT_DOMAIN_TERMS)


def load_jsonl_examples(path, default_category="dosha"):
    """Read JSONL examples and map unknown categories."""
    examples = []
    if not os.path.exists(path):
        return examples

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ex = json.loads(line)
                if "category" not in ex or not ex["category"]:
                    ex["category"] = default_category
                examples.append(ex)
            except Exception:
                continue
    return examples


def load_json_array_examples(path, default_category="dosha"):
    """Read a JSON array file (not JSONL) and return examples."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        for ex in data:
            if "category" not in ex or not ex["category"]:
                ex["category"] = default_category
            # Normalize category key (e.g. "HomeRemedy" -> "homeremedy")
            ex["category"] = ex["category"].lower().replace(" ", "")
            # Normalize dosha key
            ex["dosha"] = ex.get("dosha", "general").lower()
        return data
    except Exception:
        return []


def deduplicate_examples(examples):
    """Remove duplicate question-answer pairs."""
    seen = set()
    unique = []
    for ex in examples:
        key = (ex.get("question", "").strip().lower(), ex.get("answer", "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(ex)
    return unique

# ==================== LOGGING ====================
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== MAIN TRAINING ====================
def train_ayurveda_model():
    """Train Ayurveda model with dosha-specific data"""
    
    logger.info("=" * 60)
    logger.info("[AYURVEDA DOSHA-SPECIFIC MODEL TRAINING]")
    logger.info("=" * 60)
    
    # Load and merge data
    logger.info("[Loading training data...]")
    all_examples = []
    
    # 1. User-provided structured dosha questions (JSONL)
    user_dataset_path = "data/ayurveda_dosha_user_questions.jsonl"
    loaded_user_examples = load_jsonl_examples(user_dataset_path, default_category="dosha")
    if loaded_user_examples:
        all_examples.extend(loaded_user_examples)
        logger.info(f"   Loaded {len(loaded_user_examples)} user dosha examples from {user_dataset_path}")

    # 2. NEW: Comprehensive Ayurveda Q&A dataset (JSON array) with fever, remedies, etc.
    qa_dataset_path = "data/ayurveda_dosha_qa_dataset.json"
    loaded_qa_examples = load_json_array_examples(qa_dataset_path, default_category="dosha")
    if loaded_qa_examples:
        all_examples.extend(loaded_qa_examples)
        logger.info(f"   Loaded {len(loaded_qa_examples)} Q&A examples from {qa_dataset_path}")

    # 3. Any other JSONL files in data/
    for fname in ["ayurveda_prakriti_diet_expanded.jsonl", "ayurveda_qa.jsonl"]:
        fpath = os.path.join("data", fname)
        extra = load_jsonl_examples(fpath, default_category="dosha")
        if extra:
            all_examples.extend(extra)
            logger.info(f"   Loaded {len(extra)} examples from {fname}")

    # 4. Generate only strict dosha data to keep focus and memory usage predictable.
    generated = generate_dosha_training_data()
    all_examples.extend(generated)
    logger.info(f"   Generated {len(generated)} new dosha examples")

    # Strictly keep requested domain
    all_examples = [ex for ex in all_examples if is_in_allowed_domain(ex)]
    all_examples = [ex for ex in all_examples if str(ex.get("dosha", "")).lower() in ONLY_THREE_DOSHAS]
    all_examples = deduplicate_examples(all_examples)
    random.shuffle(all_examples)
    logger.info(f"   Filtered to strict Ayurveda domains: {len(all_examples)} examples")

    # Print category distribution
    category_counts = defaultdict(int)
    for ex in all_examples:
        category_counts[str(ex.get("category", "dosha")).lower()] += 1
    logger.info(f"   Category distribution: {dict(category_counts)}")
    
    # Split data
    split_idx = int(len(all_examples) * 0.9)
    train_examples = all_examples[:split_idx]
    eval_examples = all_examples[split_idx:]
    logger.info(f"   Split: {len(train_examples)} train, {len(eval_examples)} eval")
    
    # Load model
    logger.info("[Loading model...]")
    MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    if torch.cuda.is_available():
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
    else:
        logger.info("   CUDA not available; loading model on CPU without 4-bit quantization")
        model = AutoModelForCausalLM.from_pretrained(
            MODEL,
            torch_dtype=torch.float32,
            device_map={"": "cpu"},
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    logger.info("   Model loaded successfully")
    
    # LoRA
    logger.info("[Configuring LoRA...]")
    lora_config = LoraConfig(
        r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Datasets
    logger.info("[Creating datasets...]")
    max_length = 256 if LOW_MEMORY_MODE else 512
    train_dataset = SimpleTextDataset(train_examples, tokenizer, max_length=max_length)
    eval_dataset = SimpleTextDataset(eval_examples, tokenizer, max_length=max_length)
    logger.info(f"   Train dataset: {len(train_dataset)} examples")
    logger.info(f"   Eval dataset: {len(eval_dataset)} examples")
    
    # Training
    logger.info("[Setting training config...]")
    training_kwargs = {
        "output_dir": "models/ayurveda-lora-dosha-lowmem",
        "num_train_epochs": 2 if LOW_MEMORY_MODE else 3,
        "per_device_train_batch_size": 1 if LOW_MEMORY_MODE else 2,
        "per_device_eval_batch_size": 1 if LOW_MEMORY_MODE else 2,
        "gradient_accumulation_steps": 8 if LOW_MEMORY_MODE else 4,
        "learning_rate": 2e-4,
        "warmup_ratio": 0.05 if LOW_MEMORY_MODE else 0.1,
        "lr_scheduler_type": "cosine",
        "logging_steps": 5,
        "eval_steps": 20 if LOW_MEMORY_MODE else 10,
        "save_steps": 50 if LOW_MEMORY_MODE else 10,
        "save_total_limit": 1 if LOW_MEMORY_MODE else 2,
        "load_best_model_at_end": False if LOW_MEMORY_MODE else True,
    }

    # Handle transformers version differences safely.
    signature_params = inspect.signature(TrainingArguments.__init__).parameters
    if "overwrite_output_dir" in signature_params:
        training_kwargs["overwrite_output_dir"] = True
    if "evaluation_strategy" in signature_params:
        training_kwargs["evaluation_strategy"] = "steps"
    elif "eval_strategy" in signature_params:
        training_kwargs["eval_strategy"] = "steps"
    if "save_strategy" in signature_params:
        training_kwargs["save_strategy"] = "steps"

    training_args = TrainingArguments(**training_kwargs)
    
    logger.info("[Initializing trainer...]")
    trainer_kwargs = {
        "model": model,
        "args": training_args,
        "train_dataset": train_dataset,
        "eval_dataset": eval_dataset,
    }
    trainer_signature = inspect.signature(Trainer.__init__).parameters
    if "tokenizer" in trainer_signature:
        trainer_kwargs["tokenizer"] = tokenizer
    elif "processing_class" in trainer_signature:
        trainer_kwargs["processing_class"] = tokenizer

    trainer = Trainer(**trainer_kwargs)
    
    logger.info("=" * 60)
    logger.info("[STARTING TRAINING]")
    logger.info("=" * 60)
    trainer.train()
    
    logger.info("[Saving model...]")
    final_dir = "models/medical-lora"
    trainer.model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    
    logger.info("=" * 60)
    logger.info("[TRAINING COMPLETE]")
    logger.info(f"Model saved to: {final_dir}")
    logger.info("=" * 60)

if __name__ == "__main__":
    train_ayurveda_model()
