from myLogger import log
import time
import math


class RoboMoves():
    
    def __init__(self, robo, kinematics):
        self.robo = robo
        self.kinematics = kinematics

    
    def __getAngles(self, pos):
        angles, outOfRange = self.kinematics.getAnglesRaw(pos)
        return angles

    def simpleMovementExample(self):
        for i in range(-60,60,10):
            self.robo.moveToRaw([i,0,50])
            # time.sleep(0.5)

    def myMove(self):
        path = [[-70, 0, 20],[-70, 0, 60],[0, 0, 60],[70, 0, 60],[70, 0, 20]]
        for point in path:
            self.robo.moveToRaw(point)

    def auroraMoves(self):
        self.robo.moveToRawBlocking([30,10,60])
        time.sleep(1.0)
        self.robo.setAnglesBlocking([-120, -45, 45, 45, 45])
        time.sleep(1.0)
        self.robo.setAnglesBlocking([-167, 1, 90, 80, -70])

    def wafe(self):
        log('This is gonna take forever 😏')
        while True:
            for angle in range(-29, 30, 1):
                self.robo.setAngles([0, -angle, angle*1.1, -angle*1.4, angle*2])
            for angle in range(29, -30, -1):
                self.robo.setAngles([0, -angle, angle*1.1, -angle*1.4, angle*2])

    def dance(self):
        log('This is gonna take forever 😏')
        velocity = 50
        while True:
            self.robo.setVelocity(velocity)

            self.robo.setVelocityForIndex(2, velocity*2)
            angle = 60
            self.robo.setAnglesBlocking([0, angle, 2*angle, angle, 0])
            angle = 0
            self.robo.setAnglesBlocking([0, angle, 2*angle, angle, 0])

            self.robo.setVelocityForIndex(2, velocity)
            self.robo.setVelocityForIndex(3, velocity*2)
            angle = 60
            self.robo.setAnglesBlocking([0, 0, angle, 2*angle, angle])
            angle = 0
            self.robo.setAnglesBlocking([0, 0, angle, 2*angle, angle])
            
            self.robo.setVelocityForIndex(3, velocity)
            self.robo.setVelocityForIndex(4, velocity*2)
            angle = 60
            self.robo.setAnglesBlocking([0, 0, 0, angle, 2*angle])
            angle = 0
            self.robo.setAnglesBlocking([0, 0, 0, angle, 2*angle])

            self.robo.setVelocityForIndex(1, velocity)
            self.robo.setVelocityForIndex(2, velocity*2)
            self.robo.setVelocityForIndex(3, velocity*2)
            self.robo.setVelocityForIndex(4, velocity*2)
            angle = 60
            self.robo.setAnglesBlocking([0, angle, 2*angle, 2*angle, 2*angle])
            angle = 0
            self.robo.setAnglesBlocking([0, angle, 2*angle, 2*angle, 2*angle])


    def hello(self):
        self.robo.setAngles([-90,0,0,0,0])
        time.sleep(4)
        self.robo.setAngles([-90,0,0,0,90])
        time.sleep(1)
        self.robo.setAngles([-160,0,0,0,90])
        time.sleep(1)
        self.robo.setAngles([0,0,0,0,90])
        time.sleep(1)
        self.robo.setAngles([-70,-20,20,-20,20])

    def getLine(self):
        step = 1
        start = -60
        end = 60
        y = 0
        z = 50
        fname = "line_step{}start{}end{}".format(step,start,end)
        angles = []
        for x in range(start,end,step):
            angle, outOfRange = self.kinematics.getAnglesRaw([x,y,z])
            if not outOfRange:
                angles.append(angle)
        return angles, fname


    def createCircle(self):
        stepDegree = 6
        r = 30
        mx = 20
        my = 0
        mz = 50
        angles = []
        for alpha in range( 0, 360, stepDegree):
            [x,y,z] = self.__getCircleCoordinatesFrom(r,mx,my,mz,alpha)
            angle, outOfRange = self.kinematics.getAnglesRaw([x,y,z])
            if not outOfRange:
                angles.append(angle)
        
        fname = f'moveFiles/circle_r{r}_step{stepDegree}_mx{mx}_mz{mz}'
        return angles, fname

    def __getCircleCoordinatesFrom(self, radius, mx, my, mz, alpha):
        """ normal facing in y direction """
        y = my
        x = mx + math.cos(math.radians(alpha)) * radius
        z = mz + math.sin(math.radians(alpha)) * radius
        log("x={}, y={}, z={}".format(x,y,z))
        return [x,y,z]

    def moveCircle(self):
        stepDegree = 12
        r = 20
        mx = -40
        my = -40
        mz = 30
        angles = []
        offset = 90
        for alpha in range( 0 + offset, 360 + offset, stepDegree):
            coordinates = self.__getCircleCoordinatesFrom(r,mx,my,mz,alpha)
            angle = self.__getAngles(coordinates)
            self.robo.setAngles(angle)