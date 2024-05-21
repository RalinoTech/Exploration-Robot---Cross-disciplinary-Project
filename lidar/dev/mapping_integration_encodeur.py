#Wheel diameter: 2.5” Wheel Circumference: 7.854”
#Encoder Resolution (ticks per rev): 8
#Distance per encoder tick: 7.854” / 8 x 50 = 0.020”
#formule pour la conversion: (perimètre de la roue)/(resolution encodeur * la reduction du motoreducteur)

#bibliothèques
from math import cos, sin, radians,floor
import matplotlib.pyplot as plt
import numpy as np
from adafruit_rplidar import RPLidar
import time

#.............................................................................
#initialisation du lidar
# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
#matrice du lidar
scan_data = [-1] * 360  # Initialize data for each new scan

#.............................................................................
#recuperation des données des encodeurs
infos_encodeur1 = 0
infos_encodeur2 = 0
dist_encodeur1 = 0
dist_encodeur2 = 0

#.............................................................................
#Integration pour le mapping

nb_ligne_matrice=11000
nb_colonne_matrice=11000
matrice_stockage=np.zeros((nb_ligne_matrice,nb_colonne_matrice))

#.............................................................................
# Create a figure and axis for the plot
fig, ax = plt.subplots()

# used to scale data to fit on the screen
max_distance = 11000

#.............................................................................
#gestion des données du lidar
def process_data(data,dist_encodeur1,dist_encodeur2):

    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to equal for correct scaling

    #on recupere la matrice du lidar
    for angle, distance in enumerate(data):
        if distance != -1:
            # Convert polar coordinates to Cartesian coordinates
            y = distance * cos(radians(angle))+dist_encodeur1
            x = distance * sin(radians(angle))+dist_encodeur2

            #gestion de la position du robot pour le lidar
            # x=x+x_translation
            # y=y+y_translation

            #................................................................
            #stockage des retours lidar dans la matrice matrice_stockage
            #print("Valeur des encodeurs: ",dist_encodeur1," ",dist_encodeur2)

            matrice_stockage[round(x) +5000][round(y)+ 5000]=1

            #matrice_stockage[round(x) + dist_encodeur1][round(y)+dist_encodeur2]=1
            
            #................................................................
            plt.ylabel('<- arrière du robot            &            avant du robot ->')
            plt.xlabel('Plan détection LIDAR')
            ax.plot(x, y, 'bo', markersize=1)  # Plot each point

            #affichage de la matrice de stockage
            #print("la matrice de stockage est ",matrice_stockage)
            #np.savetxt('matrice.txt', matrice_stockage, delimiter=' ', fmt='%d')
            #print("salut")

    plt.draw()
    plt.pause(3)
    print("Fin du graphique")

#.............................................................................
#fonction pour afficher les données de la liste
def affichage_mapping(data):

    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to equal for correct scaling

    #on affiche les données stockées dans la matrice matrice_stockage
    #ax.plot(x, y, 'bo', markersize=1)  # Plot each point
    for ligne in range(nb_ligne_matrice):
        for colonne in range(nb_colonne_matrice):
            #condition
            if (matrice_stockage[ligne][colonne] == 1):
                print("Obstacle détécté dans la matrice",time.time()-tmp)
                ax.plot(ligne, colonne, 'bo', markersize=1)    

    plt.gca(); ax.text(5000, 5000, '▲',color = 'red') #♣

    plt.draw()
    plt.pause(50)
    print("Fin du graphique")

#............................................................................. 
def recup_matrice_lidar():
    #recuperation des données lidar
    #on appelle le lidar
    #.............................................................................
    # Setup the RPLidar
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(None, PORT_NAME, timeout=3)   
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            ang = int(angle) % 360
            scan_data[ang] = distance
        print(scan_data)
        #return scan_data
        lidar.stop()
        lidar.disconnect()
        break

