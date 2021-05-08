import threading
from adafruit_servokit import ServoKit

class AsyncServos(threading.Thread):
    lock = threading.Lock()
    kit = ServoKit(channels=16)

    def moveServo(self, servoIndex, angle):
        with lock:
            kit.servo[servoIndex].angle = angle