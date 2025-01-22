from database import get_db_connection

# Modèle pour les commandes
class Commande:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        commandes = conn.execute('SELECT * FROM commandes').fetchall()
        conn.close()
        return commandes

    @staticmethod
    def get_by_id(commande_id):
        conn = get_db_connection()
        commande = conn.execute('SELECT * FROM commandes WHERE id = ?', (commande_id,)).fetchone()
        conn.close()
        return commande

    @staticmethod
    def create(client_nom, client_email, plats, total, statut='en attente'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO commandes (client_nom, client_email, plats, total, statut)
        VALUES (?, ?, ?, ?, ?)
        ''', (client_nom, client_email, plats, total, statut))
        conn.commit()
        commande_id = cursor.lastrowid
        conn.close()
        return commande_id

# Modèle pour les clients
class Client:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        clients = conn.execute('SELECT * FROM clients').fetchall()
        conn.close()
        return clients

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        client = conn.execute('SELECT * FROM clients WHERE email = ?', (email,)).fetchone()
        conn.close()
        return client

    @staticmethod
    def create(nom, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (nom, email) VALUES (?, ?)', (nom, email))
        conn.commit()
        client_id = cursor.lastrowid
        conn.close()
        return client_id

# Modèle pour les stocks
class Stock:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        stocks = conn.execute('SELECT * FROM stocks').fetchall()
        conn.close()
        return stocks

    @staticmethod
    def create(ingredient, quantite):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stocks (ingredient, quantite) VALUES (?, ?)', (ingredient, quantite))
        conn.commit()
        stock_id = cursor.lastrowid
        conn.close()
        return stock_id