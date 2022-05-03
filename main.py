import imghdr
import cv2
import time


import cv2
import time
cam = cv2.VideoCapture(1)
# cam.set(3, 640)
# cam.set(4, 480)

#-----------------------------------------------------------------------------------------
# jede s 1 Bild machen

# Initialise variables to store current time difference as well as previous time call value
previous = time.time()
delta = 0

images = []  # list of images
counter = 0
timediff_in_sec = 1
# Keep looping
while True:
    # Get the current time, increase delta and update the previous variable
    current = time.time()
    delta += current - previous
    previous = current

    if delta > timediff_in_sec:
        # Operations on image
        cv2.imshow("Frame", img)
        cv2.waitKey(1)
        
        images.append(img)
        # images[counter % num_of_images] = img
        counter = counter + 1
        # Reset the time counter
        delta = 0
        
    if counter >= 10:
        del images[0] # delete first element of imagelist
        break 
        
    
    _, img = cam.read()  # Show the image and keep streaming
    
#---------------------------------------------------------------------------------

# darts = []

# while True:
#     if cv2.waitKey(1) & 0xFF == ord('b'):
#         # background = cam.read()
#         # cv2.imshow("Frame", background)
#         print("b")
#     if cv2.waitKey(1) & 0xFF == ord('d'):
#         darts.append(cam.read())  
#         cv2.imshow("Frame", darts)
        
#     if cv2.waitKey(1) & 0xFF == ord('e'):    
#         break
    

# print("test")


cam.release()
cv2.destroyAllWindows()


# compute difference
difference = cv2.subtract(images[0], images[1])

# color the mask red
Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
difference[mask != 255] = [0, 0, 255]


while (True):
    cv2.imshow("Frame", difference)
    #Waits for a user input to quit the application    
    if cv2.waitKey(1) & 0xFF == ord('q'):    
        break
