import os
from math import cos, sin, radians
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# used to scale data to fit on the screen
max_distance = 2000

def process_data(data):
    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to equal for correct scaling

    for angle, distance in enumerate(data):
        if distance != -1:
            # Convert polar coordinates to Cartesian coordinates
            x = distance * cos(radians(angle))
            y = distance * sin(radians(angle))
            plt.xlabel('<- arrière du robot            &            avant du robot ->')
            plt.ylabel('Plan détection LIDAR')
            ax.plot(x, y, 'bo', markersize=1)  # Plot each point
            #plt.title('falut')

    plt.draw()
    plt.pause(0.01)

try:
    for scan in lidar.iter_scans():
        scan_data = [-1] * 360  # Initialize data for each new scan
        for (_, angle, distance) in scan:
            ang = int(angle) % 360
            scan_data[ang] = distance
        #condition pour gérer les obstacles
        if ang>180 and ang<360 and distance<300 and distance!=-1:
                print("Alerte obstacle proche")
        else:
            print("je roule")
        #on trace le graphique
        process_data(scan_data)
        


except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()
