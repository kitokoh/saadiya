import hashlib
import json
import os
import re
import sys
import sqlite3
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox, QCheckBox, QDialog
)
from mail.mail_in_to_in import Mailer1
from mail.mail_in_to_out import Mailer2
from translation import TranslatorManager

# Chemin vers le répertoire de données utilisateur
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
db_path = os.path.join(user_data_dir, 'resources', 'data', 'users.db')

# Créer le répertoire de données si nécessaire
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table pour les utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            licence TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table pour les réseaux sociaux
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reseaux_sociaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialiser la base de données au démarrage
init_db()

import hashlib
import json
import os
import re
import sqlite3
from PyQt5.QtCore import Qt, QTranslator, QLocale, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox, QCheckBox, QDialog, QProgressBar, QApplication
)
from mail.mail_in_to_in import Mailer1
from mail.mail_in_to_out import Mailer2
from translation import TranslatorManager

# Chemin vers le répertoire de données utilisateur
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
db_path = os.path.join(user_data_dir, 'resources', 'data', 'users.db')

# Créer le répertoire de données si nécessaire
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table pour les utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            licence TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table pour les réseaux sociaux
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reseaux_sociaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialiser la base de données au démarrage
init_db()

class RegisterModule(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()

        # Mise en page principale
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))
        self.setFixedSize(700, 600)  # Taille ajustée pour accueillir plus de contenu
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Zone pour l'image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("resources/images/7.jpg").scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(self.image_label)

        # Mise en page pour le formulaire
        form_layout = QVBoxLayout()

        # Titre du formulaire
        title_label = QLabel(self.tr("Créer un compte"))
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        # Champ de saisie pour le nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet(self.input_style())
        self.username_input.textChanged.connect(self.validate_username)
        form_layout.addWidget(self.username_input)

        # Label d'erreur pour le nom d'utilisateur
        self.username_error_label = QLabel("", self)
        self.username_error_label.setStyleSheet("color: red; font-size: 12px;")
        form_layout.addWidget(self.username_error_label)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.textChanged.connect(self.validate_password)
        form_layout.addWidget(self.password_input)

        # Bouton pour afficher/masquer le mot de passe
        self.toggle_password_button = QPushButton("👁", self)
        self.toggle_password_button.setStyleSheet("font-size: 14px; border: none; background: transparent;")
        self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Layout pour le champ de mot de passe et le bouton
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        form_layout.addLayout(password_layout)

        # Label d'erreur pour le mot de passe
        self.password_error_label = QLabel("", self)
        self.password_error_label.setStyleSheet("color: red; font-size: 12px;")
        form_layout.addWidget(self.password_error_label)

        # Indicateur de force du mot de passe
        self.password_strength_label = QLabel("", self)
        self.password_strength_label.setStyleSheet("font-size: 12px;")
        form_layout.addWidget(self.password_strength_label)

        # Champ de confirmation du mot de passe
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())
        self.confirm_password_input.textChanged.connect(self.validate_confirm_password)
        form_layout.addWidget(self.confirm_password_input)

        # Label d'erreur pour la confirmation du mot de passe
        self.confirm_password_error_label = QLabel("", self)
        self.confirm_password_error_label.setStyleSheet("color: red; font-size: 12px;")
        form_layout.addWidget(self.confirm_password_error_label)

        # Champ de saisie pour l'e-mail
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setStyleSheet(self.input_style())
        self.email_input.textChanged.connect(self.validate_email)
        form_layout.addWidget(self.email_input)

        # Label d'erreur pour l'e-mail
        self.email_error_label = QLabel("", self)
        self.email_error_label.setStyleSheet("color: red; font-size: 12px;")
        form_layout.addWidget(self.email_error_label)

        # Champ "Licence" avec une liste déroulante
        self.licence_input = QComboBox(self)
        self.licence_input.addItems([self.tr("demo"), self.tr("annuelle"), self.tr("mensuelle"), self.tr("lifetime")])
        self.licence_input.setCurrentText("demo")
        self.licence_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.licence_input)

        # Cases à cocher pour les réseaux sociaux
        self.social_media_checkboxes = {
            "Facebook": QCheckBox("Facebook", self),
            "WhatsApp": QCheckBox("WhatsApp", self),
            "Instagram": QCheckBox("Instagram", self),
            "LinkedIn": QCheckBox("LinkedIn", self),
            "Reddit": QCheckBox("Reddit", self),
            "YouTube": QCheckBox("YouTube", self),
            "Blog": QCheckBox("Blog", self)
        }

        for checkbox in self.social_media_checkboxes.values():
            form_layout.addWidget(checkbox)

        # Case à cocher pour les conditions d'utilisation
        self.terms_checkbox = QCheckBox(self.tr("I agree to the terms and conditions."), self)
        form_layout.addWidget(self.terms_checkbox)

        # Lien vers les conditions d'utilisation
        self.terms_link = QLabel(self.tr('<a href="#">Read terms and conditions</a>'), self)
        self.terms_link.setOpenExternalLinks(True)
        self.terms_link.setStyleSheet("color: blue; text-decoration: underline; font-size: 12px;")
        form_layout.addWidget(self.terms_link)

        # Bouton de création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setStyleSheet(self.button_style())
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Barre de progression pour le chargement
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        form_layout.addWidget(self.progress_bar)

        # Lien vers la page de connexion
        self.login_link = QLabel(self.tr('<a href="#">Already have an account? Log in</a>'), self)
        self.login_link.setOpenExternalLinks(False)
        self.login_link.setStyleSheet("color: blue; text-decoration: underline; font-size: 12px;")
        self.login_link.linkActivated.connect(self.open_login_page)
        form_layout.addWidget(self.login_link)

        # Ajouter le layout du formulaire à la mise en page principale
        self.layout.addLayout(form_layout)

    # ... (autres méthodes comme input_style, button_style, validate_email, hash_password, etc.)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("👁")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")

    def update_password_strength(self):
        password = self.password_input.text().strip()
        strength = self.calculate_password_strength(password)
        self.password_strength_label.setText(f"Password Strength: {strength}")
        self.password_strength_label.setStyleSheet(f"color: {self.get_strength_color(strength)}; font-size: 12px;")

    def calculate_password_strength(self, password):
        if len(password) < 6:
            return "Weak"
        elif len(password) < 10:
            return "Medium"
        else:
            return "Strong"

    def get_strength_color(self, strength):
        if strength == "Weak":
            return "red"
        elif strength == "Medium":
            return "orange"
        else:
            return "green"

    def open_login_page(self):
        self.close()  # Fermer la fenêtre d'inscription
        # Ouvrir la fenêtre de connexion (à implémenter)

    def show_toast(self, message, color="green"):
        toast = QLabel(message, self)
        toast.setStyleSheet(f"background-color: {color}; color: white; padding: 10px; border-radius: 5px;")
        toast.setAlignment(Qt.AlignCenter)
        toast.setGeometry(50, 50, 200, 50)
        toast.show()

        # Fermer la notification après 3 secondes
        QTimer.singleShot(3000, toast.hide)

    # ... (autres méthodes comme create_account, clear_fields, etc.)



    def validate_username(self):
        username = self.username_input.text().strip()
        if len(username) < 3:
            self.username_error_label.setText(self.tr("Username must be at least 3 characters long."))
        else:
            self.username_error_label.setText("")


    def update_password_strength(self):
        password = self.password_input.text().strip()
        strength = self.calculate_password_strength(password)
        self.password_strength_label.setText(f"Password Strength: {strength}")
        self.password_strength_label.setStyleSheet(f"color: {self.get_strength_color(strength)}; font-size: 12px;")

    def calculate_password_strength(self, password):
        if len(password) < 6:
            return "Weak"
        elif len(password) < 10:
            return "Medium"
        else:
            return "Strong"

    def get_strength_color(self, strength):
        if strength == "Weak":
            return "red"
        elif strength == "Medium":
            return "orange"
        else:
             return "green"




    def validate_password(self):
        password = self.password_input.text().strip()
        if len(password) < 6:
            self.password_error_label.setText(self.tr("Password must be at least 6 characters long."))
        else:
            self.password_error_label.setText("")

    def validate_confirm_password(self):
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        if password != confirm_password:
            self.password_error_label.setText(self.tr("Passwords do not match."))
        else:
            self.password_error_label.setText("")

    def validate_email(self):
        email = self.email_input.text().strip()
        if not self.validate_email_format(email):
            self.email_error_label.setText(self.tr("Invalid email address."))
        else:
            self.email_error_label.setText("")
            
                    
    def input_style(self):
        return """
            QLineEdit, QComboBox {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #007BFF;
                background-color: #FFFFFF;
                font-size: 14px;
                color: #333333;
                margin-bottom: 20px;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0056b3;
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.6);
            }
            QLineEdit::placeholder {
                color: #888888;
                font-style: italic;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background: linear-gradient(45deg, #007BFF, #0056b3);
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 8px;
                border: 2px solid #0056b3;
                transition: background-color 0.3s, transform 0.2s;
            }
            QPushButton:hover {
                background: linear-gradient(45deg, #0056b3, #003d7a);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: linear-gradient(45deg, #003d7a, #002b56);
                transform: scale(0.98);
            }
        """

    def validate_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        email = self.email_input.text().strip()
        licence = self.licence_input.currentText()

        if not username or not password or not confirm_password or not email:
            QMessageBox.warning(self, self.tr("⚠️ Warning - Missing Information"), self.tr("Please fill in all required fields to proceed."))
            return

        if password != confirm_password:
            QMessageBox.warning(self, self.tr("⚠️ Error - Password Mismatch"), self.tr("The passwords entered do not match. Please check and try again."))
            return

        if len(username) < 3:
            QMessageBox.warning(self, self.tr("⚠️ Error - Username Too Short"), self.tr("The username must be at least 3 characters long. Please enter a longer username."))
            return

        if len(password) < 6:
            QMessageBox.warning(self, self.tr("⚠️ Error - Password Too Short"), self.tr("The password must be at least 6 characters long. Please choose a more secure password."))
            return

        if not self.validate_email(email):
            QMessageBox.warning(self, self.tr("⚠️ Error - Invalid Email Address"), self.tr("The entered email address is invalid. Please enter a correct email address."))
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifier si l'utilisateur ou l'e-mail existe déjà
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            QMessageBox.warning(self, self.tr("⚠️ Error - Username or Email Already Taken"), self.tr("This username or email address is already in use. Please choose a different one."))
            conn.close()
            return

        # Enregistrer le nouvel utilisateur
        hashed_password = self.hash_password(password)
        cursor.execute("INSERT INTO users (username, password, email, licence) VALUES (?, ?, ?, ?)",
                       (username, hashed_password, email, licence))
        user_id = cursor.lastrowid

        # Enregistrer les réseaux sociaux sélectionnés
        for name, checkbox in self.social_media_checkboxes.items():
            if checkbox.isChecked():
                cursor.execute("INSERT INTO reseaux_sociaux (user_id, name, description) VALUES (?, ?, ?)",
                               (user_id, name, f"Description for {name}"))

        conn.commit()
        conn.close()

        # Envoi d'un e-mail de confirmation
        mailer = Mailer1()
        mailer.send_email_to_user(user_email=email, email_type='mail4')
        mailer2 = Mailer2()
        mailer2.send_email(email_type="admin_message2", extra_subject=None)

        QMessageBox.information(self, self.tr("🎉 Success - Welcome!"), self.tr("Your account has been created successfully!\n\n✨ You’re now ready to explore our features and enhance your strategies.\n\n👉 Log in now to begin your journey with us!"))
        self.clear_fields()
        self.accept()

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()
        for checkbox in self.social_media_checkboxes.values():
            checkbox.setChecked(False)

    def init_language(self):
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar', 'pt': 'pt'}
            selected_language = language_map.get(system_locale, 'en')
        self.switch_language(selected_language)

    def switch_language(self, language):
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang', 'en_US', 'ui', 'register_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang', 'fr_FR', 'ui', 'register_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang', 'tr_TR', 'ui', 'register_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang', 'ar_SA', 'ui', 'register_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang', 'pt_BR', 'ui', 'register_translated.qm'))
        QApplication.instance().installTranslator(self.translator)
        self.save_language_choice(language)
        self.retranslateUi()

    def save_language_choice(self, language):
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)



    def load_user_data(self):
        """Charge les données des utilisateurs depuis le fichier JSON."""
        try:
            with open(os.path.join(user_data_dir, 'resources', 'data','users.json'), 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_user_data(self, user_data):
        """Enregistre les données des utilisateurs dans le fichier JSON."""
        with open(os.path.join(user_data_dir, 'resources', 'data','users.json'), 'w') as file:
            json.dump(user_data, file, indent=4)  # Ajouter un indent pour plus de lisibilité


    def user_exists(self, username, email, user_data):
        """Vérifie si l'utilisateur ou l'e-mail existe déjà."""
        return any(user['username'] == username or user['email'] == email for user in user_data)
    def retranslateUi(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterModule()
    window.show()
    sys.exit(app.exec_())

    
