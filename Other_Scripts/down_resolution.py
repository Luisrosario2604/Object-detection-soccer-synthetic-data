#!/usr/bin/python3
# Importing python3 from local, just use "python3 <binary>" if is not the same location

# /
# ** Luis ROSARIO, 2023
# ** annontation.py
# ** File description:
# ** Downscale the resolution of the images in input directory
# ** https://github.com/Luisrosario2604
# */

# Imports
import argparse
import os
from PIL import Image
import glob


# Function declarations
def get_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--input", required=True, help="path of the input data file")
    ap.add_argument("-o", "--output", required=True, help="path of the output data file")
    ap.add_argument("-r", "--res", required=True, type=int, choices=range(50, 1920), help="How many you want to decrease the resolution")
    args = vars(ap.parse_args())

    input_dir = args["input"]
    output_dir = args["output"]
    res = args["res"]

    if not os.path.isdir(input_dir):
        print("Folder not existing")
        exit(84)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    return input_dir, output_dir, res


def get_all_files(input_dir):
    file_list = []
    folder_name = str(input_dir)

    if not folder_name.endswith("/"):
        folder_name += "/"

    for file in glob.glob(folder_name + "*.png"):
        if file.split('.')[0].split('/')[-1].isnumeric():
            file_list.append(file)
    return file_list


def down_res(file_list, res, output_dir):
    w = res
    h = int(w * 1080 / 1920)
    print("Resolution : " + str(w) + "x" + str(h))

    if not output_dir.endswith("/"):
        output_dir += "/"

    for f in file_list:
        img = Image.open(f)
        img = img.resize((w, h), Image.Resampling.LANCZOS)
        f_name = f.split('.')[0].split('/')[-1] + ".png"
        img.save(output_dir + f_name)


def main():
    input_dir, output_dir, res = get_arguments()

    file_list = get_all_files(input_dir)
    down_res(file_list, res, output_dir)


# Main body
if __name__ == '__main__':
    main()
