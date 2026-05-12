import os
import struct

import pvporcupine
import sounddevice as sd


# Set to an input device index from sd.query_devices(), or None to use default
# Use a real input device (DirectSound mic). Set to None to use default input.
AUDIO_DEVICE = 1


class HotwordDetector:
    def __init__(self, keyword_path):
        if not os.path.exists(keyword_path):
            raise FileNotFoundError(f"Keyword file not found: {keyword_path}")

        self.porcupine = pvporcupine.create(
            access_key="vSvR/XwiBi64C7nNAkKkHu4Fjm9YDRtCyQtkWptPDZZVqGS2AOSU8w==",
            keyword_paths=[keyword_path],
        )

        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length

    def listen(self):
        print("🎙 Say 'Hey Jarvis' to activate...")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_length,
            dtype="int16",
            channels=1,
            device=AUDIO_DEVICE,
        ) as stream:
            while True:
                data = stream.read(self.frame_length)[0]
                pcm = struct.unpack_from("h" * self.frame_length, data)

                result = self.porcupine.process(pcm)
                if result >= 0:
                    print("🔥 Hotword Detected!")
                    return True


# -------------------------
# TEST MODE: RUN DIRECTLY
# -------------------------
if __name__ == "__main__":
    KEYWORD_FILE = "models/porcupine/jarvis.ppn"

    detector = HotwordDetector(KEYWORD_FILE)
    detector.listen()

