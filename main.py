from imageprocessor import ImageProcessor
from inversekinematics import InverseKinematics
from robo import Robo
import time
import cv2
from imutils.video import VideoStream
import imutils
from myutils import map
import math
from myLogger import log
from servo import Servo
from adafruit_servokit import ServoKit
from dynamixel import Dynamixel

import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()

# kit = ServoKit(channels=16)
# servos = [Servo(0, (-180, 180), kit, lock), Servo(1, (-90, 90), kit, lock,5), Servo(2, (-90, 90), kit, lock, -5, True), Servo(3, (-90, 90), kit, lock,7), Servo(4, (-90, 90), kit, lock, True)]
servos = [Dynamixel(0, ser), Dynamixel(1, ser), Dynamixel(2, ser), Dynamixel(3, ser), Dynamixel(4, ser)]
robo = Robo(servos)

def simpleMovementExample():
    for i in range(-80,90,10):
        robo.moveToRaw([i,0,50])
        time.sleep(0.5)

def myMove():
    path = [[30, 50, 50],[40, 50, 50],[51, 50, 50],[60, 50, 50],[70, 50, 50]]
    for point in path:
        robo.moveToSmooth(point)

def moveWithCV(showMovie=False):
    ip = ImageProcessor()
    vid = VideoStream(src=0).start()
    time.sleep(2.0)
    while True:
        frame = vid.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=600)
        if showMovie:
            if ip.contour is not None:
                cv2.drawContours(frame, [ip.contour], 0, (0,255,0),3)

        x,y = ip.getPositionFromFrame(frame)
        if showMovie:
            cv2.putText(frame,"x: {}, y: {}".format(math.floor(x),math.floor(y)),(100,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3)
            cv2.imshow("Test", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                robo.chill()
                break
        # log("x: {}, y: {}".format(x,y),'ERR')

        # robo.moveToRaw([x,-30,y])
        # time.sleep(0.1)

try:
    # robo.chill()
    # time.sleep(2.0)
    simpleMovementExample()
    # robo.moveToRaw([35/35*100,0,0/35*100])
    # robo.moveToRaw([40,-5,50])

    # time.sleep(2.0)
    # robo.chill()
    # moveWithCV()
    # robo.moveToRaw([-50,-30,50])
    # moveWithCV(showMovie=True)
    # robo.moveToRaw([0.1,-60,30])
    # robo.setAngleFor(1,5)

except KeyboardInterrupt:
    robo.chill()
    print("end")