#............................................................................. 
try:
    #on récupère les données des codeurs + on active le balayage lidar si distance activé

    tmp= time.time()
    #on recupere la matrice du lidar
    recup_matrice_lidar()
    print("je suis sortis du scan")
    #scan_data=[940.5, 933.0, 932.25, 925.0, 924.25, 918.75, 917.75, 913.75, 909.75, 909.75, 908.25, 905.0, 902.75, 902.5, 901.25, 900.5, 900.5, 901.0, 900.0, 899.75, 900.75, 902.75, 906.0, 906.5, 907.25, 910.75, 912.5, 913.25, 919.5, 924.0, 924.0, 928.0, 932.5, 937.5, 942.0, 949.0, 949.25, 957.5, 966.5, 977.0, 977.75, 986.25, 997.0, 1001.5, 1009.75, 1024.5, 1037.75, 1042.5, 1052.0, 1067.25, 1073.25, 1087.25, 1101.25, 1125.75, 1130.5, 1146.75, 1168.25, 1179.75, 1188.5, 1217.5, 1245.75, 1256.0, 1276.25, 1307.25, 1318.75, 1340.0, 1378.25, 1423.5, 1434.75, 1463.25, 1514.0, 1563.75, 1583.75, 1625.5, 1686.25, 1706.25, 1783.5, 1823.75, 1903.25, 1946.25, 1999.25, 2101.0, 2223.25, 2277.25, 2340.5, 2435.5, 2444.75, 2434.75, 2411.25, 2387.0, 2387.0, 2420.5, 2632.75, 3603.25, 3604.0, 3614.75, 3565.0, 2480.5, 2464.0, 2407.5, 2387.0, 2364.25, 2349.0, 2341.75, 2346.75, 2369.5, 2415.25, 2420.0, 3211.0, 3213.25, 3219.0, 3220.5, 3184.5, 3632.0, 3672.25, 3695.25, 3292.25, 3376.5, 3353.5, 3418.25, 2444.75, 2521.5, 2452.25, 2524.5, 2556.5, 2404.25, 2726.0, 2888.0, 2693.0, 2650.75, 2618.5, 2611.75, 2605.75, 2630.25, 2642.0, 2683.75, 2716.0, 2767.5, 1740.5, 1736.5, 1567.75, 1521.0, 1432.75, 1582.75, 1666.5, 1692.5, 1708.75, 1704.0, 1706.0, 1703.25, 1702.75, 1671.5, 5077.75, 5124.5, 5137.0, 5114.5, 1655.5, 5122.0, 8149.75, 9108.0, 9147.75, 9054.0, 9016.5, 9096.75, 8799.0, 7598.25, 7391.75, 7463.75, 7278.5, 5339.75, 5218.0, 8001.5, 6610.25, 6604.0, 6482.25, 6416.75, 6416.0, 6430.75, 6616.5, 7681.0, 6388.0, 6554.75, 6687.75, 5869.0, 4741.25, 6407.5, 6482.25, 6400.5, 6391.75, 6494.25, 6352.25, 6355.25, 6438.75, 6975.25, 6442.5, 6378.25, 7253.25, 7283.5, 7040.25, 685.75, 6244.25, 7026.25, 6364.75, 6326.75, 6233.25, 6518.25, 169.5, 6324.0, 6462.25, 6303.25, 6407.5, 5460.0, 6700.5, 5419.25, 5411.5, 5362.0, 5364.25, 5296.75, 6604.0, 6584.25, 6620.5, 6520.25, 6546.5, 6620.5, 6704.75, 5192.5, 8093.5, 6830.75, 6857.25, 7313.75, 7026.25, 7068.75, 6649.75, 6804.25, 7155.0, 5195.0, 6739.0, 134.25, 6704.75, 5200.0, 6679.25, 6662.25, 5249.25, 5510.0, 5283.5, 137.0, 5571.25, 136.25, 5361.5, 136.5, 136.5, 136.75, 234.25, 136.5, 145.0, 136.5, 136.5, 145.5, 136.25, 145.5, 138.25, 494.0, 140.75, 137.75, 141.0, 476.25, 138.0, 499.5, 137.75, 138.25, 138.25, 138.0, 138.5, 138.5, 142.0, 138.5, 139.25, 141.0, 141.0, 5386.0, 5703.75, 5164.5, 5137.0, 5286.25, 8272.75, 8570.0, 8951.75, 8672.25, 5513.0, 5307.5, 5521.5, 5703.75, 5530.25, 6185.75, 6142.5, 5427.75, 5063.25, 4888.0, 4327.0, 3923.5, 3734.25, 3566.25, 3453.25, 3286.25, 2998.75, 2897.25, 2738.5, 2555.25, 1748.5, 1698.0, 1593.0, 1551.0, 1510.25, 1461.5, 1467.5, 1477.0, 1491.75, 1505.25, 1515.0, 1535.25, 1557.0, 1557.0, 1550.25, 1496.5, 1460.25, 1433.75, 1399.75, 1571.75, 1516.25, 1464.75, 1326.5, 1305.25, 1304.75, 1264.75, 1254.75, 1241.5, 1206.75, 1182.0, 1169.5, 1138.25, 1118.0, 1107.0, 1092.0, 1080.25, 1070.0, 1059.5, 1044.75, 1038.75, 1030.5, 1015.5, 1008.5, 1007.5, 992.0, 989.25, 976.5, 962.5, 962.0, 954.5, 949.0, 944.5]
    process_data(scan_data,dist_encodeur1,dist_encodeur2)

    #on translate les données avec les encodeurs 
    # conversion incrément -> m
    # dist_encodeur1 = int(infos_encodeur1 * 1.14*(10)**(-5))
    # dist_encodeur2 = int(infos_encodeur2 * 1.14*(10)**(-5))
    temps=time.tzset()

    recup_matrice_lidar()
    #dist_encodeur1 = -3000
    dist_encodeur1 = -3000
    dist_encodeur2 = 0
    process_data(scan_data,dist_encodeur1,dist_encodeur2)

    #on affiche le mapping obtenu
    affichage_mapping(scan_data)

   
except KeyboardInterrupt:
    print('Stopping.')

#on stoppe le LIDAR
lidar.stop()
lidar.disconnect()
