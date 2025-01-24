/* 
 * ------------------------------------------------------------------------------
 * This Arduino sketch sends time data and specified signals to Python
 * Spring 2022
 * This program collects both accelerations and angular velocities from two (2)
 * LSM6DS0 devices that have been daisy-chained using I2C cables (qwiic).
 * It is assumed that the two devices have been modified to have two distinct I2C addresses.
 * The data can be collected using LMS6DS0_2_PyArduino_DAQ_Driver.py,
 * which saves the data to a *.csv file, or the Serial Monitor or Plotter can be 
 * used by typing 'f,50' to collect values for testing in a free-run mode.
 * The range must be set for acceleration and angular velocity.
 * Currently, it is default to 2g and 
 * Last updated 3/26/22 rgl
 * 
 * NOTE: The code is a simple extension of earlier version used with 1 device
 * No attempt was made to make the code compact or more efficient
 * If an experiment only needs certain data, edit to limit the data being send
 * over serial, as this will allow larger loop rates.
 * 
 * NOTES: The data is currently set to be collected in raw integer form. However,
 * examples are shown (commented out) for collecting values in g's or deg/s.
 * ------------------------------------------------------------------------------
*/

#include <Wire.h>              // Must include Wire library for I2C
#include <SparkFunLSM6DSO.h> // 

int myIMUaddr1 = 107; // this is address for device 1 (default 0x6B)
int myIMUaddr2 = 106; // this is address for device 1 (default 0x6A)

LSM6DSO myIMU1;   // constructor to name the device 1, access functions
LSM6DSO myIMU2;   // constructor to name the device2, access functions

unsigned long timer = 0;    // used to check current time [microseconds]
long loopTime = 0;       // default time between updates, but will be set in python Code [microseconds]
bool initLooptime = false;  // boolean (T/F) to check if loop time has already been set
bool stopProgram = false;

int rawAccY1 = 0;
int rawAccY2 = 0;

void setup() {
  Serial.begin(19200);         // Being serial comms and set Baud rate
  Wire.begin(myIMUaddr1);
  Wire.begin(myIMUaddr2);
  if (myIMU1.begin(myIMUaddr1)==false || myIMU2.begin(myIMUaddr2)==false){ 
    // Waits until connections are made to both
    while(1);
  }  
  myIMU1.initialize(BASIC_SETTINGS);
  myIMU2.initialize(BASIC_SETTINGS);
  timer = micros();             // start timer
  // set accelerometer 1 range (2, 4, 8, or 16 g)
  myIMU1.setAccelRange(2);
  //myIMU.setAccelRange(4); 
  //myIMU.setAccelRange(8);
  //myIMU.setAccelRange(16);
  // set gyro 1 range (125, 250 500, 1000, 2000 deg/sec)
  myIMU1.setGyroRange(125);
  //myIMU.setGyroRange(250); 
  //myIMU.setGyroRange(500);
  //myIMU.setGyroRange(1000);
  //myIMU.setGyroRange(2000);
  // set accelerometer 2 range (2, 4, 8, or 16 g)
  myIMU2.setAccelRange(2);
  //myIMU.setAccelRange(4); 
  //myIMU.setAccelRange(8);
  //myIMU.setAccelRange(16);
  // set gyro 2 range (125, 250 500, 1000, 2000 deg/sec)
  myIMU2.setGyroRange(125);
  //myIMU.setGyroRange(250); 
  //myIMU.setGyroRange(500);
  //myIMU.setGyroRange(1000);
  //myIMU.setGyroRange(2000);       
}
 
