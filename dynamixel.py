#!/usr/bin/env python3
import serial
from time import sleep
from IServo import IServo
from myLogger import log

class Dynamixel(IServo):

    def __init__(self, servoId, serialDevice):
        self.ser = serialDevice
        self.id = servoId

    def getAngle(self):
        return 0

    def setAngle(self, angle):
        function = 1
        correctedAngle = angle + 180
        log("setting {} to {}".format(self.id,correctedAngle))
        self.ser.flush()
        self.ser.write("{func}:{id}:{ang}\n".format(func=function, id=self.id, ang=correctedAngle).encode("utf-8"))
        sleep(0.1)