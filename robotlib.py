#!/usr/bin/env python3

import socket

class Server:
    def __init__(self, ip, port):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))

    def connect(self):

        self.server.listen()
        self.conn, self.robot_addr = self.server.accept()


    def send_input(self, key):

        if key == "z":
            order = 0
        elif key == "s":
            order = 1
        elif key == "d":
            order = 2
        elif key == "q":
            order = 3
        elif key == "esc":
            order = 4
        else:
            print("[x] Unrecognized key!")
            return
            
        self.conn.send(order.to_bytes(4, 'little'))

    def close_conn(self):
        self.conn.close()

if __name__ == "__main__":
    print("[x] This code is a module!")
    exit(-1)