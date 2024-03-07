from picamera2 import Picamera2
import cv2 as cv

camera = Picamera2()

def start_camera(frame_size, fps):
    config = camera.create_preview_configuration(main={"format": 'RGB888', "size": frame_size})
    camera.configure(config)
    camera.set_controls({"FrameRate": fps})
    camera.start()

def get_frame():
    frame = camera.capture_array()
    frame = cv.flip(frame, 1)
    return frame