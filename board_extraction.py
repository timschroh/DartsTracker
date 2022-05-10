# import cv2

path = 'C:\\Users\\timis\\OneDrive\\Desktop\\DartsTracker\\board_testpicture.jpg'

# img = cv2.imread('C:\\Users\\timis\\OneDrive\\Desktop\\DartsTracker\\board_testpicture.jpg', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# import numpy as np
# import cv2 as cv
# im = cv.imread(path)
# imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# ret, thresh = cv.threshold(imgray, 127, 255, 0)
# im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# cv.imshow('image',im2)
# cv.waitKey(0)
# cv.destroyAllWindows()


import cv2
import numpy as np
import matplotlib.pyplot as plt

# To open matplotlib in interactive mode
# %matplotlib qt

# Load the image
img = cv2.imread(path) 

# Create a copy of the image
img_copy = np.copy(img)

# Convert to RGB so as to display via matplotlib
# Using Matplotlib we can easily find the coordinates
# of the 4 points that is essential for finding the 
# transformation matrix
img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       # draw circle here (etc...)
       print('x = %d, y = %d'%(x, y))
       cv2.destroyAllWindows() 

cv2.imshow("image", img)
cv2.namedWindow('image')
cv2.setMouseCallback('image', onMouse)


cv2.waitKey(0)
cv2.destroyAllWindows()

# # Specify input and output coordinates that is used
# # to calculate the transformation matrix
# input_pts = np.float32([[80,1286],[3890,1253],[3890,122],[450,115]])
# output_pts = np.float32([[100,100],[100,3900],[2200,3900],[2200,100]])

# # Compute the perspective transform M
# M = cv2.getPerspectiveTransform(input_pts,output_pts)

# # Apply the perspective transformation to the image
# out = cv2.warpPerspective(img,M,(img.shape[1], img.shape[0]),flags=cv2.INTER_LINEAR)

# # Display the transformed image
# plt.imshow(out)