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
2) With these coordinates, use the distance formula to calculate the pixel distance between the tip and base of each finger
   
    $d = \sqrt{(x_(tip) - x_(base))^2 + (y_(tip) - y_(base))^2}$
