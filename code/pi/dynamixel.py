#!/usr/bin/env python3
import serial
from time import sleep
from interfaces.IServo import IServo
from myLogger import log

import struct

FUNC_SET_ANGLE = 1
FUNC_GET_ANGLE = 2
FUNC_SET_ANGLE_FOUR = 3
FUNC_SET_PROFILE_VELOCITY = 4
FUNC_SET_PROFILE_VELOCITY_ALL = 5
FUNC_HAS_REACHED_ANGLE = 6
FUNC_SET_POSITION_MODE_ALL = 7
FUNC_TORQUE_OFF_ALL = 8
FUNC_IS_MOVING = 9

class Dynamixel(IServo):

    def __init__(self, servoId, serialDevice):
        self.ser = serialDevice
        self.id = servoId
        self.goalAngle = 0.0
        self.angleOffset = 180.0

    def getAngle(self):
        function = FUNC_GET_ANGLE
        message = f'{function}:{self.id}\n'.encode("utf-8")
        self.ser.write(message)
        readBytes = self.ser.read(4)
        angle = struct.unpack('<f', readBytes)[0]

        correctedAngle = angle - self.angleOffset
        # log(f'angle read from servo {self.id} is {correctedAngle} and should be {self.goalAngle}')
        return correctedAngle

    def setAngle(self, angle):
        function = FUNC_SET_ANGLE
        correctedAngle = angle + self.angleOffset
        self.goalAngle = angle
        log(f'setting {self.id} to {angle}')
        message = f'{function}:{self.id}:{correctedAngle:.2f}\n'.encode("utf-8")
        self.ser.write(message)

    def setProfileVelocity(self, velocity):
        function = FUNC_SET_PROFILE_VELOCITY
        self.ser.write("{func}:{id}:{vel}\n".format(func=function, id=self.id, vel=velocity).encode("utf-8"))

    def hasReachedAngle(self):
        # USING HASREACHEDANGLE FROM ARDUINO
        function = FUNC_HAS_REACHED_ANGLE
        message = f'{function}:{self.id}\n'.encode("utf-8")
        self.ser.write(message)
        answer = self.ser.read(1)
        # log(f'servo {self.id} answer: {answer}')
        hasReached = int.from_bytes(answer, byteorder='big', signed=False)
        # log(f'{hasReached}')
        if hasReached > 0:
            log(f'servo {self.id} has reached goal angle, is {self.getAngle()} should {self.goalAngle}')
        return hasReached > 0
        # USING LOCAL CALCULATED HASREACHEDANGLE
        # currentAngle = self.getAngle()
        # allowedError = 4
        # hasReached = currentAngle <= self.goalAngle + allowedError and currentAngle >= self.goalAngle - allowedError
        # if hasReached:
        #     log(f'servo {self.id} hasReached position. {currentAngle}/{self.goalAngle}')
        # return hasReached
        # USING ISMOVING FROM ARDUINO
        # function = FUNC_IS_MOVING
        # message = f'{function}:{self.id}\n'.encode("utf-8")
        # self.ser.write(message)
        # isMovingByte = self.ser.read(1)
        # hasReached = int.from_bytes(isMovingByte, byteorder='big', signed=False)
        # if hasReached == 0:
        #     log(f'servo {self.id} has reached goal angle, is {self.getAngle()} should {self.goalAngle}')
        # return hasReached == 0

    def startPositionMode(self):
        function = FUNC_SET_POSITION_MODE_ALL
        message = f'{function}:{self.id}\n'.encode("utf-8")
        self.ser.write(message)

    def startTeachingMode(self):
        function = FUNC_TORQUE_OFF_ALL
        message = f'{function}:{self.id}\n'.encode("utf-8")
        self.ser.write(message)