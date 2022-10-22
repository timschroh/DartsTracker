import cv2
import const


def get_dart_coordinates(im0, im1):
    
    #compute difference between images
    dif01 = cv2.subtract(im0, im1)

    # color the mask white
    Conv_hsv_Gray = cv2.cvtColor(dif01, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 50, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    dif01[mask != 255] = [255, 255, 255]

    # ToDo: parameter bisschen anpassen, um Pfeil besser zu erkennen
    blur = cv2.medianBlur(dif01,5) #blur image to erase thin lines
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # grayscale

    corners = cv2.goodFeaturesToTrack(gray, 500, 0.05, 1) # track corners
    import numpy as np
    corners = np.int0(corners)

    # anzC = len(corners) # ToDo: evtl für späteres feature? (+ Seitenverhältnis/kleinstes Dreieck?) --> schaun obs n dartpfeil ist
        
    lowest_point = corners[0] # to find lowest corner --> tip of the dart

    for corner in corners:
        x, y = corner.ravel()
    #     cv2.circle(im1, (x, y), 3, (255, 0, 0), -1) #draw every corner found white
        
        # find lowest point:
        x_low, y_low = lowest_point.ravel()
        if (y > y_low):
            lowest_point = corner
            
            
    #print(lowest_point)
    x_low, y_low = lowest_point.ravel()
    cv2.circle(im1, (x_low, y_low), 4, (0, 0, 255), 2) # circle lowest corner red

    # cv2.imshow("shapes", im1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    
    point_of_darttip = (x_low, y_low)
    return point_of_darttip

import math
import numpy as np

from enum import Enum
class field_types(Enum):
    MISS = 1
    SINGLE = 2
    DOUBLE = 3
    TRIPLE = 4

def get_dart_score(p):
    
    half = int(const.crop_size / 2)
    bullseye_coord = (half,half)
    print()
    dif_1 = p[0] - bullseye_coord[0]
    dif_2 = p[1] - bullseye_coord[1]
    dist = math.sqrt(dif_1**2 + dif_2**2)
    # print("unscaled distance from dart to bullseye:")
    # print(dist)
    
    # distanz mit 3Satz auf echte Maße skalieren
    dartboard_lenth = 340
    scaled_dist = dist /const.crop_size * dartboard_lenth 
    print("scaled distance from dart to bullseye:")
    print(scaled_dist)
    
    p_shiftet = (p[0] - bullseye_coord[0], p[1] - bullseye_coord[1])

    ang = np.arctan2(*p_shiftet[::-1])
    angle_clockwise = np.rad2deg((ang) % (2 * np.pi)) + 90 # oben zwischen 20|1 ist 0 Grad
    
    print("angle clockwise:")
    print(angle_clockwise)
    
    field_degrees = 360 / 20 # = 18°
    field_number = int(angle_clockwise/field_degrees)
    #print(field_number)
    
    # map the score to the fields clockwise, beginning on top
    # 1 – 18 – 4 − 13 – 6 – 10 – 15 – 2 – 17 – 3 – 19 – 7 – 16 – 8 – 11 – 14 – 9 – 12 – 5 - 20
    dict = {0 : 1,
            1 : 18,
            2 : 4,
            3 : 13,
            4 : 6,
            5 : 10,
            6 : 15,
            7 : 2,
            8 : 17,
            9 : 3,
            10 : 19,
            11 : 7,
            12 : 16,
            13 : 8,
            14 : 11,
            15 : 14,
            16 : 9,
            17 : 12,
            18 : 5,
            19 : 20 }
        
    score = dict[field_number]    
    
    field_type = field_types.MISS
    
    # get single/double/triple/... through the distance to the bullseye
    if(scaled_dist <= 12.7):
        score = 50
        field_type = field_types.DOUBLE
    elif(scaled_dist <= 31.8):
        score = 25
        field_type = field_types.SINGLE
    elif(scaled_dist <= 99):
        score = score
        field_type = field_types.SINGLE
    elif(scaled_dist <= 107):
        score = score * 3
        field_type = field_types.TRIPLE
    elif(scaled_dist <= 332):
        score = score    
        field_type = field_types.SINGLE
    elif(scaled_dist <= 340):
        score = score * 2    
        field_type = field_types.DOUBLE
    else:
        score = 0
        field_type = field_types.MISS
    print("score: ")
    print(score)
    print("field type: ")
    print(field_type.name)

    return(score)
    

def detect_dart():
    
    #Video einlesen, hier müssen nun die verschiedenen USB-Kameras eingelesen werden
    # ToDo: Kamera überprüfen
    cap = cv2.VideoCapture(0)

    # evaluate frame by frame
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    motion = 0 # variable to ensure that a motion is detected
    frame_counter = 0 # variable to ensure that the dart is stuck in the board

    while cap.isOpened():

        # change the original frame into a threshold frame
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        # morphological closing (removes small holes from the foreground)
        dilated = cv2.dilate(thresh, None, iterations=3)
        eroded = cv2.erode(thresh, None, iterations=3)
        #morphological opening (removes small objects from the foreground)
        eroded = cv2.erode(thresh, None, iterations=3)
        dilated = cv2.dilate(thresh, None, iterations=3)
        # find contours in threshold
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # for loop to detect contour changes during the video capture
        for contour in contours:

            # if object is detected the motion variable is set to one and the frame counter is reseted to 0
            if cv2.contourArea(contour) > 1000:
                motion = 1
                frame_counter = 0

            # wait a view frames to ensure that the dart is stuck in the board then make a screenshot        
            if motion == 1 and frame_counter > 10 :
                motion = 0
                frame_counter = 0
                cap.release()             
                
                #ToDo: andere 2 Bilder machen
                cap2 = cv2.VideoCapture(1)
                frame2 = cap2.read()
                cap2.release()
                cap3 = cv2.VideoCapture(2)
                frame3 = cap3.read()
                cap3.release()               

                return frame1, frame2, frame3

        frame_counter += 1
        frame1 = frame2
        ret, frame2 = cap.read()

        # if (0xFF == ord('q')): # Abbruch, wenn q gedrückt
        #     return False
