from ultralytics import YOLO
import supervision as sv
import time

model = YOLO("models/best_model/bestv7.pt")
label_annotator = sv.LabelAnnotator(text_position=sv.Position.TOP_LEFT)
box_annotator = sv.BoxAnnotator()

def detect_and_annotate(frame, prev_time):
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    mask = detections.confidence >= 0.5
    filtered = detections[mask]

    annotated = label_annotator.annotate(scene=frame.copy(), detections=filtered)
    annotated = box_annotator.annotate(scene=annotated, detections=filtered)

    fps = 1.0 / (max(time.time() - prev_time, 1e-5))
    return annotated, filtered, time.time(), fps
