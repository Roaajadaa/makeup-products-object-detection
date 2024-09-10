import os
from PIL import Image , ImageDraw


def draw_bounding_boxes_with_original_coordinates(main_dir, frame_name):

    frame_image_path = os.path.join(main_dir, 'images', f'{frame_name}.jpg')
    txt_file_path = os.path.join(main_dir, 'labels', f'{frame_name}.txt')

    try:
        image = Image.open(frame_image_path)
        original_width, original_height = image.size
        print('Image Width:', original_width, 'Image Height:', original_height)
    except FileNotFoundError:
        print(f"Error: Could not load the image at '{frame_image_path}'.")
        return

    draw = ImageDraw.Draw(image)

    if not os.path.exists(txt_file_path):
        print(f"Error: Annotations file does not exist at '{txt_file_path}'.")
        return

    with open(txt_file_path, 'r') as file:
        for line in file:
            coordinates = line.strip().split()
            if len(coordinates) == 5:
                class_id, x, y, width, height = map(float, coordinates)  # Convert from str to float
                print('x:', x, 'y:', y, 'width:', width, 'height:', height)
                draw.rectangle(
                    [x, y,  x+ width , y + height],
                    outline='red',
                    width=2
                )
    image.show()


def yolo_to_original_coordinates(cx, cy, w, h, img_width, img_height):
    center_x = cx * img_width
    center_y = cy * img_height
    width = w * img_width
    height = h * img_height

    x1 = int(center_x - (width / 2))
    y1 = int(center_y - (height / 2))
    x2 = int(center_x + (width / 2))
    y2 = int(center_y + (height / 2))

    return x1, y1, x2, y2

def draw_bounding_boxes_with_yolo_format(main_dir, frame_name):

    frame_image_path = os.path.join(main_dir, 'images', f'{frame_name}.jpg')
    txt_file_path = os.path.join(main_dir, 'labels', f'{frame_name}.txt')

    try:
        image = Image.open(frame_image_path)
        original_width, original_height = image.size
        print('Image Width:', original_width, 'Image Height:', original_height)
    except FileNotFoundError:
        print(f"Error: Could not load the image at '{frame_image_path}'.")
        return

    draw = ImageDraw.Draw(image)

    if not os.path.exists(txt_file_path):
        print(f"Error: Annotations file does not exist at '{txt_file_path}'.")
        return

    with open(txt_file_path, 'r') as file:
        for line in file:
            coordinates = line.strip().split()
            if len(coordinates) == 5:
                class_id, x, y, width, height = map(float, coordinates)  # Convert from str to float
                print('x:', x, 'y:', y, 'width:', width, 'height:', height)
                x1, y1, x2, y2 = yolo_to_original_coordinates(x, y, width, height)
                draw.rectangle(
                    [x1, y1, x2, y2],
                    outline='red',
                    width=2
                )

    image.show()