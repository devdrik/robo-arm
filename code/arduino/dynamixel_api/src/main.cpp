/*******************************************************************************
* Copyright 2016 ROBOTIS CO., LTD.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#include <DynamixelShield.h>

#define DEBUG_SERIAL Serial
#define DATA_SERIAL Serial
#define SERIAL_BAUD 115200

#define DEBUG false

const float DXL_PROTOCOL_VERSION = 2.0;
const uint8_t servosIDs[] = {0,1,2,3,4,11};
// the size of goalAngles should equal the highest servoID+1. This makes it easy to use the servoId as index to access goalAngles
float goalAngles[] = {0,0,0,0,0,0,0,0,0,0,0,0};

DynamixelShield dxl;


const char separator = ':';
const char msgEndChar = '\n';
#define FUNC_SET_ANGLE 1
#define FUNC_GET_ANGLE 2
#define FUNC_SET_ANGLE_FOUR 3
#define FUNC_SET_PROFILE_VELOCITY 4
#define FUNC_SET_PROFILE_VELOCITY_ALL 5
#define FUNC_HAS_REACHED_ANGLE 6
#define FUNC_SET_POSITION_MODE_ALL 7
#define FUNC_TORQUE_OFF_ALL 8
#define FUNC_IS_MOVING 9


//This namespace is required to use Control table item names
using namespace ControlTableItem;



void setAngle(u_int8_t servoId, float angle) {
  goalAngles[servoId] = angle;
  dxl.setGoalPosition(servoId, angle, UNIT_DEGREE);
}

float getAngle(u_int8_t servoId) {
  return dxl.getPresentPosition(servoId, UNIT_DEGREE);
}

void writeToControlTable(uint8_t servoID, uint8_t itemIdx, int32_t data) {
  dxl.torqueOff(servoID);
  dxl.writeControlTableItem(itemIdx, servoID, data);
  dxl.torqueOn(servoID);
}

void setProfileVelocity(uint8_t servoID, uint32_t velocity) {
  // 0-32767; 0 -> max speed
  writeToControlTable(servoID, PROFILE_VELOCITY, velocity);
}

void setProfileVelocityAll(uint32_t velocity) {
  for (uint8_t id : servosIDs) {
    writeToControlTable(id, PROFILE_VELOCITY, velocity);
  }
}

bool hasReachedGoalAngle(uint8_t servoId) {
  delay(50);
  int moving_status = dxl.readControlTableItem(MOVING_STATUS, servoId);
  // DEBUG_SERIAL.print("moving_status: ");
  // DEBUG_SERIAL.println(moving_status, BIN);
  int mask = 3;
  return (moving_status & mask) == 1;
  // float offset = 3;
  // float currentAngle = getAngle(servoId);
  // return currentAngle >= goalAngles[servoId] - offset &&
  //         currentAngle <= goalAngles[servoId] + offset;
}

void setOperatingMode(uint8_t servoID, uint8_t mode) {
  dxl.torqueOff(servoID);
  dxl.setOperatingMode(servoID, mode);
  dxl.torqueOn(servoID);
}

void torqueOff(uint8_t servoID) {
  dxl.torqueOff(servoID);
}

void floatToByte(byte* arr, float value) {
      long l = *(long*) &value;

      arr[0] = l & 0x00FF;
      arr[1] = (l >> 8) & 0x00FF;
      arr[2] = (l >> 16) & 0x00FF;
      arr[3] = l >> 24;
}

bool isMoving(uint8_t servoID) {
  int moving_status = dxl.readControlTableItem(MOVING_STATUS, servoID);
  int mask = 2;
  return (moving_status & mask) > 0;
}

void setup() {
  // put your setup code here, to run once:
  
  // For Uno, Nano, Mini, and Mega, use UART port of DYNAMIXEL Shield to debug.
  DATA_SERIAL.begin(SERIAL_BAUD);
  // while(!DEBUG_SERIAL);
  // if (DATA_SERIAL != DEBUG_SERIAL) {
  //   DEBUG_SERIAL.begin(SERIAL_BAUD);
  // }

  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);

  // Set all servos to position mode
  for(uint8_t servoID : servosIDs) {
    if(dxl.ping(servoID)) {
      dxl.torqueOff(servoID);
      dxl.setOperatingMode(servoID, OP_POSITION);
      dxl.writeControlTableItem(MOVING_THRESHOLD, servoID, 7);
      dxl.torqueOn(servoID);
      // DEBUG_SERIAL.print("Servo ");
      // DEBUG_SERIAL.print(servoID);
      // DEBUG_SERIAL.println(" set to Position Mode");
    } else {
      // DEBUG_SERIAL.print("Servo ");
      // DEBUG_SERIAL.print(servoID);
      // DEBUG_SERIAL.println(" not responding");
    }
  }

  // setProfileVelocity(0, 20);
  // setAngle(0, 1000);
  // while (!hasReachedGoalAngle(0))
  // {
  //   DEBUG_SERIAL.print("angle: ");
  //   DEBUG_SERIAL.println(getAngle(0));
  // }
  
  // DEBUG_SERIAL.print("done, angle: ");
  // DEBUG_SERIAL.println(getAngle(0));

  // setProfileVelocity(0, 20);
  // DEBUG_SERIAL.print("moving_threashold: ");
  // DEBUG_SERIAL.println(dxl.readControlTableItem(MOVING_THRESHOLD, 0));
  // setAngle(0, 20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // hasReachedGoalAngle(0);
  // delay(20);
  // // DEBUG_SERIAL.print("hasReached2: ");
  // // DEBUG_SERIAL.println(hasReachedGoalAngle(0));
  // // delay(100);
  // // DEBUG_SERIAL.print("hasReached3: ");
  // // DEBUG_SERIAL.println(hasReachedGoalAngle(0));
  // delay(10000);
  // DEBUG_SERIAL.println("delayed 10");
  // hasReachedGoalAngle(0);
  // // DEBUG_SERIAL.print("hasReached4: ");
  // // DEBUG_SERIAL.println(hasReachedGoalAngle(0));
  // // while (!hasReachedGoalAngle(0))
  // //   DEBUG_SERIAL.println("Im looping");
  // // {
  // // DEBUG_SERIAL.print("hasReached after: ");
  // // DEBUG_SERIAL.println(hasReachedGoalAngle(0));

  // delay(500);
  // setAngle(0, 1);
  // while (!hasReachedGoalAngle(0))
  // {
  //   DEBUG_SERIAL.print("angle: ");
  //   DEBUG_SERIAL.println(getAngle(0));
  // }

  // DEBUG_SERIAL.print("done, angle: ");
  // DEBUG_SERIAL.println(getAngle(0));

  
}
// FUNC:PARAM1:PARAMX\n

void loop() {

  if ( DATA_SERIAL.available() > 0 ) {
    uint8_t function = DATA_SERIAL.readStringUntil(separator).toInt();
    uint8_t id;
    float angle;
    uint32_t profileVelocity;

    switch (function)
    {
    case FUNC_SET_ANGLE:
      // FUNC:ID:ANGLE
      id = DATA_SERIAL.readStringUntil(separator).toInt();
      angle = DATA_SERIAL.readStringUntil(msgEndChar).toFloat();
      // Serial.print("Angle read and converted from string: ");
      // Serial.println(angle);
      setAngle(id, angle);
      break;
    
    case FUNC_GET_ANGLE:
      // FUNC:ID
      id = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      angle = getAngle(id);
      byte angleBytes[4];
      floatToByte(angleBytes, angle);
      DATA_SERIAL.write(angleBytes, 4);
      break;

    case FUNC_SET_ANGLE_FOUR:
    // FUNC:ANGLE1:ANGLE2:ANGLE3:ANGLE4
      setAngle(1, DATA_SERIAL.readStringUntil(separator).toFloat());
      setAngle(2, DATA_SERIAL.readStringUntil(separator).toFloat());
      setAngle(3, DATA_SERIAL.readStringUntil(separator).toFloat());
      setAngle(4, DATA_SERIAL.readStringUntil(msgEndChar).toFloat());
      break;

    case FUNC_SET_PROFILE_VELOCITY:
      // FUNC:ID:VELOCITY
      id = DATA_SERIAL.readStringUntil(separator).toInt();
      profileVelocity = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      setProfileVelocity(id, profileVelocity);
      break;

    case FUNC_SET_PROFILE_VELOCITY_ALL:
      // FUNC:VELOCITY
      profileVelocity = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      setProfileVelocityAll(profileVelocity);
      break;

    case FUNC_HAS_REACHED_ANGLE:
      // FUNC:ID
      id = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      bool hasReachedAngle;
      hasReachedAngle = hasReachedGoalAngle(id);
      byte hasReached;
      hasReached = hasReachedAngle ? (byte) 1 : (byte) 0;
      DATA_SERIAL.write(hasReached);
      break;

    case FUNC_SET_POSITION_MODE_ALL:
      // FUNC:ID
      id = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      setOperatingMode(id, OP_POSITION);
      break;

    case FUNC_TORQUE_OFF_ALL:
      // FUNC:ID
      id = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      torqueOff(id);
      break;

    case FUNC_IS_MOVING:
      // FUNC:ID
      id = DATA_SERIAL.readStringUntil(msgEndChar).toInt();
      byte isMovingByte; 
      isMovingByte = (byte)(isMoving(id) ? 1 : 0);
      DATA_SERIAL.write(isMovingByte);
      break;

    default:
      break;
    }
  }

}