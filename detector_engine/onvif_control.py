from onvif import ONVIFCamera
import time

class CameraONVIFController:
    def __init__(self, ip, port, username, password):
        self.cam = ONVIFCamera(ip, port, username, password)
        self.media = self.cam.create_media_service()
        self.ptz = self.cam.create_ptz_service()
        self.profile = self.media.GetProfiles()[0]
        self.token = self.profile.token

    def move(self, x, y, zoom=0, duration=1):
        req = self.ptz.create_type('ContinuousMove')
        req.ProfileToken = self.token
        req.Velocity = {'PanTilt': {'x': x, 'y': y}, 'Zoom': {'x': zoom}}

        self.ptz.ContinuousMove(req)
        time.sleep(duration)
        self.stop()

    def stop(self):
        req = self.ptz.create_type('Stop')
        req.ProfileToken = self.token
        req.PanTilt = True
        req.Zoom = True
        self.ptz.Stop(req)
