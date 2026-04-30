import pyrealsense2 as rs
import cv2
import numpy as np
import os
import glob
import re

out_dir = "./photos/headphones"
os.makedirs(out_dir, exist_ok=True)

existing_files = glob.glob(os.path.join(out_dir, "frame_*.png"))
if existing_files:
    indices = [int(re.search(r"frame_(\d+)\.png", os.path.basename(f)).group(1)) for f in existing_files]
    frame_idx = max(indices) + 1
else:
    frame_idx = 0

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

try:
    frames_to_save = 15
    saved_count = 0 
    while saved_count < frames_to_save:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        
        filename = os.path.join(out_dir, f"frame_{frame_idx:05d}.png")
        cv2.imwrite(filename, color_image)
        print(f"✅ Сохранён: {filename}")

        frame_idx += 1     
        saved_count += 1   
finally:
    pipeline.stop()