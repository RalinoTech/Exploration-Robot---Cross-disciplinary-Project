from flask import Flask, render_template, request, jsonify, send_file
from serverlib import Server
import threading
import sys
import time
import os
from math import cos, sin, radians
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)
lidar_data = None

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
#lidar = RPLidar(None, PORT_NAME, timeout=3)

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# used to scale data to fit on the screen
max_distance = 5000

def affichage_lidar():
    ax.text(0, 0, '▲', color='red')  # Plot robot orientation

def actualisation():
    plt.draw()
    plt.pause(0.001)

def process_data(data):
    ax.clear()  # Clear the previous plot
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)
    ax.set_aspect('equal', adjustable='box')  # Set aspect ratio to equal for correct scaling

    for angle, distance in enumerate(data):
        if distance != -1:
            # Convert polar coordinates to Cartesian coordinates
            y = distance * cos(radians(angle))
            x = distance * sin(radians(angle))
            ax.plot(x, y, 'bo', markersize=1)  # Plot each point

    affichage_lidar()

def lidar_rnp(server):
    global lidar_data
    while True:
        recv = server.rnp()
        if recv is not None:
            lidar_data = recv
            print(f"Received LIDAR data: {lidar_data}")  # Log received data for debugging

@app.route('/api/input', methods=['GET'])
def handle_input():
    inp = request.args.get('inp')
    server.send_input(inp)
    return jsonify({"status": "OK"}), 200

@app.route("/api/lidar", methods=["GET"])
def recv_lidar_data():
    global lidar_data
    return jsonify({"status": "OK", "data": lidar_data}), 200

@app.route('/plot.png')
def plot_png():
    global lidar_data
    if lidar_data is not None:
        process_data(lidar_data)
        print("Plotting LIDAR data")  # Log when plotting data
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        print("No LIDAR data available")  # Log when no data is available
        return jsonify({"status": "NO_DATA"}), 404

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

    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
