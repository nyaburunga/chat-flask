# Mon Application Flask-SocketIO

Cette application est un exemple de messagerie instantanée utilisant Flask et SocketIO.

## Déploiement
- La commande utilisée : `gunicorn -k eventlet -w 1 -b 0.0.0.0:$PORT app:app`
