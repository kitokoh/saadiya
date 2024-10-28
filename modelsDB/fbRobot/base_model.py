import sqlite3

class BaseModel:
    def __init__(self, db_name='nova360.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        """Exécuter une requête avec ou sans paramètres."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erreur d'exécution de la requête: {e}")

    def fetch_all(self, query, params=()):
        """Récupérer plusieurs lignes avec ou sans paramètres."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        """Récupérer une seule ligne avec ou sans paramètres."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        """Fermer la connexion à la base de données."""
        self.connection.close()
