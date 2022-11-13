# Hier ganze Kalibrierung  

import cv2
import const
# from board_extraction import calib_camera, deserialize_calib, serialize_calib
from board_extraction import *#transform_point#, transformation_matrices

## Bild laden

# def img_read_resize(path):
#     img = cv2.imread(path)
#     img = cv2.resize(img, (const.length, const.width))
#     return img


# # single Dart Test:
# img_board = img_read_resize(const.path_board) 

# # transformation_matrix = calib_camera(img_board, 0)
# while(True):
#     if(calib_camera(img_board, 0) == 'no'):
#         break

# serialize_calib()
# cap1 = cv2.VideoCapture(1)
# cap2 = cv2.VideoCapture(2)
# cap3 = cv2.VideoCapture(3)
# ret, board_img_1 = cap1.read()
# ret, board_img_2 = cap2.read()
# ret, board_img_3 = cap3.read()
# # cv2.imshow("w", board_img_1)
# # cv2.waitKey(0)

# # board_img_1 = cv2.resize(board_img_1, (const.length, const.width))
# # board_img_2 = cv2.resize(board_img_2, (const.length, const.width))
# # board_img_3 = cv2.resize(board_img_3, (const.length, const.width))

# calib(board_img_1, board_img_2, board_img_3)

# print(transformation_matrices)

# m1= [[ 1.00099485e+00 -1.98280893e+00  4.00803123e+02],
#  [ 1.65587082e+00  4.67956195e+00 -8.73932596e+02],
#  [ 4.39194744e-04  7.09178539e-03  1.00000000e+00]]

a = deserialize_calib()
print(a[0])
# print(transformation_matrices)