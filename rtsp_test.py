from config import RTSP_URL
import subprocess
import numpy as np

p = subprocess.Popen(["ffmpeg", "-rtsp_transport", "tcp","-loglevel", "error", "-i", RTSP_URL, "-vn", "-ac","1", "-ar","16000", "-f","s16le","-"], stdout=subprocess.PIPE)
for i in range(10):
    data = p.stdout.read(32000)
    samples = np.frombuffer(data, dtype=np.int16)
    audio_data = samples.astype(np.float32) / 32768.0
    audio_data = audio_data.reshape(-1, 1)
    volume = abs(audio_data).max()
    print(volume)
    print(audio_data.shape)

p.terminate()