#!/usr/bin/env python3
"""
Jarvis Requirements Verification Script
Checks if all dependencies are properly installed
"""

import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    required = (3, 9)
    
    if version >= required:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (need {required[0]}.{required[1]}+)")
        return False

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip available")
        return True
    except:
        print("❌ pip not available")
        return False

def check_packages():
    """Check if required packages are installed"""
    packages = {
        "transformers": "Hugging Face Transformers",
        "torch": "PyTorch",
        "peft": "PEFT",
        "trl": "TRL",
        "datasets": "Datasets",
        "vosk": "Vosk",
        "pvporcupine": "Porcupine",
        "sounddevice": "SoundDevice",
        "dotenv": "python-dotenv",
        "numpy": "NumPy",
        "PIL": "Pillow"
    }
    
    results = {}
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
            results[package] = True
        except ImportError:
            print(f"❌ {name} (run: pip install {package})")
            results[package] = False
    
    return all(results.values())

def check_models():
    """Check if model files exist"""
    models = {
        "models/vosk-model-small-en-us-0.15/": "Vosk STT model",
        "models/porcupine/jarvis.ppn": "Porcupine hotword"
    }
    
    results = {}
    for path, name in models.items():
        if Path(path).exists():
            print(f"✅ {name}")
            results[path] = True
        else:
            print(f"⚠️  {name} (optional)")
            results[path] = False
    
    return True  # Not critical

def check_config():
    """Check if configuration exists"""
    if Path(".env").exists():
        print("✅ .env configuration file")
        return True
    else:
        print("⚠️  .env file missing (create from .env.example)")
        return False

def main():
    """Run all checks"""
    print("🧪 JARVIS REQUIREMENTS CHECK")
    print("=" * 50)
    
    checks = {
        "Python Version": check_python_version(),
        "pip": check_pip(),
    }
    
    if not checks["pip"]:
        print("\n❌ pip is required. Cannot continue.")
        return False
    
    print("\n📦 PYTHON PACKAGES")
    print("-" * 50)
    checks["Packages"] = check_packages()
    
    print("\n📁 MODEL FILES")
    print("-" * 50)
    check_models()
    
    print("\n⚙️  CONFIGURATION")
    print("-" * 50)
    check_config()
    
    print("\n" + "=" * 50)
    
    if checks["Python Version"] and checks["Packages"]:
        print("✅ All critical requirements met!")
        print("\n👉 Next: python run_jarvis_improved.py")
        return True
    else:
        print("❌ Some requirements are missing")
        print("\n👉 Install packages: pip install -r requirements_complete.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
