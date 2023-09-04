#!/usr/bin/python3
# Importing python3 from local, just use "python3 <binary>" if is not the same location

# /
# ** Luis ROSARIO, 2023
# ** predict.py
# ** File description:
# ** Predict data with a trained model
# ** https://github.com/Luisrosario2604
# */


# Imports
import argparse
import os
from ultralytics import YOLO


# Function declarations
def get_arguments():
    ap = argparse.ArgumentParser()

    ap.add_argument("-f", "--file", required=True, help="file path")
    ap.add_argument("-m", "--model", required=True, help="model path (*.pt)")
    args = vars(ap.parse_args())

    input_file = args["file"]
    model_path = args["model"]

    if not os.path.isfile(input_file):
        print("File not existing")
        exit(84)

    if not os.path.isfile(model_path):
        print("Model not existing")
        exit(84)

    if model_path[-2] != "p" and model_path[-1] != "t":
        print("Model has not the good extension (.pt)")
        exit(84)

    return input_file, model_path


def main():
    input_file, model_path = get_arguments()

    model = YOLO(model_path)
    model(input_file, save=True)


# Main body
if __name__ == '__main__':
    main()
