import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='stock.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Table des catégories
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL
            )
        ''')

        # Table des articles (avec catégorie)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                prix REAL NOT NULL,
                categorie_id INTEGER,
                FOREIGN KEY (categorie_id) REFERENCES categories(id)
            )
        ''')

        # Table des utilisateurs
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                role TEXT NOT NULL,  # 'operateur' ou 'admin'
                password TEXT NOT NULL
            )
        ''')

        # Table des logs (historique des modifications)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER,
                action TEXT NOT NULL,
                date_action TEXT NOT NULL,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            )
        ''')

        self.conn.commit()

    # Gestion des catégories
    def add_categorie(self, nom):
        self.cursor.execute('INSERT INTO categories (nom) VALUES (?)', (nom,))
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute('SELECT * FROM categories')
        return self.cursor.fetchall()

    # Gestion des articles (avec catégorie)
    def add_article(self, nom, quantite, prix, categorie_id):
        self.cursor.execute('''
            INSERT INTO articles (nom, quantite, prix, categorie_id) VALUES (?, ?, ?, ?)
        ''', (nom, quantite, prix, categorie_id))
        self.conn.commit()

    def get_articles(self):
        self.cursor.execute('''
            SELECT articles.id, articles.nom, articles.quantite, articles.prix, categories.nom
            FROM articles
            LEFT JOIN categories ON articles.categorie_id = categories.id
        ''')
        return self.cursor.fetchall()

    # Gestion des utilisateurs
    def add_utilisateur(self, nom, role, password):
        self.cursor.execute('''
            INSERT INTO utilisateurs (nom, role, password) VALUES (?, ?, ?)
        ''', (nom, role, password))
        self.conn.commit()

    def get_utilisateurs(self):
        self.cursor.execute('SELECT * FROM utilisateurs')
        return self.cursor.fetchall()

    def verifier_utilisateur(self, nom, password):
        self.cursor.execute('SELECT * FROM utilisateurs WHERE nom = ? AND password = ?', (nom, password))
        return self.cursor.fetchone()

    # Gestion des logs
    def add_log(self, utilisateur_id, action):
        date_action = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO logs (utilisateur_id, action, date_action) VALUES (?, ?, ?)
        ''', (utilisateur_id, action, date_action))
        self.conn.commit()

    def get_logs(self):
        self.cursor.execute('''
            SELECT logs.id, utilisateurs.nom, logs.action, logs.date_action
            FROM logs
            JOIN utilisateurs ON logs.utilisateur_id = utilisateurs.id
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()