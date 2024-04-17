#!/usr/bin/python3

import socket
import serial
import argparse
from clientlib import Client
from CourseLidarlib import CourseLidar

def main(ip, port, device):

    client = Client(device)
    client.connect(ip.strip(), int(port))
    course = CourseLidar()

    order = None

    """
        z: forward
        s: backward
        d: right
        q: left
        e: exit
    """

    while True:
        data = client.rnp()
        valeur= course.recup_une_valeur()
        client.send_to_computer(valeur)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--server-ip", required=True, help="Control station's IP")
    parser.add_argument("-p", "--server-port", required=True, help="Port control station is listening on")
    parser.add_argument("-d", "--serial-device", default="/dev/serial0", help="Target UART device")

    args = parser.parse_args()
    main(*vars(args).values())
