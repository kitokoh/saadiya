import sys
import sqlite3
import imaplib
import email
from email.header import decode_header
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QTabWidget, QTextEdit, QComboBox, QProgressBar,
    QFileDialog, QSplitter, QListWidget, QListWidgetItem, QFormLayout, QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from cryptography.fernet import Fernet

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Génération d'une clé de chiffrement (à stocker de manière sécurisée en production)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

# Connexion à la base de données SQLite
def create_db():
    conn = sqlite3.connect('email_manager.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            smtp_server TEXT NOT NULL,
            smtp_port INTEGER NOT NULL,
            imap_server TEXT NOT NULL,
            imap_port INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            subject TEXT,
            sender TEXT,
            date TEXT,
            body TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts (id)
        )
    ''')
    conn.commit()
    conn.close()

create_db()

# Styles CSS pour une interface moderne
STYLESHEET = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QTableWidget {
        background-color: white;
        border: 1px solid #ddd;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit {
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    QLabel {
        font-size: 14px;
    }
    QTabWidget::pane {
        border: 1px solid #ddd;
    }
    QProgressBar {
        border: 1px solid #ddd;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #4CAF50;
    }
    QListWidget {
        background-color: white;
        border: 1px solid #ddd;
    }
    QTextEdit {
        background-color: white;
        border: 1px solid #ddd;
    }
"""

class EmailFetcherThread(QThread):
    """Thread pour récupérer les e-mails en arrière-plan."""
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(list)

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    def run(self):
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (self.account_id,))
        account = cursor.fetchone()
        conn.close()

        if account:
            email, _, _, imap_server, imap_port, username, password = account
            try:
                mail = imaplib.IMAP4_SSL(imap_server, imap_port)
                mail.login(username, cipher_suite.decrypt(password.encode()).decode())
                mail.select('inbox')

                status, messages = mail.search(None, 'ALL')
                if status == 'OK':
                    email_ids = messages[0].split()
                    emails = []
                    for i, email_id in enumerate(email_ids):
                        status, msg_data = mail.fetch(email_id, '(RFC822)')
                        if status == 'OK':
                            raw_email = msg_data[0][1]
                            msg = email.message_from_bytes(raw_email)
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or 'utf-8')
                            sender, encoding = decode_header(msg.get("From"))[0]
                            if isinstance(sender, bytes):
                                sender = sender.decode(encoding or 'utf-8')
                            date = msg.get("Date")
                            body = ""
                            attachments = []
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    if content_type == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                    elif part.get_filename():
                                        attachments.append(part)
                            else:
                                body = msg.get_payload(decode=True).decode()

                            emails.append((subject, sender, date, body, attachments))
                        self.progress_signal.emit(int((i + 1) / len(email_ids) * 100))
                    self.finished_signal.emit(emails)
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des e-mails: {e}")
                self.finished_signal.emit([])

class EmailManagerApp(QMainWindow):
    """Application principale pour gérer les e-mails."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestionnaire d\'E-mails Professionnels')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(STYLESHEET)
        self.initUI()

    def initUI(self):
        # Layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Tableau des comptes e-mail
        self.accounts_table = QTableWidget(self)
        self.accounts_table.setColumnCount(7)
        self.accounts_table.setHorizontalHeaderLabels(['ID', 'E-mail', 'SMTP Server', 'IMAP Server', 'Username', 'Actions'])
        self.accounts_table.hideColumn(0)  # Cacher la colonne ID
        main_layout.addWidget(self.accounts_table)

        # Bouton pour ajouter un compte
        add_button = QPushButton('Ajouter un Compte', self)
        add_button.clicked.connect(self.show_add_account_dialog)
        main_layout.addWidget(add_button)

        # Charger les comptes
        self.load_accounts()

    def load_accounts(self):
        """Charge les comptes depuis la base de données et les affiche dans le tableau."""
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        conn.close()

        self.accounts_table.setRowCount(len(accounts))
        for row, account in enumerate(accounts):
            for col, data in enumerate(account):
                self.accounts_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_widget.setLayout(action_layout)

            edit_button = QPushButton('Éditer', self)
            edit_button.clicked.connect(lambda _, id=account[0]: self.show_edit_account_dialog(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton('Supprimer', self)
            delete_button.clicked.connect(lambda _, id=account[0]: self.delete_account(id))
            action_layout.addWidget(delete_button)

            read_button = QPushButton('Lire les E-mails', self)
            read_button.clicked.connect(lambda _, id=account[0]: self.read_emails(id))
            action_layout.addWidget(read_button)

            self.accounts_table.setCellWidget(row, 6, action_widget)

    def show_add_account_dialog(self):
        """Affiche la fenêtre modale pour ajouter un compte."""
        dialog = AddEditAccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_accounts()

    def show_edit_account_dialog(self, account_id):
        """Affiche la fenêtre modale pour modifier un compte."""
        dialog = AddEditAccountDialog(self, account_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_accounts()

    def delete_account(self, account_id):
        """Supprime un compte de la base de données."""
        confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer ce compte ?',
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect('email_manager.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
            conn.commit()
            conn.close()
            self.load_accounts()

    def read_emails(self, account_id):
        """Ouvre un nouvel onglet pour lire les e-mails."""
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
        account = cursor.fetchone()
        conn.close()

        if account:
            email_tab = QWidget()
            email_layout = QVBoxLayout()
            email_tab.setLayout(email_layout)

            # Barre de progression
            self.progress_bar = QProgressBar(self)
            email_layout.addWidget(self.progress_bar)

            # Liste des e-mails
            self.email_list = QListWidget(self)
            self.email_list.itemClicked.connect(self.show_email_details)
            email_layout.addWidget(self.email_list)

            # Détails de l'e-mail
            self.email_details = QTextEdit(self)
            self.email_details.setReadOnly(True)
            email_layout.addWidget(self.email_details)

            # Pièces jointes
            self.attachments_list = QListWidget(self)
            self.attachments_list.itemClicked.connect(self.download_attachment)
            email_layout.addWidget(QLabel('Pièces jointes:'))
            email_layout.addWidget(self.attachments_list)

            # Ajouter l'onglet à la fenêtre principale
            if not hasattr(self, 'tab_widget'):
                self.tab_widget = QTabWidget(self)
                self.centralWidget().layout().addWidget(self.tab_widget)

            self.tab_widget.addTab(email_tab, f'Inbox - {account[1]}')

            # Démarrer le thread pour récupérer les e-mails
            self.fetcher_thread = EmailFetcherThread(account_id)
            self.fetcher_thread.progress_signal.connect(self.progress_bar.setValue)
            self.fetcher_thread.finished_signal.connect(self.display_emails)
            self.fetcher_thread.start()

    def display_emails(self, emails):
        """Affiche les e-mails dans la liste."""
        self.email_list.clear()
        for subject, sender, date, body, attachments in emails:
            item = QListWidgetItem(f"{subject} - {sender} ({date})")
            item.setData(Qt.UserRole, (subject, sender, date, body, attachments))
            self.email_list.addItem(item)

    def show_email_details(self, item):
        """Affiche les détails de l'e-mail sélectionné."""
        subject, sender, date, body, attachments = item.data(Qt.UserRole)
        self.email_details.setText(f"De: {sender}\nDate: {date}\nSujet: {subject}\n\n{body}")

        # Afficher les pièces jointes
        self.attachments_list.clear()
        for attachment in attachments:
            filename = attachment.get_filename()
            if filename:
                self.attachments_list.addItem(QListWidgetItem(filename))

    def download_attachment(self, item):
        """Télécharge la pièce jointe sélectionnée."""
        filename = item.text()
        save_path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer la pièce jointe', filename)
        if save_path:
            for email_item in self.email_list.selectedItems():
                _, _, _, _, attachments = email_item.data(Qt.UserRole)
                for attachment in attachments:
                    if attachment.get_filename() == filename:
                        with open(save_path, 'wb') as f:
                            f.write(attachment.get_payload(decode=True))
                        QMessageBox.information(self, 'Succès', f'Pièce jointe enregistrée sous {save_path}')
                        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailManagerApp()
    window.show()
    sys.exit(app.exec_())