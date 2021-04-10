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
    for i in range(-80,90,2):
        robo.moveToRaw([i,0,50])
        # time.sleep(0.5)

def myMove():
    path = [[-70, 0, 20],[-70, 0, 60],[0, 0, 60],[70, 0, 60],[70, 0, 20]]
    for point in path:
        robo.moveToRaw(point)

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

kinematics = InverseKinematics()
def getAngles(pos):
    angles, outOfRange = kinematics.getAnglesRaw(pos)
    return angles

def moveCircle():
    step = 2
    r = 40
    mx = 0
    mz = 50
    angles = []
    for xc in range( - r, r, step):
        y = 0
        x = xc + mx
        z = mz + math.sqrt(r**2 - xc**2)
        log("x={}, y={}, z={}".format(x,y,z))
        angles.append(getAngles([x,y,z]))
        # robo.moveToRaw([x,y,z])
        # time.sleep(1)
    for xc in range( r, -r, -step):
        y = 0
        x = xc + mx
        z = mz - math.sqrt(r**2 - xc**2)
        log("x={}, y={}, z={}".format(x,y,z))
        angles.append(getAngles([x,y,z]))
        # robo.moveToRaw([x,y,z])
        # time.sleep(1)
    for angle in angles:
        robo.setAngles(angle)

def createCircleFile():
    step = 2
    r = 40
    mx = 0
    mz = 50
    angles = []
    for xc in range( - r, r, step):
        y = 0
        x = xc + mx
        z = mz + math.sqrt(r**2 - xc**2)
        log("x={}, y={}, z={}".format(x,y,z))
        angles.append(getAngles([x,y,z]))
    for xc in range( r, -r, -step):
        y = 0
        x = xc + mx
        z = mz - math.sqrt(r**2 - xc**2)
        log("x={}, y={}, z={}".format(x,y,z))
        angles.append(getAngles([x,y,z]))
    
    fname = "circle_r{}_step{}_mx{}_mz{}".format(r,step,mx,mz)
    with open(fname, "a") as f:
        for angle in angles:
            f.write("{},{},{},{},{}\n".format(angle[0],angle[1],angle[2],angle[3],angle[4]))



try:
    createCircleFile()
    # robo.chill()
    # time.sleep(2.0)
    # simpleMovementExample()
    # moveCircle()
    # myMove()
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

