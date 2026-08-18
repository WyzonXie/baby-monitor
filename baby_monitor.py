from datetime import datetime, timedelta
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import audio as mp_audio
from mediapipe.tasks.python.components import containers as mp_containers
from notifier import send_notification
from config import RTSP_URL
import numpy as np
import subprocess
import time

SAMPLE_RATE = 16000
SECONDS = 1
THRESHOLD = 0.1
HEARTBEAT_INTERVAL = timedelta(hours=1)  # send heartbeat every hour
CRY_COUNT_THRESHOLD = 5  # number of consecutive cries to trigger alert
SILENCE_RESET_THRESHOLD = 10  # number of consecutive silences to reset cry count
SPEECH_THRESHOLD = 0.5  # threshold for speech detection
BYTES_PER_SAMPLE = 2  # 16-bit audio
CHUNK_BYTES = SAMPLE_RATE * SECONDS * BYTES_PER_SAMPLE  # number of bytes to read per chunk


cry_count = 0
silence_count = 0
alerted = False
last_heartbeat_time = datetime.min
stream_alerted = False

def start_ffmpeg():
    p = subprocess.Popen(["ffmpeg", "-rtsp_transport","tcp","-timeout","5000000","-loglevel", "error", "-i", RTSP_URL, "-vn", "-ac","1", "-ar",str(SAMPLE_RATE), "-f","s16le","-"], stdout=subprocess.PIPE)
    return p

options = mp_audio.AudioClassifierOptions(
      base_options=mp_python.BaseOptions(model_asset_path="yamnet.tflite"),
      max_results=10,
    )
classifier = mp_audio.AudioClassifier.create_from_options(options)
print("Model loaded.")
print("Monitoring...")

log_file=open("cry_log.csv", "a", encoding="utf-8")
p = start_ffmpeg()
try:
    while True:
        speech_score = 0
        is_crying = False
        cry_score = 0
        top_category = ""
        top_score = 0
        data = p.stdout.read(CHUNK_BYTES)
        # stream error
        if len(data) < CHUNK_BYTES:
            print("Error: Could not read data.")
            if not stream_alerted:
                result=send_notification(f'datetime: {datetime.now()}, Error: Baby monitor interrupted.Reconnecting... 宝宝监护中断，重连中...')
                if result:
                    stream_alerted = True
            print("reconnecting...")    
            p.terminate()
            time.sleep(5)  # wait for a few seconds before restarting
            p = start_ffmpeg()
            continue
        if stream_alerted:
            result=send_notification(f'datetime: {datetime.now()},Reconnected. 重连成功')   
            if result:
                stream_alerted = False
        samples = np.frombuffer(data, dtype=np.int16)
        audio_data = samples.astype(np.float32) / 32768.0
        audio_data = audio_data.reshape(-1, 1)
        volume = abs(audio_data).max()
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
                if category.category_name == "Speech":
                    speech_score = category.score
        # Update cry and silence counts based on detection
        if speech_score > SPEECH_THRESHOLD:
            cry_count = 0
            silence_count = 0
            alerted = False
        elif is_crying:
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

        # Send heartbeat notification if the interval has passed
        if datetime.now() - last_heartbeat_time > HEARTBEAT_INTERVAL:
            last_heartbeat_time = datetime.now()
            send_notification(f'datetime: {datetime.now()}, Heartbeat: Baby monitor is running. 宝宝监护运行中。')

        print(volume,cry_count,speech_score)

        log_file.write(f'{datetime.now()},{volume},{is_crying},{cry_score},"{top_category}",{top_score},{speech_score}\n')
        log_file.flush()

except KeyboardInterrupt:
    print("Monitoring stopped.")

finally:
    log_file.close()
    p.terminate()