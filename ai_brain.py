import os
import re

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH = os.getenv("JARVIS_MEDICAL_ADAPTER", "models/medical-lora")

print("🧠 Loading local AI model (first run may take 1-2 minutes)...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

if os.path.isdir(ADAPTER_PATH):
    try:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, ADAPTER_PATH)
        print(f"🩺 Loaded medical adapter: {ADAPTER_PATH}")
    except Exception as adapter_error:
        print(f"⚠ Could not load medical adapter ({adapter_error}). Using base model.")
else:
    print("ℹ No medical adapter found. Using base model.")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,
)


def _build_prompt(user_prompt):
    system_prompt = (
        "You are Jarvis, a medical Q&A assistant for educational support. "
        "Answer only from reliable general medical knowledge, be concise, and ask follow-up "
        "questions when details are missing. If symptoms seem urgent (chest pain, breathing "
        "difficulty, stroke signs, heavy bleeding), clearly advise emergency care immediately. "
        "Never claim diagnosis certainty."
    )
    return f"<|system|>{system_prompt}\n<|user|>{user_prompt}\n<|assistant|>"


def _clean_response(text):
    text = text.replace("<|assistant|>", "").replace("<|user|>", "")
    text = re.split(r"<\|.*?\|>", text)[0]
    return text.strip()


def ask_ai(prompt):
    result = pipe(
        _build_prompt(prompt),
        max_new_tokens=180,
        do_sample=True,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.1,
        return_full_text=False,
        pad_token_id=tokenizer.pad_token_id,
    )
    return _clean_response(result[0]["generated_text"])
