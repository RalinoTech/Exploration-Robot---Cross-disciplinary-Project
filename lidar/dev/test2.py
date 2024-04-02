import os
from math import floor
from adafruit_rplidar import RPLidar


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0' #'/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar = RPLidar(None, PORT_NAME, timeout=50)

# used to scale data to fit on the screen
max_distance = 4000

def process_data(data):
    print(data)

scan_data = [-1]*360

try:
#    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        

        for i in range(len(scan_data)):
            if scan_data[i]<=300 and scan_data[i]!=-1:
                print("ARRA LES CONDéES")
            else:
                print("je roule")

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()

