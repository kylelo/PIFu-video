import os
import sys
import glob
import cv2
import argparse
import shutil
import numpy as np
import mediapipe as mp
from pathlib import Path

class Options:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                                           OpenCV. You can process videos.')
        self.parser.add_argument('--input_video_path', type=str, help='Path to a all input videos.', default='./sample_videos')
        self.parser.add_argument('--output_folder_path', type=str, help='Path to output folder', default='./sample_images')
        self.parser.add_argument('--algo', type=str, help='Background subtraction method (MobileNetV3, KNN, MOG2).', default='MobileNetV3')
        self.parser.add_argument('--sharpening', help='Apply sharpening kernel to each frame', action='store_true')
        self.parser.add_argument('--play_video', help='Display the frame currently under processing', action='store_true')

    def parse(self):
        return self.parser.parse_args()

class VideoProcess:
    def __init__(self, opts):
        self.sharpening_kernel = np.array([[0, -1, 0],
                                           [-1, 5,-1],
                                           [0, -1, 0]])

        self.sharpening = opts.sharpening
        self.algo = opts.algo
        if self.algo == 'MobileNetV3':
            mp_selfie_segmentation = mp.solutions.selfie_segmentation
            self.backSub = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)
        elif self.algo == 'MOG2':
            self.backSub = cv2.createBackgroundSubtractorMOG2()
        else:
            self.backSub = cv2.createBackgroundSubtractorKNN()

    def video_to_img_and_mask(self, video_path, output_path):
        # create folder with same name as video
        video_name = Path(video_path).stem
        print("Extracting frames for video: ", video_name)
        output_folder_path = os.path.join(output_path, video_name, "")
        if os.path.exists(output_folder_path):
            shutil.rmtree(output_folder_path)
        os.makedirs(output_folder_path)

        # Open video
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            print('Unable to open: ' + video_path)
            exit(0)

        frame_id = 0
        while True:
            ret, frame = capture.read()
            if frame is None:
                break

            if self.sharpening:
                frame = cv2.filter2D(src=frame, ddepth=-1, kernel=self.sharpening_kernel)

            if self.algo == 'MobileNetV3':
                results = self.backSub.process(frame)
                frame_mask = results.segmentation_mask*256
            else:
                frame_mask = self.backSub.apply(frame)

            if opts.play_video:
                cv2.imshow('Original', frame)
                cv2.imshow('Frame Mask', frame_mask)
                keyboard = cv2.waitKey(30)

            frame = np.concatenate((frame, frame_mask[:,:,None]), axis=2)

            cv2.imwrite(output_folder_path + "%s%d.png" % (video_name, frame_id), frame)
            # cv2.imwrite(output_folder_path + "%s%d_mask.png" % (video_name, frame_id), frame_mask)
            frame_id += 1

if __name__ == '__main__':
    opts = Options().parse()
    v_proc = VideoProcess(opts)

    video_paths = glob.glob(os.path.join(opts.input_video_path, '*'))
    for v_path in video_paths:
        v_proc.video_to_img_and_mask(v_path, opts.output_folder_path)
