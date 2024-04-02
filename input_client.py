#!/usr/bin/python3

import socket
import serial
import sys

def main():

    if len(sys.argv) != 3:
        print("Usage: ./input_server.py <SERVER_IP> <SERVER_PORT>")
        exit(-1)

    ip, port = sys.argv[1:]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip.strip(), int(port)))

    ser = serial.Serial(port="/dev/serial0", baudrate=19200)

    order = None

    """
        0: forward
        1: backward
        2: right
        3: left
        4: exit
    """

    while True:
        data = client.recv(4)
        if data != b"":
            order = int.from_bytes(data, 'little')
            if order == 4: exit()
            ser.write(str(order).encode("utf-8"))
    client.close()


if __name__ == "__main__":
    main()
