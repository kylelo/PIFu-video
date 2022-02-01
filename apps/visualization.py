import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from lib.colab_util import *
from lib.options import BaseOptions

# get options
opt = BaseOptions().parse()

class visualization:

    @staticmethod
    def obj_to_video(obj_path, video_path):
        if not os.path.isfile(opt.obj_path):
            raise Exception("obj file does not exist.")
        renderer = set_renderer()
        generate_video_from_obj(obj_path, video_path, renderer)


if __name__ == '__main__':
    visualization.obj_to_video(opt.obj_path, opt.video_path)
