import RPi.GPIO as GPIO
import myutils
from myLogger import log

class Servo():

    def __init__(self, pin, bounds, inverted=False):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)
        self.servo.start(7.5)
        self.bounds = bounds
        self.inverted = inverted

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()

    def setAngle(self, angle):
        if angle > self.bounds[1]:
            angle = self.bounds[1]
        if angle < self.bounds[0]:
            angle = self.bounds[0]
        dutyCycle = myutils.map(angle, self.bounds[0], self.bounds[1], 2.5, 12.5)
        if self.inverted:
            dutyCycle = 15 - dutyCycle
        log("dutyCycle is {}".format(dutyCycle))
        self.servo.ChangeDutyCycle(dutyCycle)

    def chill(self):
        self.servo.ChangeDutyCycle(0)