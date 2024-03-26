#!/home/taylordedordogne/Desktop/Work/ProjetTransversal/inputs/bin/python

import socket
import keyboard
import sys

def main():

    if len(sys.argv) != 3:
        print("Usage: ./input_server.py <SERVER_IP> <SERVER_PORT>")
        exit(-1)

    ip, port = sys.argv[1:]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip.strip(), int(port)))
    server.listen()
    conn, robot_addr = server.accept()
    print(f"[+] Robot connected with ip: {robot_addr[0]}")

    key = None

    while key != "esc":
        key = keyboard.read_key()
        if key == "up":
            order = 0
        elif key == "down":
            order = 1
        elif key == "right":
            order = 2
        elif key == "left":
            order = 3
        elif key == "esc":
            order = 4
        else:
            continue
        
        conn.send(order.to_bytes(4, 'little'))
    
    conn.close()

if __name__ == "__main__":
    main()
