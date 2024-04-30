from math import floor
from adafruit_rplidar import RPLidar
import time
import threading
import queue

class CourseLidar:
    def __init__(self, port_name='/dev/ttyUSB0', timeout=3):
        self.lidar = RPLidar(None, port_name, timeout=timeout)
        self.max_distance = 4000
        self.scan_data = [-1] * 360
        self.last_scan_data = None
        self.scan_thread = None
        self.scan_queue = queue.Queue()

    def update_scan_data(self):
        print("Scanning started.")
        try: 
            for scan in self.lidar.iter_scans():
                for (_, angle, distance) in scan:
                    ang = min([359, floor(angle)])
                    self.scan_data[ang] = distance
                self.last_scan_data = self.scan_data[:]  # Copy the data to last_scan_data
                
        except KeyboardInterrupt:
            print('Stopping.')
        

    def start_scanning(self):
        self.scan_thread = threading.Thread(target=self.update_scan_data)
        self.scan_thread.start()

    def stop_scanning(self):
        if self.scan_thread:
            self.scan_thread.join()
        self.lidar.stop()
        self.lidar.disconnect()
    def get_last_scan_data(self):
        return self.last_scan_data
    
if __name__ == "__main__":
    lidar = CourseLidar()  # Create an instance of CourseLidar
    lidar.start_scanning()

    # Do something else here, or sleep for a while
    time.sleep(5)  # Allow sufficient time for scanning
    print("Retrieving last scan data after 5 seconds:")
    print(lidar.get_last_scan_data())

    # Wait for another 5 seconds
    time.sleep(5)
    print("Retrieving last scan data after another 5 seconds:")
    print(lidar.get_last_scan_data())
    lidar.stop_scanning()