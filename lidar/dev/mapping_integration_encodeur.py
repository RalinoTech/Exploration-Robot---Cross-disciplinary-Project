#Code pour afficher un mapping AVEC l'intégration des encodeurs

#bibliothèques
from math import cos, sin, radians,floor
import matplotlib.pyplot as plt
import numpy as np
from adafruit_rplidar import RPLidar
import time

#.............................................................................
#initialisation du lidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
#matrice du lidar
scan_data = [-1] * 360  # Initialize data for each new scan

#.............................................................................
#recuperation des données des encodeurs
#informations brut des encodeurs
infos_encodeur1 = 0
infos_encodeur2 = 0
#convertions des informations précédentes en mm
dist_encodeur1 = 0
dist_encodeur2 = 0
#moyenne des 2 encodeurs pour mapping trajectoire rectiligne
dist_encodeur_moyenne= (dist_encodeur1+dist_encodeur2)/2

#.............................................................................
#Integration pour le mapping
nb_ligne_matrice=11000
nb_colonne_matrice=11000
matrice_stockage=np.zeros((nb_ligne_matrice,nb_colonne_matrice))

#.............................................................................
# Create a figure and axis for the plot
fig, ax = plt.subplots()

# taille maxi de la zone max_distance*max_distance
max_distance = 11000

#.............................................................................
#gestion des données du lidar
def process_data(data,dist_encodeur_moyenne):

    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')

    #on recupere la matrice du lidar
    for angle, distance in enumerate(data):
        if distance != -1:
            # coordonnées polaires --> coordonnées cartésiennes
            y = distance * cos(radians(angle)) + dist_encodeur_moyenne
            x = distance * sin(radians(angle))
            matrice_stockage[round(x) + 5000][round(y) + 5000] = 1
            
            plt.ylabel('<- arrière du robot            &            avant du robot ->')
            plt.xlabel('Plan détection LIDAR')
            ax.plot(x, y, 'bo', markersize=1)  # Plot each point
            #................................................................
     
    plt.draw()
    plt.pause(3)
    print("Fin du graphique")

#.............................................................................
#fonction pour afficher les données de la liste
def affichage_mapping():

    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')

    #on affiche les données stockées dans la matrice matrice_stockage
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
    #.............................................................................
    # Setup the RPLidar
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(None, PORT_NAME, timeout=3)   
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            ang = int(angle) % 360
            scan_data[ang] = distance
        print(scan_data)
        lidar.stop()
        lidar.disconnect()
        break

#............................................................................. 
try:
    #on récupère les données des codeurs + on active le balayage lidar si distance activé

    tmp= time.time()
    #on recupere la matrice du lidar
    #premier balayage du LIDAR
    recup_matrice_lidar()

    #infos_encodeur1 & infos_encodeur2
    #correspondent aux informations brutes que nous renvoi la STM32
    #conversion des données des encodeurs
    #on translate les données avec les encodeurs 
    # conversion incrément -> m
    # dist_encodeur1 = int(infos_encodeur1 * 1.14*(10)**(-5))
    # dist_encodeur2 = int(infos_encodeur2 * 1.14*(10)**(-5))
   
    #sauvegarde des points dans la matrice du mapping
    process_data(scan_data,dist_encodeur_moyenne)

    temps=time.tzset()

    #deuxième balayage
    recup_matrice_lidar()

    #on introduit un décalage pour simuler les données des encodeurs pour le mapping
    dist_encodeur1 = -3000
    dist_encodeur2 = 0
    dist_encodeur_moyenne= (dist_encodeur1+dist_encodeur2)/2

    #sauvegarde des points dans la matrice du mapping
    process_data(scan_data,dist_encodeur_moyenne)

    #on affiche le mapping final obtenu
    affichage_mapping()

   
except KeyboardInterrupt:
    print('Stopping.')

#on stoppe le LIDAR
lidar.stop()
lidar.disconnect()
