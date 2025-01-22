import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDateEdit, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    statut TEXT DEFAULT 'libre'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS commandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    plat_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    FOREIGN KEY (table_id) REFERENCES tables(id),
    FOREIGN KEY (plat_id) REFERENCES plats(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS paiements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    montant REAL NOT NULL,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES tables(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient TEXT NOT NULL,
    quantite INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
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

# Classe pour la connexion utilisateur
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Connexion')
        self.setGeometry(200, 200, 300, 150)

        layout = QFormLayout()

        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton('Se connecter', self)

        layout.addRow('Nom d\'utilisateur:', self.username)
        layout.addRow('Mot de passe:', self.password)
        layout.addRow(self.login_btn)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.verifier_connexion)

    def verifier_connexion(self):
        username = self.username.text()
        password = self.password.text()

        cursor.execute('SELECT role FROM utilisateurs WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()

        if result:
            self.role = result[0]
            self.accept()
        else:
            QMessageBox.warning(self, 'Erreur', 'Nom d\'utilisateur ou mot de passe incorrect.')

# Classe pour gérer les plats
class GestionPlats(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_plat = QLineEdit(self)
        self.prix_plat = QLineEdit(self)
        self.ajouter_plat_btn = QPushButton('Ajouter Plat', self)
        self.table_plats = QTableWidget(self)
        self.table_plats.setColumnCount(2)
        self.table_plats.setHorizontalHeaderLabels(['Nom du Plat', 'Prix'])

        layout.addWidget(QLabel('Nom du Plat:'))
        layout.addWidget(self.nom_plat)
        layout.addWidget(QLabel('Prix:'))
        layout.addWidget(self.prix_plat)
        layout.addWidget(self.ajouter_plat_btn)
        layout.addWidget(self.table_plats)

        self.setLayout(layout)

        self.ajouter_plat_btn.clicked.connect(self.ajouter_plat)
        self.charger_plats()

    def charger_plats(self):
        self.table_plats.setRowCount(0)
        cursor.execute('SELECT nom, prix FROM plats')
        plats = cursor.fetchall()
        for row_number, plat in enumerate(plats):
            self.table_plats.insertRow(row_number)
            self.table_plats.setItem(row_number, 0, QTableWidgetItem(plat[0]))
            self.table_plats.setItem(row_number, 1, QTableWidgetItem(str(plat[1])))

    def ajouter_plat(self):
        nom = self.nom_plat.text()
        prix = self.prix_plat.text()

        if nom and prix:
            cursor.execute('INSERT INTO plats (nom, prix) VALUES (?, ?)', (nom, float(prix)))
            conn.commit()
            self.charger_plats()
            self.nom_plat.clear()
            self.prix_plat.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs')

# Classe pour gérer les tables
class GestionTables(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.numero_table = QLineEdit(self)
        self.ajouter_table_btn = QPushButton('Ajouter Table', self)
        self.table_tables = QTableWidget(self)
        self.table_tables.setColumnCount(2)
        self.table_tables.setHorizontalHeaderLabels(['Numéro de Table', 'Statut'])

        layout.addWidget(QLabel('Numéro de Table:'))
        layout.addWidget(self.numero_table)
        layout.addWidget(self.ajouter_table_btn)
        layout.addWidget(self.table_tables)

        self.setLayout(layout)

        self.ajouter_table_btn.clicked.connect(self.ajouter_table)
        self.charger_tables()

    def charger_tables(self):
        self.table_tables.setRowCount(0)
        cursor.execute('SELECT numero, statut FROM tables')
        tables = cursor.fetchall()
        for row_number, table in enumerate(tables):
            self.table_tables.insertRow(row_number)
            self.table_tables.setItem(row_number, 0, QTableWidgetItem(str(table[0])))
            self.table_tables.setItem(row_number, 1, QTableWidgetItem(table[1]))

    def ajouter_table(self):
        numero = self.numero_table.text()

        if numero:
            cursor.execute('INSERT INTO tables (numero) VALUES (?)', (int(numero),))
            conn.commit()
            self.charger_tables()
            self.numero_table.clear()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs')

# Classe pour gérer les commandes
class GestionCommandes(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_table = QComboBox(self)
        self.combo_plat = QComboBox(self)
        self.quantite = QSpinBox(self)
        self.ajouter_commande_btn = QPushButton('Ajouter Commande', self)
        self.table_commandes = QTableWidget(self)
        self.table_commandes.setColumnCount(3)
        self.table_commandes.setHorizontalHeaderLabels(['Table', 'Plat', 'Quantité'])

        layout.addWidget(QLabel('Table:'))
        layout.addWidget(self.combo_table)
        layout.addWidget(QLabel('Plat:'))
        layout.addWidget(self.combo_plat)
        layout.addWidget(QLabel('Quantité:'))
        layout.addWidget(self.quantite)
        layout.addWidget(self.ajouter_commande_btn)
        layout.addWidget(self.table_commandes)

        self.setLayout(layout)

        self.charger_tables()
        self.charger_plats()
        self.ajouter_commande_btn.clicked.connect(self.ajouter_commande)
        self.charger_commandes()

    def charger_tables(self):
        self.combo_table.clear()
        cursor.execute('SELECT numero FROM tables')
        tables = cursor.fetchall()
        for table in tables:
            self.combo_table.addItem(str(table[0]))

    def charger_plats(self):
        self.combo_plat.clear()
        cursor.execute('SELECT nom FROM plats')
        plats = cursor.fetchall()
        for plat in plats:
            self.combo_plat.addItem(plat[0])

    def charger_commandes(self):
        self.table_commandes.setRowCount(0)
        cursor.execute('''
        SELECT tables.numero, plats.nom, commandes.quantite
        FROM commandes
        JOIN tables ON commandes.table_id = tables.id
        JOIN plats ON commandes.plat_id = plats.id
        ''')
        commandes = cursor.fetchall()
        for row_number, commande in enumerate(commandes):
            self.table_commandes.insertRow(row_number)
            self.table_commandes.setItem(row_number, 0, QTableWidgetItem(str(commande[0])))
            self.table_commandes.setItem(row_number, 1, QTableWidgetItem(commande[1]))
            self.table_commandes.setItem(row_number, 2, QTableWidgetItem(str(commande[2])))

    def ajouter_commande(self):
        table_numero = self.combo_table.currentText()
        plat_nom = self.combo_plat.currentText()
        quantite = self.quantite.value()

        if table_numero and plat_nom and quantite > 0:
            cursor.execute('SELECT id FROM tables WHERE numero = ?', (int(table_numero),))
            table_id = cursor.fetchone()[0]
            cursor.execute('SELECT id FROM plats WHERE nom = ?', (plat_nom,))
            plat_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO commandes (table_id, plat_id, quantite) VALUES (?, ?, ?)', (table_id, plat_id, quantite))
            conn.commit()
            self.charger_commandes()
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs')

# Classe pour gérer les paiements
class GestionPaiements(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_table_paiement = QComboBox(self)
        self.payer_btn = QPushButton('Payer', self)
        self.table_paiements = QTableWidget(self)
        self.table_paiements.setColumnCount(3)
        self.table_paiements.setHorizontalHeaderLabels(['Table', 'Montant', 'Date'])

        layout.addWidget(QLabel('Table:'))
        layout.addWidget(self.combo_table_paiement)
        layout.addWidget(self.payer_btn)
        layout.addWidget(self.table_paiements)

        self.setLayout(layout)

        self.charger_tables()
        self.payer_btn.clicked.connect(self.payer)
        self.charger_paiements()

    def charger_tables(self):
        self.combo_table_paiement.clear()
        cursor.execute('SELECT numero FROM tables')
        tables = cursor.fetchall()
        for table in tables:
            self.combo_table_paiement.addItem(str(table[0]))

    def charger_paiements(self):
        self.table_paiements.setRowCount(0)
        cursor.execute('''
        SELECT tables.numero, paiements.montant, paiements.date
        FROM paiements
        JOIN tables ON paiements.table_id = tables.id
        ''')
        paiements = cursor.fetchall()
        for row_number, paiement in enumerate(paiements):
            self.table_paiements.insertRow(row_number)
            self.table_paiements.setItem(row_number, 0, QTableWidgetItem(str(paiement[0])))
            self.table_paiements.setItem(row_number, 1, QTableWidgetItem(str(paiement[1])))
            self.table_paiements.setItem(row_number, 2, QTableWidgetItem(paiement[2]))

    def payer(self):
        table_numero = self.combo_table_paiement.currentText()

        if table_numero:
            cursor.execute('SELECT id FROM tables WHERE numero = ?', (int(table_numero),))
            table_id = cursor.fetchone()[0]
            cursor.execute('''
            SELECT SUM(plats.prix * commandes.quantite)
            FROM commandes
            JOIN plats ON commandes.plat_id = plats.id
            WHERE commandes.table_id = ?
            ''', (table_id,))
            total = cursor.fetchone()[0]
            if total:
                cursor.execute('INSERT INTO paiements (table_id, montant) VALUES (?, ?)', (table_id, total))
                conn.commit()
                self.charger_paiements()
                QMessageBox.information(self, 'Paiement', f'Paiement de {total} € enregistré.')
            else:
                QMessageBox.warning(self, 'Erreur', 'Aucune commande pour cette table.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez sélectionner une table.')

# Classe pour gérer les stocks
class GestionStocks(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_ingredient = QLineEdit(self)
        self.quantite_stock = QSpinBox(self)
        self.ajouter_stock_btn = QPushButton('Ajouter Stock', self)
        self.table_stocks = QTableWidget(self)
        self.table_stocks.setColumnCount(2)
        self.table_stocks.setHorizontalHeaderLabels(['Ingrédient', 'Quantité'])

        layout.addWidget(QLabel('Ingrédient:'))
        layout.addWidget(self.nom_ingredient)
        layout.addWidget(QLabel('Quantité:'))
        layout.addWidget(self.quantite_stock)
        layout.addWidget(self.ajouter_stock_btn)
        layout.addWidget(self.table_stocks)

        self.setLayout(layout)

        self.ajouter_stock_btn.clicked.connect(self.ajouter_stock)
        self.charger_stocks()

    def charger_stocks(self):
        self.table_stocks.setRowCount(0)
        cursor.execute('SELECT ingredient, quantite FROM stocks')
        stocks = cursor.fetchall()
        for row_number, stock in enumerate(stocks):
            self.table_stocks.insertRow(row_number)
            self.table_stocks.setItem(row_number, 0, QTableWidgetItem(stock[0]))
            self.table_stocks.setItem(row_number, 1, QTableWidgetItem(str(stock[1])))

    def ajouter_stock(self):
        ingredient = self.nom_ingredient.text()
        quantite = self.quantite_stock.value()

        if ingredient and quantite > 0:
            cursor.execute('INSERT INTO stocks (ingredient, quantite) VALUES (?, ?)', (ingredient, quantite))
            conn.commit()
            self.charger_stocks()
            self.nom_ingredient.clear()
            self.quantite_stock.setValue(0)
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

# Classe pour générer des rapports avec graphiques
class GestionRapports(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.date_rapport = QDateEdit(self)
        self.date_rapport.setDate(QDate.currentDate())
        self.generer_rapport_btn = QPushButton('Générer Rapport', self)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(QLabel('Date:'))
        layout.addWidget(self.date_rapport)
        layout.addWidget(self.generer_rapport_btn)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        self.generer_rapport_btn.clicked.connect(self.generer_rapport)

    def generer_rapport(self):
        date = self.date_rapport.date().toString('yyyy-MM-dd')
        cursor.execute('''
        SELECT paiements.date, SUM(paiements.montant)
        FROM paiements
        WHERE paiements.date LIKE ?
        GROUP BY paiements.date
        ''', (f'{date}%',))
        rapports = cursor.fetchall()

        dates = [rapport[0] for rapport in rapports]
        montants = [rapport[1] for rapport in rapports]

        self.ax.clear()
        self.ax.bar(dates, montants, color='blue')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Montant (€)')
        self.ax.set_title('Ventes par jour')
        self.canvas.draw()

# Classe principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gestion de Café/Restaurant')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(STYLESHEET)

        # Vérifier la connexion utilisateur
        self.login_dialog = LoginDialog()
        if self.login_dialog.exec_() == QDialog.Accepted:
            self.role = self.login_dialog.role
            self.init_tabs()
        else:
            sys.exit()

    def init_tabs(self):
        tab_widget = QTabWidget()
        tab_widget.addTab(GestionPlats(), 'Gestion des Plats')
        tab_widget.addTab(GestionTables(), 'Gestion des Tables')
        tab_widget.addTab(GestionCommandes(), 'Gestion des Commandes')
        tab_widget.addTab(GestionPaiements(), 'Gestion des Paiements')
        tab_widget.addTab(GestionStocks(), 'Gestion des Stocks')
        tab_widget.addTab(GestionRapports(), 'Rapports')

        self.setCentralWidget(tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())