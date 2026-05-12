import sounddevice as sd

d = sd.default.device[0]
info = sd.query_devices()[d]
print(f"Index: {d} | Name: {info['name']}")
