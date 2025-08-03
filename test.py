import math

import cv2
import mediapipe as mp
from Finger import Finger
from pyfirmata2 import SERVO
from Servo_Utils import Servo
import time

width = 1280
height = 720
indexServo = Servo(8)


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Capture frame and directly show it
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) #Set cam width
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) #Set cam height
cam.set(cv2.CAP_PROP_FPS, 30) #Set cam to 30 fps

mp_drawing = mp.solutions.drawing_utils #module that contains drawing functionalities
mp_hands = mp.solutions.hands #mp_hands is a module that contains functionalities
hand = mp_hands.Hands(max_num_hands=1) #creates an instance of the hand(its an object)

isFirstFrame = True
initialDistance = 0

tipTuple_init =(0,0)
baseTuple_init =(0,0)

baseZ_init = 0
i=1
while True:
    success, frame = cam.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts cv2 BGR frame to RGB to allow mediapipe to process the frame
        result = hand.process(frame) #store hand information in result variable
        if result.multi_hand_landmarks:
            handlandmarks = result.multi_hand_landmarks[0] #index 0 represents the first hand seen

            indexTip = handlandmarks.landmark[8]
            indexBase = handlandmarks.landmark[5]

            index = Finger(indexTip.x, indexTip.y, indexBase.x, indexBase.y, indexServo)
            d2 = index.calculateDistance()

            if i==10:
                initialDistance=d2
                tipTuple_init = (int(indexTip.x * width), int(indexTip.y * height))
                baseTuple_init = (int(indexBase.x * width), int(indexBase.y * height))
                baseZ_init = indexBase.z*1000


            #draws hand landmarks
            mp_drawing.draw_landmarks(frame, handlandmarks, mp_hands.HAND_CONNECTIONS)

            #create tuples to store thumb and index coordinates
            #normalize coordinate system by multiplying resolution width and height to the tuples, which allows opencv to draw lines now
            indexTipTuple = (int(indexTip.x * width), int(indexTip.y * height))
            indexBaseTuple = (int(indexBase.x * width), int(indexBase.y * height))

            dOffset1 = abs(indexTipTuple[1]-tipTuple_init[1])
            dOffset2 = abs(indexBaseTuple[1]-baseTuple_init[1])

            #draw a line between thumb and index finger
            cv2.line(frame, indexTipTuple, indexBaseTuple, (0, 255, 0), 3)
            cv2.line(frame, indexTipTuple, tipTuple_init, (255, 0, 0), 3)
            cv2.line(frame, indexBaseTuple, baseTuple_init, (255, 0, 0), 3)

            if (i <= 10 and d2 != 0): i = i + 1
            else: pass


            #text display of led brightness
            cv2.putText(frame, "Distance: " + str(d2), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, "X: " + str(indexBase.x*width), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, "Y: " + str(indexBase.y*height), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, "Z: " + str(indexBase.z*1000), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, "Initial Dist: " + str(initialDistance), (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, "i: " + str(i), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0), 2)

        cv2.imshow("my WEBCAM", frame)




        if cv2.waitKey(1) & 0xff == ord('q'):
            break

cam.release()