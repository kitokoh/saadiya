import json
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from mail.mail import Mailer  # Importer la classe Mailer
import hashlib  # Pour le hachage des mots de passe
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
import os
class RegisterModule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        # Mise en page principale
        self.setWindowTitle(self.tr("Créer un compte"))
        self.setFixedSize(600, 500)
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Zone pour l'image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("resources/images/2.jpg").scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        # Champ de saisie pour l'e-mail (obligatoire)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText(self.tr("Adresse e-mail"))
        self.email_input.setStyleSheet(self.input_style())
        form_layout.addWidget(self.email_input)

        # Bouton de création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setStyleSheet(self.button_style())
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Ajouter le layout du formulaire à la mise en page principale
        self.layout.addLayout(form_layout)

        # Spacer pour centrer le formulaire
        form_layout.addStretch()
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/register_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/register_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/register_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/register_translated.qm")

        # Installer le traducteur pour appliquer la nouvelle langue
        QApplication.instance().installTranslator(self.translator)
        
            # Sauvegarder le choix de l'utilisateur
        self.save_language_choice(language)


        # Réappliquer la traduction sur tous les éléments visibles de l'interface
        self.retranslateUi()

    def save_language_choice(self, language):
        """Sauvegarde le choix de langue de l'utilisateur dans un fichier JSON."""
        preferences = {'language': language}
        with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'w') as f:
            json.dump(preferences, f)
    def retranslateUi(self):
        # """Recharge les textes traduits dans l'interface."""
        # self.setWindowTitle(self.tr('AI FB ROBOT Pro'))
        # # Mettez à jour ici tous les labels, boutons, menus, etc. avec self.tr()
        # # Par exemple, pour les actions du menu :
        # self.instance_action.setText(self.tr('Instance'))
        # self.media_action.setText(self.tr('Médias'))
        # self.group_action.setText(self.tr('Groupes'))
        # self.about_action.setText(self.tr('About'))
        # self.certificate_action.setText(self.tr('Certif'))
        # self.language_menu.setTitle(self.tr('Langue'))
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        # Vérifiez si le fichier de préférences existe
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')  # Par défaut à l'anglais si non trouvé
        else:
            # Obtenir le code de langue du système
            system_locale = QLocale.system().name()[:2]  # Par exemple: 'fr', 'en', 'tr', etc.

            # Dictionnaire pour mapper les codes de langue aux traductions
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def input_style(self):
        """Retourne le style CSS pour les champs de saisie."""
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #007BFF;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #0056b3;
            }
        """

    def button_style(self):
        """Retourne le style CSS pour le bouton."""
        return """
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """

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

    def validate_email(self, email):
        """Vérifie si l'adresse e-mail est valide."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def user_exists(self, username, email, user_data):
        """Vérifie si l'utilisateur ou l'e-mail existe déjà."""
        return any(user['username'] == username or user['email'] == email for user in user_data)

    def hash_password(self, password):
        """Renvoie le hash SHA256 du mot de passe."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        email = self.email_input.text().strip()

        if not username or not password or not confirm_password or not email:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez remplir tous les champs obligatoires."))
            return

        if password != confirm_password:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Les mots de passe ne correspondent pas."))
            return

        if len(username) < 3:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le nom d'utilisateur doit comporter au moins 3 caractères."))
            return

        if len(password) < 6:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le mot de passe doit comporter au moins 6 caractères."))
            return

        if not self.validate_email(email):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Adresse e-mail invalide."))
            return

        user_data = self.load_user_data()

        if self.user_exists(username, email, user_data):
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Ce nom d'utilisateur ou cette adresse e-mail est déjà pris."))
            return

        # Chiffrement du mot de passe
        hashed_password = self.hash_password(password)

        # Enregistrer le nouvel utilisateur avec e-mail et mot de passe haché
        user_data.append({"username": username, "password": hashed_password, "email": email})
        self.save_user_data(user_data)

        # Envoi d'un e-mail de confirmation
        mailer = Mailer()
        mailer.send_email(email, 'mail1')

        QMessageBox.information(self, self.tr("Succès"), self.tr("Compte créé avec succès ! Vous pouvez maintenant vous connecter."))
        self.clear_fields()
        self.close()  # Fermez le formulaire après la création réussie du compte

    def clear_fields(self):
        """Réinitialise les champs de saisie."""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()
