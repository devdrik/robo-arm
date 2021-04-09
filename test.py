from dynamixel import Dynamixel
from time import sleep
import serial
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()

servo1 = Dynamixel(1, ser)
servo2 = Dynamixel(2, ser)
servo3 = Dynamixel(3, ser)
servo4 = Dynamixel(4, ser)

servos = [servo1, servo2, servo3, servo4]

waitUart = 0.1

for i in range(4):
    servos[i].setAngle(10)
    sleep(waitUart)

sleep(1)
for i in range(4):
    servos[i].setAngle(45)
    sleep(waitUart)

sleep(1)
for i in range(4):
    servos[i].setAngle(70)
    sleep(waitUart)



# servo1.setAngle(0)
# sleep(1)
# servo1.setAngle(-90)
# sleep(1)
# servo1.setAngle(90)
# sleep(1)
# servo1.setAngle(0)
# sleep(0.3)

# servo2.setAngle(0)
# sleep(1)
# servo2.setAngle(-90)
# sleep(1)
# servo2.setAngle(90)
# sleep(1)
# servo2.setAngle(0)
# sleep(0.3)

# servo3.setAngle(0)
# sleep(1)
# servo3.setAngle(-90)
# sleep(1)
# servo3.setAngle(90)
# sleep(1)
# servo3.setAngle(0)
# sleep(0.3)

# servo4.setAngle(0)
# sleep(1)
# servo4.setAngle(-90)
# sleep(1)
# servo4.setAngle(90)
# sleep(1)
# servo4.setAngle(0)

ser.close()