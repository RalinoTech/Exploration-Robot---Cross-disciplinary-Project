from flask import Flask, render_template, request
from serverlib import Server
import sys

app = Flask(__name__)

@app.route('/input', methods=['GET'])
def handle_input():
    inp = request.args.get('inp')
    server.send_input(inp)
    return 'confirmation'  

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: ./main.py <SERVER_IP> <SERVER_PORT>")
        exit(-1)
    
    server = Server(sys.argv[1], int(sys.argv[2]))
    server.connect()

    app.run(debug=False, port=5000, use_reloader=False)