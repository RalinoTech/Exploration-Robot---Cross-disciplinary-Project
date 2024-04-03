import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

# Setup the RPLidar
PORT_NAME = 'COM3' #'/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 4000

def process_data(data):
    print(data)

scan_data = [-1]*360

try:
#    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            ang=min([359, floor(angle)])
            scan_data[ang] = distance
            #if ang>180 and ang<360 and distance<300 and distance!=-1:
                #print("ARRA LES CONDéES")
            #else:
                #print("je roule")
           

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()



