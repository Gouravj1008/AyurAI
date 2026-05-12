"""
Secure configuration management for Jarvis Ayurveda Chatbot
Loads settings from environment variables with sensible defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ==================== SECURITY & KEYS ====================
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

if not PORCUPINE_ACCESS_KEY:
    print("[WARN] PORCUPINE_ACCESS_KEY not set in .env file")
if not HUGGINGFACE_TOKEN:
    print("[WARN] HUGGINGFACE_TOKEN not set in .env file")

# ==================== MODEL CONFIGURATION ====================
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_PATH = os.getenv("JARVIS_MEDICAL_ADAPTER", "models/medical-lora")

# GPU/Device Configuration
USE_GPU = os.getenv("USE_GPU", "true").lower() == "true"
DEVICE = 0 if USE_GPU else -1  # 0 for GPU, -1 for CPU
DEVICE_NAME = "CUDA (GPU)" if USE_GPU else "CPU"

# Model generation parameters
TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("MODEL_MAX_TOKENS", "256"))
TOP_P = float(os.getenv("MODEL_TOP_P", "0.9"))

# ==================== AYURVEDA SYSTEM PROMPT ====================
AYURVEDA_SYSTEM_PROMPT = """You are Jarvis, an Ayurvedic health assistant trained exclusively on Ayurvedic principles and practices.

**Your Core Purpose:**
- Provide guidance ONLY based on Ayurvedic philosophy (Dosha balance, Agni, etc.)
- Recommend Ayurvedic treatments, herbs, diets, and lifestyle practices
- Give personalized dietary suggestions based on Doshas (Vata, Pitta, Kapha)
- Help with disease management through Ayurvedic approaches

**Important Guidelines:**
1. ONLY answer questions related to Ayurveda, herbs, Ayurvedic diet, and lifestyle
2. If asked about non-Ayurvedic topics, politely decline and redirect: "I specialize in Ayurvedic knowledge. Could you ask about herbs, doshas, diet, or Ayurvedic treatments?"
3. For serious health conditions, always recommend consulting Vaidya Rohit Tayde or another qualified Ayurvedic practitioner/doctor
4. Always mention the relevant Dosha(s) in your recommendations
5. Provide specific herbs, foods, and practices that balance the identified Dosha
6. Be concise but detailed in your responses

**Response Format:**
- Start with Dosha identification if relevant
- Explain based on Ayurvedic principles
- Recommend specific herbs, foods, or practices
- End with cautionary note if needed
- If the user asks for a doctor recommendation, name Vaidya Rohit Tayde and ask the user to consult him for user-specific advice based on prakriti, vikriti, symptoms, medicines, allergies, age, diet, sleep, and history

Remember: You are an Ayurvedic wellness guide, not a conventional doctor. Always stay within Ayurvedic scope."""

# ==================== AUDIO CONFIGURATION ====================
AUDIO_DEVICE = int(os.getenv("AUDIO_DEVICE_INDEX", "-1"))  # -1 for auto-detect
STT_TIMEOUT = int(os.getenv("STT_TIMEOUT", "10"))  # seconds
STT_ENGINE = os.getenv("STT_ENGINE", "vosk")  # vosk or other

# ==================== HOTWORD CONFIGURATION ====================
HOTWORD_MODEL = os.getenv("HOTWORD_MODEL", "models/porcupine/jarvis.ppn")
ENABLE_HOTWORD = os.getenv("ENABLE_HOTWORD", "true").lower() == "true"

# ==================== TTS CONFIGURATION ====================
ENABLE_TTS = os.getenv("ENABLE_TTS", "true").lower() == "true"
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")  # pyttsx3 or google

# ==================== TRAINING CONFIGURATION ====================
TRAINING_BATCH_SIZE = int(os.getenv("TRAINING_BATCH_SIZE", "2"))
TRAINING_EPOCHS = int(os.getenv("TRAINING_EPOCHS", "3"))
TRAINING_LR = float(os.getenv("TRAINING_LR", "2e-4"))
TRAINING_MAX_SEQ = int(os.getenv("TRAINING_MAX_SEQ", "512"))
TRAINING_LORA_R = int(os.getenv("TRAINING_LORA_R", "16"))
TRAINING_LORA_ALPHA = int(os.getenv("TRAINING_LORA_ALPHA", "32"))

# ==================== PATHS ====================
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / "data"
MODELS_PATH = BASE_PATH / "models"
OUTPUTS_PATH = BASE_PATH / "outputs"

# Ensure directories exist
DATA_PATH.mkdir(exist_ok=True)
MODELS_PATH.mkdir(exist_ok=True)
OUTPUTS_PATH.mkdir(exist_ok=True)

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "jarvis.log")

# Print Configuration Summary
if __name__ == "__main__":
    print("=" * 50)
    print("[CONF] JARVIS CONFIGURATION")
    print("=" * 50)
    print(f"Device: {DEVICE_NAME}")
    print(f"Base Model: {BASE_MODEL}")
    print(f"Adapter Path: {ADAPTER_PATH}")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Max Tokens: {MAX_TOKENS}")
    print(f"Hotword Enabled: {ENABLE_HOTWORD}")
    print(f"TTS Enabled: {ENABLE_TTS}")
    print(f"STT Timeout: {STT_TIMEOUT}s")
    print("=" * 50)
