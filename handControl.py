import cv2
import mediapipe as mp

from Finger import Finger #Import the Finger class from the Finger file
from Finger import width,height
from Servo_Utils import Servo #Import the Servo class from Servo_Utils

indexPin = 8
middlePin = 7
ringPin = 9
pinkyPin = 10
thumbPin = 11

def drawDistanceLines(frame, arr):
    for i in range(1,len(arr)): #excludes the thumb
        cv2.line(frame, arr[i][0], arr[i][1], (0, 255, 0), 3)

    #Draws a right triangle connecting the tip of the thumb to the base of the thumb
    y1 = arr[0][0][1]
    x2 = arr[0][1][0]
    cv2.line(frame, arr[0][1], (x2, y1), (0, 255, 0), 3)
    cv2.line(frame, arr[0][0], (x2, y1), (0, 255, 0), 3)

indexServo = Servo(indexPin)
middleServo = Servo(middlePin)
ringServo = Servo(ringPin)
pinkyServo = Servo(pinkyPin)
thumbServo = Servo(thumbPin)

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #Capture frame and directly show it
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width) #Set cam width
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height) #Set cam height
cam.set(cv2.CAP_PROP_FPS, 30) #Set cam to 30 fps


mp_drawing = mp.solutions.drawing_utils #module that contains drawing functionalities
mp_hands = mp.solutions.hands #mp_hands is a module that contains functionalities
hand = mp_hands.Hands(max_num_hands=1) #creates an instance of the hand(its an object)

def main():
    while True:
        success, frame = cam.read() #returns two values, first is a boolean to indicate successful camera launch, and the second is the actual picture
        if success:
            RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts cv2 BGR frame to RGB to allow mediapipe to process the frame
            result = hand.process(frame) #store hand information in result variable

            if result.multi_hand_landmarks:

                handlandmarks = result.multi_hand_landmarks[0] #index 0 represents the first hand seen
                # draws hand landmarks
                mp_drawing.draw_landmarks(frame, handlandmarks, mp_hands.HAND_CONNECTIONS)

                #store xyz locations for the tip and base of each finger
                #represented as a tuple
                thumbTip = handlandmarks.landmark[4]
                thumbBase = handlandmarks.landmark[2]

                indexTip = handlandmarks.landmark[8]
                indexBase = handlandmarks.landmark[5]

                middleTip = handlandmarks.landmark[12]
                middleBase = handlandmarks.landmark[9]

                ringTip = handlandmarks.landmark[16]
                ringBase = handlandmarks.landmark[13]

                pinkyTip = handlandmarks.landmark[20]
                pinkyBase = handlandmarks.landmark[17]

                #Create objects for each finger
                thumb = Finger(thumbTip.x, thumbTip.y, thumbBase.x, thumbBase.y, thumbServo, True)
                index = Finger(indexTip.x, indexTip.y, indexBase.x, indexBase.y, indexServo)
                middle = Finger(middleTip.x, middleTip.y, middleBase.x, middleBase.y, middleServo)
                ring = Finger(ringTip.x, ringTip.y, ringBase.x, ringBase.y, ringServo)
                pinky = Finger(pinkyTip.x, pinkyTip.y, pinkyBase.x, pinkyBase.y, pinkyServo)

                #Calculate the distance from the tip to base of each finger and store in a list
                d1 = thumb.calculateDistance()
                d2 = index.calculateDistance()
                d3 = middle.calculateDistance()
                d4 = ring.calculateDistance()
                d5 = pinky.calculateDistance()
                distances = list((d1,d2,d3,d4,d5))

                thumbAngle = 180
                indexAngle = int(40 * d2)
                middleAngle = int(40 * d3)
                ringAngle = int(40 * d4)
                pinkyAngle = int(40 * d5)
                angles = list((indexAngle, middleAngle, ringAngle, pinkyAngle))

                #Thresholds that indicate whether a finger is fully contracted

                #Check if the tip of the finger is below the base of the finger
                #->If so, set finger servos all the way to zero to close that particular finger
                if (pinkyTip.y > pinkyBase.y): pinkyAngle=0
                if (ringTip.y > ringBase.y): ringAngle=0
                if (middleTip.y > middleBase.y): middleAngle=0
                if (indexTip.y > indexBase.y): indexAngle=0

                #Check if the tip of the thumb is to the left of the base of the thumb
                #->If so, the thumb is considered closed and set the thumb servo angle to zero
                if (thumbTip.x <= thumbBase.x): thumbAngle=0

                thumb.servo.write(thumbAngle)
                index.servo.write(indexAngle)
                middle.servo.write(middleAngle)
                ring.servo.write(ringAngle)
                pinky.servo.write(pinkyAngle)

                #create tuples to store thumb and index coordinates
                #normalize coordinate system by multiplying resolution width and height to the tuples, which allows opencv to draw lines now
                thumbTipTuple = (int(thumbTip.x * width), int(thumbTip.y * height))
                thumbBaseTuple = (int(thumbBase.x * width), int(thumbBase.y * height))

                indexTipTuple = (int(indexTip.x * width), int(indexTip.y * height))
                indexBaseTuple = (int(indexBase.x * width), int(indexBase.y * height))

                middleTipTuple = (int(middleTip.x * width), int(middleTip.y * height))
                middleBaseTuple = (int(middleBase.x * width), int(middleBase.y * height))

                ringTipTuple = (int(ringTip.x * width), int(ringTip.y * height))
                ringBaseTuple = (int(ringBase.x * width), int(ringBase.y * height))

                pinkyTipTuple = (int(pinkyTip.x * width), int(pinkyTip.y * height))
                pinkyBaseTuple = (int(pinkyBase.x * width), int(pinkyBase.y * height))

                #Store the tuples for the base and tip xyz coordinates of each finger in a list
                fingerTuples = [(thumbTipTuple, thumbBaseTuple), (indexTipTuple,indexBaseTuple),
                                (middleTipTuple, middleBaseTuple), (ringTipTuple, ringBaseTuple),
                                (pinkyTipTuple, pinkyBaseTuple)]

                #draw a line from the tip to base of each finger
                drawDistanceLines(frame, fingerTuples)

                #text display of angles and distances
                cv2.putText(frame, "middle dist: " + str(d1) + ";  indexDist: " + str(d2) + ";  ringDist: " + str(d3), (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, "Middle Angle: " + str(middleAngle) + ";  index angle: " + str(indexAngle) + "; ring angle: " + str(ringAngle),
                            (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("my WEBCAM", frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

    cam.release()

if __name__ == '__main__':
    main()


