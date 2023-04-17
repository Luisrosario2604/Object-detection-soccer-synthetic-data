# /
# ** Luis ROSARIO, 2022-2023
# ** RandomPos.py
# ** File description:
# ** Main file for the soccer addon
# ** https://github.com/Luisrosario2604
# */


# ------------------------------------------------------------------------
#
#    Imports
#
# ------------------------------------------------------------------------


import bpy
from bpy.utils import (unregister_class, register_class)
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

import time
import random
from datetime import datetime

import math
import numpy as np
from PIL import Image

import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess


# ------------------------------------------------------------------------
#
#    Global
#
# ------------------------------------------------------------------------


bl_info = {
    "name": "Soccer Generator",
    "author": "Luis ROSARIO",
    "description": "Generating soccer samples for deep learning",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "location": "3D View > Tools",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


bpy_c = bpy.data.collections
bpy_o = bpy.data.objects

outliner_structure = {
    "WhiteMan": "Man1",
    "BlackMan": "Man2",
    "GoalMan": "Man3",
    "WhiteWoman": "Woman1",
    "IdianWoman": "Woman2",
    "GoalWoman": "Woman3",
    "PlayerToCopy": "Man4",
    "Goal1": "GoalMan1",
    "Goal2": "GoalMan2",
    "PlayerToCopy_running_1": "ManToCopy_running_1",
    "PlayerToCopy_running_2": "ManToCopy_running_2",
    "PlayerToCopy_running_3": "ManToCopy_running_3",
    "PlayerToCopy_running_4": "ManToCopy_running_4",
    "PlayerToCopy_running_5": "ManToCopy_running_5",
    "PlayerToCopy_running_6": "ManToCopy_running_6",
    "PlayerToCopy_running_7": "ManToCopy_running_7",
    "PlayerToCopy_running_8": "ManToCopy_running_8",
    "PlayerToCopy_other_1": "ManToCopy_other_1",
    "PlayerToCopy_other_2": "ManToCopy_other_2",
    "PlayerToCopy_moving_1": "ManToCopy_moving_1",
    "PlayerToCopy_moving_2": "ManToCopy_moving_2",
    "PlayerToCopy_moving_3": "ManToCopy_moving_3",
    "PlayerToCopy_moving_4": "ManToCopy_moving_4",
    "PlayerToCopy_moving_5": "ManToCopy_moving_5",
    "PlayerToCopy_moving_6": "ManToCopy_moving_6",
    "PlayerToCopy_moving_7": "ManToCopy_moving_7",
    "PlayerToCopy_moving_8": "ManToCopy_moving_8",
    "PlayerToCopy_walking_1": "ManToCopy_walking_1",
    "PlayerToCopy_walking_2": "ManToCopy_walking_2",
    "PlayerToCopy_walking_3": "ManToCopy_walking_3",
    "PlayerToCopy_walking_4": "ManToCopy_walking_4",
    "PlayerToCopy_walking_5": "ManToCopy_walking_5",
    "PlayerToCopy_walking_6": "ManToCopy_walking_6",
    "PlayerToCopy_walking_7": "ManToCopy_walking_7",
    "PlayerToCopy_walking_8": "ManToCopy_walking_8",
    "PlayerToCopy_walking_9": "ManToCopy_walking_9",
    "PlayerToCopy_walking_10": "ManToCopy_walking_10",
    "PlayerToCopy_goaling_1": "ManToCopy_goaling_1",
    "PlayerToCopy_goaling_2": "ManToCopy_goaling_2",
    "PlayerToCopy_goaling_3": "ManToCopy_goaling_3",
    "PlayerToCopy_goaling_4": "ManToCopy_goaling_4",
    "PlayerToCopy_goaling_5": "ManToCopy_goaling_5",
}

colors_list = ["white",
                   "black",
                   "grey",
                   "blue",
                   "red",
                   "green",
                   "yellow",
                   "orange",
                   "purple",
                   "pink",
                   "brown"]

default_pos_ball = [34.8021, -54.591]
default_pos_goal1 = [34.8021, -1]
default_pos_goal2 = [34.8021, -108, 182]
default_pos_sun = [24, 15.6, 194, 3]


# ------------------------------------------------------------------------
#
#    Functions
#
# ------------------------------------------------------------------------


def get_plateform():
    platforms = {
        "linux" : "Linux",
        "linux1" : "Linux",
        "linux2" : "Linux",
        "darwin" : "OS X",
        "win32" : "Windows"
    }
    
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]


def get_separator():
    separators = {
        "Linux" : "/",
        "Windows" : "\\",
        "OS X" : "/"
    }
    
    platform = get_plateform()
    
    if platform not in separators:
        print("")
        exit()
    return separators[platform]


def bool_from_float_percent(percent):
    r = random.randint(0, 10000) / 100
    if r <= percent:
        return True
    return False


def bool_from_percent(percent):
    r = random.randint(0, 100)
    if r <= percent:
        return True
    return False


def get_body_name(obj):
    body_name = obj.name.split(".")
    return body_name[0] + "Body." + body_name[1]


def gaussian_rdm(mean, strd_deviation, min, max):
    nb = np.random.normal(mean, strd_deviation, 1)
    if nb > max:
        return gaussian_rdm(mean, strd_deviation, min, max)
    if nb < min:
        return gaussian_rdm(mean, strd_deviation, min, max)
    return nb


def get_sun_color():
    return random.choice([(1, 0.952714, 0.894104),
                          (0.967048, 0.879469, 1),
                          (0.779252, 0.813145, 1),
                          (0.882918, 1, 0.825325)])


def sun_rdm_param():
    sun = bpy_o["Lamp"]
    sun_shadow = bpy_o["Lamp_shadow"]
    
    strength = 4.800
    
    if bool_from_percent(50):
        strength = random.randint(4000, 6800) / 1000
    sun_shadow.data.energy = strength
    
    #if bool_from_percent(80):
    #    sun_shadow.data.color = (1, 1, 1)
    #else:
    #    sun_shadow.data.color = get_sun_color()
    


