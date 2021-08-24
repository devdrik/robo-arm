from flask import Flask
from flask import render_template

from inversekinematics import InverseKinematics
from robo import Robo
import time
import math
from myLogger import log
from dynamixel import Dynamixel
from filehandler import FileHandler
from roboMoves import RoboMoves
from robocli import RoboCLI
from actionHandler import ActionHandler

import serial

# set your serial device here:
serialPort = '/dev/ttyACM0'

ser = serial.Serial(serialPort, 115200, timeout=1)
ser.flush()

servos = [Dynamixel(0, ser), Dynamixel(1, ser), Dynamixel(2, ser), Dynamixel(3, ser), Dynamixel(4, ser)]
kinematics = InverseKinematics()
robo = Robo(servos, kinematics)

moves = RoboMoves(robo, kinematics)
fileHandler = FileHandler()
actionHandler = ActionHandler(robo, fileHandler)


app = Flask(__name__, template_folder='static', static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/setPosition")
def setPosition():
    print("fsad")
    return "done"

if __name__ == "__main__":
    app.run()