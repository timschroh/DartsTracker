import const
import cv2
import numpy as np

from tkinter import messagebox, Tk

pressed = False

x_pressed = 0
y_pressed = 0

transformation_matrices = [np.empty((3,3)),np.empty((3,3)),np.empty((3,3))]

import os
def serialize_calib():
    global transformation_matrices
    
    # alte calib löschen
    if (os.path.exists(const.path_calib)):
        os.remove(const.path_calib)
    fd = os.open(const.path_calib, os.O_RDWR|os.O_CREAT )
    print("vorm Speichern:")
    print(transformation_matrices)
    np.save(const.path_calib, transformation_matrices)
    os.close(fd)
    return

def deserialize_calib():
    global transformation_matrices
    transformation_matrices = np.load(const.path_calib)
    print("nachm Laden:")
    print(transformation_matrices)
    return transformation_matrices


def calib(board_img_1, board_img_2, board_img_3):

    while(True):
        if(calib_camera(board_img_1, 1) == 'no'):
            break
    while(True):
        if(calib_camera(board_img_2, 2) == 'no'):
            break
    while(True):
        if(calib_camera(board_img_3, 3) == 'no'):
            break

    serialize_calib()
    


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('pressed: x = %d, y = %d'%(x, y))
        global x_pressed
        x_pressed = x
        global y_pressed
        y_pressed = y 
        global pressed 
        pressed = True
        cv2.destroyAllWindows()

def click_point_calib(window_name, calib_img):    
    global pressed
    global x_pressed
    global y_pressed 
    while True:
        cv2.imshow(window_name, calib_img)
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, onMouse)
        if(pressed):
            print('x = %d, y = %d'%(x_pressed, y_pressed))   
            pressed = False
            cv2.destroyAllWindows()
            break
        cv2.waitKey(0)
    
def img_read_resize(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (const.length, const.width))
    return img