# ------------------------------------------------------------------------
#
#    Locations
#
# ------------------------------------------------------------------------


def get_squares():
    lenght_x = random.randint(4000, 6800)
    lenght_y = random.randint(2000, 10700)
    
    middle_x_lenght = int(lenght_x / 2)
    middle_y_lenght = int(lenght_y / 2)
    
    middle_x = random.randint(middle_x_lenght, 6856 - middle_x_lenght)
    middle_y = random.randint(middle_y_lenght, 10818 - middle_y_lenght)
    
    x_min = middle_x - middle_x_lenght
    x_max = middle_x + middle_x_lenght
    y_min = middle_y - middle_y_lenght
    y_max = middle_y + middle_y_lenght
    
    return x_min, x_max, y_min, y_max


def get_gaussians():
    mean_x = random.randint(1400, 5500) / 100
    mean_y = random.randint(1200, 11000) / 100
    
    sigma_x = random.randint(15, 40)
    sigma_y = random.randint(15, 60)
     
    print("MeanX : " + str(mean_x) + " - SigmaX : " + str(sigma_x) + "\n MeanY : " + str(mean_y) + " - SigmaY : " + str(sigma_y))
    return mean_x, sigma_x, mean_y, sigma_y


def choose_position_method(soctool):
    choice_random = soctool.my_lm_random # 5
    choice_gauss = soctool.my_lm_squares # 30
    
    if bool_from_percent(choice_random):
        print("METHOD : Random")
        return ["random"]
    if bool_from_percent(choice_gauss):
        mean_x, sigma_x, mean_y, sigma_y = get_gaussians()
        print("METHOD : Guassians")
        return ["gauss", mean_x, sigma_x, mean_y, sigma_y]
    
    x_min, x_max, y_min, y_max = get_squares()
    print("METHOD : Squares")
    return ["squares", x_min, x_max, y_min, y_max]


def get_location(option):
    if option[0] == "random":
        return [
            random.randint(105, 6856) / 100,
            random.randint(100, 10818) / 100 * -1
        ]
    elif option[0] == "gauss":
        return [
            gaussian_rdm(option[1], option[2], 1.05, 68.5),
            gaussian_rdm(option[3], option[4], 1, 108.18) * -1
        ]
    else:
        return [
            random.randint(option[1], option[2]) / 100,
            random.randint(option[3], option[4]) / 100 * -1
        ]
        


def get_location_referee(ball_y):
    mean_y = (-ball_y + 54.59) / 2
    return [
            gaussian_rdm(34.8, 10, 1.05, 68.56),
            gaussian_rdm(mean_y, 12, 1, 108.18) * -1
        ]
        
def get_location_goal(option):
    if option == "goal1":
        return [
            random.randint(320, 378) / 10,
            random.randint(00, 26) / 10 * -1
        ]
    elif option == "goal2":
        return [
            random.randint(320, 378) / 10,
            random.randint(106582, 109182) / 1000 * -1
        ]
        

def get_location_sun():
    sun_r = [random.randint(0, 84),
             random.randint(0, 78),
             random.randint(0, 360),
             random.randint(275, 600) / 100]
    if bool_from_percent(50):
        sun_r[0] *= -1
    if bool_from_percent(50):
        sun_r[1] *= -1
    return sun_r


def set_random_position_camera(camera):
    camera.location.x = (random.randint(2500, 3280) / 100) * -1
    camera.location.y = (random.randint(3959, 6959) / 100) * -1
    camera.location.z = random.randint(1600, 2480) / 100


# ------------------------------------------------------------------------
#
#    Move
#
# ------------------------------------------------------------------------


def move_ball(location=default_pos_ball):
    ball = bpy_o["Ball"]
    ball.location.x = location[0]
    ball.location.y = location[1]

    if location == default_pos_ball:
        ball.location.z = 0.165
    elif bool_from_percent(10):
        ball.location.z += random.randint(0000, 5000) / 1000


def move_sun(rotation=default_pos_sun):
    sun = bpy_o["Lamp"]
    sun.rotation_euler[0] = math.radians(rotation[0])
    sun.rotation_euler[1] = math.radians(rotation[1])
    sun.rotation_euler[2] = math.radians(rotation[2])
    sun_shadow = bpy_o["Lamp_shadow"]
    sun_shadow.data.energy = rotation[3]


def move_goals(goal1=bpy_o["GoalMan1"], goal2=bpy_o["GoalMan2"], goal_pos_1=default_pos_goal1,
               goal_pos_2=default_pos_goal2):
    goal1.location.x = goal_pos_1[0]
    goal1.location.y = goal_pos_1[1]
    goal1.location.z = -0.011951
    rotate_player(goal1, 20)

    goal1.scale.x = 1.3
    goal1.scale.y = 1.3
    goal1.scale.z = 1.3

    goal2.location.x = goal_pos_2[0]
    goal2.location.y = goal_pos_2[1]
    goal2.location.z = -0.011951
    rotate_player(goal2, 20)

    goal2.scale.x = 1.3
    goal2.scale.y = 1.3
    goal2.scale.z = 1.3


# ------------------------------------------------------------------------
#
#    Clear
#
# ------------------------------------------------------------------------


def clear_teams_col():
    for collection in bpy_c:
        if collection.name.split("_")[0] in ["Player1", "Player2", "Player5"]:
            for obj in collection.objects:
                bpy_o.remove(obj, do_unlink=True)
            bpy_c.remove(collection)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.armatures:
        if block.users == 0:
            bpy.data.armatures.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


def create_tmp_dir(dir_path, del_files=False):
    texture_path = dir_path + "Textures" + get_separator() + "Textures_tmp"
    if not os.path.isdir(texture_path + get_separator()):
        os.mkdir(texture_path)
    if del_files:
        onlyfiles = [f for f in listdir(texture_path) if isfile(join(texture_path, f))]
        for file in onlyfiles:
            if file.endswith("-texture.png"):
                os.remove(texture_path + get_separator() + file)


