import cv2
import time
TEST_SECONDS=1800
from config import RTSP_URL
cap=cv2.VideoCapture(RTSP_URL)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    raise SystemExit(1)
ok,frame=cap.read()
if not ok:
    print("Error: Could not read frame from video stream.")
    raise SystemExit(1)
start = time.time()
success_num=0
fail_num=0
while time.time()-start<TEST_SECONDS:
    ok,frame=cap.read()
    if ok:
        success_num+=1
    else:
        fail_num+=1
elapsed_time=time.time()-start
print("success_num:",success_num)
print("fail_num:",fail_num)
print("success_fps:",success_num/elapsed_time)
print("fail_fps:",fail_num/elapsed_time)
print("total_fps:",(success_num+fail_num)/elapsed_time)
cap.release()