# import cv2

path = 'C:\\Users\\timis\\OneDrive\\Desktop\\DartsTracker\\TestPictures\\testaufbau_dart1.jpg'
# path = 'C:\\Users\\timis\\OneDrive\\Desktop\\DartsTracker\\TestPictures\\testaufbau_board.jpg'
# path = 'TestPictures\\testaufbau_dart1.jpg'


import cv2
import numpy as np
import matplotlib.pyplot as plt

# To open matplotlib in interactive mode
# %matplotlib qt

# Load the image
img = cv2.imread(path) 
dimensions = img.shape
print(dimensions)
img = cv2.resize(img, (960, 540))

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
       global img
       img = cv2.circle(img, (x_pressed,y_pressed), radius=5, color=(0,0,255), thickness=1)
       cv2.destroyAllWindows()

def click_point_calib(window_name):    
    global img 
    global pressed
    global x_pressed
    global y_pressed 
    while True:
        cv2.imshow(window_name, img)
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, onMouse)
        if(pressed):
            # break 
            print('x = %d, y = %d'%(x_pressed, y_pressed))   
            img = cv2.circle(img, (x_pressed,y_pressed), radius=5, color=(0,0,255), thickness=1)
            pressed = False
            cv2.destroyAllWindows()
            break
        cv2.waitKey(0)
    
def calib_20_1():
    click_point_calib("20_1")
    return [x_pressed, y_pressed]
    
def calib_19_3():
    click_point_calib("19_3")
    return [x_pressed, y_pressed]
    
def calib_11_14():
    click_point_calib("11_14")
    return [x_pressed, y_pressed]
    
def calib_6_10():
    click_point_calib("6_10")
    return [x_pressed, y_pressed]
    
point_20_1 = calib_20_1()
print('Calib Point 20_1 coordinates: x = %d, y = %d'%(point_20_1[0], point_20_1[1]))    
    
point_19_3 = calib_19_3()
print('Calib Point 19_3 coordinates: x = %d, y = %d'%(point_19_3[0], point_19_3[1]))    
    
point_11_14 = calib_11_14()
print('Calib Point 11_14 coordinates: x = %d, y = %d'%(point_11_14[0], point_11_14[1]))    
    
point_6_10 = calib_6_10()
print('Calib Point 6_10 coordinates: x = %d, y = %d'%(point_6_10[0], point_6_10[1]))    

# Specify input and output coordinates that is used
# to calculate the transformation matrix

crop_size = 500
cs = 250

#evtl gehen auch mehr als 4 Punkte?
input_pts = np.float32([point_20_1,point_6_10,point_19_3,point_11_14])
output_pts = np.float32([[cs,crop_size],[crop_size,cs],[cs,0],[0,cs]])

# Compute the perspective transform M
M = cv2.getPerspectiveTransform(input_pts,output_pts)

# print(M)

# Apply the perspective transformation to the image
out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

radius = crop_size / 2
cv2.circle(out,(cs,cs), cs, (0,0,255), 2)
out = out[0:crop_size, 0:crop_size]

out = cv2.circle(out, (cs,cs), radius=7, color=(255,0,0), thickness=2)

# # Display the transformed image
cv2.imshow("image", out)
cv2.waitKey(0)
cv2.destroyAllWindows()


# [[-6.47189911e+00  6.20898423e+00  3.86857625e+03]
#  [-1.11760605e+00  2.37582334e+01 -2.55604927e+03]
#  [-2.86502475e-04  3.38309159e-02  1.00000000e+00]]

# converting point with Matrix:
# T = [200,200,1]*M


# A = np.array([200,200,1])
# T = np.matmul(M, A)
# print(T)