import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QDateEdit, QDialog, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, QTimer
import sqlite3
import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QCalendarWidget

# Connexion à la base de données SQLite
conn = sqlite3.connect('cafe_restaurant.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_client TEXT NOT NULL,
    email_client TEXT NOT NULL,
    date TEXT NOT NULL,
    heure TEXT NOT NULL,
    table_id INTEGER NOT NULL,
    FOREIGN KEY (table_id) REFERENCES tables(id)
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
    QLineEdit, QComboBox, QDateEdit {
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

# Classe pour la gestion des réservations
class GestionReservations(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.nom_client = QLineEdit(self)
        self.email_client = QLineEdit(self)
        self.date_reservation = QDateEdit(self)
        self.date_reservation.setDate(QDate.currentDate())
        self.heure_reservation = QComboBox(self)
        self.heure_reservation.addItems([f"{h:02d}:00" for h in range(9, 22)])
        self.combo_table = QComboBox(self)
        self.reserver_btn = QPushButton('Réserver', self)
        self.calendrier = QCalendarWidget(self)
        self.table_reservations = QTableWidget(self)
        self.table_reservations.setColumnCount(5)
        self.table_reservations.setHorizontalHeaderLabels(['Nom', 'Email', 'Date', 'Heure', 'Table'])

        layout.addWidget(QLabel('Nom du Client:'))
        layout.addWidget(self.nom_client)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email_client)
        layout.addWidget(QLabel('Date de Réservation:'))
        layout.addWidget(self.date_reservation)
        layout.addWidget(QLabel('Heure de Réservation:'))
        layout.addWidget(self.heure_reservation)
        layout.addWidget(QLabel('Table:'))
        layout.addWidget(self.combo_table)
        layout.addWidget(self.reserver_btn)
        layout.addWidget(self.calendrier)
        layout.addWidget(self.table_reservations)

        self.setLayout(layout)

        self.reserver_btn.clicked.connect(self.reserver_table)
        self.calendrier.clicked.connect(self.charger_reservations_par_date)
        self.charger_tables()
        self.charger_reservations()

        # Timer pour les notifications de rappel
        self.timer = QTimer()
        self.timer.timeout.connect(self.envoyer_rappels)
        self.timer.start(60000)  # Vérifie toutes les minutes

    def charger_tables(self):
        self.combo_table.clear()
        cursor.execute('SELECT numero FROM tables')
        tables = cursor.fetchall()
        for table in tables:
            self.combo_table.addItem(str(table[0]))

    def charger_reservations(self):
        self.table_reservations.setRowCount(0)
        cursor.execute('''
        SELECT nom_client, email_client, date, heure, tables.numero
        FROM reservations
        JOIN tables ON reservations.table_id = tables.id
        ''')
        reservations = cursor.fetchall()
        for row_number, reservation in enumerate(reservations):
            self.table_reservations.insertRow(row_number)
            self.table_reservations.setItem(row_number, 0, QTableWidgetItem(reservation[0]))
            self.table_reservations.setItem(row_number, 1, QTableWidgetItem(reservation[1]))
            self.table_reservations.setItem(row_number, 2, QTableWidgetItem(reservation[2]))
            self.table_reservations.setItem(row_number, 3, QTableWidgetItem(reservation[3]))
            self.table_reservations.setItem(row_number, 4, QTableWidgetItem(str(reservation[4])))

    def charger_reservations_par_date(self):
        date = self.calendrier.selectedDate().toString('yyyy-MM-dd')
        self.table_reservations.setRowCount(0)
        cursor.execute('''
        SELECT nom_client, email_client, date, heure, tables.numero
        FROM reservations
        JOIN tables ON reservations.table_id = tables.id
        WHERE date = ?
        ''', (date,))
        reservations = cursor.fetchall()
        for row_number, reservation in enumerate(reservations):
            self.table_reservations.insertRow(row_number)
            self.table_reservations.setItem(row_number, 0, QTableWidgetItem(reservation[0]))
            self.table_reservations.setItem(row_number, 1, QTableWidgetItem(reservation[1]))
            self.table_reservations.setItem(row_number, 2, QTableWidgetItem(reservation[2]))
            self.table_reservations.setItem(row_number, 3, QTableWidgetItem(reservation[3]))
            self.table_reservations.setItem(row_number, 4, QTableWidgetItem(str(reservation[4])))

    def reserver_table(self):
        nom = self.nom_client.text()
        email = self.email_client.text()
        date = self.date_reservation.date().toString('yyyy-MM-dd')
        heure = self.heure_reservation.currentText()
        table_numero = self.combo_table.currentText()

        if nom and email and date and heure and table_numero:
            cursor.execute('SELECT id FROM tables WHERE numero = ?', (table_numero,))
            table_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO reservations (nom_client, email_client, date, heure, table_id) VALUES (?, ?, ?, ?, ?)', (nom, email, date, heure, table_id))
            conn.commit()
            self.charger_reservations()
            self.nom_client.clear()
            self.email_client.clear()
            QMessageBox.information(self, 'Succès', 'Réservation effectuée avec succès.')
        else:
            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir tous les champs.')

    def envoyer_rappels(self):
        cursor.execute('''
        SELECT nom_client, email_client, date, heure
        FROM reservations
        WHERE date = ? AND strftime('%H:%M', datetime('now', '+1 hour')) = heure
        ''', (QDate.currentDate().toString('yyyy-MM-dd'),))
        rappels = cursor.fetchall()

        for rappel in rappels:
            nom, email, date, heure = rappel
            self.envoyer_email(email, f'Rappel de Réservation', f'Bonjour {nom},\n\nVotre réservation est prévue aujourd\'hui à {heure}.\n\nCordialement,\nL\'équipe du restaurant.')

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
        self.tab_widget.addTab(GestionReservations(), 'Gestion des Réservations')

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())