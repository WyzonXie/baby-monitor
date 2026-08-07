from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import audio as mp_audio
from mediapipe.tasks.python.components import containers as mp_containers
import sounddevice as sd

SAMPLE_RATE = 16000
SECONDS = 1
THRESHOLD = 0.2  # silent ~0.03 speaking ~0.3
cry_count = 0
silence_count = 0
CRY_COUNT_THRESHOLD = 5  # number of consecutive cries to trigger alert
SILENCE_RESET_THRESHOLD = 10  # number of consecutive silences to reset cry count

options = mp_audio.AudioClassifierOptions(
      base_options=mp_python.BaseOptions(model_asset_path="yamnet.tflite"),
      max_results=3,
    )
classifier = mp_audio.AudioClassifier.create_from_options(options)
print("Model loaded.")
print("Monitoring...")

try:
    while True:
        is_crying = False
        audio_data = sd.rec(SAMPLE_RATE * SECONDS, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        volume = abs(audio_data).max()
        print(volume)
        # Check if the volume exceeds the threshold
        if volume > THRESHOLD:
            print("Sound detected!")
            clip = mp_containers.AudioData.create_from_array(audio_data, SAMPLE_RATE)
            result = classifier.classify(clip)
            for category in result[0].classifications[0].categories:
                if category.category_name == "Baby cry, infant cry" and category.score > 0.5:
                    is_crying = True
        # Update cry and silence counts based on detection
        if is_crying:
            cry_count += 1
            silence_count = 0
            if cry_count >= CRY_COUNT_THRESHOLD:
                print("Baby is crying!")
        else:
            silence_count += 1
            if silence_count >= SILENCE_RESET_THRESHOLD:
                cry_count = 0
except KeyboardInterrupt:
    print("Monitoring stopped.")