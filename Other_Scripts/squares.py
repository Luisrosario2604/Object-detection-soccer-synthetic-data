#!/usr/bin/python3
# Importing python3 from local, just use "python3 <binary>" if is not the same location

# /
# ** Luis ROSARIO, 2023
# ** squares.py
# ** File description:
# ** View the annotation in an image
# ** https://github.com/Luisrosario2604
# */

# Imports
import argparse
import os
import glob


# Function declarations
class_nb = {
        0 : "Ball",
        1 : "Referee",
        2 : "Goal1",
        3: "Goal2",
        4 : "Player1_1",
        5 : "Player1_2",
        6 : "Player1_3",
        7 : "Player1_4",
        8 : "Player1_5",
        9 : "Player1_6",
        10 : "Player1_7",
        11 : "Player1_8",
        12 : "Player1_9",
        13 : "Player1_10",
        14 : "Player2_1",
        15 : "Player2_2",
        16 : "Player2_3",
        17 : "Player2_4",
        18 : "Player2_5",
        19 : "Player2_6",
        20 : "Player2_7",
        21 : "Player2_8",
        22 : "Player2_9",
        23 : "Player2_10"
    }

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


def get_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--input", required=True, help="path of the input data file")
    args = vars(ap.parse_args())

    input_dir = args["input"]

    if not os.path.isdir(input_dir):
        print("Folder not existing")
        exit(84)

    return input_dir


def get_all_files(input_dir):
    file_list = []
    folder_name = str(input_dir)

    if folder_name.endswith("/") == False and folder_name.endswith("\\") == False:
        folder_name += "/"

    for file in glob.glob(folder_name + "img/*.png"):
        if file.split('.')[-2].split('/')[-1].split('\\')[-1].isnumeric():
            file_list.append(file)
    return file_list


def get_one_square(f):
    import cv2

    img = cv2.imread(f)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    ano = f.replace("img", "ano")
    ano = ano.replace("png", "txt")
    detections = []

    with open(ano, 'r') as text_file:
        for line in text_file:
            line = line.split()
            x_min = int((float(line[1]) - float(line[3]) / 2) * img.shape[1])
            x_max = int((float(line[1]) + float(line[3]) / 2) * img.shape[1])
            y_min = int((float(line[2]) - float(line[4]) / 2) * img.shape[0])
            y_max = int((float(line[2]) + float(line[4]) / 2) * img.shape[0])

            rgb_to_detect = colors[class_nb[int(line[0])]]

            print(rgb_to_detect)

            cv2.rectangle(img_rgb, (x_min, y_min), (x_max, y_max), rgb_to_detect, 2)
            detections.append([line[0], [(x_min, y_min), (x_max, y_max)]])

    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow(f, img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return detections


def get_squares(file_list):

    for f in file_list:
        s = get_one_square(f)
        print(s)


def main():
    input_dir = get_arguments()

    file_list = get_all_files(input_dir)
    get_squares(file_list)


# Main body
if __name__ == '__main__':
    main()