void loop() {

  if (Serial.available() > 0) {       // if data is available
    String str = Serial.readStringUntil('\n');
    readFromPC(str);
  }
  if (initLooptime && !stopProgram)      // once loop time has been initialized
  {
  
    timeSync(loopTime);   // sync up time to match data rate
    unsigned long currT = micros();  // get current time
    // read accelerations from device 1
    // rawAccX1 = myIMU1.readRawAccelX();     // get X acceleration raw data (Integer value)
    // can change to read in g (float) 
    // AccX1 = myIMU1.readFloatAccelX();     // get X acceleration in g (float value)
    rawAccY1 = myIMU1.readRawAccelY();     // get Y acceleration raw data (Integer value)
    // rawAccZ1 = myIMU1.readRawAccelZ();     // get Z acceleration raw data (Integer value)
    // read gyroscope angular velocities from device 1
    // rawGyroX1 = myIMU1.readRawGyroX();     // get X gyro raw data (Integer value)
    // rawGyroY1 = myIMU1.readRawGyroY();     // get Y gyro raw data (Integer value)
    // rawGyroZ1 = myIMU1.readRawGyroZ();     // get Z gyro raw data (Integer value)
    
    // read accelerations from device 2
    // rawAccX2 = myIMU2.readRawAccelX();     // get X acceleration raw data (Integer value)
    // can change to read in g (float) 
    // AccX2 = myIMU2.readFloatAccelX();     // get X acceleration in g (float value)
    rawAccY2 = myIMU2.readRawAccelY();     // get Y acceleration raw data (Integer value)
    // rawAccZ2 = myIMU2.readRawAccelZ();     // get Z acceleration raw data (Integer value)
    // read gyroscope angular velocities from device 2
    // rawGyroX2 = myIMU2.readRawGyroX();     // get X gyro raw data (Integer value)
    // rawGyroY2 = myIMU2.readRawGyroY();     // get Y gyro raw data (Integer value)
    // rawGyroZ2 = myIMU2.readRawGyroZ();     // get Z gyro raw data (Integer value)
        
    // Send data over serial line to computer
    sendToPC(&currT);
    // sendToPC(&rawAccX1);
    // sendToPC(&AccX1); // send floats via serial (check Python reading)
    sendToPC(&rawAccY1);
    // sendToPC(&rawAccZ1);

    // sendToPC(&rawGyroX1);
    // sendToPC(&rawGyroY1);
    // sendToPC(&rawGyroZ1);

    // sendToPC(&rawAccX2);
    // sendToPC(&AccX2); // send floats via serial (check Python reading)
    sendToPC(&rawAccY2);
    // sendToPC(&rawAccZ2);

    // sendToPC(&rawGyroX2);
    // sendToPC(&rawGyroY2);
    // sendToPC(&rawGyroZ2);

  }
  else if (initLooptime && stopProgram)
  {
    // also free run
    // read accelerations from device 1
    // rawAccX1 = myIMU1.readRawAccelX();     // get X acceleration raw data (Integer value)
    //rawAccY1 = myIMU1.readRawAccelY();     // get Y acceleration raw data (Integer value)
    // rawAccZ1 = myIMU1.readRawAccelZ();     // get Z acceleration raw data (Integer value)
    // read gyroscope angular velocities from device 1
    // rawGyroX1 = myIMU1.readRawGyroX();     // get X gyro raw data (Integer value)
    // rawGyroY1 = myIMU1.readRawGyroY();     // get Y gyro raw data (Integer value)
    // rawGyroZ1 = myIMU1.readRawGyroZ();     // get Z gyro raw data (Integer value)

    // read accelerations from device 2
    // rawAccX2 = myIMU2.readRawAccelX();     // get X acceleration raw data (Integer value)
    //rawAccY2 = myIMU2.readRawAccelY();     // get Y acceleration raw data (Integer value)
    // rawAccZ2 = myIMU2.readRawAccelZ();     // get Z acceleration raw data (Integer value)
    // read gyroscope angular velocities from device 2
    // rawGyroX2 = myIMU2.readRawGyroX();     // get X gyro raw data (Integer value)
    // rawGyroY2 = myIMU2.readRawGyroY();     // get Y gyro raw data (Integer value)
    // rawGyroZ2 = myIMU2.readRawGyroZ();     // get Z gyro raw data (Integer value)

    // send to serial - free run allows use of Serial Monitor and Plotter
    // Serial.print("AccX:");
    // Serial.print(myIMU1.readFloatAccelX());
    // Serial.print(", ");
    Serial.print("AccY1:");
    Serial.print(myIMU1.readFloatAccelY());
    Serial.print(", ");
    Serial.print("AccY2:");
    Serial.print(myIMU2.readFloatAccelY());
    Serial.print("\n");
    delay(50);

  }

  // end of loop()

}

/*
 * Timesync calculates the time the arduino needs to wait so it 
 * outputs data at the specified rate
 * Input: deltaT - the data transfer period in microseconds
 */
void timeSync(unsigned long deltaT)
{
  unsigned long currTime = micros();  // get current time
  long timeToDelay = deltaT - (currTime - timer); // calculate how much time to delay for [us]
  
  if (timeToDelay > 5000) // if time to delay is large 
  {
    // Split up delay commands into delay(milliseconds)
    delay(timeToDelay / 1000);

    // and delayMicroseconds(microseconds)
    delayMicroseconds(timeToDelay % 1000);
  }
  else if (timeToDelay > 0) // If time to delay is positive and small
  {
    // Use delayMicroseconds command
    delayMicroseconds(timeToDelay);
  }
  else
  {
      // timeToDelay is negative or zero so don't delay at all
  }
  timer = currTime + timeToDelay;
}


void readFromPC(const String input)
{
  int commaIndex = input.indexOf(',');
  char command = input.charAt(commaIndex - 1);
  String data = input.substring(commaIndex + 1);    
  int rate = 0;
  switch(command)
  {
    case 'r':
      // rate command
      rate = data.toInt();
      loopTime = 1000000/rate;         // set loop time in microseconds to 1/frequency sent
      initLooptime = true;             // no longer check for data
      timer = micros();
      break;
    case 's':
      // stop command
      stopProgram = true;
      break;
    case 'f':
      // free run
      initLooptime = true;
      stopProgram = true;
      break;
    default:
    // Otherwise, do nothing
      break;
  
  }

}

// ------------------------------------------------------------------------------------------------------------
// Send Data to PC: Methods to send different types of data to PC
// ------------------------------------------------------------------------------------------------------------

void sendToPC(int* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 2);
}

void sendToPC(float* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
 
void sendToPC(double* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}

void sendToPC(unsigned long* data)
{
  byte* byteData = (byte*)(data);
  Serial.write(byteData, 4);
}
