import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète'  # Remplacez par une clé sécurisée
socketio = SocketIO(app, cors_allowed_origins="*")

# Liste des utilisateurs connectés
connected_users = {}

@app.route('/')
def home():
    return render_template('home.html')

@socketio.on('connect')
def handle_connect():
    user_id = request.sid  # Récupère l'ID de connexion du client
    connected_users[user_id] = f'Utilisateur {user_id[:5]}'  # Stocke un nom générique (ID)
    print(f"Un nouvel utilisateur est connecté ! ID : {user_id}")
    # Envoie la liste des utilisateurs connectés à tous
    emit('user_connected', list(connected_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    if user_id in connected_users:
        del connected_users[user_id]
    print(f"Un utilisateur s'est déconnecté ! ID : {user_id}")
    # Envoie la liste mise à jour des utilisateurs connectés
    emit('user_connected', list(connected_users.values()), broadcast=True)

@socketio.on('message')
def handle_message(msg):
    print(f"Message reçu : {msg}")
    # Diffuse le message à tous les clients
    send(f"Reçu : {msg}", broadcast=True)

@socketio.on('private_message')
def handle_private_message(data):
    recipient_sid = data['recipient_sid']  # ID du destinataire
    message = data['message']
    print(f"Envoi d'un message privé à {recipient_sid}: {message}")
    # Envoie un message à un seul client (privé)
    socketio.send(message, room=recipient_sid)

if __name__ == '__main__':
    # Utilise la variable d'environnement PORT ou 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
