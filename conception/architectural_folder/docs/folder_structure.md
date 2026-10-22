# Structure des Dossiers - Leopardo AI

Ce document présente l'organisation physique du dépôt et le rôle de chaque répertoire principal.

## 1. Cœur de l'Application (Version 2)
Le répertoire `leopardo_v2/` contient la version moderne et modulaire de la plateforme.
- **`app/`** : Code source principal.
  - **`api/`** : Interfaces de communication avec les services externes.
  - **`components/`** : Composants UI réutilisables (boutons, formulaires).
  - **`core/`** : Logique centrale (base de données, configuration, setup).
  - **`features/`** : Modules de fonctionnalités (Marketing, Sales, Finance, etc.). Chaque dossier est un module MVC indépendant.
  - **`services/`** : Services transversaux (Auth, Notifications, Updater).
  - **`ui/`** : Fenêtres principales (MainWindow, SideMenu, SplashScreen).
  - **`utils/`** : Fonctions utilitaires (Langues, Helpers).

## 2. Modules de Réseaux Sociaux et Bots
Plusieurs dossiers à la racine gèrent les interactions spécifiques aux plateformes :
- **`apisDelapp/`** : Endpoints API internes.
- **`facebookmodule/`**, **`instagram/`**, **`whasapping/`**, etc. : Scripts et modules spécifiques à chaque réseau.
- **`moteurdeBot/`** : Moteur d'exécution des automates et robots.
- **`sales_robots.db`** : Base de données spécifique aux automates de vente.

## 3. Gestion et Administration
- **`SUPERADMİN/`**, **`SuperAdmin2/`** : Outils pour l'administration globale du SaaS.
- **`licenceYonetimi/`** : Gestion des licences et des clés d'activation.
- **`VersionWebAPI/`** : Code lié à l'API web et aux mises à jour distantes.

## 4. Données et Configuration
- **`dataBase/`** : Stockage des bases SQLite globales.
- **`modelsDB/`** : Définitions des schémas de données.
- **`cles/`**, **`lesClesNova360/`** : Gestion de la sécurité et des clés cryptographiques.
- **`passwords/`** : (Attention) Semble contenir des données de session ou de configuration sécurisées.

## 5. Déploiement et Distribution
- **`depoloieDistribution/`** : Scripts pour packager l'application.
- **`Installs/`**, **`Installsweb/`** : Fichiers liés à l'installation client.
- **`ubuntu/`**, **`macos/`** : Scripts spécifiques au système d'exploitation.

## 6. Documentation et Conception
- **`conception/`** : Anciens cahiers des charges et le nouveau **`architectural_folder/`**.
- **`lelivre/`**, **`livre/`** : Documentation utilisateur ou guides de formation.

## 7. Autres Écosystèmes
- **`chromeExtention/`** : Extension de navigateur compagnon.
- **`mobile/`**, **`mobileNova360/`**, **`mobileSaas/`** : Code source pour les versions mobiles.
- **`trading/`** : Modules spécifiques pour les fonctionnalités de trading intégrées.

## Observations de l'IA sur l'Architecture
1. **Évolution** : Le projet semble être passé d'une structure monolithique (fichiers à la racine comme `main.py`, `api.py`) vers une structure hautement modulaire dans `leopardo_v2/`.
2. **Multi-Plateforme** : La présence de dossiers `mobile/`, `chromeExtention/` et `webVersion/` indique une volonté de présence omnicanale.
3. **Hybride Local/Cloud** : L'utilisation massive de SQLite (`.db`) combinée à Firebase montre une architecture hybride privilégiant la performance locale et la synchronisation cloud.
4. **Complexité** : Le grand nombre de dossiers à la racine suggère un projet vaste avec de nombreuses dépendances et outils internes accumulés au fil du temps.
