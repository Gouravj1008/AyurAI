# stt_vosk.py
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import logging

logger = logging.getLogger("stt_vosk")

class VoskSTT:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15", device=None, samplerate=16000):
        self.q = queue.Queue()
        self.model_path = model_path
        self.samplerate = samplerate
        self.device = device
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, samplerate)
        self.stream = None

    def _audio_callback(self, indata, frames, time_info, status):
        """
        This callback is called by sounddevice for each audio block.
        We place raw bytes into a queue for processing.
        """
        if status:
            logger.debug(f"Sounddevice status: {status}")
        # send bytes to queue
        self.q.put(bytes(indata))

    def recognize_stream(self):
        """
        Generator that yields recognized text (strings). Run this in a background thread.
        """
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16',
                               channels=1, callback=self._audio_callback, device=self.device):
            logger.info("VOSK listening (press Ctrl+C to stop)")
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    res = json.loads(self.rec.Result())
                    text = res.get("text", "")
                    if text:
                        yield text
                else:
                    # partial result can be used for live display if desired
                    # partial = json.loads(self.rec.PartialResult())["partial"]
                    pass
