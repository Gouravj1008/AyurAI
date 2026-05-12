import sounddevice as sd

devices = sd.query_devices()
print("Realtek Audio Devices:\n")
for i, device in enumerate(devices):
    if 'realtek' in device['name'].lower():
        channels_info = f"({device['max_input_channels']} in, {device['max_output_channels']} out)"
        print(f"  Index {i}: {device['name']} {channels_info}")
