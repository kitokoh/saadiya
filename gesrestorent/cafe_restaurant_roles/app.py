from flask import Flask, jsonify, request, abort
from models import Utilisateur, JournalActivite

app = Flask(__name__)

# Middleware pour vérifier les permissions
def verifier_permission(permission):
    def decorator(f):
        def wrapper(*args, **kwargs):
            email = request.headers.get('X-User-Email')
            if not email or not Utilisateur.verifier_permission(email, permission):
                abort(403, description="Permission refusée")
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Endpoint pour obtenir le journal d'activité
@app.route('/api/journal', methods=['GET'])
@verifier_permission('gestion_utilisateurs')
def get_journal():
    activites = JournalActivite.get_all()
    return jsonify([dict(activite) for activite in activites])

# Endpoint pour prendre une commande (serveur)
@app.route('/api/commandes', methods=['POST'])
@verifier_permission('prendre_commandes')
def prendre_commande():
    data = request.get_json()
    email = request.headers.get('X-User-Email')
    utilisateur = Utilisateur.get_by_email(email)
    JournalActivite.enregistrer_action(utilisateur['id'], "Prise de commande")
    return jsonify({"status": "Commande prise avec succès"}), 201

# Endpoint pour livrer une commande (livreur)
@app.route('/api/livraisons', methods=['POST'])
@verifier_permission('livrer_commandes')
def livrer_commande():
    data = request.get_json()
    email = request.headers.get('X-User-Email')
    utilisateur = Utilisateur.get_by_email(email)
    JournalActivite.enregistrer_action(utilisateur['id'], "Livraison de commande")
    return jsonify({"status": "Commande livrée avec succès"}), 201

# Gestion des erreurs 403
@app.errorhandler(403)
def permission_refusee(error):
    return jsonify({"error": str(error)}), 403

if __name__ == '__main__':
    app.run(debug=True)