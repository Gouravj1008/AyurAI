#!/usr/bin/env python3
"""
Jarvis AI Assistant - Full System Launcher
Runs both backend (AI model + voice input) and frontend (GUI)
"""

import sys
import subprocess
import platform

print("=" * 60)
print("🤖 JARVIS AI ASSISTANT - SYSTEM LAUNCHER")
print("=" * 60)

# Show system info
print(f"\n📊 System Information:")
print(f"   Platform: {platform.system()} {platform.release()}")
print(f"   Python: {sys.version.split()[0]}")
print(f"   Executable: {sys.executable}")

# Show startup status
print(f"\n🚀 Starting Jarvis AI System...")
print(f"   Backend: AI Brain (TinyLlama) + Voice Input (Vosk)")
print(f"   Frontend: Chat UI (Tkinter)")

print(f"\n{'=' * 60}")
print("Initializing AI model and voice system...\n")

# Run the main chat UI (which includes backend)
try:
    subprocess.run([sys.executable, "chat_ui.py"])
except KeyboardInterrupt:
    print("\n\n⏹  Jarvis Assistant stopped by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error running Jarvis: {e}")
    sys.exit(1)
