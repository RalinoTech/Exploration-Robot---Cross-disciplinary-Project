#!/usr/bin/python3

import socket
import serial
import argparse
from clientlib import Client

def main(ip, port, device):

    client = Client(device)
    client.connect((ip.strip(), int(port)))

    order = None

    """
        z: forward
        s: backward
        d: right
        q: left
        e: exit
    """

    while True:
        data = client.read()
        if data != b"":
            order = data.decode("utf-8")

            if order == 'e': exit()
            print(f"order: {order}")
            ser.write(order.encode("utf-8"))
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--server-ip", required=True, help="Control station's IP")
    parser.add_argument("-p", "--server-port", required=True, help="Port control station is listening on")
    parser.add_argument("-d", "--serial-device", default="/dev/serial0", help="Target UART device")

    args = parser.parse_args()
    main(*vars(args).values())