def clear_text_goals(goal1=bpy_o["GoalBody1"], goal2=bpy_o["GoalBody2"]):
    goal1.data.materials.clear()
    goal2.data.materials.clear()


def clear_scene(texture_path):
    clear_text_goals()
    clear_teams_col()
    move_sun()
    move_ball()
    move_goals()
    create_tmp_dir(texture_path)


# ------------------------------------------------------------------------
#
#    Scale
#
# ------------------------------------------------------------------------


def random_scale(player):
    scale = gaussian_rdm(1.3, 0.033, 1.2, 1.4)
    player.scale.x = scale
    player.scale.y = scale
    player.scale.z = scale


# ------------------------------------------------------------------------
#
#    Rotation
#
# ------------------------------------------------------------------------


def angle_of_vectors(vector, vector_dflt, jitter_angle):
    a = vector[0]
    b = vector[1]
    c = vector_dflt[0]
    d = vector_dflt[1]

    dotProduct = a * c + b * d
    modOfVector1 = math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d)
    angle = dotProduct / modOfVector1
    angleInDegree = math.degrees(math.acos(angle))

    jitter = random.randint(0, jitter_angle);
    if random.randint(0, 1) == 1:
        jitter *= -1

    return angleInDegree + jitter


def rotate_player(player, jitter_angle):
    ball = bpy_o["Ball"]
    vector = [ball.location.x - player.location.x, ball.location.y - player.location.y]
    vector_dflt = [0, -1]

    if bool_from_percent(5):
        angle = random.randint(00000, 36000) / 100
    elif bool_from_percent(50):
        angle = angle_of_vectors(vector, vector_dflt, jitter_angle)
    else:
        angle = angle_of_vectors(vector, vector_dflt, jitter_angle / 2)
    
    if ball.location.x > player.location.x:
        player.rotation_euler[2] = math.radians(angle)
    else:
        player.rotation_euler[2] = math.radians(-angle)
    

# Calculate the vector pointing from the camera to the ball
# Set the camera's rotation to point along this vector
def center_camera():
    camera = bpy_o["Camera"]
    ball = bpy_o["Ball"]
    
    set_random_position_camera(camera)
    focus_location = ball.location.copy()

    jitter_x = gaussian_rdm(0, 2, 0, 5)
    jitter_y = gaussian_rdm(0, 8, 0, 20)
    
    if bool_from_percent(50):
        jitter_x *= -1 
    if bool_from_percent(50):
        jitter_y *= -1

    focus_location.x = 34.8 - ((34.8 - focus_location.x) / 2.41)
    focus_location.x += jitter_x
    focus_location.y += jitter_y
    
    if focus_location.x > 68.5:
        focus_location.x = 68.5
    if focus_location.x < 1.05:
        focus_location.x = 1.05
    if focus_location.y > -1:
        focus_location.y = -1
    if focus_location.y < -108.2:
        focus_location.y = -108.2

    ball_to_camera = camera.location - focus_location
    camera.rotation_euler = ball_to_camera.to_track_quat("Z","Y").to_euler()
    camera.rotation_euler.y = 0
    
    fov = gaussian_rdm(35, 6, 25, 45)
    camera.data.angle = fov*(math.pi/180.0)


# ------------------------------------------------------------------------
#
#    Colors
#
# ------------------------------------------------------------------------


def get_black():
    return random.choice([[1, 1, 1],
                          [17, 17, 17],
                          [30, 30, 30],
                          [60, 60, 60],
                          [77, 77, 77]])
                          
def get_white():
    return random.choice([[255, 255, 255],
                          [255, 250, 250],
                          [255, 245, 238],
                          [245, 245, 220],
                          [245, 245, 245],
                          [255, 255, 240]])
                          
                          
def get_grey():
    return random.choice([[105, 105, 105],
                          [128, 128, 128],
                          [169, 169, 169],
                          [192, 192, 192],
                          [211, 211, 211],
                          [220, 220, 220]])
                          
                          
def get_blue():
    return random.choice([[0, 79, 255],
                          [0, 102, 255],
                          [0, 158, 255],
                          [0, 180, 255],
                          [67, 196, 239]])
                          
                          
def get_red():
    return random.choice([[133, 50, 41],
                          [161, 50, 39],
                          [223, 45, 28],
                          [244, 37, 37],
                          [233, 0, 0],
                          [255, 58, 58],
                          [255, 75, 75]])
                          
                        
def get_green():
    return random.choice([[173, 255, 0],
                          [11 / 6, 214, 0],
                          [2, 137, 0],
                          [0, 210, 127],
                          [0, 255, 131],
                          [15, 161, 7],
                          [89, 166, 26]])
                          
                          
def get_yellow():
    return random.choice([[249, 233, 9],
                          [253, 242, 93],
                          [252, 255, 131],
                          [251, 253, 158],
                          [218, 182, 0]])
                          
                    
def get_orange():
    return random.choice([[249, 156, 0],
                          [255, 167, 20],
                          [255, 202, 22],
                          [255, 178, 27],
                          [249, 115, 0]])
                          
                          
def get_purple():
    return random.choice([[240, 0, 255],
                          [221, 0, 200],
                          [193, 0, 185],
                          [178, 0, 152],
                          [135, 5, 123]])
                          
                          
def get_pink():
    return random.choice([[255, 119, 170],
                          [255, 153, 204],
                          [255, 187, 238],
                          [255, 85, 136],
                          [255, 51, 119]])
                          
                          
def get_brown():
    return random.choice([[124, 44, 21],
                          [128, 25, 21],
                          [141, 36, 13],
                          [163, 67, 24],
                          [199, 119, 29]])
    

