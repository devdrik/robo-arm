import RPi.GPIO as GPIO
import myutils
from myLogger import log
import time
from adafruit_servokit import ServoKit
from IServo import IServo

class Servo(IServo):

    # kit = ServoKit(channels=16)

    def __init__(self, pin, bounds, servoKit, lock, offset=0, inverted=False):
        self.bounds = bounds
        self.inverted = False
        self.servo = servoKit.servo[pin]
        self.pin = pin
        self.lock = lock
        self.offset = offset
        # self.offset = 0

    def __del__(self):
        pass

    def getCorrectedAngle(self, angle):
        if self.inverted:
            angle = -angle
        angle += self.offset
        if angle > self.bounds[1]:
            angle = self.bounds[1]
            log("angle of servo {} out of bounds. angle is {}".format(self.pin, angle),"ERR")
        if angle < self.bounds[0]:
            angle = self.bounds[0]
            log("angle of servo {} out of bounds. angle is {}".format(self.pin, angle),"ERR")
        newAngle = myutils.map(angle, self.bounds[0], self.bounds[1], 0, 180)
        return newAngle

    def getAngle(self):
        return myutils.map(self.servo.angle, 0, 180, self.bounds[0], self.bounds[1])

    def setAngle(self, angle):
        newAngle = self.getCorrectedAngle(angle)
        # log("newAngle: {}".format(newAngle))
        self.servo.angle = newAngle

    def chill(self):
        pass

    def setAngleSmooth(self, angle, controlTimeInMs):
        # log("setting angle: {}, controlTime: {}".format(angle, controlTimeInMs))
        testStartTime = time.time()
        correctedAngle = self.getCorrectedAngle(angle)
        incrementAngle = 2 # smaller one doesn't work - the actual increment is for some reason smaller than the set increment

        steps=0
        counter = 0
        deltaAngle = abs(correctedAngle - self.servo.angle)
        # log("deltaAnlge: {}".format(deltaAngle))
        if deltaAngle >= incrementAngle:
            direction = 1 if correctedAngle > self.servo.angle else -1 
            steps = deltaAngle / incrementAngle
            incrementTime = abs(controlTimeInMs) / steps if steps > 1 else controlTimeInMs
            
            startTime = time.time()
            while self.servo.angle < correctedAngle and direction is 1 or self.servo.angle > correctedAngle and direction is -1:
                now = time.time()
                if now >= startTime + incrementTime / 1000:
                    # log("I am doing something {}".format(self.pin), "OK")
                    counter += 1
                    startTime = now
                    if self.servo.angle <= 180 - incrementAngle and direction is 1 or self.servo.angle >= incrementAngle and direction is -1:
                        angleBefore = self.servo.angle
                        self.servo.angle += direction * incrementAngle
                        # here comes a hack to compensate the wrong increment angle
                        steps = deltaAngle / abs(self.servo.angle - angleBefore)
                        incrementTime = abs(controlTimeInMs) / steps if steps > 1 else incrementTime
                    else:
                        if direction is 1:
                            self.servo.angle = 180
                        if direction is -1:
                            self.servo.angle = 0
                        break
        # if time.time()-testStartTime > (controlTimeInMs - 100) / 1000:
            # log("Time to set angle: {}".format(time.time()-testStartTime))
            # log("steps proposed: {}, steps used: {}".format(steps, counter))

    def setAngleSmooth2(self, angle, controlTimeInMs):
        # print("setting angle of {} to {}".format(self.pin, angle))
        correctedAngle = self.getCorrectedAngle(angle)
        incrementAngle = 1 # smaller one doesn't work - the actual increment is for some reason smaller than the set increment

        steps=0
        counter = 0
        with self.lock:
            currentAngle = self.servo.angle
            
        deltaAngle = abs(correctedAngle - currentAngle)
        # log("deltaAnlge: {}".format(deltaAngle))
        steps = deltaAngle / incrementAngle
        if steps >= 1:
            direction = 1 if correctedAngle > currentAngle else -1 
            incrementTime = controlTimeInMs / steps / 1000
            while currentAngle < correctedAngle and direction is 1 or currentAngle > correctedAngle and direction is -1:
                nextAngle = currentAngle + direction * incrementAngle
                nextAngle = 0 if nextAngle < 0 else nextAngle
                nextAngle = 180 if nextAngle > 180 else nextAngle
                with self.lock:
                    self.servo.angle = nextAngle
                    currentAngle = self.servo.angle
                # print("current angle of {} is {}".format(self.pin, currentAngle))
                time.sleep(incrementTime)
