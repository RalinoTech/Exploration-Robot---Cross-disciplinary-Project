#!/usr/bin/python3

import socket
import serial
import argparse

def main(ip, port, device):

    if len(sys.argv) != 3:
        print("Usage: ./input_server.py <SERVER_IP> <SERVER_PORT>")
        exit(-1)

    ip, port = sys.argv[1:]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip.strip(), int(port)))

    ser = serial.Serial(port=device, baudrate=19200)

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
            print(f"order: {str(order)}")
            ser.write(str(order).encode("utf-8"))
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--server-ip", required=True, help="Control station's IP")
    parser.add_argument("-p", "--server-port", required=True, help="Port control station is listening on")
    parser.add_argument("-d", "--serial-device", default="/dev/serial0", help="Target UART device")

    args = parser.parse_args()
    print(*vars(args).values())
