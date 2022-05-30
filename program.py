import cv2 as cv
import PositionModule as pm
import math,time,keyboard
import pyfirmata
shoot = False
move = True
count = 0
prevx =340
count = 0    
global pin9
board=pyfirmata.Arduino('/dev/ttyUSB0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin9.write(90)
cap = cv.VideoCapture(0)#records video from the camera
ptrue = False
currst = 'S'
print("Please press P to Play or S to Stop")
detector = pm.poseDetector()
while True:
    if input():
        currst = input()
    if currst == "p" or ptrue:
        success, img = cap.read()
        img = cv.flip(img,1)#it is to flip the image
        cv.line(img,(320,0),(320,480),(0,255,0),2)
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            x1 = lmList[11][1]
            y1 = lmList[11][2]
            x2 = lmList[12][1]
            y2 = lmList[12][2]
            x = int((x2+x1)/2)
            y = int((y2+y1)/2)
            if x and y:
                if (abs(x-prevx) in range(0,30)):
                    pin10.write(160)
                    time.sleep(.005)
                    pin10.write(180)
                    time.sleep(.005)
                    # print("shoot!")
                    count+=1
                    cv.circle(img, (x, y), 15, (0, 0, 255), cv.FILLED)
                if (abs(x-prevx) in range(0,50)):move = True

                else:
                    cv.circle(img, (x, y), 15, (255, 255, 0), cv.FILLED)
                prevx = x
                cv.line(img,(320,480),(x,y),(0,255,0),2)
                angle = int(math.degrees(math.atan2(y - 480, x - 320) -
                                math.atan2(-480,0)))
                angle = angle+90
                # print(angle)   
                # print(prevx,x) 
            #img pos is the position coordinates of the image as a dictionary with key as name of the image,
            # print(lmList[16])
                
                #cv.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 255, 0), cv.FILLED)
                if move:
                    if ((angle>100)and(angle<180)):
                        pin9.write(angle-5)
                    if ((angle<80)and(angle>10)):
                        pin9.write(angle+5)
                    else:
                        pin9.write(angle)
                    move = False
        # angle = detector.findAngle(img, 16, 14, 12, draw=False)
        # print(angle)
        # fpsReader = cvz.FPS()
        # print(hb,wb)
        # cv.namedWindow("Image", cv.WND_PROP_FULLSCREEN)
        # cv.setWindowProperty("Image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        # _, imgResult = fpsReader.update(imgResult)
        ptrue = True
        cv.imshow("Image", img)
        cv.waitKey(1)
    if currst == "s":
        print("On Halt")
        ptrue = False