# Hier ganze Kalibrierung  

import cv2
import const
# from board_extraction import calib_camera, deserialize_calib, serialize_calib
from board_extraction import *#transform_point#, transformation_matrices

## Bild laden

def img_read_resize(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (const.length, const.width))
    return img


# single Dart Test:
img_board = img_read_resize(const.path_board) 

# transformation_matrix = calib_camera(img_board, 0)
while(True):
    if(calib_camera(img_board, 0) == 'no'):
        break

serialize_calib()
print(transformation_matrices)

# deserialize_calib()
# print(transformation_matrices)