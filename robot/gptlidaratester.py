from math import floor
from adafruit_rplidar import RPLidar

class GPTLidar:
    def __init__(self, port_name='/dev/ttyUSB0', timeout=3):
        self.lidar = RPLidar(None, port_name, timeout=timeout)
        self.max_distance = 4000
        self.scan_data = [-1] * 360
        self.last_scan_data = None

    def update_scan_data(self):
        for scan in self.lidar.iter_scans():
            for (_, angle, distance) in scan:
                ang = min([359, floor(angle)])
                self.scan_data[ang] = distance
            self.last_scan_data = self.scan_data[:]  # Copy the data to last_scan_data
            yield

    def get_last_scan_data(self):
        return self.last_scan_data

# Example usage:
lidar = GPTLidar()
lidar.update_scan_data()  # Start scanning
# Do something else here, or sleep for a while
last_scan_data = lidar.get_last_scan_data()  # Get the last scan data
print(last_scan_data)  # Or do something with the data
