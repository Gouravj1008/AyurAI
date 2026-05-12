"""
Error Handling and Exception Management for Jarvis
Centralized error handling with user-friendly messages
"""

import logging
import traceback
from typing import Callable, Optional, Type

logger = logging.getLogger(__name__)

# ==================== CUSTOM EXCEPTIONS ====================
class JarvisException(Exception):
    """Base exception for Jarvis"""
    pass

class ConfigError(JarvisException):
    """Configuration error"""
    pass

class ModelError(JarvisException):
    """Model loading/inference error"""
    pass

class AudioError(JarvisException):
    """Audio input/output error"""
    pass

class HotwordError(JarvisException):
    """Hotword detection error"""
    pass

class STTError(JarvisException):
    """Speech-to-text error"""
    pass

# ==================== ERROR HANDLING ====================
class ErrorHandler:
    """Centralized error handler"""
    
    # User-friendly error messages
    ERROR_MESSAGES = {
        ConfigError: "⚙️  Configuration error. Check your .env file.",
        ModelError: "🧠 AI model failed to load. Check GPU/VRAM availability.",
        AudioError: "🎤 Audio device error. Check microphone connection.",
        HotwordError: "🔑 Hotword detection failed. Check Porcupine key.",
        STTError: "🎙️  Speech recognition failed. Try again.",
        FileNotFoundError: "📁 Required file not found. Check paths.",
        KeyError: "🔑 Missing configuration key.",
        ValueError: "❌ Invalid input or configuration.",
        RuntimeError: "⚠️  Runtime error occurred.",
        Exception: "❌ Unexpected error. Check logs for details.",
    }
    
    @classmethod
    def handle_exception(
        cls,
        exception: Exception,
        context: str = "",
        user_friendly: bool = True,
    ) -> str:
        """
        Handle exception and return user message
        
        Args:
            exception: The exception to handle
            context: Additional context about where error occurred
            user_friendly: Return user-friendly message if True
        
        Returns:
            Error message for user
        """
        exc_type = type(exception)
        
        # Log full traceback
        logger.error(f"{'='*60}")
        logger.error(f"Exception in {context or 'unknown context'}")
        logger.error(f"Type: {exc_type.__name__}")
        logger.error(f"Message: {str(exception)}")
        logger.error("Traceback:")
        logger.error(traceback.format_exc())
        logger.error(f"{'='*60}")
        
        if user_friendly:
            # Get user-friendly message
            user_message = cls.ERROR_MESSAGES.get(exc_type)
            if user_message is None:
                for exc_class, msg in cls.ERROR_MESSAGES.items():
                    if isinstance(exception, exc_class):
                        user_message = msg
                        break
            
            return user_message or "❌ An error occurred. Please try again."
        else:
            return str(exception)
    
    @classmethod
    def retry_with_fallback(
        cls,
        primary_func: Callable,
        fallback_func: Callable,
        primary_context: str = "primary",
        fallback_context: str = "fallback",
        max_retries: int = 2,
    ):
        """
        Try primary function, fallback on error
        
        Args:
            primary_func: Function to try first
            fallback_func: Function to try if primary fails
            primary_context: Error context for primary
            fallback_context: Error context for fallback
            max_retries: Max retries on fallback
        
        Returns:
            Result from primary or fallback function
        """
        try:
            logger.info(f"🔄 Attempting: {primary_context}")
            return primary_func()
        
        except Exception as e:
            logger.warning(f"⚠️  {primary_context} failed: {e}")
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"🔄 Fallback attempt {attempt + 1}/{max_retries}")
                    return fallback_func()
                except Exception as fe:
                    logger.warning(f"⚠️  Fallback failed: {fe}")
            
            logger.error(f"❌ Both primary and fallback failed")
            raise e

# ==================== VALIDATION ====================
class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_file_exists(filepath: str, description: str = "File") -> bool:
        """Validate that file exists"""
        import os
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{description} not found: {filepath}")
        return True
    
    @staticmethod
    def validate_directory_exists(dirpath: str, description: str = "Directory") -> bool:
        """Validate that directory exists"""
        import os
        if not os.path.isdir(dirpath):
            raise FileNotFoundError(f"{description} not found: {dirpath}")
        return True
    
    @staticmethod
    def validate_config_keys(config_dict: dict, required_keys: list) -> bool:
        """Validate required config keys exist"""
        missing = [k for k in required_keys if k not in config_dict]
        if missing:
            raise KeyError(f"Missing config keys: {missing}")
        return True
    
    @staticmethod
    def validate_audio_device(device_index: int) -> bool:
        """Validate audio device is available"""
        import sounddevice as sd
        try:
            devices = sd.query_devices()
            if device_index == -1 or device_index is None:
                return True
            if not (0 <= device_index < len(devices)):
                raise ValueError(f"Invalid device index: {device_index}")
            return True
        except Exception as e:
            raise AudioError(f"Audio device validation failed: {e}")

# ==================== HEALTH CHECK ====================
class HealthCheck:
    """System health checking"""
    
    @staticmethod
    def check_gpu_availability() -> bool:
        """Check if GPU is available"""
        try:
            import torch
            available = torch.cuda.is_available()
            if available:
                logger.info(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
            else:
                logger.warning("⚠️  GPU not available, using CPU")
            return available
        except Exception as e:
            logger.error(f"❌ GPU check failed: {e}")
            return False
    
    @staticmethod
    def check_all_components() -> dict:
        """Check all system components"""
        health = {
            "gpu": HealthCheck.check_gpu_availability(),
            "model": False,
            "voice": False,
            "hotword": False,
        }
        
        try:
            from ai_brain_ayurveda import get_brain
            get_brain()
            health["model"] = True
            logger.info("✅ Model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Model check failed: {e}")
        
        try:
            from voice_input_improved import VoskSTTEngine
            VoskSTTEngine()
            health["voice"] = True
            logger.info("✅ Voice input ready")
        except Exception as e:
            logger.error(f"❌ Voice check failed: {e}")
        
        try:
            from hotword_secure import HotwordDetector
            HotwordDetector()
            health["hotword"] = True
            logger.info("✅ Hotword detector ready")
        except Exception as e:
            logger.error(f"❌ Hotword check failed: {e}")
        
        return health

# ==================== TESTING ====================
if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    print("🔧 System Health Check")
    print("=" * 50)
    
    health = HealthCheck.check_all_components()
    
    print("\n📊 Health Status:")
    for component, status in health.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component}: {'Ready' if status else 'Failed'}")
    
    all_healthy = all(health.values())
    print(f"\n{'✅ All systems ready!' if all_healthy else '⚠️  Some systems need attention'}")
