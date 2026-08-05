import sounddevice as sd
SAMPLE_RATE = 16000
SECONDS = 1
print("Recording...")
audio_data = sd.rec(SAMPLE_RATE * SECONDS, samplerate=SAMPLE_RATE, channels=1)
sd.wait()
print(abs(audio_data).max())