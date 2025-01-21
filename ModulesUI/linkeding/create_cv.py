import sys
import sqlite3
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QMessageBox, QDialog, QTabWidget, QTextEdit, QComboBox, QProgressBar,
    QFileDialog, QListWidget, QFormLayout, QGroupBox, QDateEdit, QInputDialog, QCheckBox, QColorDialog, QFontDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QColor
import logging
from fpdf import FPDF
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication, QMainWindow, QVBoxLayout, QWidget
# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Génération d'une clé de chiffrement (à stocker de manière sécurisée en production)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

# Chemin de la base de données
ROAMING_PATH = os.getenv('APPDATA')
DB_PATH = os.path.join(ROAMING_PATH, 'Saadiya Resources', 'cv_manager.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connexion à la base de données SQLite
def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL,
            font TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS educations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            degree TEXT NOT NULL,
            institution TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            level TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hobbies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS references (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            company TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (cv_id) REFERENCES cvs (id)
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
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QDateEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate

class AddEditExperienceDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier une expérience professionnelle."""
    def __init__(self, parent=None, experience_id=None, cv_id=None):
        super().__init__(parent)
        self.experience_id = experience_id
        self.cv_id = cv_id
        self.setWindowTitle('Ajouter/Modifier une Expérience' if not experience_id else 'Modifier une Expérience')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations de l'expérience
        form_layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Titre du poste')
        form_layout.addRow('Titre:', self.title_input)

        self.company_input = QLineEdit(self)
        self.company_input.setPlaceholderText('Nom de l\'entreprise')
        form_layout.addRow('Entreprise:', self.company_input)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de début:', self.start_date_input)

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de fin:', self.end_date_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText('Description de l\'expérience')
        form_layout.addRow('Description:', self.description_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_experience)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie une expérience, charger les données existantes
        if self.experience_id:
            self.load_experience_data()

    def load_experience_data(self):
        """Remplit les champs avec les données de l'expérience existante."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM experiences WHERE id = ?', (self.experience_id,))
        experience = cursor.fetchone()
        conn.close()

        if experience:
            self.title_input.setText(experience[2])
            self.company_input.setText(experience[3])
            self.start_date_input.setDate(QDate.fromString(experience[4], Qt.ISODate))
            self.end_date_input.setDate(QDate.fromString(experience[5], Qt.ISODate))
            self.description_input.setText(experience[6])

    def save_experience(self):
        """Enregistre l'expérience dans la base de données."""
        title = self.title_input.text()
        company = self.company_input.text()
        start_date = self.start_date_input.date().toString(Qt.ISODate)
        end_date = self.end_date_input.date().toString(Qt.ISODate)
        description = self.description_input.toPlainText()

        if not title or not company or not start_date or not end_date or not description:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.experience_id:
            # Mettre à jour l'expérience existante
            cursor.execute('''
                UPDATE experiences SET title = ?, company = ?, start_date = ?, end_date = ?, description = ?
                WHERE id = ?
            ''', (title, company, start_date, end_date, description, self.experience_id))
        else:
            # Ajouter une nouvelle expérience
            cursor.execute('''
                INSERT INTO experiences (cv_id, title, company, start_date, end_date, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.cv_id, title, company, start_date, end_date, description))

        conn.commit()
        conn.close()
        self.accept()
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3

class AddEditHobbyDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier un hobby."""
    def __init__(self, parent=None, hobby_id=None, cv_id=None):
        super().__init__(parent)
        self.hobby_id = hobby_id
        self.cv_id = cv_id
        self.setWindowTitle('Ajouter/Modifier un Hobby' if not hobby_id else 'Modifier un Hobby')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations du hobby
        form_layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Nom du hobby')
        form_layout.addRow('Nom:', self.name_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_hobby)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie un hobby, charger les données existantes
        if self.hobby_id:
            self.load_hobby_data()

    def load_hobby_data(self):
        """Remplit les champs avec les données du hobby existant."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hobbies WHERE id = ?', (self.hobby_id,))
        hobby = cursor.fetchone()
        conn.close()

        if hobby:
            self.name_input.setText(hobby[2])

    def save_hobby(self):
        """Enregistre le hobby dans la base de données."""
        name = self.name_input.text()

        if not name:
            QMessageBox.warning(self, 'Erreur', 'Le champ doit être rempli.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.hobby_id:
            # Mettre à jour le hobby existant
            cursor.execute('''
                UPDATE hobbies SET name = ?
                WHERE id = ?
            ''', (name, self.hobby_id))
        else:
            # Ajouter un nouveau hobby
            cursor.execute('''
                INSERT INTO hobbies (cv_id, name)
                VALUES (?, ?)
            ''', (self.cv_id, name))

        conn.commit()
        conn.close()
        self.accept()


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDateEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, Qt
import sqlite3

class AddEditProjectDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier un projet."""
    def __init__(self, parent=None, project_id=None, cv_id=None):
        super().__init__(parent)
        self.project_id = project_id
        self.cv_id = cv_id
        self.setWindowTitle('Ajouter/Modifier un Projet' if not project_id else 'Modifier un Projet')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations du projet
        form_layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Titre du projet')
        form_layout.addRow('Titre:', self.title_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText('Description du projet')
        form_layout.addRow('Description:', self.description_input)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de début:', self.start_date_input)

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de fin:', self.end_date_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_project)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie un projet, charger les données existantes
        if self.project_id:
            self.load_project_data()

    def load_project_data(self):
        """Remplit les champs avec les données du projet existant."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (self.project_id,))
        project = cursor.fetchone()
        conn.close()

        if project:
            self.title_input.setText(project[2])
            self.description_input.setText(project[3])
            self.start_date_input.setDate(QDate.fromString(project[4], Qt.ISODate))
            self.end_date_input.setDate(QDate.fromString(project[5], Qt.ISODate))

    def save_project(self):
        """Enregistre le projet dans la base de données."""
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        start_date = self.start_date_input.date().toString(Qt.ISODate)
        end_date = self.end_date_input.date().toString(Qt.ISODate)

        if not title or not description or not start_date or not end_date:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.project_id:
            # Mettre à jour le projet existant
            cursor.execute('''
                UPDATE projects SET title = ?, description = ?, start_date = ?, end_date = ?
                WHERE id = ?
            ''', (title, description, start_date, end_date, self.project_id))
        else:
            # Ajouter un nouveau projet
            cursor.execute('''
                INSERT INTO projects (cv_id, title, description, start_date, end_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.cv_id, title, description, start_date, end_date))

        conn.commit()
        conn.close()
        self.accept()
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDateEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate

class AddEditEducationDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier une formation."""
    def __init__(self, parent=None, education_id=None, cv_id=None):
        super().__init__(parent)
        self.education_id = education_id
        self.cv_id = cv_id
        self.setWindowTitle('Ajouter/Modifier une Formation' if not education_id else 'Modifier une Formation')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations de la formation
        form_layout = QFormLayout()

        self.degree_input = QLineEdit(self)
        self.degree_input.setPlaceholderText('Diplôme obtenu')
        form_layout.addRow('Diplôme:', self.degree_input)

        self.institution_input = QLineEdit(self)
        self.institution_input.setPlaceholderText('Établissement')
        form_layout.addRow('Établissement:', self.institution_input)

        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de début:', self.start_date_input)

        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())
        form_layout.addRow('Date de fin:', self.end_date_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_education)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie une formation, charger les données existantes
        if self.education_id:
            self.load_education_data()

    def load_education_data(self):
        """Remplit les champs avec les données de la formation existante."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM educations WHERE id = ?', (self.education_id,))
        education = cursor.fetchone()
        conn.close()

        if education:
            self.degree_input.setText(education[2])
            self.institution_input.setText(education[3])
            self.start_date_input.setDate(QDate.fromString(education[4], Qt.ISODate))
            self.end_date_input.setDate(QDate.fromString(education[5], Qt.ISODate))

    def save_education(self):
        """Enregistre la formation dans la base de données."""
        degree = self.degree_input.text()
        institution = self.institution_input.text()
        start_date = self.start_date_input.date().toString(Qt.ISODate)
        end_date = self.end_date_input.date().toString(Qt.ISODate)

        if not degree or not institution or not start_date or not end_date:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.education_id:
            # Mettre à jour la formation existante
            cursor.execute('''
                UPDATE educations SET degree = ?, institution = ?, start_date = ?, end_date = ?
                WHERE id = ?
            ''', (degree, institution, start_date, end_date, self.education_id))
        else:
            # Ajouter une nouvelle formation
            cursor.execute('''
                INSERT INTO educations (cv_id, degree, institution, start_date, end_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.cv_id, degree, institution, start_date, end_date))

        conn.commit()
        conn.close()
        self.accept()

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
)

class AddEditSkillDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier une compétence."""
    def __init__(self, parent=None, skill_id=None, cv_id=None):
        super().__init__(parent)
        self.skill_id = skill_id
        self.cv_id = cv_id
        self.setWindowTitle('Ajouter/Modifier une Compétence' if not skill_id else 'Modifier une Compétence')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations de la compétence
        form_layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Nom de la compétence')
        form_layout.addRow('Nom:', self.name_input)

        self.level_input = QComboBox(self)
        self.level_input.addItems(['Débutant', 'Intermédiaire', 'Expert'])
        form_layout.addRow('Niveau:', self.level_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_skill)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie une compétence, charger les données existantes
        if self.skill_id:
            self.load_skill_data()

    def load_skill_data(self):
        """Remplit les champs avec les données de la compétence existante."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills WHERE id = ?', (self.skill_id,))
        skill = cursor.fetchone()
        conn.close()

        if skill:
            self.name_input.setText(skill[2])
            self.level_input.setCurrentText(skill[3])

    def save_skill(self):
        """Enregistre la compétence dans la base de données."""
        name = self.name_input.text()
        level = self.level_input.currentText()

        if not name or not level:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.skill_id:
            # Mettre à jour la compétence existante
            cursor.execute('''
                UPDATE skills SET name = ?, level = ?
                WHERE id = ?
            ''', (name, level, self.skill_id))
        else:
            # Ajouter une nouvelle compétence
            cursor.execute('''
                INSERT INTO skills (cv_id, name, level)
                VALUES (?, ?, ?)
            ''', (self.cv_id, name, level))

        conn.commit()
        conn.close()
        self.accept()
class CVManagerApp(QMainWindow):
    """Application principale pour gérer les CV."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Gestionnaire de CV - Saadiya')
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

        # Onglet des CV
        self.cv_tab = QWidget()
        self.init_cv_tab()
        self.tab_widget.addTab(self.cv_tab, 'CV')

        # Onglet des Expériences
        self.experiences_tab = QWidget()
        self.init_experiences_tab()
        self.tab_widget.addTab(self.experiences_tab, 'Expériences')

        # Onglet des Formations
        self.educations_tab = QWidget()
        self.init_educations_tab()
        self.tab_widget.addTab(self.educations_tab, 'Formations')

        # Onglet des Compétences
        self.skills_tab = QWidget()
        self.init_skills_tab()
        self.tab_widget.addTab(self.skills_tab, 'Compétences')

        # Onglet des Loisirs
        self.hobbies_tab = QWidget()
        self.init_hobbies_tab()
        self.tab_widget.addTab(self.hobbies_tab, 'Loisirs')

        # Onglet des Projets
        self.projects_tab = QWidget()
        self.init_projects_tab()
        self.tab_widget.addTab(self.projects_tab, 'Projets')

        # Onglet des Références
        self.references_tab = QWidget()
        self.init_references_tab()
        self.tab_widget.addTab(self.references_tab, 'Références')

    def init_cv_tab(self):
        """Initialise l'onglet des CV."""
        layout = QVBoxLayout()

        # Formulaire de création de CV
        form_layout = QFormLayout()

        self.first_name_input = QLineEdit(self)
        form_layout.addRow('Prénom:', self.first_name_input)

        self.last_name_input = QLineEdit(self)
        form_layout.addRow('Nom:', self.last_name_input)

        self.address_input = QLineEdit(self)
        form_layout.addRow('Adresse:', self.address_input)

        self.phone_input = QLineEdit(self)
        form_layout.addRow('Téléphone:', self.phone_input)

        self.email_input = QLineEdit(self)
        form_layout.addRow('E-mail:', self.email_input)

        self.model_input = QComboBox(self)
        self.model_input.addItems(['Modèle 1', 'Modèle 2', 'Modèle 3'])
        form_layout.addRow('Modèle de CV:', self.model_input)

        self.color_input = QPushButton('Choisir une couleur', self)
        self.color_input.clicked.connect(self.choose_color)
        form_layout.addRow('Couleur:', self.color_input)

        self.font_input = QPushButton('Choisir une police', self)
        self.font_input.clicked.connect(self.choose_font)
        form_layout.addRow('Police:', self.font_input)

        layout.addLayout(form_layout)

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        save_button = QPushButton('Enregistrer le CV', self)
        save_button.clicked.connect(self.save_cv)
        buttons_layout.addWidget(save_button)

        export_button = QPushButton('Exporter en PDF', self)
        export_button.clicked.connect(self.export_cv_to_pdf)
        buttons_layout.addWidget(export_button)

        layout.addLayout(buttons_layout)

        self.cv_tab.setLayout(layout)

    def choose_color(self):
        """Ouvre un dialogue pour choisir une couleur."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setStyleSheet(f"background-color: {color.name()};")

    def choose_font(self):
        """Ouvre un dialogue pour choisir une police."""
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_input.setFont(font)

    def save_cv(self):
        """Enregistre le CV dans la base de données."""
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        model = self.model_input.currentText()
        color = self.color_input.palette().button().color().name()
        font = self.font_input.font().toString()

        if not first_name or not last_name or not address or not phone or not email:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cvs (first_name, last_name, address, phone, email, model, color, font)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, address, phone, email, model, color, font))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Succès', 'Le CV a été enregistré avec succès.')

    def export_cv_to_pdf(self):
        """Exporte le CV en PDF."""
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        model = self.model_input.currentText()
        color = self.color_input.palette().button().color().name()
        font = self.font_input.font()

        if not first_name or not last_name or not address or not phone or not email:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        # Création du PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"{first_name} {last_name}", ln=True, align='C')
        pdf.cell(200, 10, txt=address, ln=True, align='C')
        pdf.cell(200, 10, txt=phone, ln=True, align='C')
        pdf.cell(200, 10, txt=email, ln=True, align='C')

        # Enregistrement du PDF
        save_path, _ = QFileDialog.getSaveFileName(self, 'Enregistrer le CV', '', 'PDF Files (*.pdf)')
        if save_path:
            pdf.output(save_path)
            QMessageBox.information(self, 'Succès', f'Le CV a été exporté sous {save_path}')

    def load_experiences(self):
        """Charge les expériences depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM experiences')
        experiences = cursor.fetchall()
        conn.close()

        self.experiences_list.clear()
        for exp in experiences:
            item = QListWidgetItem(f"{exp[2]} chez {exp[3]} ({exp[4]} - {exp[5]})")
            item.setData(Qt.UserRole, exp[0])  # Stocker l'ID de l'expérience
            self.experiences_list.addItem(item)

    def add_experience(self):
        """Ajoute une expérience à la base de données."""
        dialog = AddEditExperienceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_experiences()

    def delete_experience(self):
        """Supprime une expérience de la base de données."""
        selected_item = self.experiences_list.currentItem()
        if selected_item:
            exp_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette expérience ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM experiences WHERE id = ?', (exp_id,))
                conn.commit()
                conn.close()
                self.load_experiences()

    def load_educations(self):
        """Charge les formations depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM educations')
        educations = cursor.fetchall()
        conn.close()

        self.educations_list.clear()
        for edu in educations:
            item = QListWidgetItem(f"{edu[2]} à {edu[3]} ({edu[4]} - {edu[5]})")
            item.setData(Qt.UserRole, edu[0])  # Stocker l'ID de la formation
            self.educations_list.addItem(item)

    def add_education(self):
        """Ajoute une formation à la base de données."""
        dialog = AddEditEducationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_educations()

    def delete_education(self):
        """Supprime une formation de la base de données."""
        selected_item = self.educations_list.currentItem()
        if selected_item:
            edu_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette formation ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM educations WHERE id = ?', (edu_id,))
                conn.commit()
                conn.close()
                self.load_educations()

    def load_skills(self):
        """Charge les compétences depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM skills')
        skills = cursor.fetchall()
        conn.close()

        self.skills_list.clear()
        for skill in skills:
            item = QListWidgetItem(f"{skill[2]} ({skill[3]})")
            item.setData(Qt.UserRole, skill[0])  # Stocker l'ID de la compétence
            self.skills_list.addItem(item)

    def add_skill(self):
        """Ajoute une compétence à la base de données."""
        dialog = AddEditSkillDialog(self)
        if dialog.exec_() == QDialog.Accepted:
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

    def load_hobbies(self):
        """Charge les loisirs depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM hobbies')
        hobbies = cursor.fetchall()
        conn.close()

        self.hobbies_list.clear()
        for hobby in hobbies:
            item = QListWidgetItem(hobby[2])
            item.setData(Qt.UserRole, hobby[0])  # Stocker l'ID du loisir
            self.hobbies_list.addItem(item)

    def add_hobby(self):
        """Ajoute un loisir à la base de données."""
        dialog = AddEditHobbyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_hobbies()

    def delete_hobby(self):
        """Supprime un loisir de la base de données."""
        selected_item = self.hobbies_list.currentItem()
        if selected_item:
            hobby_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer ce loisir ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM hobbies WHERE id = ?', (hobby_id,))
                conn.commit()
                conn.close()
                self.load_hobbies()

    def load_projects(self):
        """Charge les projets depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects')
        projects = cursor.fetchall()
        conn.close()

        self.projects_list.clear()
        for project in projects:
            item = QListWidgetItem(f"{project[2]} ({project[4]} - {project[5]})")
            item.setData(Qt.UserRole, project[0])  # Stocker l'ID du projet
            self.projects_list.addItem(item)

    def add_project(self):
        """Ajoute un projet à la base de données."""
        dialog = AddEditProjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_projects()

    def delete_project(self):
        """Supprime un projet de la base de données."""
        selected_item = self.projects_list.currentItem()
        if selected_item:
            project_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer ce projet ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
                conn.commit()
                conn.close()
                self.load_projects()

    def load_references(self):
        """Charge les références depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM references')
        references = cursor.fetchall()
        conn.close()

        self.references_list.clear()
        for ref in references:
            item = QListWidgetItem(f"{ref[2]} ({ref[3]})")
            item.setData(Qt.UserRole, ref[0])  # Stocker l'ID de la référence
            self.references_list.addItem(item)

    def add_reference(self):
        """Ajoute une référence à la base de données."""
        dialog = AddEditReferenceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_references()

    def delete_reference(self):
        """Supprime une référence de la base de données."""
        selected_item = self.references_list.currentItem()
        if selected_item:
            ref_id = selected_item.data(Qt.UserRole)
            confirm = QMessageBox.question(self, 'Confirmer', 'Êtes-vous sûr de vouloir supprimer cette référence ?', QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM references WHERE id = ?', (ref_id,))
                conn.commit()
                conn.close()
                self.load_references()



from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
)

class AddEditReferenceDialog(QDialog):
    """Boîte de dialogue pour ajouter ou modifier une référence."""
    def __init__(self, parent=None, reference_id=None):
        super().__init__(parent)
        self.reference_id = reference_id
        self.setWindowTitle('Ajouter/Modifier une Référence' if not reference_id else 'Modifier une Référence')
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Formulaire pour saisir les informations de la référence
        form_layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Nom de la référence')
        form_layout.addRow('Nom:', self.name_input)

        self.position_input = QLineEdit(self)
        self.position_input.setPlaceholderText('Poste occupé')
        form_layout.addRow('Poste:', self.position_input)

        self.company_input = QLineEdit(self)
        self.company_input.setPlaceholderText('Entreprise')
        form_layout.addRow('Entreprise:', self.company_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText('Téléphone')
        form_layout.addRow('Téléphone:', self.phone_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('E-mail')
        form_layout.addRow('E-mail:', self.email_input)

        layout.addLayout(form_layout)

        # Bouton pour enregistrer
        save_button = QPushButton('Enregistrer', self)
        save_button.clicked.connect(self.save_reference)
        layout.addWidget(save_button)

        self.setLayout(layout)

        # Si on modifie une référence, charger les données existantes
        if self.reference_id:
            self.load_reference_data()

    def load_reference_data(self):
        """Remplit les champs avec les données de la référence existante."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM references WHERE id = ?', (self.reference_id,))
        reference = cursor.fetchone()
        conn.close()

        if reference:
            self.name_input.setText(reference[2])
            self.position_input.setText(reference[3])
            self.company_input.setText(reference[4])
            self.phone_input.setText(reference[5])
            self.email_input.setText(reference[6])

    def save_reference(self):
        """Enregistre la référence dans la base de données."""
        name = self.name_input.text()
        position = self.position_input.text()
        company = self.company_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if not name or not position or not company or not phone or not email:
            QMessageBox.warning(self, 'Erreur', 'Tous les champs doivent être remplis.')
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if self.reference_id:
            # Mettre à jour la référence existante
            cursor.execute('''
                UPDATE references SET name = ?, position = ?, company = ?, phone = ?, email = ?
                WHERE id = ?
            ''', (name, position, company, phone, email, self.reference_id))
        else:
            # Ajouter une nouvelle référence
            cursor.execute('''
                INSERT INTO references (name, position, company, phone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, position, company, phone, email))

        conn.commit()
        conn.close()
        self.accept()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CVManagerApp()
    window.show()
    sys.exit(app.exec_())