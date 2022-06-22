import const
import cv2
import numpy as np
import matplotlib.pyplot as plt

pressed = False

x_pressed = 0
y_pressed = 0


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here and save point
       print('pressed: x = %d, y = %d'%(x, y))
       global x_pressed
       x_pressed = x
       global y_pressed
       y_pressed = y 
       global pressed 
       pressed = True
    #    global img
    #    img = cv2.circle(img, (x_pressed,y_pressed), radius=5, color=(0,0,255), thickness=1)
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
            # break 
            print('x = %d, y = %d'%(x_pressed, y_pressed))   
            calib_img = cv2.circle(calib_img, (x_pressed,y_pressed), radius=5, color=(0,0,255), thickness=1)
            pressed = False
            cv2.destroyAllWindows()
            break
        cv2.waitKey(0)
    
def calib_20_1(calib_img):
    click_point_calib("20_1", calib_img)
    return [x_pressed, y_pressed]
    
def calib_19_3(calib_img):
    click_point_calib("19_3", calib_img)
    return [x_pressed, y_pressed]
    
def calib_11_14(calib_img):
    click_point_calib("11_14", calib_img)
    return [x_pressed, y_pressed]
    
def calib_6_10(calib_img):
    click_point_calib("6_10", calib_img)
    return [x_pressed, y_pressed]

def calib(img_board):    
    
    calib_img = img_board

    point_20_1 = calib_20_1(calib_img)
    print('Calib Point 20_1 coordinates: x = %d, y = %d'%(point_20_1[0], point_20_1[1]))    
        
    point_19_3 = calib_19_3(calib_img)
    print('Calib Point 19_3 coordinates: x = %d, y = %d'%(point_19_3[0], point_19_3[1]))    
        
    point_11_14 = calib_11_14(calib_img)
    print('Calib Point 11_14 coordinates: x = %d, y = %d'%(point_11_14[0], point_11_14[1]))    
        
    point_6_10 = calib_6_10(calib_img)
    print('Calib Point 6_10 coordinates: x = %d, y = %d'%(point_6_10[0], point_6_10[1]))    


# Specify input and output coordinates that is used
# to calculate the transformation matrix

    const.crop_size = 500
    half = int(const.crop_size /2)

    # set transformations points -> input & output
    input_pts = np.float32( [point_20_1,    point_6_10,     point_19_3,     point_11_14])
    output_pts = np.float32([[half, 0],     [const.crop_size, half],   [half, const.crop_size],   [0, half]])

    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts,output_pts) #ToDo: serialisieren

    # Apply the perspective transformation to the image
    out = cv2.warpPerspective(img_board,M,(img_board.shape[1], img_board.shape[0]),flags=cv2.INTER_LINEAR)

    cv2.circle(out,(half,half), half, (0,0,255), 2)
    out = out[0:const.crop_size, 0:const.crop_size]

    out = cv2.circle(out, (half,half), radius=7, color=(255,0,0), thickness=2)

    print("Rotation matrix:")
    print(M)

    # Display the transformed image
    cv2.imshow("image", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return M 


def transform_point(p, M, img):
    
    out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

    const.crop_size = 500
    half = int(const.crop_size / 2)

    cv2.circle(out,(half,half), half, (0,0,255), 2)
    out = out[0:const.crop_size, 0:const.crop_size]

    # Transformation through Matrix-Vector-multiplication
    px = (M[0][0]*p[0] + M[0][1]*p[1] + M[0][2]) / ((M[2][0]*p[0] + M[2][1]*p[1] + M[2][2]))
    py = (M[1][0]*p[0] + M[1][1]*p[1] + M[1][2]) / ((M[2][0]*p[0] + M[2][1]*p[1] + M[2][2]))
    p_transf = (int(px), int(py))
    print("transformed point:")
    print(p_transf)
    
    #draw transformed point
    out = cv2.circle(out, p_transf, radius=7, color=(0,255,0), thickness=2)
    
    cv2.imshow("image", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return p_transf