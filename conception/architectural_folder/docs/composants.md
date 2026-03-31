# Composants Techniques - Leopardo AI

Ce document détaille les composants clés du système et leur rôle au sein de l'architecture.

## 1. Service Container
Le `ServiceContainer` (`leopardo_v2/app/services/service_container.py`) est le cœur de l'infrastructure de services. Il permet de :
- Enregistrer des services globaux via `register(name, service)`.
- Récupérer n'importe quel service depuis n'importe quel module via `get(name)`.
Cela permet une communication fluide entre les modules sans couplage direct.

## 2. Système d'Authentification et de Rôles
Le `AuthService` gère l'état de la session utilisateur et les niveaux d'accès :
- **Niveaux de Compte** :
  - `Free` : Accès limité aux fonctionnalités de base.
  - `Pro` : Accès aux outils marketing et bots avancés.
  - `Enterprise` : Accès complet, incluant la finance et la gestion avancée.
- **Vérification d'Accès** : La méthode `has_access(feature_level)` est utilisée pour restreindre l'affichage des boutons dans le menu latéral et l'accès aux fonctionnalités sensibles.

## 3. Structure d'une Feature (Module de fonctionnalité)
Toutes les fonctionnalités dans `leopardo_v2/app/features/` suivent un schéma standard :
- `__init__.py` : Contient la fonction `create_X_feature()` qui instancie le Modèle, la Vue et le Contrôleur.
- `X_model.py` : Logique de données, accès à la DB.
- `X_widget.py` : Classe héritant de `QWidget` pour l'interface.
- `X_controller.py` : Gère l'interaction entre le widget et le modèle via les signaux PyQt5.

## 4. UI Centralisée (MainWindow)
La `MainWindow` (`leopardo_v2/app/ui/main_window.py`) agit comme le chef d'orchestre :
- Elle initialise les services de base.
- Elle contient un `QStackedWidget` (`content_stack`) où tous les widgets de fonctionnalités sont chargés.
- Elle connecte les signaux du `SideMenu` pour basculer entre les widgets de la pile.

## 5. Services Transversaux
- **NotificationService** : Gère l'affichage des notifications système et les badges rouges sur les boutons du menu.
- **LanguageManager** : Permet la traduction dynamique de l'interface en plusieurs langues (FR, EN, TR, AR, PT).
- **ConfigService** : Sauvegarde et charge les préférences utilisateur locales dans un fichier JSON.
