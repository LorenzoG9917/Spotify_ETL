import random
import string
from flask import Flask, request, render_template
import webbrowser
#import pyautogui



app = Flask(__name__)

# Configuration of the Spotify application
client_id = 'd2e076e4f47b4c7d89cea47c258fb404'
redirect_uri = 'http://localhost:3000/callback'
scope = 'user-read-currently-playing,user-read-recently-played'

def generate_state(length=16):
    """Generate a random value for the state parameter"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

@app.route('/')
def authorize():
    # Generate a random value for the state parameter
    state = generate_state()

    # Render the authorize.html template with the necessary parameters
    return render_template('authorize.html', client_id=client_id, redirect_uri=redirect_uri, scope=scope, state=state)

@app.route('/callback')
def callback():
    return render_template('callback.html')

@app.route('/process_token', methods=['POST'])
def process_token():
    access_token = request.json.get('access_token')

    # Store the access_token in a file for later use
    with open('access_token.txt', 'w') as f:
        f.write(access_token)
    
    shutdown_server()
    return access_token


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    # Abre el navegador en la URL especificada
    webbrowser.open('http://localhost:3000')
     # Ejecuta la aplicación Flask
    app.run(port=3000)
  
    