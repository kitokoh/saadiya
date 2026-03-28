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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

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

class EmailFetcherThread(QThread):
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
            _, email, _, imap_server, imap_port, username, password = account
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

class EmailSmsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)

        self.accounts_table = QTableWidget(self)
        self.accounts_table.setColumnCount(7)
        self.accounts_table.setHorizontalHeaderLabels(['ID', 'E-mail', 'SMTP Server', 'IMAP Server', 'Username', 'Actions'])
        self.accounts_table.hideColumn(0)
        main_layout.addWidget(self.accounts_table)

        add_button = QPushButton('Add Account', self)
        add_button.clicked.connect(self.show_add_account_dialog)
        main_layout.addWidget(add_button)

        self.load_accounts()

    def load_accounts(self):
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        conn.close()

        self.accounts_table.setRowCount(len(accounts))
        for row, account in enumerate(accounts):
            for col, data in enumerate(account):
                self.accounts_table.setItem(row, col, QTableWidgetItem(str(data)))

            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_widget.setLayout(action_layout)

            edit_button = QPushButton('Edit', self)
            edit_button.clicked.connect(lambda _, id=account[0]: self.show_edit_account_dialog(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton('Delete', self)
            delete_button.clicked.connect(lambda _, id=account[0]: self.delete_account(id))
            action_layout.addWidget(delete_button)

            read_button = QPushButton('Read Emails', self)
            read_button.clicked.connect(lambda _, id=account[0]: self.read_emails(id))
            action_layout.addWidget(read_button)

            self.accounts_table.setCellWidget(row, 6, action_widget)

    def show_add_account_dialog(self):
        dialog = AddEditAccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_accounts()

    def show_edit_account_dialog(self, account_id):
        dialog = AddEditAccountDialog(self, account_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_accounts()

    def delete_account(self, account_id):
        confirm = QMessageBox.question(self, 'Confirm', 'Are you sure you want to delete this account?',
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect('email_manager.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
            conn.commit()
            conn.close()
            self.load_accounts()

    def read_emails(self, account_id):
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (account_id,))
        account = cursor.fetchone()
        conn.close()

        if account:
            email_tab = QWidget()
            email_layout = QVBoxLayout()
            email_tab.setLayout(email_layout)

            self.progress_bar = QProgressBar(self)
            email_layout.addWidget(self.progress_bar)

            self.email_list = QListWidget(self)
            self.email_list.itemClicked.connect(self.show_email_details)
            email_layout.addWidget(self.email_list)

            self.email_details = QTextEdit(self)
            self.email_details.setReadOnly(True)
            email_layout.addWidget(self.email_details)

            self.attachments_list = QListWidget(self)
            self.attachments_list.itemClicked.connect(self.download_attachment)
            email_layout.addWidget(QLabel('Attachments:'))
            email_layout.addWidget(self.attachments_list)

            if not hasattr(self, 'tab_widget'):
                self.tab_widget = QTabWidget(self)
                self.layout().addWidget(self.tab_widget)

            self.tab_widget.addTab(email_tab, f'Inbox - {account[1]}')

            self.fetcher_thread = EmailFetcherThread(account_id)
            self.fetcher_thread.progress_signal.connect(self.progress_bar.setValue)
            self.fetcher_thread.finished_signal.connect(self.display_emails)
            self.fetcher_thread.start()

    def display_emails(self, emails):
        self.email_list.clear()
        for subject, sender, date, body, attachments in emails:
            item = QListWidgetItem(f"{subject} - {sender} ({date})")
            item.setData(Qt.UserRole, (subject, sender, date, body, attachments))
            self.email_list.addItem(item)

    def show_email_details(self, item):
        subject, sender, date, body, attachments = item.data(Qt.UserRole)
        self.email_details.setText(f"From: {sender}\nDate: {date}\nSubject: {subject}\n\n{body}")

        self.attachments_list.clear()
        for attachment in attachments:
            filename = attachment.get_filename()
            if filename:
                self.attachments_list.addItem(QListWidgetItem(filename))

    def download_attachment(self, item):
        filename = item.text()
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Attachment', filename)
        if save_path:
            for email_item in self.email_list.selectedItems():
                _, _, _, _, attachments = email_item.data(Qt.UserRole)
                for attachment in attachments:
                    if attachment.get_filename() == filename:
                        with open(save_path, 'wb') as f:
                            f.write(attachment.get_payload(decode=True))
                        QMessageBox.information(self, 'Success', f'Attachment saved to {save_path}')
                        return

class AddEditAccountDialog(QDialog):
    def __init__(self, parent=None, account_id=None):
        super().__init__(parent)
        self.account_id = account_id
        self.setWindowTitle('Add/Edit Account' if not account_id else 'Edit Account')
        self.initUI()
        if account_id:
            self.load_account_data()

    def initUI(self):
        layout = QFormLayout()
        self.email_input = QLineEdit()
        self.smtp_server_input = QLineEdit()
        self.smtp_port_input = QLineEdit()
        self.imap_server_input = QLineEdit()
        self.imap_port_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow('Email:', self.email_input)
        layout.addRow('SMTP Server:', self.smtp_server_input)
        layout.addRow('SMTP Port:', self.smtp_port_input)
        layout.addRow('IMAP Server:', self.imap_server_input)
        layout.addRow('IMAP Port:', self.imap_port_input)
        layout.addRow('Username:', self.username_input)
        layout.addRow('Password:', self.password_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_account_data(self):
        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = ?', (self.account_id,))
        account = cursor.fetchone()
        conn.close()

        if account:
            self.email_input.setText(account[1])
            self.smtp_server_input.setText(account[2])
            self.smtp_port_input.setText(str(account[3]))
            self.imap_server_input.setText(account[4])
            self.imap_port_input.setText(str(account[5]))
            self.username_input.setText(account[6])
            self.password_input.setText(cipher_suite.decrypt(account[7].encode()).decode())

    def accept(self):
        email = self.email_input.text()
        smtp_server = self.smtp_server_input.text()
        smtp_port = int(self.smtp_port_input.text())
        imap_server = self.imap_server_input.text()
        imap_port = int(self.imap_port_input.text())
        username = self.username_input.text()
        password = cipher_suite.encrypt(self.password_input.text().encode())

        conn = sqlite3.connect('email_manager.db')
        cursor = conn.cursor()
        if self.account_id:
            cursor.execute('''
                UPDATE accounts
                SET email=?, smtp_server=?, smtp_port=?, imap_server=?, imap_port=?, username=?, password=?
                WHERE id=?
            ''', (email, smtp_server, smtp_port, imap_server, imap_port, username, password, self.account_id))
        else:
            cursor.execute('''
                INSERT INTO accounts (email, smtp_server, smtp_port, imap_server, imap_port, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email, smtp_server, smtp_port, imap_server, imap_port, username, password))
        conn.commit()
        conn.close()
        super().accept()
