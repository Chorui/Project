
# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import socket
import logging
import sys
import time
import numpy as np

from Adafruit_BNO055 import BNO055


# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
#bno = BNO055.BNO055(rst='P9_12')


# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))


UDP_IP = "192.168.137.1"
UDP_PORT = 5005

#FOR SAVING ARRAYS
#Time = np.zeros(2000)
xValues = np.zeros(2000)
yValues = np.zeros(2000)
zValues = np.zeros(2000)

print('Reading BNO055 data, press Ctrl-C to quit...')

i = 0
#Velocity = 0
#Distance = 0
#Cut = 0
#CutVel = 0


#SETUP
print('CALIBRATION PHASE')
while True:
    sys, gyro, accel, mag = bno.get_calibration_status()
    time.sleep(1)
    print('Sys: %d Gyro: %d Accel: %d Mag: %d' %(sys,gyro,accel,mag))
    if sys == 3 and gyro == 3 and accel == 3 and mag == 3:
        print('Calibrated.')       
        break

timeout = time.time() + 60/3 #20 seconds from now

#MAIN LOOP
while True:
    test = 0 
    if test == 5 or time.time() > timeout:
        break
    test = test - 1     
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Read the accelerometer data!
    x,y,z = bno.read_linear_acceleration() 
    # Print everything out.
    MESSAGE = ('Heading={0:7.2F} | Roll={1:7.2F} | Pitch={2:7.2F} | x={3:6.2F} | y={4:6.2F} | z={5:6.2F}'.format(heading, roll, pitch, x, y, z))
    print(MESSAGE)
   
    xValues[i] = x
    yValues[i] = y
    zValues[i] = z
    i += 1

   #if x < Cut:
     #   x = 0        
   # Velocity = Velocity + x
   # if Velocity < CutVel:
   #     Velocity = 0
   # Distance = Distance + Velocity
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
  #  Time[i] = x i += 1 if i == 10:
   #     i = 0
    #    print (Time)   
    time.sleep(0.01)  #0.01 is the optimum
   
   # print ("Velocity:", Velocity)
   # print ("Distance:", Distance)

print(xValues)
print(yValues)
print(zValues)  
#print(Time)
np.savetxt('xArc.out', xValues, delimiter=',')   # X is an array
np.savetxt('yArc.out', yValues, delimiter=',')
np.savetxt('zArc.out', zValues, delimiter=',')
#np.savetxt('Time.out', Time, delimiter=',')
 # Other values you can optionally read:
    # Orientation as a quaternion:
    #x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    #temp_c = bno.read_temp()
    # Magnetometer data (in micro-Teslas):
    #x,y,z = bno.read_magnetometer()
    # Gyroscope data (in degrees per second):
    #x,y,z = bno.read_gyroscope()
    # Accelerometer data (in meters per second squared):
    #x,y,z = bno.read_accelerometer()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    #x,y,z = bno.read_linear_acceleration()
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    #x,y,z = bno.read_gravity()
    # Sleep for a second until the next reading.
