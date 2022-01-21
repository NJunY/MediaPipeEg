import mediapipe as mp
import cv2
import time
import math

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0,0,255), thickness=3)
handConStyle = mpDraw.DrawingSpec(color=(0,255,0), thickness=5)
pTime = 0
cTime = 0
# pPoint = ()
cPoint = ()
# pThumb = ()
cThumb = ()
pMid = ()
cMid = ()
arrPoints = []

def drawPoint(img, arrDraw):
    for point in arrDraw:
        cv2.circle(img, point, 10, (0,0,255), cv2.FILLED)

while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        #print(result.multi_hand_landmarks)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)

                    cv2.putText(img, str(i), (xPos+25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 2)
                    if i == 4:
                        cThumb = (xPos, yPos)
                        # print(f'Thumb {cThumb}')
                    elif i == 8:
                        # cv2.circle(img, (xPos, yPos), 10, (166, 56, 56), cv2.FILLED)
                        cPoint = (xPos, yPos)
                        # print(f'Point {cPoint}')

                        xDis = (cThumb[0]-cPoint[0])**2
                        yDis = (cThumb[1]-cPoint[1])**2
                        # print(xDis)
                        # print(yDis)
                        distance = math.sqrt(xDis+yDis)
                        # print(distance)
                        if distance < 15:
                            xMid = (cThumb[0]+cPoint[0])/2
                            yMid = (cThumb[1]+cPoint[1])/2
                            cMid = (int(xMid), int(yMid))
                            if pMid != cMid:
                                arrPoints.append(cMid)
                            pMid = cMid
        drawPoint(img, arrPoints)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
        break
