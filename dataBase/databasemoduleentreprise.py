import bcrypt
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import sqlite3

# Initialisation de la clé de chiffrement
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table pour les utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,  # Mot de passe haché
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL,  # Ex: Admin, Manager, Employee
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # Table pour les entreprises
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entreprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT,
            ville TEXT,
            code_postal TEXT,
            pays TEXT,
            telephone TEXT,
            email TEXT NOT NULL UNIQUE,
            site_web TEXT,
            iban TEXT,
            numero_enregistrement TEXT,
            logo BLOB,  # Stocker le logo en binaire
            cachet BLOB,  # Stocker le cachet en binaire
            signature BLOB,  # Stocker la signature en binaire
            devise TEXT DEFAULT 'EUR',  # Ajout de la devise
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # Table pour les employés
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            entreprise_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            poste TEXT NOT NULL,  # Ex: Responsable Marketing, Assistant
            telephone TEXT,
            email TEXT NOT NULL UNIQUE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les réseaux sociaux
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reseaux_sociaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise_id INTEGER NOT NULL,
            nom TEXT NOT NULL,  # Ex: Facebook, Instagram
            identifiant TEXT,  # Identifiant du compte
            mot_de_passe TEXT,  # Mot de passe crypté
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les zones géographiques ciblées
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zones_geographiques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise_id INTEGER NOT NULL,
            nom TEXT NOT NULL,  # Ex: Europe, Afrique
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les catégories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    # Table pour les sous-catégories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sous_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (categorie_id) REFERENCES categories (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les campagnes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campagnes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise_id INTEGER NOT NULL,
            nom TEXT NOT NULL,
            description TEXT,
            date_debut TIMESTAMP,
            date_fin TIMESTAMP,
            budget REAL,
            devise TEXT DEFAULT 'EUR',  # Ajout de la devise
            statut TEXT NOT NULL,  # Ex: Brouillon, En attente, En cours, Terminé
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les informations de serveur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS serveurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise_id INTEGER NOT NULL,
            type TEXT NOT NULL,  # Ex: SMTP, FTP
            hote TEXT NOT NULL,
            port INTEGER,
            identifiant TEXT NOT NULL,
            mot_de_passe TEXT NOT NULL,  # Crypté
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_suppression TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (entreprise_id) REFERENCES entreprises (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les logs d'activité
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,  # Ex: Création, Modification, Suppression
            table_concernee TEXT NOT NULL,  # Ex: utilisateurs, entreprises
            id_concerne INTEGER NOT NULL,  # ID de l'entité concernée
            date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les connexions utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connexions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            adresse_ip TEXT,
            navigateur TEXT,
            date_connexion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Table pour l'historique des modifications
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historique_modifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            table_modifiee TEXT NOT NULL,
            id_entite INTEGER NOT NULL,
            ancienne_valeur TEXT,
            nouvelle_valeur TEXT,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Table pour les résultats des campagnes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultats_campagnes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campagne_id INTEGER NOT NULL,
            indicateur TEXT NOT NULL,  # Ex: Taux de conversion, ROI
            valeur REAL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campagne_id) REFERENCES campagnes (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les cibles marketing
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cibles_marketing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campagne_id INTEGER NOT NULL,
            age_min INTEGER,
            age_max INTEGER,
            genre TEXT,
            localisation TEXT,
            interets TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campagne_id) REFERENCES campagnes (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les logs détaillés
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_detail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            table_concernee TEXT NOT NULL,
            id_concerne INTEGER NOT NULL,
            adresse_ip TEXT,
            navigateur TEXT,
            date_action TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les feedbacks utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks_utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les sessions utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL UNIQUE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_expiration TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les interactions utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions_utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type_interaction TEXT NOT NULL,  # Ex: Connexion, Consultation, Achat
            description TEXT,
            date_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Table pour les préférences utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences_utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            preference TEXT NOT NULL,
            valeur TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Ajout d'index pour optimiser les recherches
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_entreprises_email ON entreprises(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employes_email ON employes(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_campagnes_statut ON campagnes(statut)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_entreprises_nom ON entreprises(nom)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employes_nom ON employes(nom)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_campagnes_date_debut ON campagnes(date_debut)')

    # Insertion de données fictives
    insert_fake_data(cursor, cipher_suite)

    conn.commit()
    conn.close()

# Fonction pour hacher les mots de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Fonction pour vérifier les mots de passe
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Fonction pour chiffrer les données sensibles
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode('utf-8'))

# Fonction pour déchiffrer les données sensibles
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode('utf-8')

# Fonction pour créer une session utilisateur
def create_session(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Générer un token de session unique
    session_token = Fernet.generate_key().decode('utf-8')
    
    # Définir la date d'expiration à un mois plus tard
    expiration_date = datetime.now() + timedelta(days=30)
    
    cursor.execute('''
        INSERT INTO sessions (user_id, session_token, date_expiration)
        VALUES (?, ?, ?)
    ''', (user_id, session_token, expiration_date))
    
    conn.commit()
    conn.close()
    
    return session_token

# Fonction pour vérifier la session utilisateur
def check_session(session_token):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM sessions
        WHERE session_token = ? AND date_expiration > ? AND is_active = 1
    ''', (session_token, datetime.now()))
    
    session = cursor.fetchone()
    conn.close()
    
    return session is not None

# Fonction pour insérer des données fictives
def insert_fake_data(cursor, cipher_suite):
    # Insertion d'un utilisateur
    hashed_password = hash_password("password123")
    cursor.execute('''
        INSERT INTO users (username, password, email, role)
        VALUES (?, ?, ?, ?)
    ''', ("admin", hashed_password, "admin@example.com", "Admin"))

    user_id = cursor.lastrowid

    # Insertion d'une entreprise
    cursor.execute('''
        INSERT INTO entreprises (nom, adresse, ville, code_postal, pays, telephone, email, site_web, iban, numero_enregistrement, devise)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("Entreprise Test", "123 Rue Exemple", "Paris", "75001", "France", "0123456789", "contact@entreprise.com", "www.entreprise.com", "FR7630001007941234567890185", "RCS123456789", "EUR"))

    entreprise_id = cursor.lastrowid

    # Insertion d'un employé
    cursor.execute('''
        INSERT INTO employes (user_id, entreprise_id, nom, prenom, poste, telephone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, entreprise_id, "Dupont", "Jean", "Responsable Marketing", "0987654321", "jean.dupont@entreprise.com"))

    # Insertion d'un réseau social
    encrypted_password = encrypt_data("socialpassword123")
    cursor.execute('''
        INSERT INTO reseaux_sociaux (entreprise_id, nom, identifiant, mot_de_passe, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (entreprise_id, "Facebook", "entreprise_fb", encrypted_password, "Page Facebook officielle"))

    # Insertion d'une zone géographique
    cursor.execute('''
        INSERT INTO zones_geographiques (entreprise_id, nom, description)
        VALUES (?, ?, ?)
    ''', (entreprise_id, "Europe", "Zone de marché européenne"))

    # Insertion d'une catégorie
    cursor.execute('''
        INSERT INTO categories (nom, description)
        VALUES (?, ?)
    ''', ("Marketing", "Catégorie pour les campagnes marketing"))

    categorie_id = cursor.lastrowid

    # Insertion d'une sous-catégorie
    cursor.execute('''
        INSERT INTO sous_categories (categorie_id, nom, description)
        VALUES (?, ?, ?)
    ''', (categorie_id, "Réseaux Sociaux", "Sous-catégorie pour les campagnes sur les réseaux sociaux"))

    # Insertion d'une campagne
    cursor.execute('''
        INSERT INTO campagnes (entreprise_id, nom, description, date_debut, date_fin, budget, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (entreprise_id, "Campagne Printemps", "Promotion de printemps", datetime.now(), datetime.now() + timedelta(days=30), 5000.0, "En cours"))

    # Insertion d'un serveur
    encrypted_server_password = encrypt_data("serverpassword123")
    cursor.execute('''
        INSERT INTO serveurs (entreprise_id, type, hote, port, identifiant, mot_de_passe)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entreprise_id, "SMTP", "smtp.example.com", 587, "smtp_user", encrypted_server_password))

    # Insertion d'un log d'activité
    cursor.execute('''
        INSERT INTO logs (user_id, action, table_concernee, id_concerne)
        VALUES (?, ?, ?, ?)
    ''', (user_id, "Création", "entreprises", entreprise_id))

    # Insertion d'une connexion utilisateur
    cursor.execute('''
        INSERT INTO connexions (user_id, adresse_ip, navigateur)
        VALUES (?, ?, ?)
    ''', (user_id, "192.168.1.1", "Chrome"))

