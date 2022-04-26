import cv2
import time

cam = cv2.VideoCapture(1)



# Capture frame-by-frame    
ret, frame = cam.read() 

cv2.imshow('frame', frame)



while (True):
    #Waits for a user input to quit the application    
    if cv2.waitKey(1) & 0xFF == ord('q'):    
        break

#cam.release()
#cv2.destroyAllWindows()