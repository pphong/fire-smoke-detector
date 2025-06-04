import cv2
import time
import threading
from collections import deque
from detector_engine.detector import detect_and_annotate
from detector_engine.notification_alert import send_telegram_video
from detector_engine.utils import save_clip
import json
import numpy as np
import os
import platform

# from detector_engine.streaming import RTMPStreamer

SEND_INTERVAL = 30
SIREN_INTERVAL = 5
CLIP_BEFORE = 5
CLIP_AFTER = 5
VIDEO_FPS = 20
FRAME_WIDTH, FRAME_HEIGHT = 640, 480

buffer_before = deque(maxlen=CLIP_BEFORE * VIDEO_FPS)
buffer_after = deque(maxlen=CLIP_AFTER * VIDEO_FPS)

with open("config.json", "r") as f:
    config = json.load(f)

RTSP_CONF = config["rtsp"]
DEBUG_CONF = config["debug"]

source = 0
cap = cv2.VideoCapture(source)
prev_time = time.time()
last_sent_time = 0
last_detected_time = 0
ready_clip = False
last_alert_time = 0

# streamer = RTMPStreamer(
#     rtmp_url="rtmp://localhost/live/stream",
#     width=FRAME_WIDTH,
#     height=FRAME_HEIGHT,
#     fps=VIDEO_FPS
# )

stop_flag = False

def wait_for_q():
    global stop_flag
    while True:
        user_input = input("--- Press 'q' + Enter to stop ---\n")
        if user_input.strip().lower() == 'q':
            stop_flag = True
            break

threading.Thread(target=wait_for_q, daemon=True).start()

def save_clip_and_send(pre_frames, post_frames):
    filename = f"tmp/alert_{int(time.time())}.mp4"
    save_clip(filename, pre_frames, post_frames, FRAME_WIDTH, FRAME_HEIGHT, VIDEO_FPS)
    send_telegram_video(filename)
    buffer_after.clear()

def play_sound(is_fire):
    if is_fire:
        path = "./sound/fire.wav"
    else:
        path = "./sound/beep.wav"
    system = platform.system()
    if system == "Windows":
        from playsound import playsound
        playsound(path)
    elif system == "Darwin":  # macOS
        os.system(f"afplay {path}")
    elif system == "Linux":
        os.system(f"aplay {path}")
    else:
        print(f"Unsupported OS: {system}")
while not stop_flag:
    # if keyboard.is_pressed('q'):
    #     print("Q pressed, quitting...")
    #     sys.exit(0)
    ret, frame = cap.read()
    if not ret:
        if isinstance(source, str):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        else:
            break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    annotated_frame, detections, prev_time, fps = detect_and_annotate(frame, prev_time)

    current_time = time.time()
    if len(detections) > 0 and current_time - last_alert_time >= SIREN_INTERVAL:
        last_alert_time=current_time
        threading.Thread(
            target=play_sound,
            args=(np.any(detections.class_id == 0),),
            daemon=True
        ).start()

    if last_detected_time == 0:
        buffer_before.append(annotated_frame.copy())

    if len(detections) > 0 and last_detected_time == 0:
        last_detected_time = current_time

    if not ready_clip and last_detected_time != 0:
        buffer_after.append(annotated_frame.copy())
        if current_time - last_detected_time >= CLIP_AFTER:
            ready_clip = True

    if last_detected_time and ready_clip and current_time - last_sent_time >= SEND_INTERVAL:
        last_sent_time = current_time
        last_detected_time = 0
        ready_clip = False
        threading.Thread(
            target=save_clip_and_send,
            args=(list(buffer_before), list(buffer_after)),
            daemon=True
        ).start()


    cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if DEBUG_CONF == 1:
        cv2.imshow("NCNN Detection", annotated_frame)
        # streamer.send_frame(annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
exit(0)