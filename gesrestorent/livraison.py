import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDateEdit, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
import sqlite3
import random

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS livreurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    statut TEXT DEFAULT 'disponible'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS livraisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livreur_id INTEGER NOT NULL,
    client TEXT NOT NULL,
    adresse TEXT NOT NULL,
    distance REAL NOT NULL,
    frais_livraison REAL NOT NULL,
    statut TEXT DEFAULT 'en attente',
    FOREIGN KEY (livreur_id) REFERENCES livreurs(id)
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
CREATE TABLE IF NOT EXISTS recompenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    points_requis INTEGER NOT NULL
)
''')

conn.commit()

# Styles CSS pour l'interface
STYLESHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QWidget {
        font-size: 14px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #ddd;
    }
    QLineEdit, QComboBox, QSpinBox, QDateEdit {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }
    QLabel {
        font-weight: bold;
    }
    QDialog {
        background-color: #f9f9f9;
    }
"""

# Classe pour la gestion des livreurs
class GestionLivreurs(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_livreur = QLineEdit(self)
        self.ajouter_livreur_btn = QPushButton('Ajouter Livreur', self)
        self.table_livreurs = QTableWidget(self)
        self.table_livreurs.setColumnCount(2)
        self.table_livreurs.setHorizontalHeaderLabels(['Nom', 'Statut'])

        layout.addWidget(QLabel('Nom du Livreur:'))
        layout.addWidget(self.nom_livreur)
        layout.addWidget(self.ajouter_livreur_btn)
        layout.addWidget(self.table_livreurs)

        self.setLayout(layout)

        self.ajouter_livreur_btn.clicked.connect(self.ajouter_livreur)
        self.charger_livreurs()

    def charger_livreurs(self):
        self.table_livreurs.setRowCount(0)
        cursor.execute('SELECT nom, statut FROM livreurs')
        livreurs = cursor.fetchall()
        for row_number, livreur in enumerate(livreurs):
            self.table_livreurs.insertRow(row_number)
            self.table_livreurs.setItem(row_number, 0, QTableWidgetItem(livreur[0]))
            self.table_livreurs.setItem(row_number, 1, QTableWidgetItem(livreur[1]))

    def ajouter_livreur(self):
        nom = self.nom_livreur.text()

        if nom:
            cursor.execute('INSERT INTO livreurs (nom) VALUES (?)', (nom,))
            conn.commit()
            self.charger_livreurs()
            self.nom_livreur.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

# Classe pour la gestion des livraisons
class GestionLivraisons(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_livreur = QComboBox(self)
        self.nom_client = QLineEdit(self)
        self.adresse_client = QLineEdit(self)
        self.distance_livraison = QLineEdit(self)
        self.calculer_frais_btn = QPushButton('Calculer Frais de Livraison', self)
        self.frais_livraison = QLabel('Frais de Livraison: 0 €', self)
        self.ajouter_livraison_btn = QPushButton('Ajouter Livraison', self)
        self.table_livraisons = QTableWidget(self)
        self.table_livraisons.setColumnCount(5)
        self.table_livraisons.setHorizontalHeaderLabels(['Livreur', 'Client', 'Adresse', 'Frais', 'Statut'])

        layout.addWidget(QLabel('Livreur:'))
        layout.addWidget(self.combo_livreur)
        layout.addWidget(QLabel('Nom du Client:'))
        layout.addWidget(self.nom_client)
        layout.addWidget(QLabel('Adresse:'))
        layout.addWidget(self.adresse_client)
        layout.addWidget(QLabel('Distance (km):'))
        layout.addWidget(self.distance_livraison)
        layout.addWidget(self.calculer_frais_btn)
        layout.addWidget(self.frais_livraison)
        layout.addWidget(self.ajouter_livraison_btn)
        layout.addWidget(self.table_livraisons)

        self.setLayout(layout)

        self.charger_livreurs()
        self.calculer_frais_btn.clicked.connect(self.calculer_frais)
        self.ajouter_livraison_btn.clicked.connect(self.ajouter_livraison)
        self.charger_livraisons()

    def charger_livreurs(self):
        self.combo_livreur.clear()
        cursor.execute('SELECT nom FROM livreurs WHERE statut = "disponible"')
        livreurs = cursor.fetchall()
        for livreur in livreurs:
            self.combo_livreur.addItem(livreur[0])

    def calculer_frais(self):
        distance = float(self.distance_livraison.text())
        frais = distance * 1.5  # Exemple : 1.5 € par km
        self.frais_livraison.setText(f'Frais de Livraison: {frais:.2f} €')

    def ajouter_livraison(self):
        livreur_nom = self.combo_livreur.currentText()
        client = self.nom_client.text()
        adresse = self.adresse_client.text()
        distance = float(self.distance_livraison.text())
        frais = float(self.frais_livraison.text().split('€')[0].strip())

        if livreur_nom and client and adresse and distance > 0:
            cursor.execute('SELECT id FROM livreurs WHERE nom = ?', (livreur_nom,))
            livreur_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO livraisons (livreur_id, client, adresse, distance, frais_livraison) VALUES (?, ?, ?, ?, ?)', (livreur_id, client, adresse, distance, frais))
            conn.commit()
            self.charger_livraisons()
            self.nom_client.clear()
            self.adresse_client.clear()
            self.distance_livraison.clear()
            self.frais_livraison.setText('Frais de Livraison: 0 €')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def charger_livraisons(self):
        self.table_livraisons.setRowCount(0)
        cursor.execute('''
        SELECT livreurs.nom, livraisons.client, livraisons.adresse, livraisons.frais_livraison, livraisons.statut
        FROM livraisons
        JOIN livreurs ON livraisons.livreur_id = livreurs.id
        ''')
        livraisons = cursor.fetchall()
        for row_number, livraison in enumerate(livraisons):
            self.table_livraisons.insertRow(row_number)
            self.table_livraisons.setItem(row_number, 0, QTableWidgetItem(livraison[0]))
            self.table_livraisons.setItem(row_number, 1, QTableWidgetItem(livraison[1]))
            self.table_livraisons.setItem(row_number, 2, QTableWidgetItem(livraison[2]))
            self.table_livraisons.setItem(row_number, 3, QTableWidgetItem(str(livraison[3])))
            self.table_livraisons.setItem(row_number, 4, QTableWidgetItem(livraison[4]))

# Classe pour le programme de fidélité
class ProgrammeFidelite(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_client = QLineEdit(self)
        self.email_client = QLineEdit(self)
        self.ajouter_client_btn = QPushButton('Ajouter Client', self)
        self.table_clients = QTableWidget(self)
        self.table_clients.setColumnCount(3)
        self.table_clients.setHorizontalHeaderLabels(['Nom', 'Email', 'Points'])

        self.combo_client = QComboBox(self)
        self.points_ajouter = QSpinBox(self)
        self.ajouter_points_btn = QPushButton('Ajouter Points', self)

        self.combo_recompense = QComboBox(self)
        self.echanger_points_btn = QPushButton('Échanger Points', self)

        layout.addWidget(QLabel('Nom du Client:'))
        layout.addWidget(self.nom_client)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email_client)
        layout.addWidget(self.ajouter_client_btn)
        layout.addWidget(self.table_clients)

        layout.addWidget(QLabel('Client:'))
        layout.addWidget(self.combo_client)
        layout.addWidget(QLabel('Points à Ajouter:'))
        layout.addWidget(self.points_ajouter)
        layout.addWidget(self.ajouter_points_btn)

        layout.addWidget(QLabel('Récompense:'))
        layout.addWidget(self.combo_recompense)
        layout.addWidget(self.echanger_points_btn)

        self.setLayout(layout)

        self.ajouter_client_btn.clicked.connect(self.ajouter_client)
        self.ajouter_points_btn.clicked.connect(self.ajouter_points)
        self.echanger_points_btn.clicked.connect(self.echanger_points)
        self.charger_clients()
        self.charger_recompenses()

    def charger_clients(self):
        self.table_clients.setRowCount(0)
        self.combo_client.clear()
        cursor.execute('SELECT nom, email, points_fidelite FROM clients')
        clients = cursor.fetchall()
        for row_number, client in enumerate(clients):
            self.table_clients.insertRow(row_number)
            self.table_clients.setItem(row_number, 0, QTableWidgetItem(client[0]))
            self.table_clients.setItem(row_number, 1, QTableWidgetItem(client[1]))
            self.table_clients.setItem(row_number, 2, QTableWidgetItem(str(client[2])))
            self.combo_client.addItem(client[0])

    def charger_recompenses(self):
        self.combo_recompense.clear()
        cursor.execute('SELECT description FROM recompenses')
        recompenses = cursor.fetchall()
        for recompense in recompenses:
            self.combo_recompense.addItem(recompense[0])

    def ajouter_client(self):
        nom = self.nom_client.text()
        email = self.email_client.text()

        if nom and email:
            cursor.execute('INSERT INTO clients (nom, email) VALUES (?, ?)', (nom, email))
            conn.commit()
            self.charger_clients()
            self.nom_client.clear()
            self.email_client.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def ajouter_points(self):
        client_nom = self.combo_client.currentText()
        points = self.points_ajouter.value()

        if client_nom and points > 0:
            cursor.execute('UPDATE clients SET points_fidelite = points_fidelite + ? WHERE nom = ?', (points, client_nom))
            conn.commit()
            self.charger_clients()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def echanger_points(self):
        client_nom = self.combo_client.currentText()
        recompense = self.combo_recompense.currentText()

        if client_nom and recompense:
            cursor.execute('SELECT points_requis FROM recompenses WHERE description = ?', (recompense,))
            points_requis = cursor.fetchone()[0]
            cursor.execute('SELECT points_fidelite FROM clients WHERE nom = ?', (client_nom,))
            points_client = cursor.fetchone()[0]

            if points_client >= points_requis:
                cursor.execute('UPDATE clients SET points_fidelite = points_fidelite - ? WHERE nom = ?', (points_requis, client_nom))
                conn.commit()
                QMessageBox.information(self, 'Succès', f'Récompense "{recompense}" échangée avec succès.')
                self.charger_clients()
            else:
                QMessageBox.warning(self, 'Erreur', 'Points insuffisants pour cette récompense.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

# Classe principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion de Café/Restaurant')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(STYLESHEET)

        # Tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(GestionLivreurs(), 'Gestion des Livreurs')
        self.tab_widget.addTab(GestionLivraisons(), 'Gestion des Livraisons')
        self.tab_widget.addTab(ProgrammeFidelite(), 'Programme de Fidélité')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())