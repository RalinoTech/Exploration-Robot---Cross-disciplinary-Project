import os
from math import cos, sin, radians
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Create a figure and axis for the plot
fig, ax = plt.subplots()

#global verrou
global verrou
verrou=1

# used to scale data to fit on the screen
max_distance = 5000

def affichage_lidar(verrou):
        #if verrou == 1:
        plt.gca(); ax.text(0, 0, '▲',color = 'red') #♣
        #verrou=0

def actualisation():
    plt.draw()
    plt.pause(0.001)
     

def process_data(data):
    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to equal for correct scaling

    for angle, distance in enumerate(data):
        if distance != -1:
            # Convert polar coordinates to Cartesian coordinates
            y = distance * cos(radians(angle))
            x = distance * sin(radians(angle))
            plt.ylabel('<- arrière du robot            &            avant du robot ->')
            plt.xlabel('<- gauche du robot            &            droite du robot ->')
            ax.plot(x, y, 'bo', markersize=1)  # Plot each point


try:
    #verrou pour affichage du lidar
    #verrou=1

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
        affichage_lidar(verrou)
        actualisation()
        


except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()
