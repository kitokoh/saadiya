import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDateEdit, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    seuil_alerte INTEGER NOT NULL DEFAULT 10
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fournisseurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    contact TEXT NOT NULL,
    adresse TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS commandes_fournisseurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fournisseur_id INTEGER NOT NULL,
    ingredient TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    date_commande TEXT DEFAULT CURRENT_TIMESTAMP,
    cout REAL NOT NULL,
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(id)
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

# Classe pour la gestion des stocks
class GestionStocks(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_ingredient = QLineEdit(self)
        self.quantite_stock = QSpinBox(self)
        self.seuil_alerte = QSpinBox(self)
        self.seuil_alerte.setValue(10)
        self.ajouter_stock_btn = QPushButton('Ajouter Stock', self)
        self.table_stocks = QTableWidget(self)
        self.table_stocks.setColumnCount(3)
        self.table_stocks.setHorizontalHeaderLabels(['Ingrédient', 'Quantité', 'Seuil d\'Alerte'])

        layout.addWidget(QLabel('Ingrédient:'))
        layout.addWidget(self.nom_ingredient)
        layout.addWidget(QLabel('Quantité:'))
        layout.addWidget(self.quantite_stock)
        layout.addWidget(QLabel('Seuil d\'Alerte:'))
        layout.addWidget(self.seuil_alerte)
        layout.addWidget(self.ajouter_stock_btn)
        layout.addWidget(self.table_stocks)

        self.setLayout(layout)

        self.ajouter_stock_btn.clicked.connect(self.ajouter_stock)
        self.charger_stocks()
        self.verifier_alertes_stock()

    def charger_stocks(self):
        self.table_stocks.setRowCount(0)
        cursor.execute('SELECT ingredient, quantite, seuil_alerte FROM stocks')
        stocks = cursor.fetchall()
        for row_number, stock in enumerate(stocks):
            self.table_stocks.insertRow(row_number)
            self.table_stocks.setItem(row_number, 0, QTableWidgetItem(stock[0]))
            self.table_stocks.setItem(row_number, 1, QTableWidgetItem(str(stock[1])))
            self.table_stocks.setItem(row_number, 2, QTableWidgetItem(str(stock[2])))

    def ajouter_stock(self):
        ingredient = self.nom_ingredient.text()
        quantite = self.quantite_stock.value()
        seuil_alerte = self.seuil_alerte.value()

        if ingredient and quantite >= 0:
            cursor.execute('INSERT INTO stocks (ingredient, quantite, seuil_alerte) VALUES (?, ?, ?)', (ingredient, quantite, seuil_alerte))
            conn.commit()
            self.charger_stocks()
            self.nom_ingredient.clear()
            self.quantite_stock.setValue(0)
            self.seuil_alerte.setValue(10)
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def verifier_alertes_stock(self):
        cursor.execute('SELECT ingredient, quantite, seuil_alerte FROM stocks WHERE quantite <= seuil_alerte')
        alertes = cursor.fetchall()
        if alertes:
            message = "Alertes de stock faible :\n"
            for alerte in alertes:
                message += f"{alerte[0]} (Quantité: {alerte[1]}, Seuil: {alerte[2]})\n"
            QMessageBox.warning(self, 'Alerte de Stock', message)

# Classe pour la gestion des fournisseurs
class GestionFournisseurs(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_fournisseur = QLineEdit(self)
        self.contact_fournisseur = QLineEdit(self)
        self.adresse_fournisseur = QLineEdit(self)
        self.ajouter_fournisseur_btn = QPushButton('Ajouter Fournisseur', self)
        self.table_fournisseurs = QTableWidget(self)
        self.table_fournisseurs.setColumnCount(3)
        self.table_fournisseurs.setHorizontalHeaderLabels(['Nom', 'Contact', 'Adresse'])

        layout.addWidget(QLabel('Nom du Fournisseur:'))
        layout.addWidget(self.nom_fournisseur)
        layout.addWidget(QLabel('Contact:'))
        layout.addWidget(self.contact_fournisseur)
        layout.addWidget(QLabel('Adresse:'))
        layout.addWidget(self.adresse_fournisseur)
        layout.addWidget(self.ajouter_fournisseur_btn)
        layout.addWidget(self.table_fournisseurs)

        self.setLayout(layout)

        self.ajouter_fournisseur_btn.clicked.connect(self.ajouter_fournisseur)
        self.charger_fournisseurs()

    def charger_fournisseurs(self):
        self.table_fournisseurs.setRowCount(0)
        cursor.execute('SELECT nom, contact, adresse FROM fournisseurs')
        fournisseurs = cursor.fetchall()
        for row_number, fournisseur in enumerate(fournisseurs):
            self.table_fournisseurs.insertRow(row_number)
            self.table_fournisseurs.setItem(row_number, 0, QTableWidgetItem(fournisseur[0]))
            self.table_fournisseurs.setItem(row_number, 1, QTableWidgetItem(fournisseur[1]))
            self.table_fournisseurs.setItem(row_number, 2, QTableWidgetItem(fournisseur[2]))

    def ajouter_fournisseur(self):
        nom = self.nom_fournisseur.text()
        contact = self.contact_fournisseur.text()
        adresse = self.adresse_fournisseur.text()

        if nom and contact:
            cursor.execute('INSERT INTO fournisseurs (nom, contact, adresse) VALUES (?, ?, ?)', (nom, contact, adresse))
            conn.commit()
            self.charger_fournisseurs()
            self.nom_fournisseur.clear()
            self.contact_fournisseur.clear()
            self.adresse_fournisseur.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

# Classe pour la gestion des commandes fournisseurs
class GestionCommandesFournisseurs(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_fournisseur = QComboBox(self)
        self.ingredient_commande = QLineEdit(self)
        self.quantite_commande = QSpinBox(self)
        self.cout_commande = QLineEdit(self)
        self.ajouter_commande_btn = QPushButton('Ajouter Commande', self)
        self.table_commandes = QTableWidget(self)
        self.table_commandes.setColumnCount(5)
        self.table_commandes.setHorizontalHeaderLabels(['Fournisseur', 'Ingrédient', 'Quantité', 'Coût', 'Date'])

        layout.addWidget(QLabel('Fournisseur:'))
        layout.addWidget(self.combo_fournisseur)
        layout.addWidget(QLabel('Ingrédient:'))
        layout.addWidget(self.ingredient_commande)
        layout.addWidget(QLabel('Quantité:'))
        layout.addWidget(self.quantite_commande)
        layout.addWidget(QLabel('Coût:'))
        layout.addWidget(self.cout_commande)
        layout.addWidget(self.ajouter_commande_btn)
        layout.addWidget(self.table_commandes)

        self.setLayout(layout)

        self.charger_fournisseurs()
        self.ajouter_commande_btn.clicked.connect(self.ajouter_commande)
        self.charger_commandes()

    def charger_fournisseurs(self):
        self.combo_fournisseur.clear()
        cursor.execute('SELECT nom FROM fournisseurs')
        fournisseurs = cursor.fetchall()
        for fournisseur in fournisseurs:
            self.combo_fournisseur.addItem(fournisseur[0])

    def charger_commandes(self):
        self.table_commandes.setRowCount(0)
        cursor.execute('''
        SELECT fournisseurs.nom, commandes_fournisseurs.ingredient, commandes_fournisseurs.quantite, commandes_fournisseurs.cout, commandes_fournisseurs.date_commande
        FROM commandes_fournisseurs
        JOIN fournisseurs ON commandes_fournisseurs.fournisseur_id = fournisseurs.id
        ''')
        commandes = cursor.fetchall()
        for row_number, commande in enumerate(commandes):
            self.table_commandes.insertRow(row_number)
            self.table_commandes.setItem(row_number, 0, QTableWidgetItem(commande[0]))
            self.table_commandes.setItem(row_number, 1, QTableWidgetItem(commande[1]))
            self.table_commandes.setItem(row_number, 2, QTableWidgetItem(str(commande[2])))
            self.table_commandes.setItem(row_number, 3, QTableWidgetItem(str(commande[3])))
            self.table_commandes.setItem(row_number, 4, QTableWidgetItem(commande[4]))

    def ajouter_commande(self):
        fournisseur_nom = self.combo_fournisseur.currentText()
        ingredient = self.ingredient_commande.text()
        quantite = self.quantite_commande.value()
        cout = self.cout_commande.text()

        if fournisseur_nom and ingredient and quantite > 0 and cout:
            cursor.execute('SELECT id FROM fournisseurs WHERE nom = ?', (fournisseur_nom,))
            fournisseur_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO commandes_fournisseurs (fournisseur_id, ingredient, quantite, cout) VALUES (?, ?, ?, ?)', (fournisseur_id, ingredient, quantite, float(cout)))
            conn.commit()
            self.charger_commandes()
            self.ingredient_commande.clear()
            self.quantite_commande.setValue(0)
            self.cout_commande.clear()
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
        self.tab_widget.addTab(GestionStocks(), 'Gestion des Stocks')
        self.tab_widget.addTab(GestionFournisseurs(), 'Gestion des Fournisseurs')
        self.tab_widget.addTab(GestionCommandesFournisseurs(), 'Commandes Fournisseurs')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())