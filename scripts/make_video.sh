PNG_ROOT_FOLDER_PATH='./results/video_demo'

for dir in ${PNG_ROOT_FOLDER_PATH}/*/
do
  python ./apps/png_to_video.py --png_folder_path ${dir}
done