def choose_sport_wear_random_color(nb_sorts, model_type="player"):
    if model_type == "player":
        color_choices = np.random.choice(colors_list, size=nb_sorts, replace=False, p=(
            23 / 100,  # White
            15 / 100,  # Black
            7 / 100,  # Grey
            12 / 100,  # Blue
            14 / 100,  # Red
            9 / 100,  # Green
            6 / 100,  # Yellow
            4 / 100,  # Orange
            7 / 100,  # Purple
            2 / 100,  # Pink
            1 / 100))  # brown
    elif model_type == "referee":
        color_choices = np.random.choice(colors_list, size=nb_sorts, replace=False, p=(
            0 / 100,  # White
            5 / 100,  # Black
            10 / 100,  # Grey
            10 / 100,  # Blue
            5 / 100,  # Red
            10 / 100,  # Green
            35 / 100,  # Yellow
            5 / 100,  # Orange
            5 / 100,  # Purple
            15 / 100,  # Pink
            0 / 100))  # brown
    else:
        color_choices = np.random.choice(colors_list, size=nb_sorts, replace=False, p=(
            0 / 100,  # White
            3 / 100,  # Black
            2 / 100,  # Grey
            20 / 100,  # Blue
            15 / 100,  # Red
            22 / 100,  # Green
            17 / 100,  # Yellow
            10 / 100,  # Orange
            5 / 100,  # Purple
            6 / 100,  # Pink
            0 / 100))  # brown

    color_choices = color_choices.tolist()
    random.shuffle(color_choices)

    colors_final = []

    for c in color_choices:
        if c == "white":
            colors_final.append(get_white())
        if c == "black":
            colors_final.append(get_black())
        if c == "grey":
            colors_final.append(get_grey())
        if c == "blue":
            colors_final.append(get_blue())
        if c == "red":
            colors_final.append(get_red())
        if c == "green":
            colors_final.append(get_green())
        if c == "yellow":
            colors_final.append(get_yellow())
        if c == "orange":
            colors_final.append(get_orange())
        if c == "purple":
            colors_final.append(get_purple())
        if c == "pink":
            colors_final.append(get_pink())
        if c == "brown":
            colors_final.append(get_brown())

    return colors_final


# ------------------------------------------------------------------------
#
#    Textures
#
# ------------------------------------------------------------------------


def is_color_close_white(color):
    r, g, b = color[0], color[1], color[2]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if y > 128:
        return False
    return True


def create_texture(im_to_copy, im_to_paste, color_changes):
    im = Image.open(im_to_copy)
    data = np.array(im)

    for colors in color_changes:
        r1, g1, b1 = 0, 0, colors[3]  # Original value
        r2, g2, b2 = colors[0], colors[1], colors[2]  # Value that we want to replace it with

        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        data[:, :, :3][mask] = [r2, g2, b2]

    im_to_copy = Image.fromarray(data)
    im_to_copy.save(im_to_paste)


def append_item_to_cpy_list(list, item):
    tmp = list.copy()
    tmp.append(item)
    return tmp


# colors[0] = Color shirt 1
# colors[1] = Color shirt 2
# colors[2] = Color pants
# colors[3] = Color socks
def choose_model_wear_texture(soctool, colors, model_type="player"):
    white_c = [255, 255, 255]
    black_c = [0, 0, 0]

    is_striped = False
    is_vertical = False
    is_pants_same_color = False
    is_pants_color_one = True
    if bool_from_percent(soctool.my_sw_striped):
        is_striped = True
        if bool_from_percent(soctool.my_sw_vertical):
            is_vertical = True
        if bool_from_percent(soctool.my_sw_pants_same_color_stiped):
            is_pants_same_color = True
            if bool_from_percent(50):
                is_pants_color_one = False
    elif bool_from_percent(soctool.my_sw_pants_same_color_full):
        is_pants_same_color = True

    if model_type != "player":
        is_striped = False
        is_pants_same_color = bool_from_percent(90)
    if not is_striped:
        colors[1] = colors[0]
    if is_pants_same_color:
        if is_pants_color_one:
            colors[2] = colors[1]
        colors[2] = colors[0]

    if not bool_from_percent(25):
        i = random.choice([0, 1, 2])
        colors[3] = colors[i]

    color_in_order = [append_item_to_cpy_list(colors[0], 4),
                      append_item_to_cpy_list(colors[0], 5),
                      append_item_to_cpy_list(colors[1], 6),
                      append_item_to_cpy_list(colors[2], 7),
                      append_item_to_cpy_list(colors[3], 3)]

    if is_color_close_white(colors[0]):
        color_in_order.append(append_item_to_cpy_list(white_c, 10))
    else:
        color_in_order.append(append_item_to_cpy_list(black_c, 10))

    if is_color_close_white(colors[1]):
        color_in_order.append(append_item_to_cpy_list(white_c, 11))
    else:
        color_in_order.append(append_item_to_cpy_list(black_c, 11))

    if is_color_close_white(colors[2]):
        color_in_order.append(append_item_to_cpy_list(white_c, 12))
    else:
        color_in_order.append(append_item_to_cpy_list(black_c, 12))

    return color_in_order, is_striped, is_vertical


def choose_sport_wear_referee():
    black = get_black()
    referee_color = choose_sport_wear_random_color(1, model_type="referee")
    
    color_in_order = [append_item_to_cpy_list(black, 8), # Short, shoes in black
                      append_item_to_cpy_list(black, 7),
                      append_item_to_cpy_list(black, 9),
                      append_item_to_cpy_list(black, 12)]
                      
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 3)) # Shirt, soccs in same color
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 4))
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 5))
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 6))
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 10))
    color_in_order.append(append_item_to_cpy_list(referee_color[0], 11))
    
    return color_in_order


def create_team_texture(soctool, texture_path, team_name, model_type):
    if team_name == "Team5":
        is_striped = False
        is_vertical = False
        color_in_order = choose_sport_wear_referee()
    else:
        colors = choose_sport_wear_random_color(4, model_type)
        color_in_order, is_striped, is_vertical = choose_model_wear_texture(soctool, colors, model_type)
    im_to_paste = texture_path + "Textures_tmp" + get_separator() + team_name + "-texture.png"

    im_to_copy = texture_path + "TextureHorizontalNb.png"
    if is_vertical:
        im_to_copy = texture_path + "TextureVerticalNb.png"

    create_texture(im_to_copy, im_to_paste, color_in_order)


