from dynamixel import Dynamixel
from time import sleep
import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()



servo0 = Dynamixel(0, ser)
servo1 = Dynamixel(1, ser)
servo2 = Dynamixel(2, ser)
servo3 = Dynamixel(3, ser)
servo4 = Dynamixel(4, ser)
camServo = Dynamixel(11,ser)


servos = [servo0, servo1, servo2, servo3, servo4, camServo]

for servo in servos:
    servo.setProfileVelocity(200)

waitUart = 0.1


def setAngleAll(angle1, angle2, angle3, angle4):
    function = 3
    correctedAngle1 = angle1 + 180
    correctedAngle2 = angle2 + 180
    correctedAngle3 = angle3 + 180
    correctedAngle4 = angle4 + 180
    ser.flush()
    ser.write("{func}:{ang1}:{ang2}:{ang3}:{ang4}\n".format(func=function, ang1=correctedAngle1, ang2=correctedAngle2, ang3=correctedAngle3, ang4=correctedAngle4).encode("utf-8"))
    sleep(0.2)


ang=0

servo0.setAngle(180)
setAngleAll(ang,ang,ang,ang)
camServo.setAngle(ang)

# for i in range(4):
#     servos[i].setAngle(10)
#     sleep(waitUart)

# sleep(1)
# for i in range(4):
#     servos[i].setAngle(45)
#     sleep(waitUart)

# sleep(1)
# for i in range(4):
#     servos[i].setAngle(70)
#     sleep(waitUart)

sleep(3)

servo4.setAngle(0)
camServo.setAngle(0)
sleep(1)
servo4.setAngle(-90)
camServo.setAngle(90)
sleep(1)
servo4.setAngle(90)
camServo.setAngle(-90)
sleep(1)
servo4.setAngle(0)
camServo.setAngle(0)

servo3.setAngle(0)
camServo.setAngle(0)
sleep(1)
servo3.setAngle(-90)
camServo.setAngle(-90)
sleep(1)
servo3.setAngle(90)
camServo.setAngle(90)
sleep(1)
servo3.setAngle(0)
camServo.setAngle(0)
sleep(0.3)

servo2.setAngle(0)
camServo.setAngle(0)
sleep(1)
servo2.setAngle(-90)
camServo.setAngle(90)
sleep(1)
servo2.setAngle(90)
camServo.setAngle(-90)
sleep(1)
servo2.setAngle(0)
camServo.setAngle(0)
sleep(0.3)

servo1.setAngle(0)
camServo.setAngle(0)
sleep(1)
servo1.setAngle(-90)
camServo.setAngle(-90)
sleep(1)
servo1.setAngle(90)
camServo.setAngle(90)
sleep(1)
servo1.setAngle(0)
camServo.setAngle(0)
sleep(0.3)

setAngleAll(ang,ang,ang,ang)
camServo.setAngle(ang)

ser.close()