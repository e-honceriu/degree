import util.camera as camera
import util.args as arguments
import util.key_handler as key_handler
import cv2 as cv
import time
import util.image_saver as image_saver
import segmentation
import numpy as np
import copy
from util.cvfpscalc import CvFpsCalc
import mediapipe

if __name__ == "__main__":
    args = arguments.parse_args()
    cvFpsCalc = CvFpsCalc(buffer_len=10)
    segmentation.compute_lookup_table()
    camera.start_camera(frame_size=(args.width, args.height), fps=args.fps)
    lookup = args.lookup
    while True:
        print(f"FPS: {cvFpsCalc.get()}")
        op = key_handler.get_operation()
        if op == key_handler.EXIT:
            exit()
        if op == key_handler.CHANGE_LOOKUP:
            lookup = not lookup
        im = camera.get_frame()
        skin, rois = segmentation.segment_skin(im, lookup)
        if args.display:
            cv.imshow("Skin", skin)
        if op == key_handler.SAVE:
            image_saver.save_image(im, skin, rois)