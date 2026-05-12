# 🌿 Jarvis - Ayurvedic Health Assistant Chatbot

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)

A production-ready, **offline** Ayurveda-focused chatbot with voice input, Dosha detection, and personalized diet/wellness recommendations.

## 🎯 Features

### Core Capabilities
- ✅ **Ayurveda-Only Knowledge**: Trained specifically to answer ONLY Ayurvedic questions (Vata, Pitta, Kapha Doshas)
- ✅ **Offline & Private**: Runs completely offline - no data sent to cloud
- ✅ **Dosha Detection**: Identifies user's constitution and provides personalized guidance
- ✅ **Diet Recommendations**: Dosha-specific meal plans and food lists
- ✅ **Wellness Plans**: Personalized treatment plans for digestion, sleep, stress management
- ✅ **Voice Input**: Hotword detection ("Hey Jarvis") + speech-to-text
- ✅ **GPU Support**: Accelerated inference on NVIDIA GPUs, fallback to CPU
- ✅ **Error Handling**: Comprehensive error detection and user-friendly messages
- ✅ **Session Management**: Saves chat history and health profiles

### Technical Stack
- **Model**: TinyLlama-1.1B (lightweight, runs on CPU/GPU)
- **Fine-tuning**: LoRA (Low-Rank Adaptation) with 44+ Ayurveda examples
- **Voice**: Vosk (offline STT) + Porcupine (hotword detection)
- **UI**: Tkinter (cross-platform, no dependencies)
- **Logging**: Structured logging with file and console output

## 📋 Requirements

### System Requirements
- **Python**: 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended for GPU)
- **GPU** (optional): NVIDIA GPU with CUDA support for faster inference
- **Microphone**: For voice input
- **Storage**: ~5GB (includes models)

### Installation

#### 1. Clone/Download Project
```bash
cd e:\Jarvis
```

#### 2. Create Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements_complete.txt
```

#### 4. Download Models (if not already present)

**Vosk Speech-to-Text Model**:
```bash
# Download and extract to: models/vosk-model-small-en-us-0.15/
# Get from: https://github.com/alphacep/vosk-models/releases/download/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15.zip
```

**Porcupine Hotword Model**:
- Already included in `models/porcupine/jarvis.ppn` (no download needed)

#### 5. Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows
```

Edit `.env` and add your API keys:
```env
# Get free key from: https://picovoice.ai/console/
PORCUPINE_ACCESS_KEY=your_key_here

# Optional: HuggingFace token for private models
HUGGINGFACE_TOKEN=

# GPU support
USE_GPU=true
```

#### 6. (Optional) Train Model on Ayurveda Data

```bash
python train_ayurveda_lora.py
```

This fine-tunes the model on Ayurvedic knowledge (44 example Q&As). Takes 5-10 minutes on GPU, 30+ on CPU.

## 🚀 Running the Application

### Main UI (Recommended)
```bash
python run_jarvis_improved.py
```

Features:
- 💬 **Chat Tab**: Talk to Jarvis about Ayurveda
- 👤 **Health Profile**: Detect your Dosha
- 🍽️ **Diet Plans**: Dosha-specific meal recommendations
- ⚕️ **Wellness Plans**: Treatment plans for specific conditions
- ⚙️ **Settings**: System health check and configuration

### CLI Mode (Fallback)
```bash
python run_jarvis_improved.py
```
(If UI fails, automatically falls back to CLI)

## 🎮 Usage Guide

### 1. First Time Setup - Detect Your Dosha

1. Go to **Health Profile** tab
2. Describe your constitution:
   - Vata: "I am thin, creative, anxious, get cold easily"
   - Pitta: "I am ambitious, sharp-minded, have oily skin"
   - Kapha: "I am calm, stable, tend to gain weight easily"
3. Click **Detect Dosha**
4. Review your health profile

### 2. Get Diet Recommendations

1. Go to **Diet Plans** tab
2. Click button for your Dosha (Vata/Pitta/Kapha)
3. Read specific foods to include/avoid
4. Follow the recommendations

### 3. Get Wellness Plans

1. Go to **Wellness Plans** tab
2. Select your Dosha and condition (Digestion/Sleep/Stress)
3. Click **Get Plan**
4. Follow the personalized recommendations

### 4. Chat with Jarvis

1. Go to **Chat** tab
2. Type your question (e.g., "What herbs help balance Pitta?")
3. Press Ctrl+Enter or click **Send**
4. Or use 🎤 **Voice** button for speech input
5. Or use 🔥 **Hotword** button to activate with "Hey Jarvis"

## 🔧 Configuration

Edit `.env` file to customize:

```env
# AI Model
USE_GPU=true                          # Use GPU if available
MODEL_TEMPERATURE=0.3                 # 0.0=deterministic, 1.0=creative
MODEL_MAX_TOKENS=256                  # Response length

# Audio
AUDIO_DEVICE_INDEX=-1                 # -1 for auto-detect
STT_TIMEOUT=10                        # Listening timeout in seconds

# Features
ENABLE_HOTWORD=true                   # Enable hotword detection
ENABLE_TTS=true                       # Enable text-to-speech

# Training (if you train your own model)
TRAINING_EPOCHS=3                     # Number of training epochs
TRAINING_BATCH_SIZE=2                 # Batch size
TRAINING_LR=2e-4                      # Learning rate
```

## 🐛 Troubleshooting

### Issue: "PORCUPINE_ACCESS_KEY not set"
**Solution**: 
1. Get free key from https://picovoice.ai/console/
2. Add to `.env` file: `PORCUPINE_ACCESS_KEY=your_key_here`

