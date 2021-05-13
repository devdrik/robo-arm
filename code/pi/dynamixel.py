#!/usr/bin/env python3
import serial
from time import sleep
from interfaces.IServo import IServo
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
        self.ser.flush()
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))
        self.ser.flush()
        myByte = []
        for k in range(4):
            myByte.append(int.from_bytes(self.ser.read(1), byteorder='big', signed=False))
            print(f'byte[{k}]={myByte[k]}')
        self.ser.flush()
        angle= struct.unpack('<f', bytearray(myByte))[0]
        print(f'floatAngle={angle}')

        # angle = int.from_bytes(self.ser.read(1), byteorder='big', signed=False)
        correctedAngle = angle - 180
        log("angle read from servo {} is {} and should be {}".format(self.id, correctedAngle, self.goalAngle))
        return correctedAngle

    def setAngle(self, angle):
        function = 1
        correctedAngle = angle + 180
        self.goalAngle = correctedAngle
        log("setting {} to {}".format(self.id,correctedAngle))
        self.ser.flush()
        self.ser.write("{func}:{id}:{ang:.2f}\n".format(func=function, id=self.id, ang=correctedAngle).encode("utf-8"))
        self.ser.flush()
        # sleep(0.01)

    def setProfileVelocity(self, velocity):
        function = 4
        print("writing velocity: ", velocity)
        self.ser.flush()
        self.ser.write("{func}:{id}:{vel}\n".format(func=function, id=self.id, vel=velocity).encode("utf-8"))

    def hasReachedAngle(self):
        # hasReached = self.goalAngle - self.offset  <= self.getAngle() <= self.goalAngle + self.offset
        function = 6
        self.ser.flush()
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))
        self.ser.flush()
        hasReached = int.from_bytes(self.ser.read(1), byteorder='big', signed=False)
        if hasReached == 0:
            pass
            # log("hasReached for {}:{}, angle is: {}, should: {}".format(self.id, hasReached, self.getAngle(), self.goalAngle-180))
        else:
            log("hasReached for {}:{}".format(self.id, hasReached))
        return hasReached > 0

    def startPositionMode(self):
        function = 7
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))

    def startTeachingMode(self):
        function = 8
        self.ser.write("{func}:{id}\n".format(func=function, id=self.id).encode("utf-8"))