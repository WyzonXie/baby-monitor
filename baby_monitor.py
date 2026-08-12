from datetime import datetime, timedelta
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import audio as mp_audio
from mediapipe.tasks.python.components import containers as mp_containers
from notifier import send_notification
import sounddevice as sd


SAMPLE_RATE = 16000
SECONDS = 1
THRESHOLD = 0.2  # silent ~0.03 speaking ~0.3
cry_count = 0
silence_count = 0
alerted = False
last_heartbeat_time = datetime.min

HEARTBEAT_INTERVAL = timedelta(hours=1)  # send heartbeat every hour
CRY_COUNT_THRESHOLD = 5  # number of consecutive cries to trigger alert
SILENCE_RESET_THRESHOLD = 10  # number of consecutive silences to reset cry count

options = mp_audio.AudioClassifierOptions(
      base_options=mp_python.BaseOptions(model_asset_path="yamnet.tflite"),
      max_results=10,
    )
classifier = mp_audio.AudioClassifier.create_from_options(options)
print("Model loaded.")
print("Monitoring...")

log_file=open("cry_log.csv", "a", encoding="utf-8")

try:
    while True:
        is_crying = False
        cry_score = 0
        top_category = ""
        top_score = 0
        audio_data = sd.rec(SAMPLE_RATE * SECONDS, samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        volume = abs(audio_data).max()
        print(volume)
        # Check if the volume exceeds the threshold
        if volume > THRESHOLD:
            print("Sound detected!")
            clip = mp_containers.AudioData.create_from_array(audio_data, SAMPLE_RATE)
            result = classifier.classify(clip)
            top = result[0].classifications[0].categories[0]
            top_category = top.category_name
            top_score = top.score
            for category in result[0].classifications[0].categories:
                if category.category_name == "Baby cry, infant cry":
                    cry_score = category.score
                    if cry_score > 0.5:
                        is_crying = True
        
        # Update cry and silence counts based on detection
        if is_crying:
            cry_count += 1
            silence_count = 0
            if cry_count >= CRY_COUNT_THRESHOLD and not alerted:
                print("Baby is crying!")
                send_notification(f'datetime: {datetime.now()}, Baby is crying! 宝宝正在哭泣！')
                alerted = True
        else:
            silence_count += 1
            if silence_count >= SILENCE_RESET_THRESHOLD:
                cry_count = 0
                alerted = False

        if datetime.now() - last_heartbeat_time > HEARTBEAT_INTERVAL:
            last_heartbeat_time = datetime.now()
            send_notification(f'datetime: {datetime.now()}, Heartbeat: Baby monitor is running. 宝宝监护运行中。')

        log_file.write(f'{datetime.now()},{volume},{is_crying},{cry_score},"{top_category}",{top_score}\n')
        log_file.flush()

except KeyboardInterrupt:
    print("Monitoring stopped.")
    log_file.close()