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

import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()

servos = [Dynamixel(0, ser), Dynamixel(1, ser), Dynamixel(2, ser), Dynamixel(3, ser), Dynamixel(4, ser)]
robo = Robo(servos)

def simpleMovementExample():
    for i in range(-60,60,10):
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

def getCoordinatesFrom(radius, mx, my, mz, alpha):
    y = my
    x = mx + math.cos(math.radians(alpha)) * radius
    z = mz + math.sin(math.radians(alpha)) * radius
    log("x={}, y={}, z={}".format(x,y,z))
    return [x,y,z]

def moveCircle():
    stepDegree = 12
    r = 20
    mx = -40
    my = -40
    mz = 30
    angles = []
    offset = 90
    for alpha in range( 0 + offset, 360 + offset, stepDegree):
        coordinates = getCoordinatesFrom(r,mx,my,mz,alpha)
        angle = getAngles(coordinates)
        robo.setAngles(angle)

def createCircleFile():
    stepDegree = 6
    r = 30
    mx = 20
    mz = 50
    angles = []
    for alpha in range( 0, 360, stepDegree):
        [x,y,z] = getCoordinatesFrom(r,mx,my,mz,alpha)
        angle, outOfRange = kinematics.getAnglesRaw([x,y,z])
        if not outOfRange:
            angles.append(angle)
    
    fname = "moveFiles/circle_r{}_step{}_mx{}_mz{}".format(r,stepDegree,mx,mz)
    with open(fname, "w") as f:
        for angle in angles:
            f.write("{},{},{},{},{}\n".format(angle[0],angle[1],angle[2],angle[3],angle[4]))

def readAngles():
    r=40
    step=2
    mx=0
    mz=50
    fname = "circle_r{}_step{}_mx{}_mz{}".format(r,step,mx,mz)
    with open(fname) as f:
        lines = f.readlines()
    angles = []
    # print(lines)
    for line in lines:
        lineValues = []
        for value in line.split(','):
            if value.endswith("\n"):
                value=value[:-2]
            lineValues.append(float(value))
        angles.append(lineValues)
    return angles

def getAnglesFromFile(fname):
    with open("moveFiles/" + fname) as f:
        lines = f.readlines()
    angles = []
    # print(lines)
    for line in lines:
        lineValues = []
        for value in line.split(','):
            if value.endswith("\n"):
                value=value[:-1]
            lineValues.append(float(value))
        angles.append(lineValues)
    return angles
        
def auroraMoves():
    # robo.setVelocity(100)
    robo.moveToRawBlocking([30,10,60])
    time.sleep(1.0)
    # robo.moveToRawBlocking([120,-30,30])
    # time.sleep(2.0)
    robo.setAnglesBlocking([-120, -45, 45, 45, 45])
    time.sleep(1.0)
    robo.setAnglesBlocking([-167, 1, 90, 80, -70])

def wafe():
    # for angle in range(-50, 50, 1):
    #     robo.setAngles([0, -angle, angle, -angle, angle])
    while True:
        for angle in range(-29, 30, 1):
            robo.setAngles([0, -angle, angle*1.1, -angle*1.4, angle*2])
        for angle in range(29, -30, -1):
            robo.setAngles([0, -angle, angle*1.1, -angle*1.4, angle*2])

def dance():
    # for angle in range(-50, 50, 1):
    #     robo.setAngles([0, -angle, angle, -angle, angle])
    # while True:
    #     for angle in range(0, 60, 1):
    #         robo.setAngles([0, angle, 2*angle, angle, 0])
    #     for angle in range(59, 1, -1):
    #         robo.setAngles([0, angle, 2*angle, angle, 0])
    #     for angle in range(0, 60, 1):
    #         robo.setAngles([0, 0, angle, 2*angle, angle])
    #     for angle in range(59, 1, -1):
    #         robo.setAngles([0, 0, angle, 2*angle, angle])
    #     for angle in range(0, 60, 1):
    #         robo.setAngles([0, 0, 0, angle, 2*angle])
    #     for angle in range(59, 1, -1):
    #         robo.setAngles([0, 0, 0, angle, 2*angle])
    velocity = 50
    while True:
        robo.setVelocity(velocity)

        robo.setVelocityForIndex(2, velocity*2)
        angle = 60
        robo.setAnglesBlocking([0, angle, 2*angle, angle, 0])
        angle = 0
        robo.setAnglesBlocking([0, angle, 2*angle, angle, 0])

        robo.setVelocityForIndex(2, velocity)
        robo.setVelocityForIndex(3, velocity*2)
        angle = 60
        robo.setAnglesBlocking([0, 0, angle, 2*angle, angle])
        angle = 0
        robo.setAnglesBlocking([0, 0, angle, 2*angle, angle])
        
        robo.setVelocityForIndex(3, velocity)
        robo.setVelocityForIndex(4, velocity*2)
        angle = 60
        robo.setAnglesBlocking([0, 0, 0, angle, 2*angle])
        angle = 0
        robo.setAnglesBlocking([0, 0, 0, angle, 2*angle])

        robo.setVelocityForIndex(1, velocity)
        robo.setVelocityForIndex(2, velocity*2)
        robo.setVelocityForIndex(3, velocity*2)
        robo.setVelocityForIndex(4, velocity*2)
        angle = 60
        robo.setAnglesBlocking([0, angle, 2*angle, 2*angle, 2*angle])
        angle = 0
        robo.setAnglesBlocking([0, angle, 2*angle, 2*angle, 2*angle])

        robo.setVelocity(velocity)
        break

