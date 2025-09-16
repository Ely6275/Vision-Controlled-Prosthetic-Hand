# Vision-Controlled-Prosthetic-Hand
A low-cost prosthetic hand that utilizes camera-based hand recognition and Arduino to mimic hand movement in real time.

![Hand](Hand.jpg)

# Demonstrations

Click the images below to view demos of the hand's functionality

[![Demo #1](https://img.youtube.com/vi/b7CLX6D0mAc/0.jpg)](https://youtu.be/b7CLX6D0mAc)

[![Demo #2](https://img.youtube.com/vi/DjKZX3GeChw/0.jpg)](https://youtu.be/DjKZX3GeChw)



# Overview
This project explores a low-cost approach to traditional prosthetics by using a standard webcam and 3D-printed parts. With OpenCV and MediaPipe, this prosthetic leverages computer vision to track hand landmarks in realtime and translates gestures to actuate servo motors controlling each finger. This approach eliminates the need for flex sensors or wearable gloves, providing a more cost-effective solution to gesture recognition. 


# Technologies Used
- **OpenCV** to access webcam and store frame information
- **MediaPipe** for hand landmark recognition and accessing joint locations
- **Arduino Uno** and 5 MG996R servo motors that are attached to fishing line threaded through each finger
  - 3D-Model of the Prosthetic is open source retrieved from https://inmoov.fr/
- **PyFirmata2** Library to communicate with the Arduino

# Approach

1) Using MediaPipe, I was able to access the xyz coordinates of each finger tip and finger base (the point that connects the finger to the hand)
2) With these coordinates, use the distance formula to calculate the pixel distance between the tip and base of each finger.
   In the demonstration, the green lines indicate the length from the tip to base of each finger, and the blue numbers at the top of each finger is the calculated distance
   
    $d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$
3) Using each finger distance, I created a linear function to map the angle of each servo to distance
   - After some adjustments, I found a multiplier of 40 allowed for a full range of finger motion
   - $\theta = 40d$
     - Where theta is the servo angle and d is the measured finger length
    
4) If the software recognizes that a finger tip reaches below its base landmark, that means the finger is closed and the servo should be written to its max value of 180
   - To detect this, use an if statement to check if the y coordinate of the tip is greater than the y coordinate of the base
  
# File Breakdown
  ## Servo_Utils.py
  This file stores functionalities for the Servos and creates a Servo object with methods

  Initialize and store board object that connects to the USB Serial Port
  ```python
  board = pyfirmata2.Arduino("COM3")
  ```

  Writes the angle passed to the servo
  ```python
  def write(self, angle):
        board.digital[self.pin].write(angle)
  ```

  ## Finger.py
  This file defines a Finger object and methods that can be operated on each finger

  Constructor that stores the xy coordinates of the tip and base of the finger, as well as the servo controlling the finger
  - The isThumb parameter is a default parameter that simply indicates whether the finger is a thumb or not
  ```python
   def __init__(self, tipX, tipY, baseX, baseY, servo, isThumb=False):
        self.tipX = tipX
        self.tipY = tipY
        self.baseX = baseX
        self.baseY = baseY
        self.servo = servo
        self.isThumb = isThumb
  ```

  ## handControl.py
  This is the main file that runs all functionalities of the hand

  Initialize each servo to a pin on the Arduino, then create servo objects using the corresponding pin. This allows me to perform methods on each finger.
  ```python
  indexPin = 8
  middlePin = 7
  ringPin = 9
  pinkyPin = 10
  thumbPin = 11
  
  indexServo = Servo(indexPin)
  middleServo = Servo(middlePin)
  ringServo = Servo(ringPin)
  pinkyServo = Servo(pinkyPin)
  thumbServo = Servo(thumbPin)
  ```
  The drawDistanceLines function draws 5 green connecting lines from the tip to base of each finger, excluding the thumb. For the thumb, this function draws a       right triangle using the base and tip coordinates of the thumb (x2 and y1)
  
  - Parameters
    - frame: the current frame captured by the camera
    - arr: a list of tuples that store xyz coordinates of each finger
  
  ```python
  def drawDistanceLines(frame, arr):
    for i in range(1,len(arr)): #excludes the thumb
        cv2.line(frame, arr[i][0], arr[i][1], (0, 255, 0), 3)

    #Draws a right triangle connecting the tip of the thumb to the base of the thumb
    y1 = arr[0][0][1]
    x2 = arr[0][1][0]
    cv2.line(frame, arr[0][1], (x2, y1), (0, 255, 0), 3)
    cv2.line(frame, arr[0][0], (x2, y1), (0, 255, 0), 3)
  ```

# What's Next?
Looking ahead, I aim to integrate computer vision with neural-muscular signals to better mimic arm movement. With EMG sensors, I can record signals from the arm/hand muscles as numerical dataand train machine learning models recognize the patterns that correspond to specific arm and hand movements. The prosthetic will be able to predict the movement of the user and actuate accordingly, enabling more natural control.  

In future prototypes, I will address these main concerns:
- Adjusting the servo angle functions to work for different hand sizes (smaller/longer fingers will yield different results when measuring tip-to-base distances)
- Depth perception (Stereo Vision): the servo angle functions will change depending on how far away your hand is from the camera due to camera perspective
  - For example, moving your hand away from the camera will decrease the calculated tip-to-base distance for each finger, even if they are still open.
