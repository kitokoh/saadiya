import sys
import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QLineEdit

# Initialisation Firebase
cred = credentials.Certificate("firebase_config.json")  # Remplace avec ton fichier JSON Firebase
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

class DatabaseManager:
    def __init__(self):
        self.local_db = "database.db"
        self.init_local_db()

    def init_local_db(self):
        """Création de la base SQLite locale"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                synced INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    def insert_local(self, name):
        """Insérer un produit dans SQLite et le marquer comme non synchronisé"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produits (name, synced) VALUES (?, 0)", (name,))
        conn.commit()
        conn.close()

    def get_unsynced_data(self):
        """Récupérer les données non synchronisées"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM produits WHERE synced = 0")
        data = cursor.fetchall()
        conn.close()
        return data

    def mark_as_synced(self, product_id):
        """Marquer un produit comme synchronisé"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        cursor.execute("UPDATE produits SET synced = 1 WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    def sync_with_firestore(self):
        """Synchronisation automatique avec Firestore"""
        unsynced_data = self.get_unsynced_data()
        for product in unsynced_data:
            product_id, name = product
            db_firestore.collection("produits").add({"name": name})
            self.mark_as_synced(product_id)  # Marquer comme synchronisé

    def get_all_products(self):
        """Récupérer tous les produits depuis SQLite"""
        conn = sqlite3.connect(self.local_db)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM produits")
        products = cursor.fetchall()
        conn.close()
        return products


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.initUI()
        self.db.sync_with_firestore()  # Synchronisation automatique au démarrage

    def initUI(self):
        self.setWindowTitle("Gestion des Produits")
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.refresh_list()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nom du produit")

        self.add_button = QPushButton("Ajouter Produit")
        self.add_button.clicked.connect(self.add_product)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.input_name)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def refresh_list(self):
        """Mettre à jour la liste des produits"""
        self.list_widget.clear()
        products = self.db.get_all_products()
        for product in products:
            self.list_widget.addItem(f"{product[0]} - {product[1]}")

    def add_product(self):
        """Ajouter un produit et synchroniser"""
        name = self.input_name.text()
        if name:
            self.db.insert_local(name)  # Ajouter en local
            self.db.sync_with_firestore()  # Synchroniser avec Firebase
            self.refresh_list()
            self.input_name.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
