# simple_rms_wake.py
import sounddevice as sd
import numpy as np
import queue
import time

Q = queue.Queue()
THRESHOLD = 500  # tune this value per mic; it's RMS of int16
SAMPLE_RATE = 16000
BLOCKSIZE = 1024

def audio_callback(indata, frames, time_info, status):
    Q.put(indata.copy())

def rms(arr):
    # arr dtype: int16 or float32 normalized; convert safely
    a = np.frombuffer(arr, dtype=np.int16)
    return np.sqrt(np.mean(a.astype(np.float64) ** 2))

with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCKSIZE, dtype='int16', channels=1, callback=audio_callback):
    print("Listening for energy...")
    buffer = bytearray()
    last_trigger = 0
    while True:
        data = Q.get()
        level = rms(data)
        if level > THRESHOLD and time.time() - last_trigger > 1.0:
            print("Potential speech detected, recording chunk...")
            # capture a short chunk (e.g., 2s) for keyword checking
            buffer.extend(data)
            # collect more frames to reach 2s
            target_frames = SAMPLE_RATE * 2
            frames_collected = len(buffer) // 2  # int16 => 2 bytes
            while frames_collected < target_frames:
                buffer.extend(Q.get())
                frames_collected = len(buffer) // 2
            # save to disk or feed to quick STT to check for wakeword
            with open("chunk.wav", "wb") as f:
                f.write(buffer)  # Note: you'd need WAV header; this is simplified
            print("Chunk saved; run keyword check with STT model.")
            buffer.clear()
            last_trigger = time.time()
