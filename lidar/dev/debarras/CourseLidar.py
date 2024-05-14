from math import floor
from adafruit_rplidar import RPLidar

class CourseLidar:
    def __init__(self, port_name='/dev/ttyUSB0', timeout=3):
        self.lidar = RPLidar(None, port_name, timeout=timeout)
        self.max_distance = 4000
        self.scan_data = [-1] * 360

    def récup_une_valeur(self):
        compteur=0
        try:
            for scan in self.lidar.iter_scans():
                compteur=compteur+1
                for (_, angle, distance) in scan:
                    ang = min([359, floor(angle)])
                    self.scan_data[ang] = distance
                if compteur==5:
                    return(self.scan_data)
                

        except KeyboardInterrupt:
            print('Stopping.')

        self.stop_measurement()  # Arrêter le moteur du lidar

if __name__ == "__main__":
    course = CourseLidar()
    course.run_course()