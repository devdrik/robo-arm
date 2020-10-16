import RPi.GPIO as GPIO
import time
import myutils
from servo import Servo

class Robo():

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.servos = [Servo(37, (-180, 180)), Servo(35, (-90, 90)), Servo(33, (-90, 90), True), Servo(31, (-90, 90))]
            
    def __del__(self):
        pass

    def moveTo(self, angles):
        dutyCycles = []
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])

    def moveBy(self, position):
        pass
