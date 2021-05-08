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

    def setAnglesBlocking(self, angles, timeout=5):
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])
        done = [False for n in self.servos]
        startTime = time.time()
        while time.time() - startTime < timeout:
            for i in range(len(angles)):
                if not done[i]:
                    done[i] = self.servos[i].hasReachedAngle()
            if all(i for i in done):
                break

    def setAnglesEqualized(self, angles):
        # calculate the necessary velocities to make all servos reach the goalAngle at the same time
        raise NotImplementedError

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
        self._moveToRaw(pos, self.setAngles)

    def moveToRawBlocking(self, pos):
        self._moveToRaw(pos, self.setAnglesBlocking)

    def _moveToRaw(self, pos, setAngles):
        # startTime = time.time()
        angles, outOfRange = self.kinematics.getAnglesRaw(pos)
        # log("elapsed time: {}".format(time.time() - startTime))
        if not outOfRange:
            setAngles(angles)
        else:
            log("out of range!", "ERR")

    def moveBy(self, position):
        self.moveTo(self.position + position)

    def setVelocity(self, velocity):
        for servo in self.servos:
            self._setVelocityForServo(servo, velocity)

    def setVelocityForIndex(self, servoIndex, velocity):
        self._setVelocityForServo(self.servos[servoIndex], velocity)

    def _setVelocityForServo(self, servo, velocity):
        vel = velocity if velocity < 32767 and velocity > 0 else 0
        print("vel: ", vel)
        servo.setProfileVelocity(vel)

    def startTeachMode(self):
        for servo in self.servos:
            servo.startTeachingMode()

    def startPositionMode(self):
        for servo in self.servos:
            servo.startPositionMode()

    def getAngles(self):
        angles = []
        for servo in self.servos:
            angles.append(servo.getAngle())
        return angles