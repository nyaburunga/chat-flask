from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return "Bienvenue sur mon application Flask-SocketIO !"

@socketio.on('message')
def handle_message(msg):
    print(f"Message reçu : {msg}")
    socketio.send(f"Reçu : {msg}")

if __name__ == '__main__':
    socketio.run(app)
