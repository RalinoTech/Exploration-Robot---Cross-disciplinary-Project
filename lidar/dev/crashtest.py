#Code avec recuperation angle/distance

import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

# Setup the RPLidar
PORT_NAME = 'COM9' #'/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar = RPLidar(None,PORT_NAME)
# used to scale data to fit on the screen
max_distance = 4000

def process_data(data):
    print(data)

scan_data = [-1]*360

try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            ang = min([359, floor(angle)])
            scan_data[ang] = distance

        # Affichage des données sur un graphique polaire
        print("caca")

        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, polar=True)

        theta = np.radians(range(360))
        ax.scatter(theta, scan_data)  # Utilisation de ax.scatter() pour afficher des points
        ax.set_rmax(max_distance)
        ax.set_title('Graphique polaire des données du Lidar')

        print("kiki")
        #plt.draw()
        plt.show()
        plt.clear()


        #plt.pause(0.001)  # Pause pour rafraîchir le tracé
        #plt.clear()

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()
lidar.reset()