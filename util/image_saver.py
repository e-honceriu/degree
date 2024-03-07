import cv2 as cv
import os
from datetime import datetime

frame_count = 0

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
folder_name = f"./output/{timestamp}"
os.makedirs(folder_name)

signal_fifo_start_path = '/home/honceriue/repos/ipc/fifo_start'
signal_fifo_end_path = '/home/honceriue/repos/ipc/fifo_end'
image_path = '/home/honceriue/repos/ipc/frame.png'

if not os.path.exists(signal_fifo_start_path):
    os.mkfifo(signal_fifo_start_path)

if not os.path.exists(signal_fifo_end_path):
    os.mkfifo(signal_fifo_end_path)

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

def send_image(original_frame):
    cv.imwrite(image_path, original_frame)
    with open(signal_fifo_start_path, "wb") as pipe:
        pipe.write(b"\x01")
    with open(signal_fifo_end_path, 'rb') as pipe:
        byte = pipe.read(1) 
  
