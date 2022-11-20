import cv2
import const
import numpy 

img_counter = 0

def get_dart_coordinates(im0, im1):
    global img_counter
    
    dif01 = cv2.absdiff(im0, im1)
    mask = cv2.cvtColor(dif01, cv2.COLOR_BGR2GRAY)

    th = 55
    imask =  mask>th

    dif01 = numpy.zeros_like(im1, numpy.uint8)
    dif01[imask] = im1[imask]
    
    direction = "C:/Users/timis/OneDrive/Desktop/DartsTracker/Dart_Screenshots/"
    cv2.imwrite(direction+"{}_board.png".format(img_counter),im0)
    cv2.imwrite(direction+"{}_dart.png".format(img_counter),im1)
    cv2.imwrite(direction+"{}_dif.png".format(img_counter),dif01)

    blur = cv2.medianBlur(dif01,5) #blur image to erase thin lines
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # grayscale

    corners = cv2.goodFeaturesToTrack(gray, 500, 0.05, 1) # track corners
    import numpy as np
    corners = np.int0(corners)
        
    lowest_point = corners[0] # to find lowest corner --> tip of the dart

    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(im1, (x, y), 3, (255, 0, 0), -1) #draw every corner found white
        
        # find lowest point:
        x_low, y_low = lowest_point.ravel()
        if (y > y_low):
            lowest_point = corner
            
            
    #print(lowest_point)
    x_low, y_low = lowest_point.ravel()
    cv2.circle(im1, (x_low, y_low), 4, (0, 0, 255), 2) # circle lowest corner red
    
    
    cv2.imwrite(direction+"{}_tip.png".format(img_counter),im1)
    img_counter += 1
    
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
    print(dist)
    
    # distanz mit 3Satz auf echte Maße skalieren:
    dartboard_lenth = 340
    scaled_dist = dist /const.crop_size * dartboard_lenth 
    # print("scaled distance from dart to bullseye:")
    print(scaled_dist)
    
    p_shiftet = (p[0] - bullseye_coord[0], p[1] - bullseye_coord[1])

    ang = np.arctan2(*p_shiftet[::-1])
    # print("angle (rad):")
    # print(ang)
    angle_clockwise = np.rad2deg((ang) % (2 * np.pi)) + 90 # oben zwischen 20|1 ist 0 Grad
    
    # print("angle clockwise:")
    # print(angle_clockwise)
    
    if(angle_clockwise >= 360):
        angle_clockwise -= 360
    
    field_degrees = 360 / 20 # = 18°
    field_number = int(angle_clockwise/field_degrees)

    
    print("field_number: "+ str(field_number))
    
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
        
    score_raw = dict[field_number]    
    
    field_type = field_types.MISS
    
   
    if(dist <= 10):
        score = 50
        field_type = field_types.DOUBLE
    elif(dist <= 25):
        score = 25
        field_type = field_types.SINGLE
    elif(dist <= 141):#200):
        score = score_raw
        field_type = field_types.SINGLE
    elif(dist <= 157):#220):
        score = score_raw * 3
        field_type = field_types.TRIPLE
    elif(dist <= 252):#320):
        score = score_raw    
        field_type = field_types.SINGLE
    elif(dist <= 275):
        score = score_raw * 2    
        field_type = field_types.DOUBLE
    else:
        score = 0
        field_type = field_types.MISS
    print("score: ")
    print(score)
    print("field type: ")
    print(field_type.name)

    return score, field_type, score_raw
    

def detect_dart(cap1, cap2, cap3):

    # evaluate frame by frame
    ret, frame1 = cap3.read()
    ret, frame2 = cap3.read()
    motion = 0 # variable to ensure that a motion is detected
    frame_counter = 0 # variable to ensure that the dart is stuck in the board
    print("ready for throw!")
    while cap3.isOpened():

        # change the original frame into a threshold frame
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # for loop to detect contour changes during the video capture
        for contour in contours:

            # if object is detected the motion variable is set to one and the frame counter is reseted to 0
            if cv2.contourArea(contour) > 500:
                motion = 1
                frame_counter = 0

            # wait a view frames to ensure that the dart is stuck in the board then make a screenshot        
            if motion == 1 and frame_counter > 10 :
                motion = 0
                frame_counter = 0
                
                #andere 2 Bilder machen
                ret, frame_c2 = cap2.read()
                ret, frame_c1 = cap1.read()
                print("Pfeil erkannt")
                return frame_c1, frame_c2, frame1

        frame_counter += 10
        frame1 = frame2
        ret, frame2 = cap3.read()

        # if (0xFF == ord('q')): # Abbruch, wenn q gedrückt
        #     return False
