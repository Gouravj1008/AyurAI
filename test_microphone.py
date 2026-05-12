"""
Test which microphone device is working
"""
import sounddevice as sd
import numpy as np

print("Testing all microphones for 3 seconds each...")
print("=" * 60)

devices = sd.query_devices()

for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:  # Only input devices
        print(f"\n🎤 Testing device #{i}: {device['name']}")
        try:
            # Record 3 seconds of audio
            duration = 3
            fs = 16000
            print(f"   Recording for {duration} seconds...")
            
            audio = sd.rec(int(fs * duration), samplerate=fs, channels=1, device=i)
            sd.wait()
            
            # Check audio level
            audio_level = np.abs(audio).mean()
            print(f"   Average audio level: {audio_level:.4f}")
            
            if audio_level > 0.01:
                print(f"   ✅ AUDIO DETECTED! This microphone works.")
            else:
                print(f"   ❌ No audio detected")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test complete! Use the device number that shows 'AUDIO DETECTED'")
