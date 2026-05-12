# 🚀 JARVIS STARTUP GUIDE - QUICK START

## ⚡ 3-Minute Setup (Windows)

### Step 1: One-Click Launch
1. Navigate to `e:\Jarvis\`
2. Double-click **`START_JARVIS.bat`**
3. Wait for dependencies to install (first time only, 5-10 minutes)
4. Application launches automatically

That's it! 🎉

---

## 🐧 3-Minute Setup (Mac/Linux)

### Step 1: Make script executable
```bash
cd e/Jarvis
chmod +x start_jarvis.sh
```

### Step 2: Run
```bash
./start_jarvis.sh
```

First run installs dependencies, then launches.

---

## 📋 Manual Setup (if automated fails)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements_complete.txt
```

### Step 3: Setup Configuration
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### Step 4: Edit `.env` file
Add your Porcupine API key:
```
PORCUPINE_ACCESS_KEY=your_key_here
```

Get free key from: https://picovoice.ai/console/

### Step 5: Run Validation
```bash
python validate_system.py
```

### Step 6: Launch
```bash
python run_jarvis_improved.py
```

---

## 🔧 What Gets Installed

First run automatically installs:

| Component | Size | Purpose |
|-----------|------|---------|
| PyTorch | ~2GB | Deep learning framework |
| Transformers | ~500MB | Model loading |
| TinyLlama Model | ~1GB | AI model |
| Vosk Model | ~1GB | Speech recognition |
| Other deps | ~500MB | Various utilities |
| **Total** | **~5GB** | **Full system** |

---

## ✅ First Time Checklist

After launching, verify these work:

- [ ] **Chat UI opens** - Tkinter window appears
- [ ] **AI responds** - Type something in chat, get response in 5-10 seconds
- [ ] **Voice works** - Click 🎤 button, speak into mic
- [ ] **Hotword works** - Click 🔥 button, say "Hey Jarvis"
- [ ] **Dosha detected** - Go to Health Profile, describe yourself, click Detect
- [ ] **Diet shown** - Go to Diet Plans, click a Dosha
- [ ] **Settings load** - Go to Settings, click "Check Health"

All green? Perfect! Ready to use. ✨

---

## ⏱️ First Launch Timing

| Task | Time |
|------|------|
| Install dependencies | 5-10 min (first run only) |
| Download models | Included |
| Load AI brain | 1-2 min |
| Load Vosk | 10 sec |
| Load Porcupine | 5 sec |
| **Total** | **~10 min first run** |

Subsequent launches: **~30 seconds**

---

## 🎯 Common First-Time Issues

### Issue: "PORCUPINE_ACCESS_KEY not set"
✅ **Fix**: 
1. Go to https://picovoice.ai/console/
2. Sign up (free)
3. Copy your access key
4. Edit `.env` file
5. Set: `PORCUPINE_ACCESS_KEY=your_key`
6. Restart app

### Issue: "Vosk model not found"
✅ **Fix**:
1. Download: https://github.com/alphacep/vosk-models/releases/download/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15.zip
2. Extract to: `e:\Jarvis\models\vosk-model-small-en-us-0.15\`
3. Restart app

### Issue: Slow AI responses
✅ **Fix**:
1. Edit `.env` file
2. Set `USE_GPU=false` temporarily to test CPU
3. Or wait 1-2 minutes for GPU to warm up
4. First response is always slow (model loading)

### Issue: Microphone not working
✅ **Fix**:
1. Check Windows/Mac/Linux microphone permissions
2. Test microphone in system settings
3. Edit `.env` file
4. Set `AUDIO_DEVICE_INDEX=-1` (auto-detect)
5. Or run: `python -c "import sounddevice as sd; sd.query_devices()"` to find device index

### Issue: "Python not found"
✅ **Fix**:
1. Install Python 3.9+ from python.org
2. Check "Add Python to PATH" during install
3. Restart terminal/cmd
4. Try again

---

## 📊 First-Time Performance Expectations

### Chat Response Time
- **First response**: 30-120 seconds (model loading)
- **Subsequent**: 5-10 seconds (GPU) or 20-30 seconds (CPU)

### Voice Input
- **Listening**: 8-10 seconds max
- **Recognition**: 2-5 seconds
- **Total**: 10-15 seconds

### Hotword Detection
- **Detection time**: 1-30 seconds (always listening)
- **Response**: Same as voice

### Dosha Detection
- **Processing**: < 1 second

### Diet/Wellness Plans
- **Display**: < 1 second

---

## 🎮 First Chat Session

### Try these questions:

1. **Simple intro**
   - Q: "What is Ayurveda?"
   - ✅ Should get Ayurvedic explanation

2. **Dosha question**
   - Q: "What are the three Doshas?"
   - ✅ Should explain Vata, Pitta, Kapha

3. **Diet question**
   - Q: "What should a Vata person eat?"
   - ✅ Should get diet recommendations

4. **Dosha detection**
   - Go to Health Profile
   - Describe: "I am thin, creative, and anxious"
   - Click "Detect Dosha"
   - ✅ Should show Vata profile

5. **Wellness plan**
   - Go to Wellness Plans
   - Select: Vata + Digestion
   - Click "Get Plan"
   - ✅ Should show plan

If these work, you're all set! 🎉

---

## 🚨 Emergency Fixes

### If app crashes:
1. Check `jarvis.log` for error
2. Close application
3. Run `python validate_system.py`
4. Fix any reported issues
5. Restart

### If stuck on "Initializing":
1. Check internet connection
2. Try again with `USE_GPU=false` in `.env`
3. Check Windows Defender/firewall allowing Python
4. Restart computer

### If no sound:
1. Check volume settings
2. Check microphone permissions
3. Try different audio device: `AUDIO_DEVICE_INDEX=X` (0, 1, 2, etc.)
4. Test: `python -c "import sounddevice as sd; sd.rec(1000, 16000)"`

---

## 🎬 Next Steps

### After successful launch:

1. **Explore Features**
   - Try all chat tabs
   - Detect your Dosha
   - Get diet plan
   - Get wellness plan

2. **Customize (Optional)**
   - Edit `.env` for preferences
   - Add more training data to `data/ayurveda_qa.jsonl`
   - Retrain: `python train_ayurveda_lora.py`

3. **For Startup Deployment**
   - Package as executable: Use PyInstaller
   - Deploy to cloud: Use Docker
   - Share with users: Send whole folder

---

## 📞 Help Resources

| Issue | Resource |
|-------|----------|
| Porcupine key | https://picovoice.ai/console/ |
| Vosk models | https://github.com/alphacep/vosk-models/releases |
| Python install | https://www.python.org/downloads/ |
| PyTorch GPU | https://pytorch.org/get-started/locally/ |
| Troubleshooting | See README_AYURVEDA.md |

---

## ✨ Success Indicators

You'll know everything works when:

- ✅ App window opens with 🌿 logo
- ✅ Status shows "Ready! 🟢"
- ✅ Chat responds to messages (in 5-30 seconds)
- ✅ Voice input recognizes speech
- ✅ Hotword detects "Hey Jarvis"
- ✅ Dosha detection identifies your type
- ✅ Diet plan displays recommendations
- ✅ No red error messages in console

---

**🎉 Congratulations! Your Ayurvedic Chatbot is ready for your startup! 🚀**

For production deployment, see **DEPLOYMENT_GUIDE.md**

---

Made with ❤️ for holistic health

*"Health is the greatest of all goods" - Ancient Ayurvedic Saying*
