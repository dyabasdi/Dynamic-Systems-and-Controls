from ArduinoDAQ import SerialConnect
import numpy as np
import time

portName = 'COM8' # Communications port name. 
# Make sure portName matches port in Arduino IDE
# portName = '/dev/ttyUSB0'
baudRate   = 19200                     # Baud Rate
dataRate   = 100                       # Acquisition data rate (Hz), do not exceed 500
recordTime = 10                        # Number of seconds to record data
numDataPoints = recordTime * dataRate  # Total number of data points to be saved

print('numDataPoints = ', numDataPoints)
#%% Data lists and Arduino commands
#----------------------------------------------------------------------
# Data to read from Arduino file
#----------------------------------------------------------------------
# NOTE: The following assumes Arduino is sending accelerometer and gyroscope data
# from 3 channels each for 2 LSM6DSO devices, and that the data is in raw integer form
#
# It is recommended that for some experiments, like the two-story, to only collect only those components needed
# for example, may only need accX1 and accX2 (depends on how the device is oriented on the mass/story)
# This will enable maximimizing the data rates

dataNames = ['Time', 'accY1', 'accY2']
dataTypes = [  '=L', '=h', '=h']

#---------------------------------------------------------------------- 
# Command strings that can be sent to Arduino
#----------------------------------------------------------------------
rate_c     = 'r' # Data rate command
stop_c     = 's' # Data rate command


#%% Command data structures 
# Set recordTime variable to 10 seconds
#----------------------------------------------------------------------
commandTimes = [recordTime] # Time to send command
commandData  = [0] # Value to send over
commandTypes = ['s'] # Type of command

# The following creates a unique filename based on universal time
# (so you don't overwrite a previous file)
now = int( time.time() )
snow = str(now)
fileName     = 'test'+snow+'.csv'


#%% Communication with Arduino
#----------------------------------------------------------------------
# Do not edit code below
#----------------------------------------------------------------------
# initializes all required variables
s = SerialConnect(portName, fileName, baudRate, dataRate, \
                  dataNames, dataTypes, commandTimes, commandData, commandTypes)

# Connect to Arduino and send over rate
s.connectToArduino()

# Start Recording Data
print("Recording...")

# Collect data
while len(s.dataStore[0]) < numDataPoints:
    s.getSerialData()
    
    s.sendCommand() # send command to arduino if ready
    
    # Print number of seconds that have passed
    if len(s.dataStore[0]) % dataRate == 0:
        print(len(s.dataStore[0]) /dataRate)   

# Close Arduino connection and save data
s.close()
