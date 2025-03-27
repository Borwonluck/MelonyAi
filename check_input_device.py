import sounddevice as sd

print("🎙️ Available Input Devices:\n")
devices = sd.query_devices()
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        print(f"{i}: {device['name']}")
