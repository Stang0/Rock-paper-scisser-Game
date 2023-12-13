import random
import time

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
cap = cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,650)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
score = [0,0]
while True:
    imgBg = cv2.imread("Assets/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,50:1000]


    hands, img = detector.findHands(imgScaled, draw=True, flipType=True)


    if startGame:

        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBg,str(int(timer)),(885,1000),cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNum = random.randint(1,3)
                    imgAI = cv2.imread(f'Assets/{randomNum}.png',cv2.IMREAD_UNCHANGED)


                    if (playerMove == 1 and randomNum == 3) or (playerMove == 2 and randomNum == 1) or (playerMove == 3 and randomNum == 2):
                        score[0] += 1

                    if (playerMove == 3 and randomNum == 1) or (playerMove == 1 and randomNum == 2) or (playerMove == 2 and randomNum == 3):
                        score[1] += 1
    
    imgBg[294:863,1194:1774] = imgScaled

    if stateResult:
        imgBg = cvzone.overlayPNG(imgBg,imgAI,(129,400))

    cv2.putText(imgBg,str(score[0]),(1657,265),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),6)
    cv2.putText(imgBg,str(score[1]),(530,265),cv2.FONT_HERSHEY_PLAIN,4,(255,0,255),6)

    #cv2.imshow("Image",img)
    cv2.imshow("BG",imgBg)
    #cv2.imshow("scaled",imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False
