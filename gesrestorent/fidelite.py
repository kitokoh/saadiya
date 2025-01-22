import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QSpinBox, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
import sqlite3
import smtplib
from email.mime.text import MIMEText

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
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

        self.envoyer_offre_btn = QPushButton('Envoyer une Offre Personnalisée', self)

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

        layout.addWidget(self.envoyer_offre_btn)

        self.setLayout(layout)

        self.ajouter_client_btn.clicked.connect(self.ajouter_client)
        self.ajouter_points_btn.clicked.connect(self.ajouter_points)
        self.echanger_points_btn.clicked.connect(self.echanger_points)
        self.envoyer_offre_btn.clicked.connect(self.envoyer_offre)
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

    def envoyer_offre(self):
        client_nom = self.combo_client.currentText()
        cursor.execute('SELECT email FROM clients WHERE nom = ?', (client_nom,))
        email = cursor.fetchone()[0]

        if email:
            sujet = "Offre Personnalisée"
            message = f"Bonjour {client_nom},\n\nNous avons une offre spéciale pour vous !\n\nCordialement,\nL'équipe du restaurant."
            self.envoyer_email(email, sujet, message)
            QMessageBox.information(self, 'Succès', 'Offre envoyée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Client non trouvé.')

    def envoyer_email(self, destinataire, sujet, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = sujet
            msg['From'] = 'votre_email@gmail.com'
            msg['To'] = destinataire

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('votre_email@gmail.com', 'votre_mot_de_passe')
                server.sendmail('votre_email@gmail.com', destinataire, msg.as_string())
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")

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
        self.tab_widget.addTab(ProgrammeFidelite(), 'Programme de Fidélité')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())