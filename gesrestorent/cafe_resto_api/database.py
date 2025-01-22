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
    CREATE TABLE IF NOT EXISTS commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_nom TEXT NOT NULL,
        client_email TEXT NOT NULL,
        plats TEXT NOT NULL,
        total REAL NOT NULL,
        statut TEXT DEFAULT 'en attente'
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        points_fidelite INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient TEXT NOT NULL,
        quantite INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()