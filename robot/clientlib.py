#!/usr/bin/env python3
import struct
import socket
import serial

"""
    Magic headers:
        'INPT' : Key inputs
            - Key char (1 byte)
        'DATA' : Lidar data
            - Data size (4 bytes)
            - Data (size)
        ...
"""

class Client:
    def __init__(self, device_string):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.device = serial.Serial(port=device_string, baudrate=19200)

    def connect(self, ip, port):

        self.client.connect((ip, port))

    def send_to_ST(self, data):
        self.device.write(data)

    def rnp(self):

        hdr = self.client.recv(4).decode("utf-8")

        if hdr == "INPT":
            key = self.client.recv(1).decode("utf-8")
            if key == "e":
                self.client.close()
                exit()
            else:
                print(f"order: {key}")
                self.send_to_ST(key.encode("utf-8"))

    def send_to_computer(self, data):

        self.client.send(b"DATA")

        data_bytes = data.encode('utf-8')
        length_bytes = len(data_bytes)
        length_bytes_struct = struct.pack('I', length_bytes)
        self.client.send(length_bytes_struct)
        for i in range (len(data)):
            self.client.send(data[i].encode("utf-8"))
            




if __name__ == "__main__":
    print("[x] This code is a module!")
    exit(-1)