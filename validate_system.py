#!/usr/bin/env python3
"""
Jarvis Complete System Validation & Testing Suite
Tests all components before deployment
"""

import json
import logging
import os
import sys
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

# ==================== VALIDATION SUITE ====================
class JarvisValidator:
    """Complete validation of Jarvis system"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_skipped = 0
        self.results = []
    
    def log_test(self, name: str, status: str, message: str = ""):
        """Log test result"""
        status_icon = {
            "PASS": "✅",
            "FAIL": "❌",
            "SKIP": "⏭️"
        }.get(status, "❓")
        
        self.results.append({
            "name": name,
            "status": status,
            "message": message
        })
        
        if status == "PASS":
            self.tests_passed += 1
        elif status == "FAIL":
            self.tests_failed += 1
        else:
            self.tests_skipped += 1
        
        print(f"{status_icon} {name}")
        if message:
            print(f"   → {message}")
    
    # ==================== DEPENDENCY TESTS ====================
    def test_python_version(self):
        """Test Python version"""
        version = sys.version_info
        required = (3, 9)
        
        if version >= required:
            self.log_test("Python Version", "PASS", f"{version.major}.{version.minor}.{version.micro}")
        else:
            self.log_test("Python Version", "FAIL", f"Need {required[0]}.{required[1]}+, have {version.major}.{version.minor}")
    
    def test_imports(self):
        """Test core imports"""
        imports = {
            "transformers": "Hugging Face transformers",
            "torch": "PyTorch",
            "peft": "PEFT LoRA",
            "vosk": "Vosk STT",
            "pvporcupine": "Porcupine hotword",
            "sounddevice": "Sound device I/O",
            "dotenv": "Environment config"
        }
        
        for package, name in imports.items():
            try:
                __import__(package)
                self.log_test(f"Import {name}", "PASS")
            except ImportError as e:
                self.log_test(f"Import {name}", "FAIL", str(e))
    
    # ==================== FILE & MODEL TESTS ====================
    def test_files(self):
        """Test required files exist"""
        required_files = {
            "config.py": "Configuration module",
            "ai_brain_ayurveda.py": "AI brain module",
            "chat_ui_ayurveda.py": "Chat UI module",
            "voice_input_improved.py": "Voice input module",
            "hotword_secure.py": "Hotword module",
            "error_handler.py": "Error handler module",
            ".env": "Environment file"
        }
        
        for filename, description in required_files.items():
            filepath = Path(filename)
            if filepath.exists():
                self.log_test(f"File {description}", "PASS", str(filepath.stat().st_size) + " bytes")
            else:
                if filename == ".env":
                    self.log_test(f"File {description}", "SKIP", "Create from .env.example")
                else:
                    self.log_test(f"File {description}", "FAIL", f"Not found: {filepath}")
    
    def test_models(self):
        """Test model files"""
        models = {
            "models/vosk-model-small-en-us-0.15/": "Vosk STT model",
            "models/porcupine/jarvis.ppn": "Porcupine hotword model",
            "data/ayurveda_qa.jsonl": "Ayurveda training data"
        }
        
        for path, description in models.items():
            if os.path.exists(path):
                self.log_test(f"Model {description}", "PASS")
            else:
                self.log_test(f"Model {description}", "SKIP", f"Not found: {path}")
    
    # ==================== CONFIGURATION TESTS ====================
    def test_configuration(self):
        """Test configuration loading"""
        try:
            import config
            self.log_test("Configuration loading", "PASS")
            
            # Check critical config values
            if config.PORCUPINE_ACCESS_KEY and config.PORCUPINE_ACCESS_KEY != "":
                self.log_test("Porcupine API key configured", "PASS")
            else:
                self.log_test("Porcupine API key", "SKIP", "Add to .env for hotword")
            
            self.log_test("Device selection", "PASS", config.DEVICE_NAME)
            self.log_test("Base model", "PASS", config.BASE_MODEL)
        
        except Exception as e:
            self.log_test("Configuration loading", "FAIL", str(e))
    
    # ==================== AI BRAIN TESTS ====================
    def test_ai_brain_loading(self):
        """Test AI brain initialization"""
        try:
            print("\\n  (This may take 1-2 minutes on first run...)")
            from ai_brain_ayurveda import AyurvedicBrain
            
            brain = AyurvedicBrain()
            self.log_test("AI brain initialization", "PASS")
            
            # Test Dosha detection
            dosha = brain.detect_dosha("I am thin and creative")
            if dosha:
                self.log_test("Dosha detection", "PASS", f"Detected: {dosha}")
            else:
                self.log_test("Dosha detection", "SKIP", "Insufficient description")
            
            # Test response generation
            response = brain.ask_ayurveda("What is Vata?")
            if response and len(response) > 10:
                self.log_test("Response generation", "PASS", f"{len(response)} characters")
            else:
                self.log_test("Response generation", "FAIL", "Empty response")
        
        except Exception as e:
            self.log_test("AI brain initialization", "FAIL", str(e))
    
    # ==================== VOICE INPUT TESTS ====================
    def test_voice_engine(self):
        """Test voice input engine"""
        try:
            from voice_input_improved import VoskSTTEngine
            engine = VoskSTTEngine()
            self.log_test("Vosk STT engine", "PASS")
            engine.cleanup()
        except FileNotFoundError:
            self.log_test("Vosk STT engine", "SKIP", "Model not found")
        except Exception as e:
            self.log_test("Vosk STT engine", "FAIL", str(e))
    
    # ==================== HOTWORD TESTS ====================
    def test_hotword_detector(self):
        """Test hotword detection"""
        try:
            from hotword_secure import HotwordDetector
            detector = HotwordDetector()
            self.log_test("Hotword detector", "PASS")
            detector.cleanup()
        except ValueError as e:
            if "Porcupine access key" in str(e):
                self.log_test("Hotword detector", "SKIP", "API key not configured")
            else:
                self.log_test("Hotword detector", "FAIL", str(e))
        except Exception as e:
            self.log_test("Hotword detector", "FAIL", str(e))
    
    # ==================== AUDIO DEVICE TESTS ====================
    def test_audio_devices(self):
        """Test audio device availability"""
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if input_devices:
                default_input = sd.default.device[0]
                self.log_test("Audio input devices", "PASS", f"{len(input_devices)} device(s) found")
                self.log_test("Default input device", "PASS", devices[default_input]['name'])
            else:
                self.log_test("Audio input devices", "FAIL", "No input devices found")
        
        except Exception as e:
            self.log_test("Audio device check", "FAIL", str(e))
    
    # ==================== GPU TESTS ====================
    def test_gpu(self):
        """Test GPU availability"""
        try:
            import torch
            
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                vram = torch.cuda.get_device_properties(0).total_memory / 1e9
                self.log_test("GPU availability", "PASS", f"{gpu_name} ({vram:.1f}GB VRAM)")
            else:
                self.log_test("GPU availability", "SKIP", "No CUDA device, using CPU")
        
        except Exception as e:
            self.log_test("GPU check", "FAIL", str(e))
    
    # ==================== DATA TESTS ====================
    def test_training_data(self):
        """Test training data"""
        try:
            with open("data/ayurveda_qa.jsonl", "r", encoding="utf-8") as f:
                lines = f.readlines()
                count = len(lines)
            
            if count > 0:
                self.log_test("Training data", "PASS", f"{count} Q&A pairs")
            else:
                self.log_test("Training data", "FAIL", "Empty training file")
        
        except FileNotFoundError:
            self.log_test("Training data", "SKIP", "ayurveda_qa.jsonl not found")
        except Exception as e:
            self.log_test("Training data", "FAIL", str(e))
    
    # ==================== UI TESTS ====================
    def test_ui_components(self):
        """Test UI components"""
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            self.log_test("Tkinter UI", "PASS")
            root.destroy()
        except Exception as e:
            self.log_test("Tkinter UI", "FAIL", str(e))
    
    # ==================== RUN ALL TESTS ====================
    def run_all_tests(self):
        """Run complete validation suite"""
        print("\\n" + "="*70)
        print("🧪 JARVIS SYSTEM VALIDATION SUITE")
        print("="*70 + "\\n")
        
        print("📋 System & Dependencies")
        print("-" * 70)
        self.test_python_version()
        self.test_imports()
        self.test_gpu()
        
        print("\\n📁 Files & Models")
        print("-" * 70)
        self.test_files()
        self.test_models()
        self.test_training_data()
        
        print("\\n⚙️  Configuration")
        print("-" * 70)
        self.test_configuration()
        
        print("\\n🎤 Audio & Input")
        print("-" * 70)
        self.test_audio_devices()
        self.test_hotword_detector()
        self.test_voice_engine()
        
        print("\\n🧠 AI Components")
        print("-" * 70)
        self.test_ai_brain_loading()
        
        print("\\n🎨 UI Components")
        print("-" * 70)
        self.test_ui_components()
        
        # Summary
        print("\\n" + "="*70)
        print(f"📊 VALIDATION RESULTS")
        print("="*70)
        print(f"✅ Passed:  {self.tests_passed}")
        print(f"❌ Failed:  {self.tests_failed}")
        print(f"⏭️  Skipped: {self.tests_skipped}")
        print(f"📈 Total:   {self.tests_passed + self.tests_failed + self.tests_skipped}")
        
        if self.tests_failed == 0:
            print("\\n✅ All critical tests passed! System ready to launch.")
            return True
        else:
            print(f"\\n⚠️  {self.tests_failed} critical test(s) failed. Please fix before launching.")
            return False

# ==================== MAIN ====================
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    validator = JarvisValidator()
    success = validator.run_all_tests()
    
    # Save results
    with open("validation_results.json", "w") as f:
        json.dump({
            "passed": validator.tests_passed,
            "failed": validator.tests_failed,
            "skipped": validator.tests_skipped,
            "results": validator.results
        }, f, indent=2)
    
    print(f"\\n📄 Results saved to validation_results.json")
    
    sys.exit(0 if success else 1)
