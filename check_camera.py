import cv2
from config import RTSP_URL
cap=cv2.VideoCapture(RTSP_URL)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    raise SystemExit(1)
ok,frame=cap.read()
if not ok:
    print("Error: Could not read frame from video stream.")
    raise SystemExit(1)

print("resolution ratio:", cap.get(cv2.CAP_PROP_FRAME_WIDTH), "x", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("shape:", frame.shape)
print("fps:", cap.get(cv2.CAP_PROP_FPS))

cap.release()