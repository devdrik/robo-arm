import time
from myLogger import log


class Robo():

    def __init__(self, servos, kinematics):
        self.kinematics = kinematics
        self.servos = servos
        angles = []
        for servo in self.servos:
            angles.append(servo.getAngle())
        self.position = self.kinematics.getPosition(angles)
            
    def __del__(self):
        pass

    def setAngles(self, angles):
        for i in range(len(angles)):
            self.servos[i].setAngle(angles[i])

    def setAnglesBlocking(self, angles, timeout=5):
        allServosReachedAngle = False
        self.setAngles(angles)
        done = [False for n in self.servos]
        startTime = time.time()
        while time.time() - startTime < timeout:
            for i in range(len(angles)):
                if not done[i]:
                    done[i] = self.servos[i].hasReachedAngle()
            if all(i for i in done):
                allServosReachedAngle = True
                break
        return allServosReachedAngle

    def chill(self):
        for servo in self.servos:
            servo.setAngle(0)

    def setAngleForAllServos(self, angle):
        for servo in self.servos:
            servo.setAngle(angle)
    
    def setAngleForServo(self, servoId, angle):
        self.servos[servoId].setAngle(angle)

    def moveToPosition(self, pos):
        self._moveToPosition(pos, self.setAngles)

    def moveToPositionBlocking(self, pos):
        self._moveToPosition(pos, self.setAnglesBlocking)

    def _moveToPosition(self, pos, setAngles):
        angles, outOfRange = self.kinematics.getAnglesRaw(pos)
        if not outOfRange:
            setAngles(angles)
        else:
            log("out of range!", "ERR")
        return outOfRange

    def setVelocity(self, velocity):
        for servo in self.servos:
            self._setVelocityForServo(servo, velocity)

    def setVelocityForIndex(self, servoIndex, velocity):
        self._setVelocityForServo(self.servos[servoIndex], velocity)

    def _setVelocityForServo(self, servo, velocity):
        vel = velocity if velocity < 32767 and velocity > 0 else 0
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