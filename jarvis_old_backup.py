from ai_brain import ask_ai
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import webbrowser
import time
import os
import numpy as np
import difflib
# ========================
# LIVE TRANSCRIPT CALLBACK (for GUI)
# ========================
live_text_callback = None

def set_live_text_callback(callback):
    global live_text_callback
    live_text_callback = callback


# ========================
# AUDIO DEVICE SETTINGS
# ========================
AUDIO_DEVICE = 1   # set None to use Windows default mic
TARGET_RATE = 16000

print("🎤 Available audio devices:")
print(sd.query_devices())
print(f"\n📍 Using audio device: {AUDIO_DEVICE if AUDIO_DEVICE is not None else 'Default'}\n")

# ========================
# TEXT TO SPEECH
# ========================
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

# ========================
# LOAD VOSK MODEL
# ========================
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

if not os.path.exists(MODEL_PATH):
    print("❌ VOSK model folder not found!")
    exit()

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, TARGET_RATE)
audio_queue = queue.Queue()

# ========================
# AUDIO CALLBACK
# ========================
def callback(indata, frames, time_info, status):
    if status:
        print("⚠️", status)
    audio_queue.put(bytes(indata))

def resample(buffer_bytes, in_rate):
    if in_rate == TARGET_RATE:
        return buffer_bytes
    data = np.frombuffer(buffer_bytes, dtype=np.int16)
    if data.size == 0:
        return buffer_bytes
    ratio = TARGET_RATE / float(in_rate)
    out_len = int(data.size * ratio)
    x_old = np.linspace(0, 1, data.size)
    x_new = np.linspace(0, 1, out_len)
    resampled = np.interp(x_new, x_old, data).astype(np.int16)
    return resampled.tobytes()

# ========================
# WINDOWS START MENU SCAN
# ========================
START_MENU_PATHS = [
    os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs"),
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
]

def find_installed_apps():
    apps = {}
    for base in START_MENU_PATHS:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().endswith(".lnk"):
                    name = file.replace(".lnk", "").lower()
                    apps[name] = os.path.join(root, file)
    return apps

INSTALLED_APPS = find_installed_apps()
print(f"📦 Detected {len(INSTALLED_APPS)} installed apps")

def open_app_by_voice(app_name):
    app_name = app_name.lower()

    matches = difflib.get_close_matches(
        app_name,
        INSTALLED_APPS.keys(),
        n=1,
        cutoff=0.6
    )

    if not matches:
        speak(f"I could not find {app_name}")
        return

    app = matches[0]
    try:
        os.startfile(INSTALLED_APPS[app])
        speak(f"Opening {app}")
    except Exception as e:
        print(e)
        speak("Failed to open the application")

# ========================
# COMMAND HANDLER
# ========================
def handle_command(text):
    text = text.lower().strip()

    if live_text_callback:
        live_text_callback("", final=True)


    # ----------------
    # OPEN ANY APP BY VOICE
    # ----------------
    if text.startswith("open "):
        app_name = text.replace("open", "").strip()
        open_app_by_voice(app_name)
        return

    # ----------------
    # BASIC COMMANDS
    # ----------------
    if "browser" in text:
        speak("Opening browser.")
        webbrowser.open("https://www.google.com")
        return

    if "time" in text:
        speak("The time is " + time.strftime("%I:%M %p"))
        return

    if "note" in text:
        with open("notes.txt", "a") as f:
            f.write(text + "\n")
        speak("Note saved.")
        return

    if "exit" in text or "quit" in text:
        speak("Shutting down. Goodbye.")
        exit()

    # ----------------
    # AI FALLBACK
    # ----------------
    speak("Thinking...")
    try:
        answer = ask_ai(text)
        speak(answer)
    except Exception as e:
        print("AI error:", e)
        speak("Sorry, I could not think right now.")

# ========================
# LISTEN ONCE
# ========================
def listen_once():
    chosen = AUDIO_DEVICE if AUDIO_DEVICE is not None else sd.default.device[0]
    info = sd.query_devices(chosen, "input")
    in_rate = int(info["default_samplerate"])

    with sd.RawInputStream(
        samplerate=in_rate,
        blocksize=8000,
        dtype="int16",
        channels=1,
        device=chosen,
        callback=callback,
    ):
        while True:
            data = audio_queue.get()
            audio = resample(data, in_rate)

            if recognizer.AcceptWaveform(audio):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if text:
                    if live_text_callback:
                        live_text_callback(text, final=True)

                    print("✨ You:", text)
                    handle_command(text)
                    break
            else:
                try:
                    partial_json = recognizer.PartialResult()
                    partial = json.loads(partial_json).get("partial", "")
                    if partial and live_text_callback:
                        live_text_callback(partial, final=False)
                except json.JSONDecodeError:
                    pass

# ========================
# HOTWORD LOOP
# ========================
from hotword import HotwordDetector

KEYWORD_FILE = "models/porcupine/jarvis.ppn"
detector = HotwordDetector(KEYWORD_FILE)

def run_jarvis_hotword():
    speak("Jarvis is ready. Say Hey Jarvis.")
    while True:
        print("🎙 Waiting for hotword...")
        detector.listen()
        speak("Yes sir. I am listening.")
        listen_once()


if __name__ == "__main__":
    run_jarvis_hotword()

    speak("Yes sir. I am listening.")
    listen_once()
def run_jarvis_once():
    listen_once()
