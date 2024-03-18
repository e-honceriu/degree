import cv2 as cv
import numpy as np
import json
import os

error_weights = np.array([0.298936021293775390, 0.587043074451121360, 0.140209042551032500])

lookup_table_path = './data/lookup_table.json'
lookup_table = []

kernel = np.ones((5, 5), np.uint8)

def is_skin_pixel(b, g, r):
    error_value = (b / 255.0) * error_weights[0] + (g / 255.0) * error_weights[1] + (r / 255.0) * error_weights[2] - max((b / 255.0), (g / 255.0))
    if (error_value >= 0.02511 and error_value <= 0.1177):
        return True
    return False

def compute_lookup_table():
    global lookup_table
    if os.path.exists(lookup_table_path):
        with open(lookup_table_path, 'r') as f:
            lookup_table = np.array(json.load(f), dtype=np.uint8)
    else:
        lookup_table = np.zeros((256, 256, 256), dtype=np.uint8)
        for b in range(256):
            for g in range(256):
                for r in range(256):
                    lookup_table[b, g, r] = 255 if is_skin_pixel(b, g, r) else 0
        with open(lookup_table_path, 'w') as f:
            json.dump(lookup_table.tolist(), f)

def bgr_to_error(bgr_frame):
    error_frame = np.dot(bgr_frame / 255.0, error_weights)
    max_bg = np.maximum(bgr_frame[:, :, 0], bgr_frame[:, :, 1])
    return error_frame - max_bg / 255.0

def get_contours(skin_mask):
    contours, _ = cv.findContours(skin_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    area_threshold = 0.05 * skin_mask.shape[0] * skin_mask.shape[1]
    contours = [cnt for cnt in contours if cv.contourArea(cnt) >= area_threshold]
    return contours

def get_skin_mask(bgr_frame, use_lookup=True):
    
    if use_lookup:
        global lookup_table
        return lookup_table[bgr_frame[..., 0], bgr_frame[..., 1], bgr_frame[..., 2]]

    error_frame = bgr_to_error(bgr_frame)
    return np.where((error_frame >= 0.02511) & (error_frame <= 0.1177), 255, 0).astype(np.uint8)

def segment_skin(bgr_frame, use_lookup=True):
    skin_mask = get_skin_mask(bgr_frame, use_lookup)
    skin_mask = cv.morphologyEx(skin_mask, cv.MORPH_CLOSE, kernel)
    skin_mask = cv.dilate(skin_mask, kernel, iterations=1)
    contours = get_contours(skin_mask)
    skin_mask = np.zeros(skin_mask.shape)
    rois = []
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        roi = bgr_frame[y:y+h, x:x+w].copy()
        rois.append(roi)
        cv.drawContours(skin_mask, [contour], -1, 255, -1)
    skin_mask = cv.morphologyEx(skin_mask, cv.MORPH_CLOSE, kernel)
    return skin_mask, rois
