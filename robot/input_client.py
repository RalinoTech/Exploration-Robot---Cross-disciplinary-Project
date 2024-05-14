#!/usr/bin/python3

import socket
import serial
import time
import argparse
from clientlib import Client
from CourseLidarlib import CourseLidar
import threading

def recup_data(client):
    while True: 
        data = client.rnp()
        # Do something with the received data

def main(ip, port, device):
    client = Client(device)
    client.connect(ip.strip(), int(port))
    
    # Test sending a matrix
    course = CourseLidar()
    course.start_scanning()

    # Sending the JSON string to the server
    order = None

    """
        z: forward
        s: backward
        d: right
        q: left
        e: exit
    """
    time.sleep(5)

    # Start the thread for receiving data
    threadlid = threading.Thread(target=recup_data, args=(client,))
    threadlid.start()

    # Main loop for sending Lidar data
    while True:
        mat = course.get_last_scan_data()
        client.send_to_computer(mat)
        print(mat)
        time.sleep(2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--server-ip", required=True, help="Control station's IP")
    parser.add_argument("-p", "--server-port", required=True, help="Port control station is listening on")
    parser.add_argument("-d", "--serial-device", default="/dev/serial0", help="Target UART device")

    args = parser.parse_args()
    main(*vars(args).values())