def create_player_texure(path_team_texture, path_player_texture, team_name, soctool):
    colors = choose_sport_wear_random_color(2)
    if team_name == "Team5":
        percent_to_be_black = soctool.my_skin_referee
    else:
        percent_to_be_black = soctool.my_skin_player
        
    if bool_from_percent(percent_to_be_black):
        hair_color = random.choice([[35, 18, 11],
                                    [61, 35, 20],
                                    [90, 56, 37],
                                    [35, 18, 11],
                                    [61, 35, 20],
                                    [90, 56, 37]])

        skin_color = random.choice([[161, 102, 94],
                                    [80, 51, 53],
                                    [99, 82, 61]])
    else:
        hair_color = random.choice([[35, 18, 11],
                                    [61, 35, 20],
                                    [90, 56, 37],
                                    [251, 231, 161],
                                    [241, 204, 143],
                                    [35, 18, 11],
                                    [61, 35, 20],
                                    [90, 56, 37],
                                    [251, 231, 161],
                                    [241, 204, 143],
                                    [255, 147, 33]])

        skin_color = random.choice([[197, 140, 133],
                                    [236, 188, 180],
                                    [209, 163, 164]])
    if team_name != "Team5":
        color_in_order = [append_item_to_cpy_list(colors[0], 8),
                          append_item_to_cpy_list(colors[1], 9),
                          append_item_to_cpy_list(hair_color, 1),
                          append_item_to_cpy_list(skin_color, 2)]
    else:
        color_in_order = [append_item_to_cpy_list(hair_color, 1),
                          append_item_to_cpy_list(skin_color, 2)]

    create_texture(path_team_texture, path_player_texture, color_in_order)


def apply_texture_to_player(player_name, path_player_texture):
    material_obj = bpy.data.materials.new(player_name + '-Material')
    material_obj.use_nodes = True

    bsdf = material_obj.node_tree.nodes["Principled BSDF"]
    texImage = material_obj.node_tree.nodes.new("ShaderNodeTexImage")
    texImage.image = bpy.data.images.load(path_player_texture)
    material_obj.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])
    bpy_o[player_name].data.materials.append(material_obj)


def change_groundtruth_color(player_name, team_name, i):
    if team_name == "Team1":
        gt_color = (i/255, 130/255, 0, 1)
    elif team_name == "Team2":
        gt_color = (190 / 255, i/255, 0, 1)
    elif team_name == "Team3":
        gt_color = (204/255, 70/255, 0, 1)
    elif team_name == "Team4":
        gt_color = (8/255, 14/255, 204/255, 1)
    else:
        gt_color = (119/255, 86/255, 92/255, 1)

    bpy_o[player_name].active_material.diffuse_color = gt_color
    bpy_o[player_name].active_material.roughness = 1


def change_player_texture(soctool, player_name, team_name, i, gen_nb, model_type):
    my_new_texture_ = soctool.my_new_texture
    texture_path = soctool.my_path_dir + "Textures" + get_separator()
    path_team_texture = texture_path + "Textures_tmp" + get_separator() + team_name + "-texture.png"
    path_player_texture = texture_path + "Textures_tmp" + get_separator() + team_name + "-" + player_name + "-texture.png"

    if gen_nb % soctool.my_change_texture_time == 0 and my_new_texture_:
        if i == 1:
            if team_name == "Team1":
                create_tmp_dir(soctool.my_path_dir, True)
            create_team_texture(soctool, texture_path, team_name, model_type)
        create_player_texure(path_team_texture, path_player_texture, team_name, soctool)
        
        
    if not os.path.isfile(path_player_texture):
        create_player_texure(path_team_texture, path_player_texture, team_name, soctool)

    apply_texture_to_player(player_name, path_player_texture)
    change_groundtruth_color(player_name, team_name, i)


# ------------------------------------------------------------------------
#
#    Armature
#
# ------------------------------------------------------------------------


def select_player_armature(obj):
    bpy.context.view_layer.objects.active = obj
    obj = bpy.context.active_object
    bpy.ops.object.select_grouped(type="CHILDREN_RECURSIVE")
    obj.select_set(True)
    return obj


def random_flip_armature(obj_to_flip):
    if bool_from_percent(50):
        #print("FLIP ->" + str(obj_to_flip.name))
        select_player_armature(obj_to_flip)
        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.copy()
        bpy.ops.pose.paste(flipped=True)
        bpy.ops.object.mode_set(mode="OBJECT")
    #else:
        #print("NO FLIP ->" + str(obj_to_flip.name))


def copy_paste_armature(obj_to_copy, obj_to_paste):
    obj = select_player_armature(obj_to_copy)
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.copy()
    bpy.ops.object.mode_set(mode="OBJECT")

    select_player_armature(obj_to_paste)
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.paste(flipped=False)
    bpy.ops.object.mode_set(mode="OBJECT")


def get_armature_model_goal(soctool):
    if bool_from_float_percent(soctool.my_ar_other): #5
        return "PlayerToCopy_other_" + str(random.randint(1, 2))

    if bool_from_percent(soctool.my_ar_running): #5
        return "PlayerToCopy_running_" + str(random.randint(1, 8))

    if bool_from_percent(soctool.my_ar_moving): #20
        return "PlayerToCopy_moving_" + str(random.randint(1, 8))

    if bool_from_percent(soctool.my_ar_walking): # 20
        return "PlayerToCopy_walking_" + str(random.randint(1, 10))
    return "PlayerToCopy_goaling_" + str(random.randint(1, 5))


def get_armature_model_player(running_prob, soctool, referee=False):
    if bool_from_float_percent(soctool.my_ar_p_other) and not referee:
        return "PlayerToCopy_other_" + str(random.randint(1, 1))

    if bool_from_percent(running_prob) and soctool.my_ar_p_running:
        return  "PlayerToCopy_running_" + str(random.randint(1, 8))

    if bool_from_percent(soctool.my_ar_p_moving):
        return "PlayerToCopy_moving_" + str(random.randint(1, 8))
    
    return "PlayerToCopy_walking_" + str(random.randint(1, 10))


