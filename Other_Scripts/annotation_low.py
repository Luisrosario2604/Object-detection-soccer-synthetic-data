#!/usr/bin/python3
# Importing python3 from local, just use "python3 <binary>" if is not the same location

# /
# ** Luis ROSARIO, 2023
# ** annontation_low.py
# ** File description:
# ** Create the annotations automatically from groundtruth
# ** https://github.com/Luisrosario2604
# */

# Imports
import argparse
import os
import glob
import cv2
import numpy as np

# Global variables
colors = {
        "Ball": [204, 0, 112],
        "Referee": [119, 86, 92],
        "Goal1": [8, 14, 204],
        "Goal2": [204, 70, 0],
        "Player1_1": [1, 130, 0],
        "Player1_2": [2, 130, 0],
        "Player1_3": [3, 130, 0],
        "Player1_4": [4, 130, 0],
        "Player1_5": [5, 130, 0],
        "Player1_6": [6, 130, 0],
        "Player1_7": [7, 130, 0],
        "Player1_8": [8, 130, 0],
        "Player1_9": [9, 130, 0],
        "Player1_10": [10, 130, 0],
        "Player2_1": [190, 1, 0],
        "Player2_2": [190, 2, 0],
        "Player2_3": [190, 3, 0],
        "Player2_4": [190, 4, 0],
        "Player2_5": [190, 5, 0],
        "Player2_6": [190, 6, 0],
        "Player2_7": [190, 7, 0],
        "Player2_8": [190, 8, 0],
        "Player2_9": [190, 9, 0],
        "Player2_10": [190, 10, 0]
    }

class_nb = {
        "Ball": 0,
        "Referee": 1,
        "Goal1": 2,
        "Goal2": 2,
        "Player1_1": 3,
        "Player1_2": 3,
        "Player1_3": 3,
        "Player1_4": 3,
        "Player1_5": 3,
        "Player1_6": 3,
        "Player1_7": 3,
        "Player1_8": 3,
        "Player1_9": 3,
        "Player1_10": 3,
        "Player2_1": 3,
        "Player2_2": 3,
        "Player2_3": 3,
        "Player2_4": 3,
        "Player2_5": 3,
        "Player2_6": 3,
        "Player2_7": 3,
        "Player2_8": 3,
        "Player2_9": 3,
        "Player2_10": 3
    }


# Function declarations
def get_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--input", required=True, help="path of the input data file")
    ap.add_argument("-o", "--output", required=True, help="path of the output data file")
    args = vars(ap.parse_args())

    input_dir = args["input"]
    output_dir = args["output"]

    if not os.path.isdir(input_dir):
        print("Folder not existing")
        exit(84)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    return input_dir, output_dir


def get_all_files(input_dir):
    file_list = []
    folder_name = str(input_dir)

    if not folder_name.endswith("/"):
        folder_name += "/"

    for file in glob.glob(folder_name + "*.png"):
        if file.split('.')[0].split('/')[-1].isnumeric():
            file_list.append(file)
    return file_list


def get_one_square(f, img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = []

    for c, rgb_to_detect in colors.items():
        try:
            indices = np.where(np.all(img_rgb == rgb_to_detect, axis=-1))
            y_min, x_min = np.min(indices, axis=1)
            y_max, x_max = np.max(indices, axis=1)
            cv2.rectangle(img_rgb, (x_min, y_min), (x_max, y_max), rgb_to_detect, 2)

            #print("Coords - " + str(f) + " - " + str([(x_min, y_min), (x_max, y_max)]))
            detections.append([c, [(x_min, y_min), (x_max, y_max)]])
        except Exception:
            pass
    return detections


def coords_to_yolo(top_left, bottom_right, w, h):
    return [
        (top_left[0] + bottom_right[0]) / 2 / w,
        (top_left[1] + bottom_right[1]) / 2 / h,
        (bottom_right[0] - top_left[0]) / w,
        (bottom_right[1] - top_left[1]) / h
    ]


def create_annotation_file(detections, w, h, f_number, output_dir):
    with open(str(output_dir) + str(f_number) + ".txt", 'w') as f:
        f.write("")
    for d in detections:
        top_left = d[1][0]
        bottom_right = d[1][1]
        coords = coords_to_yolo(top_left, bottom_right, w, h)
        class_n = str(class_nb[d[0]])

        with open(str(output_dir) + str(f_number) + ".txt", 'a') as f:
            f.write(f"{class_n} {str(coords[0])} {str(coords[1])} {str(coords[2])} {str(coords[3])}\n")


def get_squares(file_list, output_dir):
    if not output_dir.endswith("/"):
        output_dir += "/"

    for f in file_list:
        img = cv2.imread(f)
        w = img.shape[1]
        h = img.shape[0]

        detections = get_one_square(f, img)
        f_number = f.split('.')[0].split('/')[-1]
        create_annotation_file(detections, w, h, f_number, output_dir)


def main():
    input_dir, output_dir = get_arguments()

    file_list = get_all_files(input_dir)
    get_squares(file_list, output_dir)


# Main body
if __name__ == '__main__':
    main()

