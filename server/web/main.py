from flask import Flask, render_template, request
from serverlib import Server
import threading
import sys
import time

app = Flask(__name__)
lidar_data = None

def lidar_rnp(server):
    global lidar_data
    while True:
        recv = server.rnp()
        if recv != None:
            lidar_data = recv


@app.route('/input', methods=['GET'])
def handle_input():
    inp = request.args.get('inp')
    server.send_input(inp)
    return 'confirmation'

@app.route("/lidar", methods=["GET"])
def recv_lidar_data():
    global lidar_data
    return jsonify(lidar_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: ./main.py <SERVER_IP> <SERVER_PORT>")
        exit(-1)
    
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.connect()
    threading.Thread(target=lidar_rnp, args=(server,)).start()

    app.run(debug=False, port=5000, use_reloader=False)

