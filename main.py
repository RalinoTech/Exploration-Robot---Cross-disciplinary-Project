from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/input', methods=['GET'])
def handle_input():
    inp = request.args.get('inp')
    print("Touche enfoncée :", inp)
    return 'confirmation'  

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