# ------------------------------------------------------------------------
#
#    Goals & referee
#
# ------------------------------------------------------------------------


def generation_goal(soctool, gen_nb):
    goal1 = bpy_o["GoalMan1"]
    goal2 = bpy_o["GoalMan2"]
    goal_pos_1 = get_location_goal("goal1")
    goal_pos_2 = get_location_goal("goal2")

    move_goals(goal1, goal2, goal_pos_1, goal_pos_2)

    change_player_texture(soctool, "GoalBody1", "Team3", 1, gen_nb, "goal")
    change_player_texture(soctool, "GoalBody2", "Team4", 1, gen_nb, "goal")

    copy1 = bpy_o[outliner_structure[get_armature_model_goal(soctool)]]
    copy_paste_armature(copy1, goal1)
    goal1.location.z = copy1.location.z
    goal1.rotation_euler.x = copy1.rotation_euler.x
    random_flip_armature(goal1)
    random_scale(goal1)

    copy2 = bpy_o[outliner_structure[get_armature_model_goal(soctool)]]
    copy_paste_armature(copy2, goal2)
    goal2.location.z = copy2.location.z
    goal2.rotation_euler.x = copy2.rotation_euler.x
    random_flip_armature(goal2)
    random_scale(goal2)
    
    
def generation_referee(soctool, gen_nb, ball_y):
    player_type_tmp = get_armature_model_player(30, soctool, True)
    location = get_location_referee(ball_y)
    create_new_player_col(soctool, "Player5_1", 1, gen_nb, "Team5", player_type_tmp, location)


# ------------------------------------------------------------------------
#
#    Creating players
#
# ------------------------------------------------------------------------


def duplicate_player(new_col, team_name, collection_to_copy):
    global outliner_structure

    select_player_armature(bpy_o[outliner_structure[collection_to_copy]])

    bpy.ops.object.duplicate()
    dupli_obj = bpy.context.object

    body_name = get_body_name(dupli_obj)

    bpy_c[collection_to_copy].objects.unlink(bpy_o[body_name])
    bpy_c[collection_to_copy].objects.unlink(dupli_obj)

    new_col.objects.link(dupli_obj)
    new_col.objects.link(bpy_o[body_name])

    dupli_obj.name = "PlayerCopied"
    bpy_o[body_name].name = "PlayerCopiedBody"

    return dupli_obj


def create_new_player_col(soctool, col_name, i, gen_nb, team_name, collection_to_copy, location=[34.8, -54.591]):
    jitter_angle = soctool.my_rotation_jitter
    dir_path = soctool.my_path_dir
    new_col = bpy_c.new(name=col_name)

    bpy_c[team_name].children.link(new_col)

    new_player = duplicate_player(new_col, team_name, collection_to_copy)

    new_player.location.x = location[0]
    new_player.location.y = location[1]

    rotate_player(new_player, jitter_angle)
    change_player_texture(soctool, get_body_name(new_player), team_name, i, gen_nb, "player")

    random_flip_armature(new_player)
    random_scale(new_player)
    
    
def move_sun_ball(soctool, positions_choice_method):
    ball_location = get_location(positions_choice_method)
    sun_rotation = get_location_sun()

    if bool_from_percent(soctool.my_sun_chance):
        move_sun(sun_rotation)
    else:
        move_sun()

    move_ball(ball_location)
    return ball_location[1]


def new_generation(soctool, gen_nb, one_gen=True):
    positions_choice_method = choose_position_method(soctool)
    ball_y = move_sun_ball(soctool, positions_choice_method)
    sun_rdm_param()
    running_prob = random.randint(10, 90)

    #if one_gen:
    nb_players_1 = soctool.my_nb_player_team1 + 1
    nb_players_2 = soctool.my_nb_player_team2 + 1
    #else:
    #    nb_players_1 = int(gaussian_rdm(8, 3, 0, 10.99)) + 1
    #    nb_players_2 = int(gaussian_rdm(8, 3, 0, 10.99)) + 1

    for i in range(1, nb_players_1):
        player_type_tmp = get_armature_model_player(running_prob, soctool)
        #player_type_tmp = "PlayerToCopy_running_1"
        location = get_location(positions_choice_method)
        create_new_player_col(soctool, "Player1_" + str(i), i, gen_nb, "Team1", player_type_tmp, location)
        #print("Player1_" + str(i) + " = " + str(player_type_tmp))

    for i in range(1, nb_players_2):
        player_type_tmp = get_armature_model_player(running_prob, soctool)
        #player_type_tmp = "PlayerToCopy_running_1"
        location = get_location(positions_choice_method)
        create_new_player_col(soctool, "Player2_" + str(i), i, gen_nb, "Team2", player_type_tmp, location)
        #print("Player2_" + str(i) + " = " + str(player_type_tmp))
        
    generation_goal(soctool, gen_nb)
    generation_referee(soctool, gen_nb, ball_y)  


# ------------------------------------------------------------------------
#
#    Render
#
# ------------------------------------------------------------------------

#def change_view_port_shading(mode):
#    for window in bpy.context.window_manager.windows:
#        for area in window.screen.areas:  # iterate through areas in current screen
#            if area.type == "VIEW_3D":
#                for space in area.spaces:  # iterate through spaces in current VIEW_3D area
#                    if space.type == "VIEW_3D":  # check if space is a 3D view
#S                        space.shading.type = mode


def create_directories(path_dir):
    now = datetime.now()
    dt_str = now.strftime("%Y-%m-%d-_%H;%M;%S")
    path_full = path_dir + dt_str
    path_render = path_full + get_separator() + "render"
    path_groundtruth = path_full + get_separator() + "groundtruth"

    os.mkdir(path_full)
    os.mkdir(path_render)
    os.mkdir(path_groundtruth)

    return path_render, path_groundtruth


