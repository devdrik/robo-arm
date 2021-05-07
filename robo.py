import RPi.GPIO as GPIO
import time
import myutils
from threading import Thread
from threading import Lock
from inversekinematics import InverseKinematics
from myLogger import log

class Robo():

    def __init__(self, servos):
        
        lock = Lock()
        self.kinematics = InverseKinematics()
        self.servos = servos
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

    def setAnglesBlocking(self, angles):
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])
        done = [False for n in self.servos]
        while True:
            for i in range(len(angles)):
                if not done[i]:
                    done[i] = self.servos[i].hasReachedAngle()
            if all(i for i in done):
                break



        

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
        # startTime = time.time()
        angles, outOfRange = self.kinematics.getAnglesRaw(pos)
        # log("elapsed time: {}".format(time.time() - startTime))
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

    def setVelocity(self, velocity):
        vel = velocity if velocity < 32767 and velocity > 0 else 0
        print("vel: ", vel)
        for servo in self.servos:
            servo.setProfileVelocity(vel)
