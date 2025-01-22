6. Utilisation de l'API
Démarrer l'API :

Exécutez la commande suivante pour démarrer l'API :

bash
Copy
python app.py
L'API sera accessible à l'adresse http://127.0.0.1:5000.

Endpoints Disponibles :

Commandes :

GET /api/commandes : Obtenir toutes les commandes.

GET /api/commandes/<id> : Obtenir une commande par son ID.

POST /api/commandes : Créer une nouvelle commande.

Clients :

GET /api/clients : Obtenir tous les clients.

GET /api/clients/<email> : Obtenir un client par son email.

POST /api/clients : Créer un nouveau client.

Stocks :

GET /api/stocks : Obtenir tous les stocks.

POST /api/stocks : Ajouter un nouvel ingrédient en stock.

Exemple de Requête :

Créer une nouvelle commande :

bash
Copy
curl -X POST -H "Content-Type: application/json" -d '{
  "client_nom": "John Doe",
  "client_email": "john@example.com",
  "plats": "Pizza x2, Burger x1",
  "total": 25.50
}' http://127.0.0.1:5000/api/commandes
Prochaines Étapes
Ajouter une authentification (API keys ou OAuth) pour sécuriser l'API.

Intégrer des webhooks pour notifier les systèmes externes des mises à jour (par exemple, une nouvelle commande).

Documenter l'API avec Swagger ou OpenAPI.

Ce code est un point de départ solide pour une API ouverte. Vous pouvez l'étendre en fonction de vos besoins spécifiques.

