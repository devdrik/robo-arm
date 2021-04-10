from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import math
import myutils
from myLogger import log

class InverseKinematics():

    def __init__(self):
        # Second robo, with dynamixel
        self.armLength = 4
        self.smallArmLength = 4
        lim = 7*math.pi/9
        self.chain = Chain(name='arm', links=[
            OriginLink(
            ),
            URDFLink(
            name="base",
            translation_vector=[0, 0, 0],
            orientation=[0, 0, 0],
            rotation=[0, 0, 1],
            bounds=(-math.pi,math.pi)
            ),
            URDFLink(
            name="first",
            translation_vector=[0, 0, 0],
            orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-lim,lim)
            ),
            URDFLink(
            name="second",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, -1, 0],
            bounds=(-lim,lim)
            ),
            URDFLink(
            name="third",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-lim,lim)
            ),
            URDFLink(
            name="fourth",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, -1, 0],
            bounds=(-lim,lim)
            ),
            URDFLink(
            name="tip",
            translation_vector=[0, 0, self.smallArmLength],
            orientation=[0, 0, 0],
            rotation=[0, 0, 0],
            )
        ])
        self.xMin = -3*self.armLength - self.smallArmLength
        self.xMax = 3*self.armLength + self.smallArmLength
        self.yMin = -3*self.armLength - self.smallArmLength
        self.yMax = 3*self.armLength + self.smallArmLength
        self.zMin = 0
        self.zMax = 3*self.armLength + self.smallArmLength
        self.radToDegreeFactor = 180 / math.pi
        self.degreeToRadFactor = math.pi / 180
        self.numberOfLinks = len(self.chain.links)


    # def __init__(self):
    #     # First robo, with MG995 Servos
    #     self.armLength = 10
    #     self.smallArmLength = 5
    #     self.chain = Chain(name='arm', links=[
    #         OriginLink(
    #         ),
    #         URDFLink(
    #         name="base",
    #         translation_vector=[0, 0, 0],
    #         orientation=[0, 0, 0],
    #         rotation=[0, 0, 1],
    #         bounds=(-math.pi,math.pi)
    #         ),
    #         URDFLink(
    #         name="first",
    #         translation_vector=[0, 0, 0],
    #         orientation=[0, 0, 0],
    #         rotation=[0, 1, 0],
    #         bounds=(-4*math.pi/9,4*math.pi/9)
    #         ),
    #         URDFLink(
    #         name="second",
    #         translation_vector=[0, 0, self.armLength],
    #         orientation=[0, 0, 0],
    #         rotation=[0, -1, 0],
    #         bounds=(-4*math.pi/9,4*math.pi/9)
    #         ),
    #         URDFLink(
    #         name="third",
    #         translation_vector=[0, 0, self.armLength],
    #         orientation=[0, 0, 0],
    #         rotation=[0, 1, 0],
    #         bounds=(-4*math.pi/9,4*math.pi/9)
    #         ),
    #         URDFLink(
    #         name="fourth",
    #         translation_vector=[0, 0, self.armLength],
    #         orientation=[0, 0, 0],
    #         rotation=[0, -1, 0],
    #         bounds=(-4*math.pi/9,4*math.pi/9)
    #         ),
    #         URDFLink(
    #         name="tip",
    #         translation_vector=[0, 0, self.smallArmLength],
    #         orientation=[0, 0, 0],
    #         rotation=[0, 0, 0],
    #         )
    #     ])
    #     self.xMin = -3*self.armLength - self.smallArmLength
    #     self.xMax = 3*self.armLength + self.smallArmLength
    #     self.yMin = -3*self.armLength - self.smallArmLength
    #     self.yMax = 3*self.armLength + self.smallArmLength
    #     self.zMin = 0
    #     self.zMax = 3*self.armLength + self.smallArmLength
    #     self.radToDegreeFactor = 180 / math.pi
    #     self.degreeToRadFactor = math.pi / 180
    #     self.numberOfLinks = len(self.chain.links)

    def __del__(self):
        pass

    def getPosition(self, angles, allLinks=False):
        anglesRad = []
        if not allLinks:
            anglesRad.append(0)
        for angle in angles:
            anglesRad.append(angle * self.degreeToRadFactor)
        if not allLinks:
            anglesRad.append(0)
        # print("anglesRad: {}".format(anglesRad))
        calcPos = self.chain.forward_kinematics(anglesRad)[:3,3]
        calcPosPerc = []
        calcPosPerc.append(myutils.map(calcPos[0],self.xMin,self.xMax,-100,100))
        calcPosPerc.append(myutils.map(calcPos[1],self.yMin,self.yMax,-100,100))
        calcPosPerc.append(myutils.map(calcPos[2],self.zMin,self.zMax,0,100))
        return calcPosPerc
        

    def getAngles(self, pos):
        if pos[0] == 0:
            pos[0] = 0.01 
        if pos[1] == 0:
            pos[1] = 0.01 
        if pos[2] == 0:
            pos[2] = 0.01 
        pos[0] = myutils.map(pos[0], 0, 100, self.xMin, self.xMax)
        pos[1] = myutils.map(pos[1], 0, 100, self.yMin, self.yMax)
        pos[2] = myutils.map(pos[2], 0, 100, self.zMin, self.zMax)
        anglesRad = self.chain.inverse_kinematics(pos)
        angles = anglesRad * self.radToDegreeFactor
        
        calcPos = self.chain.forward_kinematics(anglesRad)[:3,3]
        calcPosPerc = self.getPosition(angles, True)

        newAngles = []
        for i in range(1, self.numberOfLinks - 1):
            # newAngles.append(math.floor(angles[i]))
            newAngles.append(angles[i])
        outOfRange = False
        for i in range(len(calcPosPerc)):
            if abs(calcPosPerc[i] - pos[i]) > 2:
                outOfRange = True
                break
        log("{} calcPosPerc {}".format(outOfRange, calcPosPerc),"OK")
        print("Angles are: {}".format(newAngles))
        return newAngles, outOfRange
    
    def getAnglesRaw(self, pos):
        if pos[0] == 0:
            pos[0] = 0.01 
        if pos[1] == 0:
            pos[1] = 0.01 
        if pos[2] == 0:
            pos[2] = 0.01 
        corrPos = []
        corrPos.append(pos[0]*self.xMax/100)
        corrPos.append(pos[1]*self.yMax/100)
        corrPos.append(pos[2]*self.zMax/100)
        anglesRad = self.chain.inverse_kinematics(corrPos)
        angles = anglesRad * self.radToDegreeFactor
        
        calcPos = self.chain.forward_kinematics(anglesRad)[:3,3]
        calcPosPerc = self.getPosition(angles, True)
        
        newAngles = []
        for i in range(1, self.numberOfLinks - 1):
            newAngles.append(angles[i])
        outOfRange = False
        for i in range(len(calcPosPerc)):
            if abs(calcPosPerc[i] - pos[i]) > 2:
                outOfRange = True
                break
        log("all Angles: {}".format(angles))
        log("Out of range: {}, calcPosPerc {}".format(outOfRange, calcPosPerc),"OK")
        log("set pos: {}".format(pos),"OK")
        log("Angles are: {}".format(newAngles))
        return newAngles, outOfRange