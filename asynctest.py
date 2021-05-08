from inversekinematics import InverseKinematics
import time
import threading
from adafruit_servokit import ServoKit

class move(threading.Thread):
    
    def __init__(self, servoIndex, angle, controlTimeInMs): 
        threading.Thread.__init__(self) 
        self.servoIndex = servoIndex
        self.angle = angle
        self.controlTimeInMs = controlTimeInMs
 
    def run(self): 
        with lock:
            currentAngle = kit.servo[self.servoIndex].angle
        deltaAngle = abs(currentAngle - self.angle)
        incrementAngle = 3
        if deltaAngle > incrementAngle:
            waitTime = self.controlTimeInMs / deltaAngle / 1000
            direction = 1 if self.angle > currentAngle else -1
            while abs(currentAngle - self.angle) > incrementAngle:
                with lock:
                    kit.servo[self.servoIndex].angle += incrementAngle * direction
                    currentAngle = kit.servo[self.servoIndex].angle
                time.sleep(waitTime)

class moveSpeed(threading.Thread):
    
    def __init__(self, servoIndex, angle, speed): 
        threading.Thread.__init__(self) 
        self.servoIndex = servoIndex
        self.angle = angle
        self.speed = speed
 
    def run(self): 
        with lock:
            currentAngle = kit.servo[self.servoIndex].angle
        deltaAngle = abs(currentAngle - self.angle)
        incrementAngle = 2
        if deltaAngle > incrementAngle:
            direction = 1 if self.angle > currentAngle else -1
            while abs(currentAngle - self.angle) > incrementAngle:
                with lock:
                    kit.servo[self.servoIndex].angle += incrementAngle * direction
                    currentAngle = kit.servo[self.servoIndex].angle
                time.sleep(self.speed)

kit = ServoKit(channels=16)
lock = threading.Lock()

def moveAngles(angles, controlTimeInMs):
    moves = []
    for i in range(len(angles)):
        print("move no: {}, angle: {}".format(i, angles[i]))
        mov = move(i+1, angles[i], controlTimeInMs)
        mov.start()
        moves.append(mov)
    for mov in moves:
        mov.join()

def moveAnglesSpeed(angles, speed):
    moves = []
    for i in range(len(angles)):
        print("moveSpeed no: {}, angle: {}".format(i, angles[i]))
        mov = moveSpeed(i+1, angles[i], speed)
        mov.start()
        moves.append(mov)
    for mov in moves:
        mov.join()


angles1 = [[45,45,45], [135,135,135], [90,90,90]]
for angle in angles1:
    moveAngles(angle, 500)
for angle in angles1:
    moveAnglesSpeed(angle, 0.1)