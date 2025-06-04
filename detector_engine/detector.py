from ultralytics import YOLO
import supervision as sv
import time
import json
with open("config.json", "r") as f:
    config = json.load(f)

MODEL_PATH_CONF = config["model_path"]
CONFIDENCE_CONF = config["confidence"]

model = YOLO(MODEL_PATH_CONF)
label_annotator = sv.LabelAnnotator(text_position=sv.Position.TOP_LEFT)
box_annotator = sv.BoxAnnotator()

def detect_and_annotate(frame, prev_time):
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    mask = detections.confidence >= CONFIDENCE_CONF
    filtered = detections[mask]

    annotated = label_annotator.annotate(scene=frame.copy(), detections=filtered)
    annotated = box_annotator.annotate(scene=annotated, detections=filtered)

    fps = 1.0 / (max(time.time() - prev_time, 1e-5))
    return annotated, filtered, time.time(), fps
