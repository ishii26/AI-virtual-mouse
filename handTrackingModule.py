import cv2 as cv
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackingConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConfidence,
            min_tracking_confidence=self.trackingConfidence
            )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)      
        return img
    
    def findPosition(self, img, handNo = 0, draw = True):
        
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for handLandmarks in self.results.multi_hand_landmarks:              
                for id, lm in enumerate(handLandmarks.landmark):
                    #print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    #print(id, cx, cy)
                    xList.append(cx)
                    yList.append(cy)
                    self.lmList.append([id, cx, cy])
                   # if draw:
                   #     if id == 8 or id == 12:
                   #         cv.circle(img, (cx,cy), 10, (255,0,255), -1)
                
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax #bounding box

                if draw: #bbox
                    cv.rectangle(img, (xmin-20, ymin-20), (xmax+20, ymax+20), (0,255,0), 2)

        return self.lmList, bbox
    
    def fingersUp(self):
        if not hasattr(self, 'lmList') or len(self.lmList) < 21:
            return []  # Return empty list if landmarks are incomplete

        fingers = []
        tips = [8, 12, 16, 20]

        #thumb
        if self.lmList[4][1] < self.lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #fingers
        for tip in tips:
            if self.lmList[tip][2] < self.lmList[tip - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        if draw:
             cv.line(img, (x1,y1), (x2,y2), (255,0,255), t)
             cv.circle(img, (x1,y1), r, (255,0,255), -1)
             cv.circle(img, (x2,y2), r, (255,0,255), -1)
             cv.circle(img, (cx,cy), r, (255,0,255), -1)
        length = math.hypot(x2-x1, y2-y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0

    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:    
            print(lmList[4]) # printing for index 0 ie palm 

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX, 1.0, (255,0,255), 3)

        cv.imshow('Image', img)
        cv.waitKey(1)



if __name__ == "__main__":
    main()








