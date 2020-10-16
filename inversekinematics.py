from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import math
import myutils

class InverseKinematics():

    def __init__(self):
        self.armLength = 15.7
        self.chain = Chain(name='left_arm', links=[
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
            bounds=(-math.pi/2,math.pi/2)
            ),
            URDFLink(
            name="second",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-math.pi/2,math.pi/2)
            ),
            URDFLink(
            name="third",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, 1, 0],
            bounds=(-math.pi/2,math.pi/2)
            ),
            URDFLink(
            name="tip",
            translation_vector=[0, 0, self.armLength],
            orientation=[0, 0, 0],
            rotation=[0, 0, 0],
            )
        ])
        self.xMin = -3*self.armLength
        self.xMax = 3*self.armLength
        self.yMin = -3*self.armLength
        self.yMax = 3*self.armLength
        self.zMin = -3*self.armLength
        self.zMax = 3*self.armLength

    def __del__(self):
        pass

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
        angles = self.chain.inverse_kinematics(pos)*180/math.pi
        newAngles = [math.floor(angles[1]), math.floor(angles[2]), math.floor(angles[3]), math.floor(angles[4])]
        print("Angles are: {}".format(newAngles))
        return newAngles