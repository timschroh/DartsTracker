import cv2

# path = "C:\\Users\\timis\\OneDrive\\Desktop\\DartsTracker\\TestPictures"
path = "TestPictures"
im0 = cv2.imread(path + "\\tp0.jpg") 
im1 = cv2.imread(path + "\\tp1.jpg") 
# im1 = cv2.imread(path + "\\tp2.jpg") 
# im1 = cv2.imread(path + "\\tp3.jpg") 


# compute difference
dif01 = cv2.subtract(im0, im1)

# color the mask white
Conv_hsv_Gray = cv2.cvtColor(dif01, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(Conv_hsv_Gray, 50, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
dif01[mask != 255] = [255, 255, 255]


blur = cv2.medianBlur(dif01,5) #blur image to erase thin lines
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # grayscale

corners = cv2.goodFeaturesToTrack(gray, 500, 0.05, 1) # track corners
import numpy as np
corners = np.int0(corners)

# anzC = len(corners) # evtl für späteres feature? (+ Seitenverhältnis/kleinstes Dreieck?)
    
lowest_point = corners[0] # to find lowest corner --> tip of the dart

for corner in corners:
    x, y = corner.ravel()
#     cv2.circle(im1, (x, y), 3, (255, 0, 0), -1) #draw every corner found white
    
    # find lowest point:
    x_low, y_low = lowest_point.ravel()
    if (y > y_low):
        lowest_point = corner
        
        
print(lowest_point)
x_low, y_low = lowest_point.ravel()
cv2.circle(im1, (x_low, y_low), 4, (0, 0, 255), 2) # circle lowest corner red

cv2.imshow("shapes", im1)
cv2.waitKey(0)
cv2.destroyAllWindows()