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
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        message TEXT NOT NULL,
        destinataire TEXT NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        fcm_token TEXT  # Token FCM pour les notifications push
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient TEXT NOT NULL,
        quantite INTEGER NOT NULL,
        seuil_alerte INTEGER NOT NULL DEFAULT 10
    )
    ''')

    conn.commit()
    conn.close()