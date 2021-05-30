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
from dynamixel import Dynamixel
from filehandler import FileHandler
from roboMoves import RoboMoves
from robocli import RoboCLI

import serial

serialPort = '/dev/ttyACM0'
ser = serial.Serial(serialPort, 115200, timeout=1)
ser.flush()

servos = [Dynamixel(0, ser), Dynamixel(1, ser), Dynamixel(2, ser), Dynamixel(3, ser), Dynamixel(4, ser)]
kinematics = InverseKinematics()
robo = Robo(servos, kinematics)

moves = RoboMoves(robo, kinematics)
fileHandler = FileHandler()
cli = RoboCLI(robo, fileHandler)


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

def createCircleFile():
    angles, fname = moves.createCircle()
    fileHandler.saveToFile(fname, angles)

def saveLine():
    angles, fname = moves.getLine()
    fileHandler.saveToFile(fname, angles)

def moveLine():
    angles, fname = moves.getLine()
    moveAngles(angles)

def moveAngles(angles):
    for angle in angles:
        robo.setAngles(angle)

def teachPositions():
    cli.startCli()

try:
    log("starting actual programm")
    robo.chill()
    time.sleep(2.0)

    # moves.auroraMoves()
    # moves.dance()
    # moves.hello()
    # moves.wafe()
    # moves.simpleMovementExample()
    # moves.myMove()
    # moves.createCircle()
    # moves.moveCircle()

    teachPositions()

    # time.sleep(2.0)
    # robo.chill()
    # moveWithCV()
    # robo.moveToRaw([-50,-30,50])
    # moveWithCV(showMovie=True)
    # robo.moveToRaw([0.1,-60,30])
    # robo.setAngleForServo(1,5)

except KeyboardInterrupt:
    robo.startPositionMode()
    robo.chill()
    print("end")
