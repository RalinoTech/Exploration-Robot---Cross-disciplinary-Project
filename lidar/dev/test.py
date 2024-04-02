#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM9'
DMAX = 4000
IMIN = 0
IMAX = 500

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line

def affichage_comprehension(iterator,line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    #scan permet de stocker la qualité de la mesure, l'angle et la mesure de la distance
    print(scan)
    #for meas in scan:
     #   print(meas[0])

def run():
    while(1):
        print("salut")
        lidar = RPLidar(PORT_NAME)
       # fig = plt.figure()
        ax = plt.subplot(111, projection='polar')
        line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                            cmap=plt.cm.Greys_r, lw=0)
       # ax.set_rmax(DMAX)
        #ax.grid(True)

        iterator = lidar.iter_scans(max_buf_meas=1000, min_len=5)

        affichage_comprehension(iterator,line)

        #ani = animation.FuncAnimation(fig, update_line,
         #   fargs=(iterator, line), interval=50,cache_frame_data=False)
        
       # plt.show()
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    run()