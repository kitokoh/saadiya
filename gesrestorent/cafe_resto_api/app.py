from flask import Flask, jsonify, request, abort
from models import Commande, Client, Stock

app = Flask(__name__)

# Endpoint pour obtenir toutes les commandes
@app.route('/api/commandes', methods=['GET'])
def get_commandes():
    commandes = Commande.get_all()
    return jsonify([dict(commande) for commande in commandes])

# Endpoint pour obtenir une commande par son ID
@app.route('/api/commandes/<int:commande_id>', methods=['GET'])
def get_commande(commande_id):
    commande = Commande.get_by_id(commande_id)
    if commande is None:
        abort(404, description="Commande non trouvée")
    return jsonify(dict(commande))

# Endpoint pour créer une nouvelle commande
@app.route('/api/commandes', methods=['POST'])
def create_commande():
    data = request.get_json()
    if not data or not all(key in data for key in ['client_nom', 'client_email', 'plats', 'total']):
        abort(400, description="Données invalides")
    commande_id = Commande.create(data['client_nom'], data['client_email'], data['plats'], data['total'])
    return jsonify({"id": commande_id}), 201

# Endpoint pour obtenir tous les clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.get_all()
    return jsonify([dict(client) for client in clients])

# Endpoint pour obtenir un client par son email
@app.route('/api/clients/<string:email>', methods=['GET'])
def get_client(email):
    client = Client.get_by_email(email)
    if client is None:
        abort(404, description="Client non trouvé")
    return jsonify(dict(client))

# Endpoint pour créer un nouveau client
@app.route('/api/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    if not data or not all(key in data for key in ['nom', 'email']):
        abort(400, description="Données invalides")
    client_id = Client.create(data['nom'], data['email'])
    return jsonify({"id": client_id}), 201

# Endpoint pour obtenir tous les stocks
@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.get_all()
    return jsonify([dict(stock) for stock in stocks])

# Endpoint pour créer un nouvel ingrédient en stock
@app.route('/api/stocks', methods=['POST'])
def create_stock():
    data = request.get_json()
    if not data or not all(key in data for key in ['ingredient', 'quantite']):
        abort(400, description="Données invalides")
    stock_id = Stock.create(data['ingredient'], data['quantite'])
    return jsonify({"id": stock_id}), 201

# Gestion des erreurs 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}), 404

# Gestion des erreurs 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

if __name__ == '__main__':
    app.run(debug=True)