import RPi.GPIO as GPIO
import myutils
from myLogger import log

class Servo():

    def __init__(self, pin, bounds, servoKit, inverted=False):
        self.bounds = bounds
        self.inverted = inverted
        self.servo = servoKit.servo[pin]

    def __del__(self):
        # self.servo.stop()
        # GPIO.cleanup()
        pass

    def setAngle(self, angle):
        if self.inverted:
            angle = -angle
        if angle > self.bounds[1]:
            angle = self.bounds[1]
        if angle < self.bounds[0]:
            angle = self.bounds[0]
        newAngle = myutils.map(angle, self.bounds[0], self.bounds[1], 0, 180)
        log("newAngle: {}".format(newAngle))
        self.servo.angle = newAngle

    def chill(self):
        # self.servo.ChangeDutyCycle(0)
        pass