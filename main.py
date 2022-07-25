import const
from board_extraction import calib, transform_point
from dart_extraction import get_dart_coordinates, get_dart_score

import cv2
import numpy as np

def img_read_resize(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (const.length, const.width))
    return img

# Load the images
img_board = img_read_resize(const.path_board) 
img_dart = img_read_resize(const.path_dart) 

transformation_matrix = calib(img_board)

dart_coordinates = get_dart_coordinates(img_board, img_dart)

dart_coordinates_transformed = transform_point(dart_coordinates, transformation_matrix, img_board)

get_dart_score(dart_coordinates_transformed)

