# Architecture Globale - Leopardo AI

## Introduction
Leopardo AI est une application de bureau avancée conçue pour l'automatisation, la sécurité et l'optimisation de la gestion des réseaux sociaux. Elle offre une suite complète d'outils pour gérer la présence en ligne, l'engagement client et la croissance commerciale.

## Pile Technologique
- **Langage** : Python 3.x
- **Interface Graphique (GUI)** : PyQt5
- **Moteur Web** : QtWebEngine (pour l'affichage de contenus web distants)
- **Bases de Données** :
  - SQLite (Local) pour les données d'application, les contacts, et la gestion des sessions.
  - Firebase (Cloud) pour la configuration à distance et certaines fonctionnalités temps réel.
- **Sécurité** : Chiffrement des données sensibles, authentification basée sur les rôles.

## Modèles de Conception (Design Patterns)

### 1. MVC (Modèle-Vue-Contrôleur)
L'application est structurée de manière modulaire en suivant le patron MVC pour chaque fonctionnalité (`feature`) :
- **Modèle (Model)** : Gère les données et la logique métier spécifique.
- **Vue (View/Widget)** : Composants d'interface PyQt5.
- **Contrôleur (Controller)** : Fait le lien entre la vue et le modèle, gère les signaux et les événements.

Chaque module dans `leopardo_v2/app/features/` suit cette structure, permettant une isolation claire des responsabilités.

### 2. Service Container (Injection de Dépendances)
L'application utilise un conteneur de services (`ServiceContainer`) pour centraliser l'accès aux composants transversaux :
- Authentification (`AuthService`)
- Configuration (`ConfigService`)
- Notifications (`NotificationService`)
- Gestion des langues (`LanguageManager`)
- Mise à jour (`UpdaterService`)

Cela facilite le test des composants et évite le couplage fort entre les modules.

## Flux de l'Application
1. **Démarrage** : `main.py` initialise l'application et affiche le `SplashScreen`.
2. **Initialisation** : `MainWindow` instancie les services de base et charge la configuration.
3. **Authentification** : Vérification de la session ou affichage du `LoginDialog`.
4. **Chargement des Modules** : `init_features` dans `app_setup.py` instancie tous les modèles, vues et contrôleurs, puis les ajoute au `QStackedWidget` central.
5. **Boucle d'Événements** : Interaction de l'utilisateur via le `SideMenu` pour naviguer entre les différentes fonctionnalités.
