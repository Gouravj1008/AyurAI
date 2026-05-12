import sounddevice as sd

devices = sd.query_devices()
print("All Input Devices (with 2+ input channels):\n")
for i, device in enumerate(devices):
    if device['max_input_channels'] >= 2:
        channels_info = f"({device['max_input_channels']} in, {device['max_output_channels']} out)"
        api = device['name'].split(',')[-1].strip() if ',' in device['name'] else "Unknown"
        print(f"  Index {i}: {device['name']} {channels_info}")