def create_final_directories(path_dir):
    path_full = path_dir + "final_render"
    path_render = path_full + get_separator() + "render"
    path_groundtruth = path_full + get_separator() + "groundtruth"

    if not os.path.exists(path_full):
        os.mkdir(path_full)
    if not os.path.exists(path_render):
        os.mkdir(path_render)
    if not os.path.exists(path_groundtruth):
        os.mkdir(path_groundtruth)

    return path_render, path_groundtruth


#def enable_armature_and_camera(bool):
#    bpy.context.space_data.show_object_viewport_armature = bool
#    bpy.context.space_data.show_object_viewport_camera = bool
#    bpy.context.space_data.show_object_viewport_light = bool


def render_in_render_mode(path_render, i):
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.display_settings.display_device = 'sRGB'

    bpy.context.scene.world.color = (0.050876, 0.050876, 0.050876)
    bpy.context.scene.render.filepath = path_render + get_separator() + str(i)
    bpy.ops.render.render(animation=False, write_still=True)


def render_in_solid_mode(path_groundtruth, i):
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.context.scene.display_settings.display_device = 'None'
    bpy.context.scene.display.render_aa = 'OFF'
    bpy.data.scenes['Scene'].display.shading.light = 'FLAT'
    bpy.context.scene.world.color = (1, 1, 1)
    
    bpy.context.scene.render.filepath = path_groundtruth + get_separator() + str(i)
    bpy.ops.render.render(animation=False, write_still=True)
    
    bpy.context.scene.display_settings.display_device = 'sRGB'
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.world.color = (0.050876, 0.050876, 0.050876)
    

def render_and_save(soctool, i, path_render="", path_groundtruth=""):
    center_camera()
    
    if i == 1:
        if soctool.my_new_texture:
            path_render, path_groundtruth = create_final_directories(soctool.my_path_dir)
        else:
            path_render, path_groundtruth = create_directories(soctool.my_path_dir)
    
    i_added = i + soctool.my_first_name_generation - 1
    render_in_render_mode(path_render, i_added)
    render_in_solid_mode(path_groundtruth, i_added)
    
    return path_render, path_groundtruth


# ------------------------------------------------------------------------
#
#    Scene Properties
#
# ------------------------------------------------------------------------


class MyProperties(PropertyGroup):
    my_generations: IntProperty(
        name="Generations :",
        description="Number of images generated",
        default=2,
        min=1,
        max=1000
    )

    my_sun_chance: IntProperty(
        name="Sun % change :",
        description="Chance of changing lignting position",
        default=30,
        min=0,
        max=100
    )

    my_nb_player_team1: IntProperty(
        name="Nb of team1 players :",
        description="Number of players in team1",
        default=10,
        min=1,
        max=10
    )

    my_nb_player_team2: IntProperty(
        name="Nb of team2 players :",
        description="Number of players in team2",
        default=10,
        min=1,
        max=10
    )

    my_rotation_jitter: IntProperty(
        name="Max angle player jitter :",
        description="The maximum of jitter angle applied to one player ",
        default=80,
        min=0,
        max=180
    )

    my_path_dir: StringProperty(
        name="Save directory",
        description="Choose a directory:",
        default="D:\TFM_Images\\",
        maxlen=1024,
        subtype="DIR_PATH"
    )

    my_sw_striped: IntProperty(
        name="Striped % :",
        description="Percentage of chance that the shirt is striped",
        default=40,
        min=0,
        max=100
    )

    my_sw_vertical: IntProperty(
        name="Vertical % :",
        description="Percentage of chance that the shirt is striped vertically (if not it's horizontaly)",
        default=67,
        min=0,
        max=100
    )

    my_sw_pants_same_color_full: IntProperty(
        name="Pants same color full % :",
        description="Percentage of chance that pants have same colors as the shirt (for full shirt)",
        default=25,
        min=0,
        max=100
    )

    my_sw_pants_same_color_stiped: IntProperty(
        name="Pants same color stiped % :",
        description="Percentage of chance that pants have same colors as the shirt (for striped shirt)",
        default=90,
        min=0,
        max=100
    )
    my_change_texture_time: IntProperty(
        name="Change texture every x render :",
        description="Number of render before changing textures (every change = 20sec)",
        default=10,
        min=1,
        max=100
    )
    my_new_texture: BoolProperty(
        name="New texture",
        description="Generate new texture for players",
        default=True
    )
    my_real_gen: BoolProperty(
        name="Use the final directory",
        description="Use the final directory and not a temporary one",
        default=False
    )
    my_first_name_generation: IntProperty(
        name="First png name :",
        description="First png name (used for mutliple generations)",
        default=1,
        min=1,
        max=100000
    )
    my_lm_random: IntProperty(
        name="Random location chance % :",
        description="Chances to choose the random location method",
        default=5,
        min=0,
        max=100
    )
    my_lm_squares: IntProperty(
        name="Square location chance % :",
        description="Chances to choose the square location method",
        default=30,
        min=0,
        max=100
    )
    my_skin_referee: IntProperty(
        name="Referee dark skin  % :",
        description="Chances for the referee to have a dark skin",
        default=5,
        min=0,
        max=100
    )
    my_skin_player: IntProperty(
        name="Plyer dark skin  % :",
        description="Chances for the players to have a dark skin",
        default=50,
        min=0,
        max=100
    )
    my_ar_other: IntProperty(
        name="Armature goal other % :",
        description="Chances for the goals to have a other armature",
        default=5,
        min=0,
        max=100
    )
    my_ar_running: IntProperty(
        name="Armature goal running % :",
        description="Chances for the goals to have a running armature",
        default=5,
        min=0,
        max=100
    )
    my_ar_moving: IntProperty(
        name="Armature goal moving % :",
        description="Chances for the goals to have a moving armature",
        default=20,
        min=0,
        max=100
    )
    my_ar_walking: IntProperty(
        name="Armature goal walking % :",
        description="Chances for the goals to have a walking armature",
        default=20,
        min=0,
        max=100
    )
    my_ar_p_other: FloatProperty(
        name="Armature player other % :",
        description="Chances for the players to have a other armature",
        default=0.17,
        min=0.00,
        max=100.00,
    )
    my_ar_p_moving: IntProperty(
        name="Armature player moving % :",
        description="Chances for the players to have a moving armature",
        default=15,
        min=0,
        max=100
    )
    my_ar_p_running: BoolProperty(
        name="Armature player running method",
        description="Disable or not running armature for players",
        default=True
    )


