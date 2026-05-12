"""
Secure Hotword Detection - Jarvis
Loads Porcupine access key from config instead of hardcoding
Auto-detects audio device
"""

import logging
import struct

import pvporcupine
import sounddevice as sd

import config

logger = logging.getLogger(__name__)

# ==================== AUDIO DEVICE AUTO-DETECTION ====================
def auto_detect_microphone():
    """Automatically detect best microphone device"""
    try:
        devices = sd.query_devices()
        
        # Prefer devices with "Microphone" in name
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                if 'microphone' in device['name'].lower() or 'mic' in device['name'].lower():
                    logger.info(f"✅ Auto-detected microphone: {device['name']} (Device {i})")
                    return i
        
        # Fallback: first input device
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                logger.info(f"✅ Using input device: {device['name']} (Device {i})")
                return i
        
        logger.warning("⚠️  No input devices found, using default")
        return None
    
    except Exception as e:
        logger.error(f"❌ Error detecting microphone: {e}")
        return None

# ==================== HOTWORD DETECTOR ====================
class HotwordDetector:
    """Detects 'Hey Jarvis' hotword using Porcupine"""
    
    def __init__(self, keyword_path=None):
        self.keyword_path = keyword_path or config.HOTWORD_MODEL
        self.porcupine = None
        self.sample_rate = None
        self.frame_length = None
        self.audio_device = None
        
        self._initialize()
    
    def _initialize(self):
        """Initialize Porcupine hotword detector"""
        try:
            if not config.PORCUPINE_ACCESS_KEY:
                raise ValueError(
                    "🔐 Porcupine access key not configured!\n"
                    "Set PORCUPINE_ACCESS_KEY in .env file\n"
                    "Get free key from: https://picovoice.ai/console/"
                )
            
            logger.info("🔑 Initializing Porcupine hotword detector")
            
            self.porcupine = pvporcupine.create(
                access_key=config.PORCUPINE_ACCESS_KEY,
                keyword_paths=[self.keyword_path],
            )
            
            self.sample_rate = self.porcupine.sample_rate
            self.frame_length = self.porcupine.frame_length
            
            # Auto-detect microphone if not specified
            if config.AUDIO_DEVICE == -1:
                self.audio_device = auto_detect_microphone()
            else:
                self.audio_device = config.AUDIO_DEVICE
            
            logger.info(f"✅ Porcupine initialized")
            logger.info(f"   Sample rate: {self.sample_rate} Hz")
            logger.info(f"   Frame length: {self.frame_length} samples")
            logger.info(f"   Audio device: {self.audio_device}")
        
        except Exception as e:
            logger.error(f"❌ Hotword initialization failed: {e}")
            raise
    
    def listen_for_hotword(self, timeout_seconds=None):
        """
        Listen for 'Hey Jarvis' hotword
        Returns True if detected, False if timeout
        """
        try:
            logger.info("🎙️  Listening for 'Hey Jarvis'...")
            
            import threading
            detected = False
            should_stop = False
            
            def listen_thread():
                nonlocal detected, should_stop
                try:
                    with sd.RawInputStream(
                        samplerate=self.sample_rate,
                        blocksize=self.frame_length,
                        dtype="int16",
                        channels=1,
                        device=self.audio_device,
                    ) as stream:
                        while not should_stop:
                            data = stream.read(self.frame_length)[0]
                            pcm = struct.unpack_from("h" * self.frame_length, data)
                            
                            result = self.porcupine.process(pcm)
                            if result >= 0:
                                detected = True
                                should_stop = True
                                logger.info("🔥 Hotword Detected!")
                                break
                
                except Exception as e:
                    logger.error(f"❌ Hotword detection error: {e}")
                    should_stop = True
            
            thread = threading.Thread(target=listen_thread, daemon=True)
            thread.start()
            
            if timeout_seconds:
                thread.join(timeout=timeout_seconds)
                should_stop = True
            else:
                thread.join()
            
            return detected
        
        except Exception as e:
            logger.error(f"❌ Failed to listen for hotword: {e}")
            return False
    
    def cleanup(self):
        """Clean up Porcupine resources"""
        if self.porcupine:
            self.porcupine.delete()
            logger.info("🧹 Porcupine resources cleaned up")

# ==================== TESTING ====================
if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    try:
        detector = HotwordDetector()
        print("Say 'Hey Jarvis' to test...")
        if detector.listen_for_hotword(timeout_seconds=30):
            print("✅ Hotword detected successfully!")
        else:
            print("❌ Hotword not detected within timeout")
        detector.cleanup()
    except Exception as e:
        print(f"Error: {e}")
