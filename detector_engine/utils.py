import cv2

def save_clip(filename, pre_frames, main_frames, frame_width, frame_height, fps):
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    for f in pre_frames + main_frames:
        out.write(f)
    out.release()
