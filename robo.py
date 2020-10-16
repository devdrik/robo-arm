import RPi.GPIO as GPIO
import time
import myutils
from adafruit_servokit import ServoKit
from servo import Servo

class Robo():

    def __init__(self):
        kit = ServoKit(channels=16)
        self.servos = [Servo(0, (-180, 180), kit), Servo(1, (-90, 90), kit), Servo(2, (-90, 90), kit, True), Servo(3, (-90, 90), kit)]
            
    def __del__(self):
        pass

    def moveTo(self, angles):
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])

    def moveBy(self, position):
        pass