def saveToFile(fname, angles):
    with open("moveFiles/" + fname, "w") as f:
        for angle in angles:
            f.write("{},{},{},{},{}\n".format(angle[0],angle[1],angle[2],angle[3],angle[4]))

def saveLine():
    step = 1
    start = -60
    end = 60
    y = 0
    z = 50
    angles = []
    for x in range(start,end,step):
        angle, outOfRange = kinematics.getAnglesRaw([x,y,z])
        if not outOfRange:
            angles.append(angle)
    fname = "line_step{}start{}end{}".format(step,start,end)
    saveToFile(fname, angles)

def moveAngles(angles):
    for angle in angles:
        robo.setAngles(angle)

def teachPositions():
    angles = []
    while True:
        robo.startTeachMode()
        options=[
            "[1] set Position",
            "[2] save to file",
            "[3] read from file",
            "[4] play angles",
            "[5] set speed",
            "[6] end"
        ]
        menu = ""
        for option in options:
            menu += option + '\n'
        menu += "your choice: "
        inp = input(menu)
        try:
            inp = int(inp)
        except:
            continue
        if inp == 6:
            break
        elif inp == 1:
            angle = robo.getAngles()
            angles.append(angle)
            print(angle)
        elif inp == 2:
            fname = input("enter filename: ")
            saveToFile(fname, angles)
        elif inp == 3:
            fname = input("enter filename: ")
            try:
                anglesFromFile = getAnglesFromFile(fname)
                angles = anglesFromFile
            except:
                print("Error, filename not existent?")
        elif inp == 4:
            robo.startPositionMode()
            robo.setVelocity(getVelocityInput())
            for angle in angles:
                # robo.setAnglesBlocking(angle)
                robo.setAngles(angle)
                time.sleep(2)
        elif inp == 5:
            vel = getVelocityInput()
            robo.startPositionMode()
            robo.setVelocity(vel)
    
def getVelocityInput():
    while True:
        vel = input("enter velocity: ")
        try:
            vel = int(vel)
        except:
            print("Not a number, try again")
            continue
        break
    return vel

def hello():
    robo.setAngles([-90,0,0,0,0])
    time.sleep(4)
    robo.setAngles([-90,0,0,0,90])
    time.sleep(1)
    robo.setAngles([-160,0,0,0,90])
    time.sleep(1)
    robo.setAngles([0,0,0,0,90])
    time.sleep(1)
    robo.setAngles([-70,-20,20,-20,20])

try:
    log("starting actual programm")
    # saveLine()
    # createCircleFile()
    # for angles in readAngles():
    #     print(angles)
    #     robo.setAngles(angles)
    robo.chill()
    # time.sleep(2.0)
    # dance()

    # robo.setAnglesBlocking([0, 0, 0, 0, 0])
    # robo.setAnglesBlocking([0, -10, 20, -30, 40])
    # servos[1].getAngle()

    # moveAngles(getAnglesFromFile("line_step1start-60end60"))
    # time.sleep(2.0)
    # robo.chill()

    # simpleMovementExample()
    # auroraMoves()
    teachPositions()
    # dance()
    # hello()


    # robo.moveToRaw([-50,-50,0])
    # robo.moveToRaw([-60,-60,0])
    # robo.moveToRaw([-65,-65,0])


    # robo.moveToRaw([-50,-50,50])
    # robo.moveToRaw([-50,-50,40])
    # robo.moveToRaw([-50,-50,30])
    # robo.moveToRaw([-50,-50,20])
    # robo.moveToRaw([-50,-50,10])
    # robo.moveToRaw([-50,-50,0])

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
    robo.startPositionMode()
    robo.chill()
    print("end")
