import os
import glob
import cv2
import argparse
from pathlib import Path
from natsort import natsorted



def png_to_video(png_folder_path, video_name="output.mp4"):
    png_paths = natsorted(glob.glob(os.path.join(png_folder_path, '*.png')))
    img_array = []
    if not png_paths:
        raise Exception("Cannot find png folder!")
    for png_path in png_paths:
        img = cv2.imread(png_path)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(os.path.join(png_folder_path, video_name), cv2.VideoWriter_fourcc(*'mp4v'), 20.0, size)

    for img in img_array:
        out.write(img)

    out.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This program converts a series of png into mp4 video')
    parser.add_argument('--png_folder_path', type=str, help='Path to png folder', default=None)
    parser.add_argument('--video_name', type=str, help='Name of the output video.', default="output.mp4")
    opts = parser.parse_args()
    png_to_video(opts.png_folder_path, opts.video_name)
