from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

ADMINS = ['Admin1', 'Admin2']

@app.route('/')
def home():
    return render_template('home.html')

@socketio.on('connect')
def handle_connect():
    emit('message', {'sender': 'System', 'message': 'Un utilisateur a rejoint le chat.'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    emit('message', {'sender': 'System', 'message': 'Un utilisateur a quitté le chat.'}, broadcast=True)

@socketio.on('chatMessage')
def handle_chat_message(data):
    emit('message', data, broadcast=True)

@socketio.on('deleteMessage')
def handle_delete_message(data):
    if data['username'] in ADMINS:
        emit('deleteMessage', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
