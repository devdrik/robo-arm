import RPi.GPIO as GPIO
import time
import myutils
from adafruit_servokit import ServoKit
from servo import Servo
from threading import Thread
from threading import Lock
from inversekinematics import InverseKinematics
from myLogger import log

class Robo():


    def __init__(self):
        kit = ServoKit(channels=16)
        lock = Lock()
        self.kinematics = InverseKinematics()
        self.servos = [Servo(0, (-180, 180), kit, lock), Servo(1, (-90, 90), kit, lock,5), Servo(2, (-90, 90), kit, lock, -5, True), Servo(3, (-90, 90), kit, lock,7), Servo(4, (-90, 90), kit, lock, True)]
        angles = []
        for servo in self.servos:
            angles.append(servo.getAngle())
        self.position = self.kinematics.getPosition(angles)
        # print("üpsition: {}".format(self.position))
            
    def __del__(self):
        pass

    def setAngles(self, angles):
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])

    def setAnglesSmooth(self, servoIndex, angles, controlTimeInMs):
        self.servos[servoIndex].setAngleSmooth2(angles, controlTimeInMs)

    def setAnglesSmooth2(self, angles):
        threads = []
        for i in range(len(angles)):
            thread = Thread(target=self.moveSmooth, args=(i, angles[i],1000,))
            thread.start()
            threads.append(thread)
            # print("started thread {}".format(i))
        for t in threads:
            t.join()
        # print("all threads done")

    def chill(self):
        for servo in self.servos:
            servo.setAngle(0)

    def setAngleAll(self, angle):
        for servo in self.servos:
            servo.setAngle(angle)
    
    def setAngleFor(self, servo, angle):
        self.servos[servo].setAngle(angle)

    def moveTo(self, pos):
        angles, outOfRange = self.kinematics.getAngles(pos)
        if not outOfRange:
            self.setAngles(angles)

    def moveToRaw(self, pos):
        angles, outOfRange = self.kinematics.getAnglesRaw(pos)
        if not outOfRange:
            self.setAngles(angles)
        else:
            log("out of range!", "ERR")

    def moveBy(self, position):
        self.moveTo(self.position + position)

    def moveToSmooth(self, pos):
        angles, outOfRange = self.kinematics.getAngles(pos)
        if not outOfRange:
            self.setAnglesSmooth2(angles)

    def moveBySmooth(self, position):
        self.moveToSmooth(self.position + position)