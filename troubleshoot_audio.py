"""
Check microphone and system audio settings
"""
import sounddevice as sd
import sys

print("🔍 Microphone Troubleshooting Guide")
print("=" * 70)

# Show default devices
print("\n1️⃣  DEFAULT DEVICES:")
print(f"   Default Input: {sd.default.device[0]} - {sd.query_devices(sd.default.device[0])['name']}")
print(f"   Default Output: {sd.default.device[1]} - {sd.query_devices(sd.default.device[1])['name']}")

# List all input devices
print("\n2️⃣  ALL INPUT DEVICES:")
devices = sd.query_devices()
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        marker = "→ " if i == sd.default.device[0] else "  "
        print(f"   {marker}#{i}: {device['name']}")

print("\n3️⃣  TROUBLESHOOTING STEPS:")
print("   a) Check Windows Settings → Sound → Input devices")
print("   b) Make sure your microphone is NOT muted")
print("   c) Check if microphone permissions are allowed in Windows")
print("   d) Try unplugging/replugging your microphone")
print("   e) Check device manager for driver issues")

print("\n4️⃣  TO USE A SPECIFIC MICROPHONE:")
print("   - Edit hotword.py line 14 and add 'device=X':")
print("     sd.RawInputStream(samplerate=..., device=4, ...)")
print("   - Edit jarvis.py lines 112 and 122 the same way")

print("\n5️⃣  CHECK YOUR PHYSICAL MICROPHONE:")
try:
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print("   Open Settings → Sound → Volume mixer")
    print("   Speak into your microphone and watch the input levels")
    input("   Press Enter when done...")
except:
    pass

print("\n" + "=" * 70)
