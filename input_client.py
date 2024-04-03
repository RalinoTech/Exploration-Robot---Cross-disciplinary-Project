#!/usr/bin/python3

import socket
import serial
import argparse

def main(ip, port, device):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip.strip(), int(port)))

    ser = serial.Serial(port=device, baudrate=19200)

    order = None

    """
        z: forward
        s: backward
        d: right
        q: left
        e: exit
    """

    while True:
        data = client.recv(1)
        if data != b"":
            order = data.decode("utf-8"))
            if order == 'e': exit()
            print(f"order: {str(order)}")
            ser.write(str(order).encode("utf-8"))
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--server-ip", required=True, help="Control station's IP")
    parser.add_argument("-p", "--server-port", required=True, help="Port control station is listening on")
    parser.add_argument("-d", "--serial-device", default="/dev/serial0", help="Target UART device")

    args = parser.parse_args()
    main(*vars(args).values())
