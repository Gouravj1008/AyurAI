#!/usr/bin/env python3
"""
Jarvis Ayurvedic Health Assistant - Launcher
Main entry point for the application
"""

import logging
import os
import shutil
import subprocess
import threading
import sys
import time
import webbrowser
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ==================== SETUP LOGGING ====================
import io
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("jarvis.log", encoding="utf-8"),
        logging.StreamHandler(stream=io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace'))
    ]
)

logger = logging.getLogger(__name__)

# ==================== PRE-LAUNCH CHECKS ====================
def check_dependencies():
    """Check if all required dependencies are installed"""
    logger.info("[*] Checking dependencies...")
    
    required_packages = [
        "transformers",
        "torch",
        "peft",
        "trl",
        "datasets",
        "vosk",
        "pvporcupine",
        "sounddevice",
        "dotenv",
        "flask",
        "flask_cors",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"[ERR] Missing packages: {', '.join(missing_packages)}")
        logger.error("Install with: pip install -r requirements_complete.txt")
        return False
    
    logger.info("[OK] All dependencies installed")
    return True

def check_models():
    """Check if required model files exist"""
    logger.info("[*] Checking model files...")
    
    required_models = [
        "models/vosk-model-small-en-us-0.15",
        "models/porcupine/jarvis.ppn"
    ]
    
    missing_models = []
    
    for model_path in required_models:
        if not os.path.exists(model_path):
            missing_models.append(model_path)
    
    if missing_models:
        logger.warning(f"[WARN] Missing model files:")
        logger.warning("   - Vosk model: Download from https://github.com/alphacep/vosk-models/releases")
        logger.warning("   - Porcupine model: Available in porcupine/ directory")
        return False
    
    logger.info("[OK] All model files found")
    return True

def check_configuration():
    """Check if configuration is set up"""
    logger.info("[*] Checking configuration...")
    
    if not os.path.exists(".env"):
        logger.warning("[WARN] .env file not found")
        logger.warning("   Creating .env from .env.example...")
        
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            logger.info("[OK] .env created. Please edit and add your Porcupine API key")
            return False
        else:
            logger.error("[ERR] .env.example not found")
            return False
    
    logger.info("[OK] Configuration file found")
    return True

def pre_launch_diagnostics():
    """Run pre-launch diagnostics"""
    logger.info("="*60)
    logger.info("JARVIS AYURVEDIC HEALTH ASSISTANT - PRE-LAUNCH CHECK")
    logger.info("="*60)
    
    checks = {
        "Dependencies": check_dependencies(),
        "Configuration": check_configuration(),
        "Models": check_models(),
    }
    
    logger.info("\nCheck Results:")
    for check_name, result in checks.items():
        status = "[PASS]" if result else "[FAIL]"
        logger.info(f"  {status} - {check_name}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        logger.info("\n[OK] All checks passed! Launching application...")
        return True
    else:
        logger.error("\n[ERR] Some checks failed. Please fix issues before launching.")
        logger.info("\nCommon fixes:")
        logger.info("  1. Install dependencies: pip install -r requirements_complete.txt")
        logger.info("  2. Copy .env.example to .env and add your API keys")
        logger.info("  3. Download models from provided links")
        logger.info("  4. Check internet connection for model downloads")
        return False

# ==================== LAUNCH APPLICATION ====================
def launch_ui():
    """Launch the main UI"""
    try:
        logger.info("[*] Launching UI...")
        from chat_ui_ayurveda import AyurvedicChatbot
        
        app = AyurvedicChatbot()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        logger.info("[OK] UI launched successfully")
        app.mainloop()
        
    except ImportError as e:
        logger.error(f"[ERR] UI import failed: {e}")
        logger.error("Make sure all UI dependencies are installed")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[ERR] UI launch failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def launch_web_ui():
    """Launch the React frontend and Flask API server."""
    frontend_dir = PROJECT_ROOT / "frontend"

    if not frontend_dir.exists():
        logger.warning("[WARN] React frontend not found. Falling back to desktop UI.")
        return launch_ui()

    npm_executable = shutil.which("npm")
    if not npm_executable:
        logger.warning("[WARN] npm not found. Falling back to desktop UI.")
        return launch_ui()

    try:
        logger.info("[*] Starting Flask API server on 127.0.0.1:5000...")
        from api_server import run_api_server

        api_thread = threading.Thread(
            target=run_api_server,
            kwargs={"host": "127.0.0.1", "port": 5000},
            daemon=True,
        )
        api_thread.start()

        time.sleep(1.5)

        logger.info("[*] Starting React frontend on 127.0.0.1:3000...")
        frontend_process = subprocess.Popen(
            [npm_executable, "run", "dev"],
            cwd=str(frontend_dir),
        )

        webbrowser.open("http://127.0.0.1:3000")
        logger.info("[OK] React UI launched successfully")

        try:
            frontend_process.wait()
        except KeyboardInterrupt:
            frontend_process.terminate()
            frontend_process.wait(timeout=10)

    except Exception as e:
        logger.error(f"[ERR] Web UI launch failed: {e}")
        logger.info("[WARN] Falling back to desktop UI.")
        launch_ui()

def launch_cli():
    """Launch CLI mode (fallback)"""
    logger.info("[*] Launching CLI mode...")
    
    try:
        from ai_brain_ayurveda import get_brain
        
        brain = get_brain()
        brain.update_status("Ready!")
        
        print("\n" + "="*60)
        print("JARVIS AYURVEDIC HEALTH ASSISTANT - CLI MODE")
        print("="*60)
        print("Commands:")
        print("  'quit' or 'exit' - Exit program")
        print("  'dosha' - Detect Dosha")
        print("  'diet DOSHA' - Get diet (vata/pitta/kapha)")
        print("  'plan DOSHA CONDITION' - Get wellness plan")
        print("="*60 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit"]:
                logger.info("[*] Goodbye!")
                break
            
            elif user_input.lower().startswith("dosha"):
                description = user_input[6:].strip() or input("Describe your constitution: ")
                dosha = brain.detect_dosha(description)
                print(brain.get_health_summary())
            
            elif user_input.lower().startswith("diet"):
                parts = user_input.split()
                dosha = parts[1] if len(parts) > 1 else "vata"
                print(brain.get_diet_recommendation(dosha))
            
            elif user_input.lower().startswith("plan"):
                parts = user_input.split()
                dosha = parts[1] if len(parts) > 1 else "vata"
                condition = parts[2] if len(parts) > 2 else "digestion"
                print(brain.create_wellness_plan(dosha, condition))
            
            else:
                response = brain.ask_ayurveda(user_input)
                print(f"Jarvis: {response}\n")
    
    except Exception as e:
        logger.error(f"[ERR] CLI failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point"""
    
    # Pre-launch checks
    if not pre_launch_diagnostics():
        sys.exit(1)
    
    # Try web UI first, fallback to desktop GUI, then CLI
    try:
        launch_web_ui()
    except Exception as e:
        logger.warning(f"[WARN] Web UI failed, falling back to CLI mode: {e}")
        try:
            launch_cli()
        except Exception as cli_error:
            logger.error(f"[ERR] Both UI and CLI failed: {cli_error}")
            sys.exit(1)

if __name__ == "__main__":
    main()
