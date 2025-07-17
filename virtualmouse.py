import cv2
import numpy as np
import HandTracking as htm
import time
import autopy
import mouse
###################
wCam,hCam = 640,480
frameR = 90
smoothening = 7
###################

pTime = 0
plocX,plocY = 0,0
clocX,clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    # 1. HAND LANDMARKS
    success, img = cap.read()
    img = cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. INDEX AND MIDDLE FINGER COORDINATE
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

    # 3. CHECKING FINGERS WITH THE COORDINATES
    fingers = detector.fingersUp()
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. ONLY INDEX FINGER CAN MOVE THE MOUSE
    if fingers[1]==1 and fingers[2]==0:

        # 5. CONVERT COORDINATES
        x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
        # 6. SMOOTHEN VALUES
        clocX = plocX + (x3 - plocX) /smoothening
        clocY = plocY + (y3 - plocY) /smoothening

        # 7. MOVING CURSOR
        autopy.mouse.move(clocX, clocY)
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        plocX,plocY = clocX, clocY


    # 8. CHECKING THE INDEX AND MIDDLE FINGER SAME TIME
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
        # 9. DISTANCE BETWEEN FINGERS
        length, img, lineInfo = detector.findDistance(8,12,img)
        # 10. CLICK WHEN DISTANCE IS SHORT
        if length <39:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255,0), cv2.FILLED)
            mouse.click(button='left')

    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
        # 9. DISTANCE BETWEEN FINGERS
        length, img, lineInfo = detector.findDistance(8,12,img)
        # 10. CLICK WHEN DISTANCE IS SHORT
        if length <39:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255,0,0), cv2.FILLED)
            mouse.click(button='right')

    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        # 9. DISTANCE BETWEEN FINGERS
        length, img, lineInfo = detector.findDistance(8,12,img)
        # 10. CLICK WHEN DISTANCE IS SHORT
        if length <39:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255, 166, 124), cv2.FILLED)
            mouse.wheel(delta=1)

    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
        # 9. DISTANCE BETWEEN FINGERS
        length, img, lineInfo = detector.findDistance(8,12,img)
        # 10. CLICK WHEN DISTANCE IS SHORT
        if length <39:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (119, 130, 137), cv2.FILLED)
            mouse.wheel(delta=-1)



    # 11. FRAME RATE OR FPS IN WEB CAM
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_DUPLEX,2,(255,0,0),2)
    # 12. DISPLAY CAMERA
    cv2.imshow("Image", img)
    cv2.waitKey(1)
