#!/usr/bin/env python3
"""
Jarvis Project Status Check - Comprehensive Diagnostic
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("JARVIS PROJECT STATUS CHECK")
print("=" * 70)

# 1. Check Python version
print(f"\n1️⃣  Python Version: {sys.version}")
print(f"   Executable: {sys.executable}")

# 2. Check project structure
print(f"\n2️⃣  Project Structure Check:")
required_files = {
    "ai_brain_ayurveda.py": "AI Brain (Ayurveda)",
    "chat_ui_ayurveda.py": "Chat UI (Ayurveda)",
    "voice_input_improved.py": "Voice Input",
    "hotword_secure.py": "Hotword Detection",
    "config.py": "Configuration",
    "error_handler.py": "Error Handler",
    ".env": "Environment Config",
    "models/vosk-model-small-en-us-0.15/": "Vosk Model",
    "models/medical-lora/": "Medical LoRA Adapter",
}

for file_path, description in required_files.items():
    exists = Path(file_path).exists()
    status = "✅" if exists else "❌"
    print(f"   {status} {description:30} - {file_path}")

# 3. Check dependencies
print(f"\n3️⃣  Dependency Check:")
dependencies = [
    ("transformers", "Hugging Face Transformers"),
    ("torch", "PyTorch"),
    ("peft", "PEFT Library"),
    ("vosk", "Vosk STT"),
    ("pvporcupine", "Porcupine"),
    ("sounddevice", "Sound Device"),
    ("tkinter", "Tkinter GUI"),
    ("dotenv", "Python-dotenv"),
    ("PIL", "Pillow"),
]

for package, name in dependencies:
    try:
        __import__(package)
        print(f"   ✅ {name:30}")
    except ImportError as e:
        print(f"   ❌ {name:30} - {str(e)}")

# 4. Check key functions
print(f"\n4️⃣  Module Import Check:")
modules_to_check = [
    "config",
    "error_handler",
    "ai_brain_ayurveda",
    "voice_input_improved",
    "hotword_secure",
]

for module_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"   ✅ {module_name:30}")
    except Exception as e:
        print(f"   ❌ {module_name:30} - {str(e)[:50]}")

# 5. Environment check
print(f"\n5️⃣  Environment Variables:")
env_vars = ["HF_API_KEY", "PORCUPINE_ACCESS_KEY", "USE_GPU"]
for var in env_vars:
    value = os.environ.get(var, "NOT SET")
    if value != "NOT SET":
        value = value[:20] + "..." if len(value) > 20 else value
    print(f"   {var:25} - {value}")

print("\n" + "=" * 70)
print("END OF STATUS CHECK")
print("=" * 70)
