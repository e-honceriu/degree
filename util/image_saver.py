import cv2 as cv
import os
from datetime import datetime

frame_count = 0

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
folder_name = f"./output/{timestamp}"
os.makedirs(folder_name)

def save_image(original_frame, segmented_frame, filtered_frame, final_frames):
    global frame_count
    current_frame_dir = f"{folder_name}/{frame_count}"
    os.makedirs(current_frame_dir)
    cv.imwrite(current_frame_dir + "/original_frame.jpg", original_frame)
    cv.imwrite(current_frame_dir + "/segmented_frame.jpg", segmented_frame)
    cv.imwrite(current_frame_dir + "/filtered_frame.jpg", filtered_frame)
    final_frame_cnt = 0
    for frame in final_frames:
        cv.imwrite(current_frame_dir + f"/final_frame_{final_frame_cnt}.jpg", frame)
        final_frame_cnt += 1
    frame_count += 1