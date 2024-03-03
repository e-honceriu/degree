from picamera2 import Picamera2
import cv2 as cv

camera = Picamera2()

def start_camera(frame_size=(960, 540), fps=30):
    config = camera.create_preview_configuration(main={"format": 'BGR888', "size": frame_size})
    camera.configure(config)
    camera.set_controls({"FrameRate": fps})
    camera.start()

def get_frame():
    frame = camera.capture_array()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    return frame