import pyaudio

def get_audio_output_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxOutputChannels"] > 0:
            devices.append((i, info["name"]))
    return devices

def play_test_sound(device_index):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        output_device_index=device_index,
        channels=1,
        rate=44100,
        output=True
    )

    # Generate a simple test tone (sine wave)
    import numpy as np
    duration = 2.0
    frequency = 440.0
    samples = (np.sin(2 * np.pi * np.arange(44100 * duration) * frequency / 44100.0)).astype(np.float32)

    # Play the test sound
    stream.write(samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    audio_devices = get_audio_output_devices()

    if not audio_devices:
        print("No audio output devices found.")
        return

    for i, (device_index, device_name) in enumerate(audio_devices):
        print(f"Device {i}: {device_name}")
        play_test_sound(device_index)
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
