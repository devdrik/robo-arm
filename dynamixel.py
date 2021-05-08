#!/usr/bin/env python3
import serial
from time import sleep
from IServo import IServo
from myLogger import log

import struct


class Dynamixel(IServo):

    

    def __init__(self, servoId, serialDevice):
        self.ser = serialDevice
        self.id = servoId
        self.goalAngle = 0
        self.offset = 1

    def getAngle(self):
        function = 2
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))
        self.ser.flush()
        angle = int.from_bytes(self.ser.read(1), byteorder='big', signed=False)
        log("angle read from servo {} is {} and should be {}".format(self.id, angle, self.goalAngle))
        return angle

    def setAngle(self, angle):
        function = 1
        correctedAngle = angle + 180
        self.goalAngle = correctedAngle
        log("setting {} to {}".format(self.id,correctedAngle))
        self.ser.flush()
        self.ser.write("{func}:{id}:{ang}\n".format(func=function, id=self.id, ang=correctedAngle).encode("utf-8"))
        # sleep(0.01)

    def setProfileVelocity(self, velocity):
        function = 4
        self.ser.flush()
        self.ser.write("{func}:{id}:{vel}\n".format(func=function, id=self.id, vel=velocity).encode("utf-8"))

    def hasReachedAngle(self):
        # hasReached = self.goalAngle - self.offset  <= self.getAngle() <= self.goalAngle + self.offset
        function = 6
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))
        self.ser.flush()
        hasReached = int.from_bytes(self.ser.read(1), byteorder='big', signed=False)
        if hasReached == 0:
            log("hasReached for {}:{}, angle is: {}, should: {}".format(self.id, hasReached, self.getAngle(), self.goalAngle))
        else:
            log("hasReached for {}:{}".format(self.id, hasReached))
        return hasReached > 0