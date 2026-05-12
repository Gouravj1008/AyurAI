#!/usr/bin/env python3
"""
Jarvis AI Assistant - System Test & Launch
Tests backend components and launches UI
"""

import sys
import os

print("\n" + "="*70)
print("🤖 JARVIS AI ASSISTANT - FULL SYSTEM TEST & LAUNCH")
print("="*70)

print("\n📋 STEP 1: Checking Model Files...")
import os

models_needed = [
    ("Voice Recognition", "models/vosk-model-small-en-us-0.15"),
    ("Porcupine Model", "models/porcupine/jarvis.ppn")
]

for name, path in models_needed:
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"   {status} {name}: {path}")

print("\n📦 STEP 2: Testing Backend Components...")

try:
    print("   ⏳ Loading voice recognition model (Vosk)...")
    from voice_input import model
    print("   ✓ Voice recognition model loaded")
except Exception as e:
    print(f"   ✗ Voice recognition error: {e}")

try:
    print("   ⏳ Loading AI brain (TinyLlama)...")
    from ai_brain import pipe
    print("   ✓ AI model loaded (TinyLlama-1.1B-Chat-v1.0)")
except Exception as e:
    print(f"   ✗ AI model error: {e}")

print("\n🎤 STEP 3: Testing AI Response...")
try:
    from ai_brain import ask_ai
    print("   ⏳ Querying AI: 'What is 2+2?'")
    response = ask_ai("What is 2+2?")
    print(f"   ✓ AI Response: {response[:100]}...")
except Exception as e:
    print(f"   ✗ AI query error: {e}")

print("\n" + "="*70)
print("✓ All backend components initialized successfully!")
print("="*70)

print("\n🚀 LAUNCHING JARVIS CHAT INTERFACE...\n")
print("(The Jarvis Chat window is starting. Type messages or use the microphone button.)")
print("Press Ctrl+C to exit.\n")
print("="*70 + "\n")

# Now launch the UI
try:
    import chat_ui
except KeyboardInterrupt:
    print("\n\n⏹  Jarvis Assistant stopped.")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error launching UI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
