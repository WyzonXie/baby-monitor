from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import audio as mp_audio
from mediapipe.tasks.python.components import containers as mp_containers
import sounddevice as sd

SAMPLE_RATE = 16000
SECONDS = 1
THRESHOLD = 0.2  # silent ~0.03 speaking ~0.3

options = mp_audio.AudioClassifierOptions(
      base_options=mp_python.BaseOptions(model_asset_path="yamnet.tflite"),
      max_results=3,
    )
classifier = mp_audio.AudioClassifier.create_from_options(options)
print("Model loaded.")
print("Monitoring...")

while True:
    audio_data = sd.rec(SAMPLE_RATE * SECONDS, samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    volume = abs(audio_data).max()
    print(volume)
    if volume > THRESHOLD:
        print("Sound detected!")
        clip = mp_containers.AudioData.create_from_array(audio_data, SAMPLE_RATE)
        result = classifier.classify(clip)
        for category in result[0].classifications[0].categories:
            print(category.category_name, category.score)