from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(PORT_NAME)
try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            print(f'Angle: {angle}, Distance: {distance}')
except KeyboardInterrupt:
    print('Stopped by user')
    lidar.stop()
    lidar.disconnect()
