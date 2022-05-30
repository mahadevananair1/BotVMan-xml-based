from curses import baudrate
from re import A, X
import re
import time
import cv2 as cv
# from cv2 import VideoCapture
import mediapipe as mp
from numpy import angle
import PositionModule as pm
import math
import serial
cap = cv.VideoCapture(0)#records video from the  in built camera
ret, img = cap.read()
pTime = 0
detector = pm.poseDetector()

# arduino = serial.Serial(port='COM6',baudrate=115200,timeout=0.1)

def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv.EVENT_LBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv.imshow('image', img)

    # checking for right mouse clicks    
    if event==cv.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv.imshow('image', img)


while True:
    
    success, img = cap.read()
    img = cv.flip(img,1)#it is to flip the image
    img = detector.findPose(img)
    cv.line(img,(320,0),(320,480),(0,255,0),3)
    x,y,c = img.shape
    # print(x,y)

    lmList = detector.findPosition(img, draw=False)

    try:
    
        twl = lmList[12][1]
        elv = lmList[11][1]
        y12 = lmList[12][2]
        y11 = lmList[11][2]
        y_aim = round((y12+y11)/2)
        # Distance person in x axis from origin
        aim_circ = twl + (elv-twl)/2
        cv.circle(img, (round(aim_circ), y_aim), 5, (255, 0, ), cv.FILLED)
        cv.line(img,(320,480),(round(aim_circ), y_aim),(0,255,0),3)
        # Calculate the Angle
        # angle = math.degrees(math.atan2(y_aim - 240, round(aim_circ) - 320) -
        #                      math.atan2(0 - 240,0))
        # if angle < 0:
        #     angle += 360
        # print(angle)
        distPerPx = 0.461
        adjSide = 321

        center = 320 
        direction = None

        if center == aim_circ:
            angle_req = 0

        if aim_circ>center:
            req_Xdist = distPerPx*(aim_circ-center)
            # print(f"R reqDIST:{req_Xdist}")
            direction = "r"

        if aim_circ<center:
            req_Xdist = distPerPx*(center - aim_circ)
            # print(f"L reqDIST:{req_Xdist}")
            direction = "l"

        # Angle finding

        if direction == "r":
            temp = math.atan(req_Xdist/adjSide)
            raw_angle = math.degrees(temp)
            angle_req = round(raw_angle)
            print(f"Right:{angle_req+20}")

        if direction == "l":
            temp = math.atan(req_Xdist/adjSide)
            raw_angle = math.degrees(temp)
            angle_req = round(raw_angle)
            print(f"Left:{angle_req+20}")

        # print(angle_req)
        # arduino.write(bytes(angle_req,'utf-8'))
        time.sleep(0.5)

    except:
        # print("no point found")
        None
        time.sleep(0.5)





    # hb, wb, cb = img.shape
    # print(hb,wb)
    # cv.namedWindow("Image", cv.WND_PROP_FULLSCREEN)
    # cv.setWindowProperty("Image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

   
    cv.imshow("Image", img)
    cv.setMouseCallback('Image', click_event)
    cv.waitKey(1)


