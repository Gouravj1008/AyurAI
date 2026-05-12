"""
Ayurveda-Specialized LoRA Training Pipeline
Trains TinyLlama with Ayurvedic knowledge for strict Dosha-based recommendations
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

import config

STRICT_DOSHA_TERMS = {"vata", "pitta", "kapha", "dosha", "prakriti", "vaidya", "ayurveda", "herb", "diet", "wellness"}


def is_strict_dosha_example(example):
    """Keep only examples that are directly tied to dosha-based Ayurveda guidance."""
    combined = f"{example.get('question', '')} {example.get('answer', '')}".lower()
    return any(term in combined for term in STRICT_DOSHA_TERMS)

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== DEVICE DETECTION ====================
def get_device_info():
    """Detect and report available compute resources"""
    if torch.cuda.is_available():
        logger.info(f"✅ CUDA Available: {torch.cuda.get_device_name(0)}")
        logger.info(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        return "cuda"
    elif torch.backends.mps.is_available():
        logger.info("✅ Metal Performance Shaders (MPS) available on Mac")
        return "mps"
    else:
        logger.warning("⚠️  GPU not available, using CPU (training will be slow)")
        return "cpu"

device = get_device_info()

# ==================== DATA LOADING ====================
def load_ayurveda_data(data_path="data/ayurveda_qa.jsonl"):
    """Load Ayurveda Q&A dataset"""
    try:
        data = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                example = json.loads(line)
                if is_strict_dosha_example(example):
                    data.append(example)
        logger.info(f"✅ Loaded {len(data)} Ayurveda Q&A pairs")
        return data
    except FileNotFoundError:
        logger.error(f"❌ Dataset not found: {data_path}")
        return []

def format_ayurveda_prompt(example):
    """Format Q&A into instruction-following prompt"""
    text = f"""<|system|>You are Jarvis, an Ayurveda-only assistant trained strictly on dosha-based guidance.
Answer only about Vata, Pitta, Kapha, prakriti, Ayurvedic diet, herbs, routine, and Vaidya guidance.
If the user asks anything outside Ayurveda, politely redirect them back to dosha, diet, herbs, sleep, stress, digestion, or Vaidya recommendations.
Always tie the answer to the user's dosha when possible and recommend Vaidya Rohit Tayde or another qualified Vaidya for personalized review.
Stay strictly within Ayurvedic scope and keep the answer concise but specific.
<|user|>{example['question']}
<|assistant|>{example['answer']}<|end|>"""
    return {"text": text}

# ==================== MODEL CONFIGURATION ====================
def setup_model_and_tokenizer():
    """Load base model and configure LoRA"""
    logger.info(f"📦 Loading base model: {config.BASE_MODEL}")
    
    tokenizer = AutoTokenizer.from_pretrained(config.BASE_MODEL)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # 4-bit quantization for memory efficiency
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        config.BASE_MODEL,
        quantization_config=quantization_config,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    
    logger.info("✅ Model loaded successfully")
    return model, tokenizer

def configure_lora(model):
    """Apply LoRA configuration"""
    lora_config = LoraConfig(
        r=config.TRAINING_LORA_R,
        lora_alpha=config.TRAINING_LORA_ALPHA,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    
    model = get_peft_model(model, lora_config)
    logger.info(f"✅ LoRA configured: r={config.TRAINING_LORA_R}, alpha={config.TRAINING_LORA_ALPHA}")
    return model

# ==================== TRAINING SETUP ====================
def train_ayurveda_model(train_data, output_dir="models/medical-lora"):
    """Main training pipeline"""
    
    logger.info("=" * 60)
    logger.info("🧘 JARVIS AYURVEDA LoRA TRAINING PIPELINE")
    logger.info("=" * 60)
    logger.info(f"Device: {device.upper()}")
    logger.info(f"Training data: {len(train_data)} examples")
    logger.info(f"Base model: {config.BASE_MODEL}")
    logger.info(f"Output: {output_dir}")
    logger.info("=" * 60)
    
    # Load model and tokenizer
    model, tokenizer = setup_model_and_tokenizer()
    
    # Configure LoRA
    model = configure_lora(model)
    
    # Format and create dataset
    formatted_data = [format_ayurveda_prompt(ex) for ex in train_data]
    dataset = Dataset.from_dict({
        "text": [d["text"] for d in formatted_data]
    })
    
    logger.info(f"📊 Dataset prepared: {len(dataset)} formatted examples")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=config.TRAINING_EPOCHS,
        per_device_train_batch_size=config.TRAINING_BATCH_SIZE,
        gradient_accumulation_steps=8,
        learning_rate=float(config.TRAINING_LR),
        logging_steps=5,
        save_steps=50,
        save_total_limit=2,
        warmup_steps=10,
        weight_decay=0.01,
        optim="paged_adamw_8bit",
        bf16=device == "cuda",
        max_grad_norm=0.3,
        dataloader_pin_memory=True,
        report_to="none",
    )
    
    # Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        tokenizer=tokenizer,
        args=training_args,
        packing=False,
        max_seq_length=config.TRAINING_MAX_SEQ,
    )
    
    logger.info("🚀 Starting training...")
    trainer.train()
    
    # Save model and tokenizer
    logger.info(f"💾 Saving model to {output_dir}")
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save training config
    with open(f"{output_dir}/training_config.json", "w") as f:
        json.dump({
            "base_model": config.BASE_MODEL,
            "dataset_size": len(train_data),
            "epochs": config.TRAINING_EPOCHS,
            "batch_size": config.TRAINING_BATCH_SIZE,
            "learning_rate": str(config.TRAINING_LR),
            "device": device,
            "training_date": datetime.now().isoformat(),
        }, f, indent=2)
    
    logger.info("✅ Training complete!")
    logger.info(f"📁 Model saved to {output_dir}")

# ==================== EVALUATION ====================
def evaluate_model(model, tokenizer, test_questions):
    """Quick evaluation on test questions"""
    logger.info("\n🧪 Model Evaluation")
    logger.info("=" * 60)
    
    from transformers import pipeline
    
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if device == "cuda" else -1,
    )
    
    for question in test_questions:
        prompt = f"<|system|>You are Jarvis, an Ayurveda-only assistant focused strictly on dosha guidance.\n<|user|>{question}\n<|assistant|>"
        response = pipe(prompt, max_new_tokens=100, temperature=0.3, do_sample=True)
        answer = response[0]["generated_text"].split("<|assistant|>")[-1].strip()
        logger.info(f"\nQ: {question}")
        logger.info(f"A: {answer}")

# ==================== MAIN ====================
if __name__ == "__main__":
    # Load Ayurveda dataset
    ayurveda_data = load_ayurveda_data()
    
    if not ayurveda_data:
        logger.error("No training data available. Exiting.")
        exit(1)
    
    # Train model
    train_ayurveda_model(ayurveda_data)
    
    # Quick evaluation
    test_questions = [
        "What herbs help balance Vata Dosha?",
        "How do I improve my digestion through Ayurveda?",
        "What diet should a Pitta person follow?",
    ]
    
    # Reload model for evaluation
    from transformers import AutoModelForCausalLM, AutoTokenizer
    model = AutoModelForCausalLM.from_pretrained("models/medical-lora")
    tokenizer = AutoTokenizer.from_pretrained("models/medical-lora")
    
    evaluate_model(model, tokenizer, test_questions)
    
    logger.info("\n✅ All done! Ready to chat with Ayurvedic knowledge!")
