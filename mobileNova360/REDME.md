lib/
│
├── core/                   # Partie contenant les composants et configurations réutilisables
│   ├── constants/          # Ficnctions utilitaires (ex: formatage des dates, validation des inputs, etc.)
│   └── widgets/            # Widghiers constants (ex: couleurs, styles, API URLs, etc.)
│   ├── utils/              # Foets réutilisables et génériques (ex: boutons, cartes, loaders)
│
├── data/                   # Gestion des données
│   ├── models/             # Classes de modèles de données (ex: User, Product)
│   ├── repositories/       # Abstractions des sources de données (APIs, local storage)
│   └── providers/          # Gestion des états (Flutter Provider, Riverpod, Bloc)
│
├── features/               # Fonctionnalités principales de l'application
│   ├── auth/               # Authentification (pages de login, registration)
│   ├── home/               # Fonctionnalité principale (dashboard ou accueil)
│   └── profile/            # Exemple d'une autre fonctionnalité (profil utilisateur)
│
├── services/               # Services connectés (APIs, services tiers, etc.)
│   └── api_service.dart    # Classe gérant les appels aux APIs
│
├── routes/                 # Gestion des routes et navigation
│   └── app_routes.dart     # Configuration de toutes les routes de l'application
│
└── main.dart               # Point d'entrée de l'application
