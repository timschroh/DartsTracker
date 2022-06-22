import const
from board_extraction import calib, transform_point
from dart_extraction import get_dart_coordinates, get_dart_score

import cv2
import numpy as np

# Load the image
img_board = cv2.imread(const.path_board) 
img_board = cv2.resize(img_board, (const.length, const.width)) # muss iwo einheitlich passieren

img_dart = cv2.imread(const.path_dart)
img_dart = cv2.resize(img_dart, (const.length, const.width)) # muss iwo einheitlich passieren

transformation_matrix = calib(img_board)

dart_coordinates = get_dart_coordinates(img_board, img_dart)

dart_coordinates_transformed = transform_point(dart_coordinates, transformation_matrix, img_board)

get_dart_score(dart_coordinates_transformed)

