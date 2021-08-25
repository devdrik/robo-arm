:fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire:

:bangbang: **Video on Serworm Michael is online** :bangbang: 

:point_right: https://youtu.be/1fdFsHWkn9U :point_left:

:bangbang: **Subscribe on YouTube, don't miss the next part!** :bangbang:

:fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire::fire:

# robo arm

This repo is all about the little robo arm. The community named it **Serworm Michael**, so that is his name now. The arm has a very simple structure, but still enough DoFs to make it a fun challenge to work with. The structure can be 3D printed. The servos are Dynamixel XL330-M288-T. There should be everything you need in this repo. If not, please let me know! 

The project is work in progress, but it already works. I am very happy, if you add features, refactor the code or point out bad practices. Feel free to open an issue, a pull-request or contact me.

You can find a more detailed (german) description here: [devdrik.de/robo-arm](https://devdrik.de/robo-arm/)

**There will be a video on Serworm Michael soon!**

## Material

You wont need much, but you need something for this robo. Here is a list:
* 1 Arduino MKR
* 1 DYNAMIXEL Shield for Arduino MKR
* 5 DYNAMIXEL-XL330-M288-T
* 1 Raspberry Pi
* USB-a to micro USB cable
* A 3D-Printer could help

Find product links here: [devdrik.de/hardware-von-serworm-michael](https://devdrik.de/hardware-von-serworm-michael/)

## Setup

### Arduino
Nothing to setup here. Just flash dynamixel_api from the code/arduino folder to your Arduino and you are all set.

### Python environment

You need a python3 environment with pip installed in order to get the robo arm to work. In that env you need to install [ikpy](https://github.com/Phylliade/ikpy).
```
pip install ikpy
```

### 3D prints

The files to print can be found in the cad section. They should be easy prints, nothing special here. 
You will need:
* 1 base.stl (clamp to table)
* 1 base_element.stl (screwed to base servo)
* 4 arm_element.stl

## Build the bot

Building the robo arm is very easy! 
Put a servo in the base, screw the base_element on that. Then screw the arm_elements to it one after another. done!
You can use the screws shipped with the servos.
Make sure to clamp the base to a table or something solid, otherwise the arm will fall :(

## Configuration

You need to define the serial device in ```main.py```. This device is the arduino with the API.

## Usage

There is not yet a GUI or any other interface. You need to open the main file and write some code in order to get results. The easiest way is to comment in an example. Usually you want to use the API of robo.py to interact with the arm and the API of inversekinematics.py to calculate the input (angles) for the robo API.

You can also use the `teachposition` function to get a little cli and teach the arm some positions and save those for later.

There might be some helpful (german) articles on my blog: [devdrik.de/robo-arm](https://devdrik.de/robo-arm/)

# HAVE FUN!
