# Vision-Controlled-Prosthetic-Hand
A low-cost prosthetic hand that utilizes camera-based hand recognition and Arduino to mimic hand movement in real time.

![Hand](Hand.jpg)


# Overview
This project explores a low-cost approach to traditional prosthetics by using a standard webcam and 3D-printed parts. With OpenCV and MediaPipe, this prosthetic leverages computer vision to track hand landmarks in realtime and translates gestures to actuate servo motors controlling each finger. This approach eliminates the need for flex sensors or wearable gloves, providing a more cost-effective solution to gesture recognition. 


# Technologies Used
- **OpenCV** to access webcam and store frame information
- **MediaPipe** for hand landmark recognition and accessing joint locations
- **Arduino Uno** and 5 MG996R servo motors that are attached to fishing line threaded through each finger
  - 3D-Model of the Prosthetic is open source retrieved from https://inmoov.fr/
- **PyFirmata2** Library to communicate with the Arduino

# Approach
