from datetime import timedelta

THRESHOLD = 0.1
HEARTBEAT_INTERVAL = timedelta(hours=1)  # send heartbeat every hour
CRY_COUNT_THRESHOLD = 5  # number of consecutive cries to trigger alert
SILENCE_RESET_THRESHOLD = 10  # number of consecutive silences to reset cry count
SPEECH_THRESHOLD = 0.5  # threshold for speech detection
