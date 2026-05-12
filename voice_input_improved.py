"""
Improved Voice Input - Vosk Speech-to-Text with Error Handling
Listens to microphone and converts speech to text in real-time
"""

import json
import logging
import os
import threading
from typing import Callable, Optional

import sounddevice as sd
import vosk

import config
from hotword_secure import auto_detect_microphone

logger = logging.getLogger(__name__)

# ==================== VOSK INITIALIZATION ====================
class VoskSTTEngine:
    """Speech-to-Text using Vosk (offline, local)"""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or "models/vosk-model-small-en-us-0.15"
        self.model = None
        self.rec = None
        self.is_listening = False
        self.audio_device = None
        self.sample_rate = 16000  # Vosk standard
        
        self._initialize()
    
    def _initialize(self):
        """Initialize Vosk model and recorder"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"❌ Vosk model not found at: {self.model_path}\n"
                    f"Download from: https://github.com/alphacep/vosk-models/releases"
                )
            
            logger.info(f"📦 Loading Vosk model from {self.model_path}")
            self.model = vosk.Model(self.model_path)
            self.rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
            self.rec.SetWords(["jarvis", "ayurveda", "dosha", "vata", "pitta", "kapha"])
            
            # Auto-detect microphone
            self.audio_device = auto_detect_microphone()
            
            logger.info("✅ Vosk STT engine initialized")
        
        except Exception as e:
            logger.error(f"❌ Vosk initialization failed: {e}")
            raise
    
    def listen(
        self,
        timeout_seconds=config.STT_TIMEOUT,
        partial_callback: Optional[Callable[[str], None]] = None,
        complete_callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Listen to microphone and return recognized text
        
        Args:
            timeout_seconds: Max listening time
            partial_callback: Called with partial recognition
            complete_callback: Called with final recognition
        
        Returns:
            Recognized text or empty string if timeout/error
        """
        result_text = ""
        self.is_listening = True
        
        try:
            logger.info(f"🎤 Listening for {timeout_seconds} seconds...")
            
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=4000,
                dtype="int16",
                channels=1,
                device=self.audio_device,
            ) as stream:
                import time
                start_time = time.time()
                
                while self.is_listening:
                    # Check timeout
                    if time.time() - start_time > timeout_seconds:
                        logger.warning(f"⏱️  Listening timeout after {timeout_seconds}s")
                        break
                    
                    # Read audio data
                    data = stream.read(4000)[0]
                    
                    if self.rec.AcceptWaveform(data):
                        # Final result
                        result_json = json.loads(self.rec.Result())
                        if "result" in result_json:
                            result_text = " ".join([word["conf"] if "conf" in word else word.get("result", "")
                                                   for word in result_json.get("result", [])])
                        
                        if "text" in result_json:
                            result_text = result_json["text"]
                        
                        if result_text:
                            logger.info(f"✅ Recognized: {result_text}")
                            if complete_callback:
                                complete_callback(result_text)
                            break
                    else:
                        # Partial result
                        partial_json = json.loads(self.rec.PartialResult())
                        if "partial" in partial_json:
                            partial_text = partial_json["partial"]
                            if partial_text:
                                logger.debug(f"🔄 Partial: {partial_text}")
                                if partial_callback:
                                    partial_callback(partial_text)
        
        except KeyboardInterrupt:
            logger.info("⚠️  Listening interrupted by user")
        
        except Exception as e:
            logger.error(f"❌ STT error: {e}")
        
        finally:
            self.is_listening = False
        
        if not result_text:
            logger.warning("❌ No speech recognized")
        
        return result_text
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        logger.info("🛑 Stopped listening")
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
        logger.info("🧹 Vosk resources cleaned up")

# ==================== UTILITY FUNCTIONS ====================
def get_user_speech(timeout_seconds=config.STT_TIMEOUT) -> str:
    """Quick function to get user speech"""
    try:
        engine = VoskSTTEngine()
        text = engine.listen(timeout_seconds=timeout_seconds)
        engine.cleanup()
        return text
    except Exception as e:
        logger.error(f"❌ Speech recognition failed: {e}")
        return ""

# ==================== TESTING ====================
if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    try:
        print("🎤 Testing Vosk STT Engine")
        print("=" * 50)
        
        engine = VoskSTTEngine()
        
        def on_partial(text):
            print(f"  🔄 Partial: {text}")
        
        def on_complete(text):
            print(f"  ✅ Complete: {text}")
        
        text = engine.listen(
            timeout_seconds=10,
            partial_callback=on_partial,
            complete_callback=on_complete
        )
        
        print(f"\n📝 Final text: {text}")
        engine.cleanup()
    
    except Exception as e:
        print(f"Error: {e}")
