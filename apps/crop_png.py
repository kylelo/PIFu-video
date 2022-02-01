import os
import cv2
import glob
import numpy as np

from pathlib import Path
import argparse

def get_bbox(msk):
    rows = np.any(msk, axis=1)
    cols = np.any(msk, axis=0)
    rows_ids = np.where(rows)[0]
    cols_ids = np.where(cols)[0]
    rmin, rmax = rows_ids[[0,-1]] if len(rows_ids) else (0, rows.shape[0])
    cmin, cmax = cols_ids[[0,-1]] if len(cols_ids) else (cols.shape[0], 0)

    return rmin, rmax, cmin, cmax

def process_img(img, msk, bbox=None):
    if bbox is None:
        bbox = get_bbox(msk > 100)
    cx = (bbox[3] + bbox[2])//2
    cy = (bbox[1] + bbox[0])//2

    w = img.shape[1]
    h = img.shape[0]
    height = int(1.138*(bbox[1] - bbox[0]))
    hh = height//2

    # crop
    dw = min(cx, w-cx, hh)
    if cy-hh < 0:
        img = cv2.copyMakeBorder(img,hh-cy,0,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
        msk = cv2.copyMakeBorder(msk,hh-cy,0,0,0,cv2.BORDER_CONSTANT,value=0)
        cy = hh
    if cy+hh > h:
        img = cv2.copyMakeBorder(img,0,cy+hh-h,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
        msk = cv2.copyMakeBorder(msk,0,cy+hh-h,0,0,cv2.BORDER_CONSTANT,value=0)
    img = img[cy-hh:(cy+hh),cx-dw:cx+dw,:]
    msk = msk[cy-hh:(cy+hh),cx-dw:cx+dw]
    dw = img.shape[0] - img.shape[1]
    if dw != 0:
        img = cv2.copyMakeBorder(img,0,0,dw//2,dw//2,cv2.BORDER_CONSTANT,value=[0,0,0])
        msk = cv2.copyMakeBorder(msk,0,0,dw//2,dw//2,cv2.BORDER_CONSTANT,value=0)
    img = cv2.resize(img, (512, 512))
    msk = cv2.resize(msk, (512, 512))

    kernel = np.ones((3,3),np.uint8)
    msk = cv2.erode((255*(msk > 100)).astype(np.uint8), kernel, iterations = 1)

    return img, msk


def save_img_and_mask(png_path, output_folder_path):
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    if img.shape[2] == 4:
        msk = img[:,:,3:]
        img = img[:,:,:3]
    else:
        raise Exception("Cannot read png files.")

    img_new, msk_new = process_img(img, msk)

    img_name = Path(png_path).stem

    cv2.imwrite(os.path.join(output_folder_path, "%s.png" % img_name), img_new)
    cv2.imwrite(os.path.join(output_folder_path, "%s_mask.png" % img_name), msk_new)


if __name__ == "__main__":
    '''
    given foreground mask, this script crops and resizes an input image and mask for processing.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder_path", type=str, help='input_folder_path/video_name/frames.png', default="./sample_images")
    opts = parser.parse_args()

    video_folders = os.listdir(opts.input_folder_path)
    for v_folder in video_folders:
        print("Making masks using frames from video: ", v_folder)
        png_paths = glob.glob(os.path.join(opts.input_folder_path, v_folder, '*'))
        for png_path in png_paths:
            save_img_and_mask(png_path, os.path.join(opts.input_folder_path, v_folder))
