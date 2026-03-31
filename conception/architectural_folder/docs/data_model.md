# Modèle de Données - Leopardo AI

Ce document détaille les bases de données et les fichiers de configuration utilisés par l'application.

## 1. Bases de Données SQLite

### Base Principale : `leopardo_v2.db`
Située dans `/leopardo_v2/app/data/leopardo_v2.db`. Elle stocke les données essentielles :
- **Table `contacts`** : Stocke les informations clients (Nom, Email, Téléphone).
- **Table `groups`** : Gestion des groupes de contacts pour les campagnes marketing.
- **Table `crm`** : Suivi des prospects et clients avec leur statut.
- **Table `dms`** : Gestion des documents (titre, type, chemin d'accès).
- **Table `project_management`** : Suivi des projets et tâches.
- **Table `sav`** : Système de tickets pour le service après-vente.
- **Table `short_links`** : Raccourcisseur d'URL et suivi des clics.
- **Table `prospection`** : Gestion de la prospection commerciale.
- **Table `sales_templates`** : Modèles de textes commerciaux.
- **Table `prompts_tools`** : Bibliothèque de prompts IA.
- **Table `detection_rules`** : Règles métier pour les robots d'automatisation (mot-clé -> plateforme -> template -> action).

### Base Utilisateur : `nova360.db`
Gère les accès utilisateur et les informations de compte :
- **Table `users`** : Contient les informations d'authentification (ID, Nom d'utilisateur, Mot de passe haché, Rôle).

## 2. Fichiers de Configuration (JSON)

- **`config.json`** : Stocke les paramètres globaux de l'application (Langue par défaut, thème, URLs de l'API).
- **`session.json`** : Conserve l'état de la session utilisateur actuelle (Connecté, nom d'utilisateur, rôles).
- **`translations.json`** : Dictionnaire des chaînes de caractères pour les différentes langues supportées.
- **`version.json`** : Information sur la version actuelle de l'application pour les mises à jour.

## 3. Configuration Distante (Firebase)
L'application utilise Firebase pour la configuration dynamique et la récupération de données temps réel sans mise à jour complète de l'application cliente.
- **`firebase.json`** : Configuration du projet Firebase.
- **`secretforapidrive.json`** : Clés privées pour l'accès aux services cloud.