def calib_camera(img, cam_nr):    
    
    img_board = cv2.resize(img, (const.length, const.width))
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ calib 20/1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    coord_20_1_cam1 = [241,100]
    coord_20_1_cam2 = [733,144]
    coord_20_1_cam3 = [394,377]
    calib_img_20_1 = img_board
    if (cam_nr == 1):     
        coord = coord_20_1_cam1
    elif (cam_nr == 2):     
        coord = coord_20_1_cam2
    elif (cam_nr == 3):     
        coord = coord_20_1_cam3
    
    calib_img_20_1 = cv2.circle(calib_img_20_1, coord, radius=30, color=(255,0,0), thickness=3)
    click_point_calib("Kalbrierung Kamer Nr. " + str(cam_nr) + ": Aeussersten Punkt der 20|1 Grenze anklicken", calib_img_20_1)
    point_20_1 = [x_pressed, y_pressed]
    
    print('Calib Point 20_1 coordinates: x = %d, y = %d'%(point_20_1[0], point_20_1[1])) 
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ calib 219/3 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    coord_19_3_cam1 = [779,227]
    coord_19_3_cam2 = [142,235]
    coord_19_3_cam3 = [483,112]
    calib_img_19_3  = img_board#= img_read_resize(const.path_board) 

    if (cam_nr == 1):     
        coord = coord_19_3_cam1
    elif (cam_nr == 2):     
        coord = coord_19_3_cam2
    elif (cam_nr == 3):     
        coord = coord_19_3_cam3
    
    calib_img_20_1 = cv2.circle(calib_img_20_1, coord, radius=30, color=(0,255,0), thickness=3)
    calib_img_19_3 = cv2.circle(calib_img_19_3, coord, radius=30, color=(255,0,0), thickness=3)
    
    click_point_calib("Kalbrierung Kamer Nr. " + str(cam_nr) + ": Aeussersten Punkt der 19|3 Grenze anklicken", calib_img_19_3)
    point_19_3 = [x_pressed, y_pressed]
    
    print('Calib Point 19_3 coordinates: x = %d, y = %d'%(point_19_3[0], point_19_3[1])) 
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ calib 11/14 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    coord_11_14_cam1 = [175,291]
    coord_11_14_cam2 = [398,109]
    coord_11_14_cam3 = [774,214]
    calib_img_11_14 = img_board#img_read_resize(const.path_board) 
    if (cam_nr == 1):     
        coord = coord_11_14_cam1
    elif (cam_nr == 2):     
        coord = coord_11_14_cam2
    elif (cam_nr == 3):     
        coord = coord_11_14_cam3
    
    calib_img_19_3 = cv2.circle(calib_img_19_3, coord, radius=30, color=(0,255,0), thickness=3)
    calib_img_11_14 = cv2.circle(calib_img_11_14, coord, radius=30, color=(255,0,0), thickness=3)
    click_point_calib("Kalbrierung Kamer Nr. " + str(cam_nr) + ": Aeussersten Punkt der 11|14 Grenze anklicken", calib_img_11_14)
    point_11_14 = [x_pressed, y_pressed]
    
    print('Calib Point 11_14 coordinates: x = %d, y = %d'%(point_11_14[0], point_11_14[1])) 
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ calib 6/10 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    coord_6_10_cam1 = [602,65]
    coord_6_10_cam2 = [656,333]
    coord_6_10_cam3 = [162,178]
    calib_img_6_10  = img_board# = img_read_resize(const.path_board)  #?
    if (cam_nr == 1):     
        coord = coord_6_10_cam1
    elif (cam_nr == 2):     
        coord = coord_6_10_cam2
    elif (cam_nr == 3):     
        coord = coord_6_10_cam3
    
    calib_img_11_14 = cv2.circle(calib_img_11_14, coord, radius=30, color=(0,255,0), thickness=3)
    calib_img_6_10 = cv2.circle(calib_img_6_10, coord, radius=30, color=(255,0,0), thickness=3)
    click_point_calib("Kalbrierung Kamer Nr. " + str(cam_nr) + ": Aeussersten Punkt der 6|10 Grenze anklicken", calib_img_6_10)
    point_6_10 = [x_pressed, y_pressed]
    
    print('Calib Point 6_10 coordinates: x = %d, y = %d'%(point_6_10[0], point_6_10[1])) 

    calib_img_6_10 = cv2.circle(calib_img_6_10, coord, radius=30, color=(0,255,0), thickness=3)

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ transformation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Specify input and output coordinates that is used
# to calculate the transformation matrix

    const.crop_size = 500
    half = int(const.crop_size /2)

    # set transformations points -> input & output
    input_pts = np.float32([point_20_1,    point_6_10,     point_19_3,     point_11_14])
    output_pts = np.float32([[half, 0],     [const.crop_size, half],   [half, const.crop_size],   [0, half]])

    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts,output_pts) 
    
    # save transformation Matrix for serialization
    transformation_matrices[cam_nr-1] = M

    # Apply the perspective transformation to the image
    out = cv2.warpPerspective(img_board,M,(img_board.shape[1], img_board.shape[0]),flags=cv2.INTER_LINEAR)

    cv2.circle(out,(half,half), half, (255,0,0), 2) # ideale Aussenkontur einzeichnen
    out = out[0:const.crop_size, 0:const.crop_size]
    out = cv2.circle(out, (half,half), radius=7, color=(255,0,0), thickness=2) # ideales Bullseye einzechnen

    print("Rotation matrix:")
    print(M)
        
    cv2.namedWindow("image")
    cv2.imshow("image", out)
    
    root = Tk()
    root.withdraw()
    mb_answer = messagebox.askquestion("Kalibrierergebnis Kamera " + str(cam_nr), "Kalibrierung von Kamera " + str(cam_nr) + " wiederholen?")
    root.destroy()
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return mb_answer
    
    #return M 

def transform_point(p, M, img):
    
    out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

    const.crop_size = 500
    half = int(const.crop_size / 2)

    cv2.circle(out,(half,half), half, (0,0,255), 2)
    out = out[0:const.crop_size, 0:const.crop_size]
    print(M)
    # Transformation through Matrix-Vector-multiplication
    px = (M[0][0]*p[0] + M[0][1]*p[1] + M[0][2]) / ((M[2][0]*p[0] + M[2][1]*p[1] + M[2][2]))
    py = (M[1][0]*p[0] + M[1][1]*p[1] + M[1][2]) / ((M[2][0]*p[0] + M[2][1]*p[1] + M[2][2]))
    p_transf = (int(px), int(py))
    print("transformed point:")
    print(p_transf)
    
    #draw transformed point
    out = cv2.circle(out, p_transf, radius=7, color=(0,255,0), thickness=2)
    
    # cv2.imshow("image", out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return p_transf