### Issue: "Vosk model not found"
**Solution**:
1. Download from: https://github.com/alphacep/vosk-models/releases/download/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15.zip
2. Extract to: `models/vosk-model-small-en-us-0.15/`

### Issue: "CUDA out of memory"
**Solution**:
1. Set `USE_GPU=false` in `.env` to use CPU
2. Or reduce `MODEL_MAX_TOKENS` to reduce memory usage
3. Or close other applications to free up GPU memory

### Issue: Microphone not detected
**Solution**:
1. Check system microphone settings
2. Set `AUDIO_DEVICE_INDEX=-1` in `.env` for auto-detection
3. Or list devices: `python -c "import sounddevice as sd; sd.query_devices()"`
4. Then set `AUDIO_DEVICE_INDEX=X` where X is device number

### Issue: Voice input not working
**Solution**:
1. Check microphone is connected and working
2. Check microphone permissions in system settings
3. Test with: `python test_microphone.py` (if available)
4. Check STT timeout in `.env` - increase if needed

### Issue: Slow response time
**Solution**:
1. First response is slow (model loading) - this is normal
2. Subsequent responses are faster
3. Use GPU for ~10x speedup: `USE_GPU=true`
4. Reduce `MODEL_MAX_TOKENS` for faster generation

### Issue: Getting non-Ayurveda responses
**Solution**:
1. Ensure model is trained on Ayurveda data: `python train_ayurveda_lora.py`
2. Check system prompt in `ai_brain_ayurveda.py`
3. Be explicit in your questions: "According to Ayurveda, what herbs help..."

## 📊 System Health Check

In **Settings** tab, click **Check Health** to verify:
- ✅ GPU availability
- ✅ Model loading
- ✅ Voice input ready
- ✅ Hotword detector ready

## 📁 Project Structure

```
e:\Jarvis/
├── config.py                          # Configuration management
├── ai_brain_ayurveda.py              # AI model with Dosha detection
├── chat_ui_ayurveda.py               # Main GUI
├── voice_input_improved.py           # Speech-to-text engine
├── hotword_secure.py                 # Hotword detection
├── error_handler.py                  # Error handling utilities
├── train_ayurveda_lora.py            # LoRA training pipeline
├── run_jarvis_improved.py            # Main launcher
├── .env                               # Configuration (create from .env.example)
├── .env.example                       # Configuration template
├── requirements_complete.txt          # Python dependencies
├── data/
│   └── ayurveda_qa.jsonl            # Training data (44 Q&As)
├── models/
│   ├── medical-lora/                 # Trained LoRA adapter
│   ├── vosk-model-small-en-us-0.15/  # Speech recognition model
│   └── porcupine/
│       └── jarvis.ppn                # Hotword model
├── outputs/
│   └── medical-lora-checkpoints/     # Training checkpoints
├── sessions/                          # Saved chat sessions
└── jarvis.log                         # Application log
```

## 🚀 Deployment for Startup

### Build Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Jarvis" run_jarvis_improved.py
```

Executable will be in `dist/` folder.

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements_complete.txt
CMD ["python", "run_jarvis_improved.py"]
```

### Cloud Deployment (AWS/GCP/Azure)
1. Use GPU instances for faster inference
2. Mount models from S3/Cloud Storage
3. Use REST API wrapper for web access
4. Example: Flask/FastAPI wrapper around `ai_brain_ayurveda.py`

## 🎓 Training Custom Models

### Add More Ayurveda Training Data

Edit `data/ayurveda_qa.jsonl`:
```jsonl
{"question": "Your question", "answer": "Your answer"}
```

Then retrain:
```bash
python train_ayurveda_lora.py
```

### Recommended Data Addition
- Add 5-10 more Q&A pairs per Dosha
- Focus on: herbs, diet, diseases, lifestyle recommendations
- Use consistent terminology (Vata, Pitta, Kapha)

## 📝 Logging

Logs are saved to `jarvis.log` and console output.

Change log level in `.env`:
```env
LOG_LEVEL=DEBUG    # For debugging
LOG_LEVEL=INFO     # Normal operation
LOG_LEVEL=WARNING  # Only warnings/errors
```

## 🔐 Security & Privacy

- ✅ **Offline Operation**: No internet required, all processing local
- ✅ **API Key Protection**: Never hardcoded, loaded from `.env`
- ✅ **No Data Collection**: Sessions saved locally only
- ✅ **Open Source**: Full code transparency

## 🤝 Contributing

Found a bug or have an improvement?

1. Create an issue with detailed description
2. Submit pull request with fixes
3. Add more Ayurveda Q&A data
4. Improve accuracy with better training data

## 📄 License

Licensed under MIT - See [LICENSE.txt](LICENSE.txt)

## 🙏 Acknowledgments

- **TinyLlama**: Efficient language model
- **Vosk**: Offline speech recognition
- **Porcupine**: Hotword detection
- **PEFT**: Parameter-efficient fine-tuning
- **Ayurveda**: Ancient wisdom

## 📞 Support

Issues? Questions? Check:
1. Troubleshooting section above
2. `jarvis.log` file for error details
3. GitHub Issues (if available)
4. Verify .env configuration

## 🎯 Roadmap

Future improvements:
- [ ] Multiple language support
- [ ] Database backend for history
- [ ] REST API for web/mobile
- [ ] Enhanced Dosha-specific responses
- [ ] Integration with smart home devices
- [ ] Medicine interaction checker
- [ ] Prescription parser
- [ ] Cloud-based model serving

---

**Made with ❤️ for holistic health and Ayurvedic wellness**

🌿 *"Health is the greatest of all goods" - Ancient Ayurvedic Saying*
