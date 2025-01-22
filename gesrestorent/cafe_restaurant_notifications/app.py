from flask import Flask, jsonify, request
from models import Notification, Stock
import threading
import time

app = Flask(__name__)

# Endpoint pour envoyer une notification
@app.route('/api/notifications', methods=['POST'])
def envoyer_notification():
    data = request.get_json()
    if not data or not all(key in data for key in ['destinataire', 'message', 'type_notification']):
        return jsonify({"error": "Données invalides"}), 400
    Notification.envoyer_notification(data['destinataire'], data['message'], data['type_notification'])
    return jsonify({"status": "Notification envoyée"}), 200

# Fonction pour vérifier les stocks en arrière-plan
def verifier_stocks_en_arriere_plan():
    while True:
        Stock.verifier_stocks()
        time.sleep(3600)  # Vérifie toutes les heures

if __name__ == '__main__':
    # Démarrer le thread pour vérifier les stocks
    thread = threading.Thread(target=verifier_stocks_en_arriere_plan)
    thread.daemon = True
    thread.start()

    # Démarrer l'application Flask
    app.run(debug=True)