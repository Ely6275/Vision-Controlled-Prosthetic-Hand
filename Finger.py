import math

from Servo_Utils import Servo

width = 1280
height = 720

class Finger:
    #distance=0
    def __init__(self, tipX, tipY, baseX, baseY, servo):
        self.tipX = tipX
        self.tipY = tipY
        self.baseX = baseX
        self.baseY = baseY
        self.servo = servo

    def calculateDistance(self):
        distance = math.sqrt(width * (self.tipX - self.baseX) ** 2 + height * (self.tipY - self.baseY) ** 2)
        return distance