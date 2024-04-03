#!/usr/bin/env python3

import socket

class Server:
    def __init__(self, ip, port):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))

        self.keymap = "zqsde"

    def connect(self):

        self.server.listen()
        self.conn, self.robot_addr = self.server.accept()


    def send_input(self, key):

        if key not in self.keymap:
            print("[x] Unrecognized key!")
            return
            
        self.conn.send(key.encode("utf-8"))

    def close_conn(self):
        self.conn.close()

if __name__ == "__main__":
    print("[x] This code is a module!")
    exit(-1)