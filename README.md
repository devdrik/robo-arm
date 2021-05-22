# robo arm

This repo is all about the little robo arm. The community named it **Serworm Michael**, so that is his name now. The arm has a very simple structure, but still enough DoFs to make it a fun challenge to work with. The structure can be 3D printed. The servos are Dynamixel XL330-M288-T. There should be everything you need in this repo. If not, please let me know! 

The project is work in progress, but it already works. I am very happy, if you add features, refactor the code or point out bad practices. Feel free to open an issue, a pull-request or contact me.

## Setup

### Arduino
Nothing to setup here. Just flash dynamixel_api from the code/arduino folder to your Arduino and you are all set.

### Python environment

You need a python3 environment with pip installed in order to get the robo arm to work. In that env you to install [ikpy](https://github.com/Phylliade/ikpy).
```
pip install ikpy
```

### 3D prints

The files to print can be found in the cad section. They should be easy prints, nothing special here. 


## Usage

There is not yet a GUI or any other interface. You need to open the main file and write some code in order to get results. The easiest way is to comment in an example. Usually you want to use the API of robo.py to interact with the arm and the API of inversekinematics.py to calculate the input (angles) for the robo API.

You can also use the `teachposition` function to get a little cli and teach the arm some positions and save those for later.