# ------------------------------------------------------------------------
#
#    Operators
#
# ------------------------------------------------------------------------


class SP_OT_Clean_Scene(Operator):
    '''This will clean all components generated and replace the basics ones'''

    bl_label = "Clean the scene"
    bl_idname = "sp.clean_scene"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        clear_scene(soctool.my_path_dir)
        return {"FINISHED"}


class SP_OT_Open_Images_Dir(Operator):
    '''This will open the directory where are all the images'''

    bl_label = "Open img dir"
    bl_idname = "sp.open_images_dir"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        subprocess.Popen(r"explorer /open," + soctool.my_path_dir)
        return {"FINISHED"}


class SP_OT_Generate(Operator):
    '''This will generate the players and the ball'''

    bl_label = "Generate"
    bl_idname = "sp.generate"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        now = time.time()
        clear_scene(soctool.my_path_dir)
        print("Clear in : ", time.time() - now, "s")

        now = time.time()
        new_generation(soctool, 0, True)
        print("Generation in : ", time.time() - now, "s")

        return {"FINISHED"}


class SP_OT_Render(Operator):
    '''This will do a render and save it'''

    bl_label = "Render"
    bl_idname = "sp.render"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        render_and_save(soctool, 1)
        return {"FINISHED"}


class SP_OT_Generate_And_Render(Operator):
    '''This will generate the players, ball ... and do a render + save'''

    bl_label = "Generate and render"
    bl_idname = "sp.generate_and_render"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        clear_scene(soctool.my_path_dir)
        new_generation(soctool, 0, True)
        render_and_save(soctool, 1)
        return {"FINISHED"}


class SP_OT_Generate_And_Render_Many(Operator):
    '''This will generate the players, ball ... and do a render + save x times'''

    bl_label = "Generate and render"
    bl_idname = "sp.generate_and_render_many"

    def execute(self, context):
        scene = context.scene
        soctool = scene.soccer_tool

        path_render = None
        path_groundtruth = None

        for i in range(soctool.my_generations):
            now = time.time()
            
            clear_scene(soctool.my_path_dir)
            print("Clear in : ", time.time() - now, "s")
            new_generation(soctool, i, False)
            print("Generation at : ", time.time() - now, "s")
            path_render, path_groundtruth = render_and_save(soctool, i + 1, path_render, path_groundtruth)
            print("Render at : ", time.time() - now, "s")
            
        return {"FINISHED"}


# ------------------------------------------------------------------------
#
#    Panel in Object Mode
#
# ------------------------------------------------------------------------


class OBJECT_PT_SoccerPanel(Panel):
    bl_idname = "OBJECT_PT_soccer_panel"
    bl_label = "SoccerPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Soccer Tab"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        soctool = scene.soccer_tool

        layout.label(text="Tools")
        box = layout.box()
        box.operator("sp.clean_scene")
        box.prop(soctool, "my_path_dir")
        box.operator("sp.open_images_dir")
        box.prop(soctool, "my_first_name_generation")

        layout.label(text="Parameters")
        box = layout.box()
        box.prop(soctool, "my_sun_chance")
        box.prop(soctool, "my_rotation_jitter")
        box.prop(soctool, "my_nb_player_team1")
        box.prop(soctool, "my_nb_player_team2")
        box.prop(soctool, "my_change_texture_time")

        layout.label(text="Sport wear parameters")
        box = layout.box()
        box.prop(soctool, "my_sw_striped")
        box.prop(soctool, "my_sw_vertical")
        box.prop(soctool, "my_sw_pants_same_color_full")
        box.prop(soctool, "my_sw_pants_same_color_stiped")
        
        layout.label(text="Skin color")
        box = layout.box()
        box.prop(soctool, "my_skin_referee")
        box.prop(soctool, "my_skin_player")
        
        layout.label(text="Location method")
        box = layout.box()
        box.prop(soctool, "my_lm_random")
        box.prop(soctool, "my_lm_squares")
        
        layout.label(text="Goals armature")
        box = layout.box()
        box.prop(soctool, "my_ar_other")
        box.prop(soctool, "my_ar_running")
        box.prop(soctool, "my_ar_moving")
        box.prop(soctool, "my_ar_walking")
        
        layout.label(text="Players armature")
        box = layout.box()
        box.prop(soctool, "my_ar_p_other")
        box.prop(soctool, "my_ar_p_running")
        box.prop(soctool, "my_ar_p_moving")

        layout.label(text="One time")
        box = layout.box()
        box.prop(soctool, "my_new_texture")
        box.operator("sp.generate")
        box.operator("sp.render")
        box.operator("sp.generate_and_render")

        layout.label(text="Many times")
        box = layout.box()
        box.prop(soctool, "my_real_gen")
        box.prop(soctool, "my_generations")
        box.operator("sp.generate_and_render_many")


# ------------------------------------------------------------------------
#
#    Registration
#
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    SP_OT_Clean_Scene,
    SP_OT_Open_Images_Dir,
    SP_OT_Generate,
    SP_OT_Render,
    SP_OT_Generate_And_Render,
    SP_OT_Generate_And_Render_Many,
    OBJECT_PT_SoccerPanel
)


def register():
    print("Registered")
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.soccer_tool = PointerProperty(type=MyProperties)


def unregister():
    print("Unregistered")
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.soccer_tool


if __name__ == "__main__":
    register()
    # unregister()
