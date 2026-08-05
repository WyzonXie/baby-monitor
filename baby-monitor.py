import sounddevice as sd
SAMPLE_RATE = 16000
SECONDS = 1
THRESHOLD = 0.2  #silent ~0.03 speaking ~0.3
print("Monitoring...")
while True:
    audio_data = sd.rec(SAMPLE_RATE * SECONDS, samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    volume = abs(audio_data).max()
    print(volume)
    if volume > THRESHOLD:
        print("Sound detected!")