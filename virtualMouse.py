import cv2 as cv
import mediapipe as mp
import numpy as np
import handTrackingModule as htm
import time
import pyautogui as aug

#index finger to move
#index and middle finger togther to click
#use distance between index and middle finger 

# Steps -->
#find hand lanmarks 
#find tips of index and middle finger
#check which fingers are up
#only index finger : Moving mode
#Convert coordinates
#Smoothen values
#move mouse
#both index and middle finger : Clicking mode
#find distance between fingers
#click mouse if distance is lesss

wCam, hCam = 640, 480
wScreen, hScreen = aug.size()
frameR = 100 #frame reduction

smoothVar = 5
px, py = 0,0 #previous location 
curx, cury = 0,0 #current location  

cap = cv.VideoCapture(0)

cap.set(3, wCam) #width
cap.set(4, hCam) #height

cTime = 0
pTime = 0

detector = htm.handDetector(maxHands=1) #one hand for mouse -- 2 not needed

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    cv.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    

    if len(lmList) != 0:
        x0, y0 = lmList[4][1:] #thummb 
        x1, y1 = lmList[8][1:] #index finger tip
        x2, y2 = lmList[12][1:] #middle finger tip
        x3, y3 = lmList[16][1:] #ring finger
        x4, y4 = lmList[20][1:] #pinky finger

        #print(x1, y1, x2, y2)
    
    fingers = detector.fingersUp()
    #print(fingers)

    if fingers == [0, 1, 0, 0, 0]:
        x5 = np.interp(x1, (frameR, wCam- frameR), (0, wScreen))
        y5 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))

        curx = px + (x5 - px)/ smoothVar
        cury = py + (y5 - py)/ smoothVar

        aug.moveTo(curx, cury)
        cv.circle(img, (x1,y1), 15, (255,0,255), -1)
        px, py = curx, cury
    
    if fingers == [0, 1, 1, 0, 0]:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        #print(length)
        if length < 80:
            cv.circle(img, (lineInfo[4],lineInfo[5]), 15, (0,255,0), -1)
            aug.click()
    
    if fingers == [1, 1, 0, 0, 0]:
            length2, img, _ = detector.findDistance(4, 8, img)
            if length2 < 50:
                aug.mouseDown()
                aug.moveTo(curx, cury)
            else:
                aug.mouseUp()
    
    if fingers == [0, 0, 0, 0, 1]:
            aug.click(button='right')
            time.sleep(0.6)
    
    if fingers == [0, 1, 1, 0, 0]:
            print(length)
            if length > 100:
                aug.doubleClick()
                time.sleep(0.3)

    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (20,50), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,0,0), 3)

    cv.imshow("Image", img)
    cv.waitKey(1)
