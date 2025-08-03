import pyfirmata2
from pyfirmata2 import SERVO

board = pyfirmata2.Arduino("COM3") #configure arduino board and its port

class Servo:
    def __init__(self, pin):
        self.pin = pin

        #Attach the Servo pin to the board
        board.digital[self.pin].mode = SERVO


    def write(self, angle):
        board.digital[self.pin].write(angle)

