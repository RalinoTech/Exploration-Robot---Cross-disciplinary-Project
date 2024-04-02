from flask import Flask, render_template, request
from robotlib import Server

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
    server = Server("192.168.166.148", 7070)
    server.connect()
    app.run(debug=True)