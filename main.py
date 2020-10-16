from cv import CV
from inversekinematics import InverseKinematics
from robo import Robo
import time

try:
    myCv = CV()
    kinematics = InverseKinematics()
    myRobo = Robo()

    while True:
        x,y = myCv.getPosition()
        angles = kinematics.getAngles([x, 50, 60])
        myRobo.moveTo(angles)
        time.sleep(2)
except KeyboardInterrupt:
    print("end")

