import os
import json

import cv2
from PIL import Image , ImageDraw
import numpy as np


def get_video_info(videopath):
    video_capture = cv2.VideoCapture(videopath)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return None, None

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    print(f"Total number of frames: {total_frames}")
    print(f"Frames per second (FPS): {fps}")

    video_capture.release()
    return total_frames, fps


def get_specific_frame_by_number(videopath, frame_number):

    video = cv2.VideoCapture(videopath)
    if not video.isOpened():
        print("Error: Could not open video.")
        return False

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    success, frame = video.read()

    if success:

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame_rgb)

        image.show()

        width, height = image.size
        print('Height:', height, 'Width:', width)

        video.release()
        return True

    else:

        print("Error: Could not read the frame.")
        video.release()
        return False


def extract_frames_and_boxes(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    frame_data = {}

    for item in data:
        annotations = item.get('annotations', [])
        for annotation in annotations:
            results = annotation.get('result', [])
            for result in results:
                sequence = result['value'].get('sequence', [])
                for frame_info in sequence:
                    frame_number = frame_info['frame']

                    # You can now include all frames regardless of enabled status
                    bbox_tuple = (
                        frame_info['x'],
                        frame_info['y'],
                        frame_info['width'],
                        frame_info['height']
                    )

                    if frame_number not in frame_data:
                        frame_data[frame_number] = []

                    frame_data[frame_number].append(bbox_tuple)

    return frame_data

def save_frames_and_annotations(main_directory, data_dict, video_path):
    if not os.path.exists(main_directory):
        os.makedirs(main_directory)

    images_folder = os.path.join(main_directory, 'images')
    labels_folder = os.path.join(main_directory, 'labels')

    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)

    video_id = os.path.splitext(os.path.basename(video_path))[0]
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f"Error: Could not open video '{video_path}'.")
        return

    for frame_number, tuples in data_dict.items():
        video.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number) - 1 )
        success, frame = video.read()

        if success:
            frame_image_name = f'{video_id}_frame_{int(frame_number) - 1 }.jpg'
            frame_image_path = os.path.join(images_folder, frame_image_name)

            cv2.imwrite(frame_image_path, frame)
            height, width, _ = frame.shape
            print(f"Frame {frame_number} saved as '{frame_image_path}'")

            txt_file_path = os.path.join(labels_folder, f'{video_id}_frame_{int(frame_number) - 1}.txt')

            with open(txt_file_path, 'w') as f:
                for tuple_data in tuples:
                    pixel_x = tuple_data[0] / 100.0 * width
                    pixel_y = tuple_data[1] / 100.0 * height
                    pixel_width = tuple_data[2] / 100.0 * width
                    pixel_height = tuple_data[3] / 100.0 * height
                    f.write(f"0 {pixel_x} {pixel_y} {pixel_width} {pixel_height}\n")

            print(f"Annotations for frame {int(frame_number) - 1 } saved as '{txt_file_path}'")
        else:
            print(f"Error: Could not read frame {int(frame_number) - 1 }.")

    video.release()

def convert_to_yolo_format(x, y, width, height, image_width, image_height):
    cx = (x + width / 2) / image_width
    cy = (y + height / 2) / image_height
    w = width / image_width
    h = height / image_height
    return cx, cy, w, h


def convert_annotations_to_yolo_for_all_folders(base_folder):
    image_folder = os.path.join(base_folder, 'images')
    txt_file_folder = os.path.join(base_folder, 'labels')

    success_count = 0

    for image in os.listdir(image_folder):
        image_name = image.split('.')[0]
        frame_image_path = os.path.join(image_folder, f'{image_name}.jpg')
        txt_file_path = os.path.join(txt_file_folder, f'{image_name}.txt')

        try:
            image = Image.open(frame_image_path)
            original_width, original_height = image.size
            print(f'Image Width: {original_width}, Image Height: {original_height}')

            if os.path.exists(txt_file_path):
                with open(txt_file_path, 'r') as infile:
                    lines = infile.readlines()

                yolo_labels = []
                for line in lines:
                    coordinates = line.strip().split()
                    if len(coordinates) == 5:
                        class_id, x, y, width, height = map(float, coordinates)
                        yolo_format = convert_to_yolo_format(x, y, width, height, original_width, original_height)
                        yolo_labels.append(
                            f"{int(class_id)} {yolo_format[0]} {yolo_format[1]} {yolo_format[2]} {yolo_format[3]}")

                with open(txt_file_path, 'w') as outfile:
                    outfile.write("\n".join(yolo_labels))
                print(f"Converted annotations to YOLO format for image: {image_name}")
                success_count += 1

            else:
                print(f"Error: Label file '{txt_file_path}' does not exist.")
        except FileNotFoundError as e:
            print(f"Error processing file {frame_image_path}: {e}")

    print(f"Total number of successfully converted images: {success_count}")

