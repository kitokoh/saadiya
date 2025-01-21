import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QTabWidget, QTextEdit, QComboBox, QProgressBar,
    QFileDialog, QListWidget, QFormLayout, QGroupBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont
import logging
from cryptography.fernet import Fernet

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Génération d'une clé de chiffrement (à stocker de manière sécurisée en production)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

# Chemin de la base de données
ROAMING_PATH = os.getenv('APPDATA')
DB_PATH = os.path.join(ROAMING_PATH, 'Saadiya Resources', 'job_applications.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connexion à la base de données SQLite
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            platform TEXT NOT NULL,
            status TEXT NOT NULL,
            applied_at TEXT NOT NULL,
            cv_id INTEGER,
            cover_letter_id INTEGER,
            FOREIGN KEY (cv_id) REFERENCES documents (id),
            FOREIGN KEY (cover_letter_id) REFERENCES documents (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            level TEXT NOT NULL
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

class JobApplicationManager(QMainWindow):
    """Application principale pour gérer les candidatures."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestionnaire de Candidatures - Saadiya')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(STYLESHEET)
        self.initUI()

    def initUI(self):
        # Layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Onglets
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget)

        # Onglet des documents
        self.documents_tab = QWidget()
        self.init_documents_tab()
        self.tab_widget.addTab(self.documents_tab, 'Documents')

        # Onglet des candidatures
        self.applications_tab = QWidget()
        self.init_applications_tab()
        self.tab_widget.addTab(self.applications_tab, 'Candidatures')

        # Onglet des compétences
        self.skills_tab = QWidget()
        self.init_skills_tab()
        self.tab_widget.addTab(self.skills_tab, 'Compétences')

    def init_documents_tab(self):
        """Initialise l'onglet des documents."""
        layout = QVBoxLayout()

        # Liste des documents
        self.documents_list = QListWidget(self)
        layout.addWidget(self.documents_list)

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        add_button = QPushButton('Ajouter un Document', self)
        add_button.clicked.connect(self.add_document)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton('Supprimer', self)
        delete_button.clicked.connect(self.delete_document)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        self.documents_tab.setLayout(layout)
        self.load_documents()

    def init_applications_tab(self):
        """Initialise l'onglet des candidatures."""
        layout = QVBoxLayout()

        # Liste des candidatures
        self.applications_table = QTableWidget(self)
        self.applications_table.setColumnCount(7)
        self.applications_table.setHorizontalHeaderLabels(['ID', 'Titre', 'Entreprise', 'Plateforme', 'Statut', 'Date', 'Actions'])
        self.applications_table.hideColumn(0)  # Cacher la colonne ID
        layout.addWidget(self.applications_table)

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        add_button = QPushButton('Ajouter une Candidature', self)
        add_button.clicked.connect(self.add_application)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton('Supprimer', self)
        delete_button.clicked.connect(self.delete_application)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        self.applications_tab.setLayout(layout)
        self.load_applications()

    def init_skills_tab(self):
        """Initialise l'onglet des compétences."""
        layout = QVBoxLayout()

        # Liste des compétences
        self.skills_list = QListWidget(self)
        layout.addWidget(self.skills_list)

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        add_button = QPushButton('Ajouter une Compétence', self)
        add_button.clicked.connect(self.add_skill)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton('Supprimer', self)
        delete_button.clicked.connect(self.delete_skill)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        self.skills_tab.setLayout(layout)
        self.load_skills()

    def load_documents(self):
        """Charge les documents depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM documents')
        documents = cursor.fetchall()
        conn.close()

        self.documents_list.clear()
        for doc in documents:
            item = QListWidgetItem(f"{doc[1]} ({doc[2]})")
            item.setData(Qt.UserRole, doc[0])  # Stocker l'ID du document
            self.documents_list.addItem(item)

    def load_applications(self):
        """Charge les candidatures depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM applications')
        applications = cursor.fetchall()
        conn.close()

        self.applications_table.setRowCount(len(applications))
        for row, app in enumerate(applications):
            for col, data in enumerate(app):
                self.applications_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Boutons d'action
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_widget.setLayout(action_layout)

            edit_button = QPushButton('Éditer', self)
            edit_button.clicked.connect(lambda _, id=app[0]: self.edit_application(id))
            action_layout.addWidget(edit_button)

            delete_button = QPushButton('Supprimer', self)
            delete_button.clicked.connect(lambda _, id=app[0]: self.delete_application(id))
            action_layout.addWidget(delete_button)

            self.applications_table.setCellWidget(row, 6, action_widget)

    def load_skills(self):
        """Charge les compétences depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills')
        skills = cursor.fetchall()
        conn.close()

        self.skills_list.clear()
        for skill in skills:
            item = QListWidgetItem(f"{skill[1]} ({skill[2]})")
            item.setData(Qt.UserRole, skill[0])  # Stocker l'ID de la compétence
            self.skills_list.addItem(item)

    def add_document(self):
        """Ajoute un document à la base de données."""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Sélectionner un document', '', 'PDF Files (*.pdf);;Word Files (*.docx)')
        if file_path:
            name = os.path.basename(file_path)
            doc_type = QInputDialog.getItem(self, 'Type de document', 'Sélectionnez le type de document:', ['CV', 'Lettre de motivation', 'Référence'], 0, False)
            if doc_type[1]:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO documents (name, type, path, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (name, doc_type[0], file_path, QDate.currentDate().toString(Qt.ISODate)))
                conn.commit()
                conn.close()
                self.load_documents()

    def delete_document(self):
        """Supprime un document de la base de données."""
        selected_item = self.documents_list.currentItem()
        if selected_item:
            doc_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer ce document ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
                conn.commit()
                conn.close()
                self.load_documents()

    def add_application(self):
        """Ajoute une candidature à la base de données."""
        dialog = AddEditApplicationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_applications()

    def delete_application(self, app_id):
        """Supprime une candidature de la base de données."""
        confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette candidature ?', QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM applications WHERE id = ?', (app_id,))
            conn.commit()
            conn.close()
            self.load_applications()

    def add_skill(self):
        """Ajoute une compétence à la base de données."""
        name, ok = QInputDialog.getText(self, 'Ajouter une compétence', 'Nom de la compétence:')
        if ok and name:
            level, ok = QInputDialog.getItem(self, 'Niveau de compétence', 'Sélectionnez le niveau:', ['Débutant', 'Intermédiaire', 'Expert'], 0, False)
            if ok:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO skills (name, level)
                    VALUES (?, ?)
                ''', (name, level))
                conn.commit()
                conn.close()
                self.load_skills()

    def delete_skill(self):
        """Supprime une compétence de la base de données."""
        selected_item = self.skills_list.currentItem()
        if selected_item:
            skill_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette compétence ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM skills WHERE id = ?', (skill_id,))
                conn.commit()
                conn.close()
                self.load_skills()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JobApplicationManager()
    window.show()
    sys.exit(app.exec_())