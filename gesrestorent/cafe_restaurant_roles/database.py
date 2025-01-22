import sqlite3

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('cafe_restaurant.db')
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    return conn

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Création des tables si elles n'existent pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        permission TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal_activite (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
    )
    ''')

    # Ajouter des rôles et permissions par défaut
    roles_permissions = [
        ('administrateur', 'gestion_utilisateurs'),
        ('administrateur', 'gestion_stocks'),
        ('serveur', 'prendre_commandes'),
        ('livreur', 'livrer_commandes')
    ]
    cursor.executemany('INSERT OR IGNORE INTO permissions (role, permission) VALUES (?, ?)', roles_permissions)

    conn.commit()
    conn.close()