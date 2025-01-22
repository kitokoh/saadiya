import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import sqlite3
import random

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS commandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_nom TEXT NOT NULL,
    client_email TEXT NOT NULL,
    plats TEXT NOT NULL,
    total REAL NOT NULL,
    type_commande TEXT NOT NULL,
    statut TEXT DEFAULT 'en attente'
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

# Classe pour la commande en ligne
class CommandeEnLigne(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.client_nom = QLineEdit(self)
        self.client_email = QLineEdit(self)
        self.combo_plat = QComboBox(self)
        self.quantite_plat = QSpinBox(self)
        self.type_commande = QComboBox(self)
        self.type_commande.addItems(['Livraison', 'Retrait sur place'])
        self.passer_commande_btn = QPushButton('Passer Commande', self)
        self.table_commandes = QTableWidget(self)
        self.table_commandes.setColumnCount(6)
        self.table_commandes.setHorizontalHeaderLabels(['ID', 'Client', 'Email', 'Plats', 'Total', 'Statut'])

        layout.addWidget(QLabel('Nom du Client:'))
        layout.addWidget(self.client_nom)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.client_email)
        layout.addWidget(QLabel('Plat:'))
        layout.addWidget(self.combo_plat)
        layout.addWidget(QLabel('Quantité:'))
        layout.addWidget(self.quantite_plat)
        layout.addWidget(QLabel('Type de Commande:'))
        layout.addWidget(self.type_commande)
        layout.addWidget(self.passer_commande_btn)
        layout.addWidget(self.table_commandes)

        self.setLayout(layout)

        self.charger_plats()
        self.passer_commande_btn.clicked.connect(self.passer_commande)
        self.charger_commandes()

        # Timer pour le suivi des commandes
        self.timer = QTimer()
        self.timer.timeout.connect(self.mettre_a_jour_statuts)
        self.timer.start(5000)  # Vérifie toutes les 5 secondes

    def charger_plats(self):
        self.combo_plat.clear()
        cursor.execute('SELECT nom, prix FROM plats')
        plats = cursor.fetchall()
        for plat in plats:
            self.combo_plat.addItem(f"{plat[0]} - {plat[1]} €")

    def charger_commandes(self):
        self.table_commandes.setRowCount(0)
        cursor.execute('SELECT id, client_nom, client_email, plats, total, statut FROM commandes')
        commandes = cursor.fetchall()
        for row_number, commande in enumerate(commandes):
            self.table_commandes.insertRow(row_number)
            self.table_commandes.setItem(row_number, 0, QTableWidgetItem(str(commande[0])))
            self.table_commandes.setItem(row_number, 1, QTableWidgetItem(commande[1]))
            self.table_commandes.setItem(row_number, 2, QTableWidgetItem(commande[2]))
            self.table_commandes.setItem(row_number, 3, QTableWidgetItem(commande[3]))
            self.table_commandes.setItem(row_number, 4, QTableWidgetItem(str(commande[4])))
            self.table_commandes.setItem(row_number, 5, QTableWidgetItem(commande[5]))

    def passer_commande(self):
        nom = self.client_nom.text()
        email = self.client_email.text()
        plat = self.combo_plat.currentText().split(' - ')[0]
        quantite = self.quantite_plat.value()
        type_commande = self.type_commande.currentText()

        if nom and email and plat and quantite > 0:
            cursor.execute('SELECT prix FROM plats WHERE nom = ?', (plat,))
            prix = cursor.fetchone()[0]
            total = prix * quantite

            # Simuler un paiement en ligne (remplacer par Stripe ou PayPal)
            if self.simuler_paiement(total):
                cursor.execute('INSERT INTO commandes (client_nom, client_email, plats, total, type_commande) VALUES (?, ?, ?, ?, ?)', (nom, email, f"{plat} x {quantite}", total, type_commande))
                conn.commit()
                self.charger_commandes()
                self.client_nom.clear()
                self.client_email.clear()
                self.quantite_plat.setValue(0)
                QMessageBox.information(self, 'Succès', 'Commande passée avec succès.')
            else:
                QMessageBox.warning(self, 'Erreur', 'Paiement échoué.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def simuler_paiement(self, montant):
        # Simuler un paiement réussi (à remplacer par une API de paiement)
        return random.choice([True, False])

    def mettre_a_jour_statuts(self):
        cursor.execute('SELECT id, statut FROM commandes WHERE statut != "livré"')
        commandes = cursor.fetchall()
        for commande in commandes:
            id_commande, statut = commande
            nouveaux_statuts = ['en préparation', 'prêt', 'en livraison', 'livré']
            nouvel_index = nouveaux_statuts.index(statut) + 1 if statut in nouveaux_statuts else 0
            if nouvel_index < len(nouveaux_statuts):
                nouveau_statut = nouveaux_statuts[nouvel_index]
                cursor.execute('UPDATE commandes SET statut = ? WHERE id = ?', (nouveau_statut, id_commande))
                conn.commit()
        self.charger_commandes()

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
        self.tab_widget.addTab(CommandeEnLigne(), 'Commande en Ligne')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())