import subprocess
import cv2

class RTMPStreamer:
    def __init__(self, rtmp_url, width, height, fps=20):
        self.rtmp_url = rtmp_url
        self.process = subprocess.Popen([
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', f"{width}x{height}",
            '-r', str(fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'flv',
            rtmp_url
        ], stdin=subprocess.PIPE)

    def send_frame(self, frame):
        try:
            self.process.stdin.write(frame.tobytes())
        except Exception as e:
            print("RTMP streaming error:", e)
