import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import os
import time

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("VOSK model not found")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
audio_q = queue.Queue()

def callback(indata, frames, time_info, status):
    audio_q.put(bytes(indata))

def listen_live(on_partial, timeout=8):
    """
    Live speech-to-text.
    on_partial(text) is called continuously.
    Returns final text.
    """
    final_text = ""
    last_audio_time = time.time()

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            data = audio_q.get()
            last_audio_time = time.time()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                final_text = result.get("text", "")
                break
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "")
                if partial:
                    on_partial(partial)

            if time.time() - last_audio_time > timeout:
                break

    return final_text
