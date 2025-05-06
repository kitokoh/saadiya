import hashlib
import os
import re
import sqlite3
from datetime import datetime

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                            QLabel, QMessageBox, QHBoxLayout, QComboBox)

from mail.mail_in_to_in import Mailer1
from mail.mail_in_to_out import Mailer2
from translation import TranslatorManager

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
DB_PATH = os.path.join(user_data_dir, 'resources', 'data', 'leopardo.db')

class RegisterModule(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        
        # Initialisation du traducteur
        self.translator = QTranslator()
        self.init_language()
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        
        # Configuration de l'interface
        self.setup_ui()

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))
        self.setFixedSize(700, 500)
        
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Zone pour l'image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("resources/images/7.jpg").scaled(
            450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        form_layout.addWidget(self.username_input)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.password_input)

        # Champ de confirmation du mot de passe
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText(self.tr("Confirmer le mot de passe"))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.confirm_password_input)

        # Champ de saisie pour l'e-mail
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.email_input)

        # Champ "Licence" avec une liste déroulante
        self.licence_input = QComboBox(self)
        self.licence_input.addItems([
            self.tr("demo"),
            self.tr("annuelle"),
            self.tr("mensuelle"),
            self.tr("lifetime")
        ])
        self.licence_input.setCurrentText("demo")
        self.licence_input.setStyleSheet(self.combo_box_style())
        form_layout.addWidget(self.licence_input)

        # Bouton de création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setStyleSheet(self.button_style())
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Ajouter le layout du formulaire à la mise en page principale
        self.layout.addLayout(form_layout)

    def combo_box_style(self):
        """Retourne le style CSS pour la combo box."""
        return """
            QComboBox {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #007BFF;
                background-color: #F8F9FA;
                font-size: 14px;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            QComboBox:hover {
                border-color: #0056b3;
            }
            QComboBox:focus {
                border-color: #0056b3;
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.4);
            }
            QComboBox::drop-down {
                border: none;
                background-color: #FFFFFF;
            }
            QComboBox::down-arrow {
                image: url('resources/icons/telgrampng.png');
            }
        """

    def input_style(self):
        """Retourne le style CSS pour les champs de saisie."""
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #007BFF;
                background-color: #FFFFFF;
                font-size: 14px;
                color: #333333;
                margin-bottom: 20px;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }
            QLineEdit:focus {
                border: 1px solid #0056b3;
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.6);
            }
            QLineEdit:disabled {
                background-color: #f2f2f2;
                border: 1px solid #cccccc;
                color: #999999;
            }
            QLineEdit::placeholder {
                color: #888888;
                font-style: italic;
            }
        """

    def button_style(self):
        """Retourne le style CSS pour les boutons."""
        return """
            QPushButton {
                background: linear-gradient(45deg, #007BFF, #0056b3);
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                border-radius: 8px;
                border: 2px solid #0056b3;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: linear-gradient(45deg, #0056b3, #003d7a);
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background: linear-gradient(45deg, #003d7a, #002b56);
                transform: scale(0.98);
            }
            QPushButton:disabled {
                background: #cccccc;
                border: 2px solid #999999;
            }
        """

    def validate_email(self, email):
        """Vérifie si l'adresse e-mail est valide."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def hash_password(self, password):
        """Renvoie le hash SHA256 du mot de passe."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_inputs(self):
        """Valide tous les champs de saisie."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        email = self.email_input.text().strip()

        if not all([username, password, confirm_password, email]):
            QMessageBox.warning(
                self, 
                self.tr("⚠️ Warning - Missing Information"), 
                self.tr("Please fill in all required fields to proceed."))
            return False

        if password != confirm_password:
            QMessageBox.warning(
                self, 
                self.tr("⚠️ Error - Password Mismatch"), 
                self.tr("The passwords entered do not match. Please check and try again."))
            return False

        if len(username) < 3:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username Too Short"),
                self.tr("The username must be at least 3 characters long. Please enter a longer username."))
            return False

        if len(password) < 6:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Password Too Short"),
                self.tr("The password must be at least 6 characters long. Please choose a more secure password."))
            return False

        if not self.validate_email(email):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Invalid Email Address"),
                self.tr("The entered email address is invalid. Please enter a correct email address."))
            return False

        # Vérifier si l'utilisateur existe déjà
        if self.db.get_user(username):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username Already Taken"),
                self.tr("This username is already in use. Please choose a different one."))
            return False

        # Vérifier si l'email existe déjà
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Email Already Registered"),
                self.tr("This email address is already registered. Please use a different email."))
            return False

        return True

    def create_account(self):
        """Crée un nouveau compte utilisateur."""
        if not self.validate_inputs():
            return

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        email = self.email_input.text().strip()
        license_type = self.licence_input.currentText()

        try:
            # Ajouter l'utilisateur à la base de données
            hashed_password = self.hash_password(password)
            if not self.db.add_user(username, hashed_password, email):
                QMessageBox.warning(
                    self,
                    self.tr("⚠️ Error - Registration Failed"),
                    self.tr("An error occurred while creating your account. Please try again."))
                return

            # Envoi d'emails de confirmation
            mailer = Mailer1()
            mailer.send_email_to_user(user_email=email, email_type='mail4')
            
            mailer2 = Mailer2()
            mailer2.send_email(email_type="admin_message2", extra_subject=None)

            # Afficher le message de succès
            QMessageBox.information(
                self, 
                self.tr("🎉 Success - Welcome!"), 
                self.tr("Your account has been created successfully!\n\n"
                        "✨ You're now ready to explore our features and enhance your strategies.\n\n"
                        "👉 Log in now to begin your journey with us!"))
            
            self.clear_fields()
            self.accept()

        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("⚠️ Critical Error"),
                self.tr("An unexpected error occurred: {}").format(str(e)))

    def clear_fields(self):
        """Réinitialise les champs de saisie."""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()

    def switch_language(self, language):
        """Change la langue de l'interface."""
        translation_path = os.path.join(
            user_data_dir, 'resources', 'lang', language, 'ui', 'register_translated.qm')
        if os.path.exists(translation_path):
            self.translator.load(translation_path)
            QApplication.instance().installTranslator(self.translator)
            self.retranslate_ui()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur."""
        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO preferences (user_id, language) VALUES (1, ?)",
            (language,))
        self.db.conn.commit()

    def init_language(self):
        """Initialise la langue par défaut."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT language FROM preferences WHERE user_id = 1")
        result = cursor.fetchone()
        
        if result:
            self.switch_language(result[0])
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar', 'pt': 'pt'}
            selected_language = language_map.get(system_locale, 'en')
            self.switch_language(selected_language)

    def retranslate_ui(self):
        """Retraduit l'interface après un changement de langue."""
        # Implémentez la mise à jour des textes ici si nécessaire
        pass