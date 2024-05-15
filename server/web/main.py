from flask import Flask, render_template, request
from serverlib import Server
import sys
import time

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
    
    #server = Server(sys.argv[1], int(sys.argv[2]))
    #server.connect()
    """time.sleep(5)
    while(1):
        print(server.rnp())
        time.sleep(1)"""
    app.run(debug=False, port=5000, use_reloader=False)

