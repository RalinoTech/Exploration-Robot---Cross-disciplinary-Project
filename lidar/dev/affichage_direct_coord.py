import os
from math import floor
from adafruit_rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0' #'/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar = RPLidar(None, PORT_NAME, timeout=3)

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
        process_data(scan_data)
        #...............................................................................................................
        #affichage des datas
        # Créer une liste d'angles en degrés
        distance_lidar = scan_data
        angles_lidar=[]
        for i in range(360):
            angles_lidar.append(i)

        print("taille angle", len(angles_lidar), "taille matrice", len(distance_lidar))
        print("nouvelle matrice ",distance_lidar)

        # Convertir les angles en radians
        #angles_rad = np.deg2rad(angles_lidar)

        # Créer une liste de distances
        # distances_int = np.random.sample(len(angles))
        # distances = distances_int*5000

        # Créer un graphique en coordonnées polaires
        fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))

        #on filtre les points

        # Afficher le graphique
        ax.scatter(angles_lidar, distance_lidar, c=distance_lidar, cmap='viridis')

        #intervalle etendu
        #ax.set_rticks([0,1000,5000,10000, 15000])  # Less radial ticks

        #intervalle précis
        ax.set_rticks([0,1000,5000,10000])

        ax.set_rlabel_position(-22.5)  # Get radial labels away from plotted point
        ax.grid(True)

        # Afficher les angles en degrés
        ax.set_xticklabels([0,45,90,135,180,225,270,325,360])
        ax.set_theta_zero_location("N")  # Theta zero location (North)
        ax.set_theta_direction(-1)  # Theta increasing direction (clockwise)

        plt.show()

    #...............................................................................................................





except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()
