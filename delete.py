import cv2
import numpy as np
import lololo as htm
import time
from time import sleep
from pynput.mouse import Button , Controller
import pyautogui
import autopy
import streamlit as st

# print(wScr, hScr)






mouse = Controller()

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
p = 1
while (p):

    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x0, y0 = lmList[4][1:]

        lx = (x1+x2)/2
        ly = (y1+y2)/2


        # print(x1,y1)



        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            #cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        if fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            #cv2.circle(img, (fingers[1], fingers[2]),15, (0, 255, 0), cv2.FILLED)
            mouse.press(Button.left)
            mouse.release(Button.left)
            sleep(0.4)

        # 10. right click
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            #cv2.circle(img, (fingers[1], fingers[2]),15, (0, 255, 0), cv2.FILLED)
            mouse.press(Button.right)
            mouse.release(Button.right)
            sleep(0.4)


        # 10. switch tabs(left)
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
            sleep(1)
            # 10. Click mouse if distance short
            pyautogui.hotkey('ctrlleft','left')
            sleep(1)

        # 11. switch tabs(right)
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
            # 10. Click mouse if distance shor
            sleep(1)
            pyautogui.hotkey('ctrlleft','right')
            sleep(1)



    #Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)




#if __name__ == '__main__':
 #   main()