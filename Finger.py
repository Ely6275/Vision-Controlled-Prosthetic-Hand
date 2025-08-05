import math

from Servo_Utils import Servo

width = 1280
height = 720

class Finger:
    #distance=0
    def __init__(self, tipX, tipY, baseX, baseY, servo, isThumb=False):
        self.tipX = tipX
        self.tipY = tipY
        self.baseX = baseX
        self.baseY = baseY
        self.servo = servo
        self.isThumb = isThumb

    def calculateDistance(self):
        if self.isThumb: distance = (self.tipX - self.baseX)
        else: distance = math.sqrt(width * (self.tipX - self.baseX) ** 2 + height * (self.tipY - self.baseY) ** 2)

        return distance