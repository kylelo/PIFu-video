# An improved video2mesh tool based-on PIFu

<p float="left">
    <img src="https://user-images.githubusercontent.com/7735800/152027398-0a5a2c1d-d869-4fad-baa3-2174b8bcb83f.png" width="230" />
    <img src="https://user-images.githubusercontent.com/7735800/152027436-41cdbedf-48ad-4267-88a5-c46b9949dbbe.png" width="230" />
    <img src="https://user-images.githubusercontent.com/7735800/152030987-b27ab68a-cadc-42dd-b3ac-9cca73f25d2d.gif" width="480" />
</p>

This project chooses the pre-trained [PIFu](https://shunsukesaito.github.io/PIFu/) as the based-model, which takes in an (or multiple) image and outputs a shape represented by SDF (signed-distance function). One can leverage voxel sampling and [marching cube](https://en.wikipedia.org/wiki/Marching_cubes) algorithm to generate mesh.

The video2mesh tool adds the following features on top of PIFu:

1. Auto extract video frames as png files where the alpha (4-th) channel contains the mask info (0: background, 255: foreground)
2. Use [MobileNetV3](https://arxiv.org/abs/1905.02244) to extract human from background (beat traditional method [KNN](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html) and [MOG2](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html))
3. Add video frame sharpening kernel 3x3
4. Use [DeFMO](https://github.com/rozumden/DeFMO) to do motion deblurring on test video (Failed)

## Additional Required Libraries
* [OpenCV](https://opencv.org/) for image sharpening, KNN, and MOG2 background segmentation, video encoding and decoding.
* [MediaPipe](https://google.github.io/mediapipe/) for MobileNetV3 background segmentation.
* [natsort](https://pypi.org/project/natsort/) for image file sorting

## Usage

1. Put video into `smaple_video` folder (accept more than one)
2. Run `./scripts/make_test_set.sh` to generate testing png (one mask and one cropped image per frame) in `sample_images`

Please feel free to modify the script
```
python ./apps/video_to_png.py \
    --input_folder_path [path to folder contains videos] \    # default="./sample_videos"
    --output_folder_path [path to output folder] \            # default="./sample_images"
    --algo ["MobileNetV3", "KNN", "MOG2"] \                   # default="MobileNetV3"
    --sharpening \                                            # enable sharpening, default=False
    --play_video                                              # play frame while processing, default=False
```
3. Run `./scripts/test_video.sh` to generate obj file frame by frame.

Others:
* Run `./scripts/make_video.sh` to convert masked png into a mp4 video
* Run `./scripts/display.sh` to generate video of a rotating obj file

## Results
Please find the comparison and discussion [here](https://drive.google.com/file/d/1npRGv6JietWmnu4BKZ1CeMzKEQ4T_qnP/view?usp=sharing).

Please find all predicted mesh files [here](https://drive.google.com/drive/u/1/folders/1USnjproKSMqUb3mXg6Vv3G7vFmOC8wOw)
