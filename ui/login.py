import json
import os
import hashlib  # Pour le hachage des mots de passe
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSignal
from home import HomePage
from .carousel import CarouselWidget  # Assurez-vous que CarouselWidget est importé
from .register import RegisterModule
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class LoginModule(QWidget):
    # Définir un signal pour indiquer que la connexion a réussi
    connection_successful = pyqtSignal()

    def __init__(self, parent=None):
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        super().__init__(parent)
        # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        # Mise en page principale
        self.layout = QHBoxLayout(self)
        self.setStyleSheet("background-color: #F5F5F5;")  # Fond général en gris clair

        # Carrousel d'images
        self.carousel_widget = CarouselWidget()
        self.layout.addWidget(self.carousel_widget)

        # Section du formulaire de connexion
        form_frame = QFrame(self)
        form_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        form_layout = QVBoxLayout(form_frame)

        # Titre du formulaire
        title_label = QLabel(self.tr("Connexion à Nova360Pro"))
        title_label.setFont(QFont("Roboto", 20, QFont.Bold))  # Police moderne
        title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title_label)

        # Champ de saisie pour le nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet("""
            padding: 12px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 14px;
            transition: transform 0.2s ease-in-out;
        """)
        form_layout.addWidget(self.username_input)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 12px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 14px;
            transition: transform 0.2s ease-in-out;
        """)
        form_layout.addWidget(self.password_input)

        # Bouton de connexion
        self.login_button = QPushButton(self.tr("Se connecter"), self)
        self.login_button.setIcon(QIcon("resources/images/login.jpg"))  # Ajout d'une icône
        self.login_button.setStyleSheet("""
            background-color: #007BFF;
            color: white;
            padding: 12px;
            border-radius: 55px;
            font-size: 18px;
            transition: background-color 0.3s ease;
        """)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet(self.login_button.styleSheet() + """
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)

        # Lien pour mot de passe oublié
        self.forgot_password_button = QPushButton(self.tr("Mot de passe oublié ?"), self)
        self.forgot_password_button.setStyleSheet("""
            background: transparent;
            color: #007BFF;
            border: none;
            font-size: 12px;
            margin-top: 10px;
        """)
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.reset_password)
        form_layout.addWidget(self.forgot_password_button)

        # Lien pour créer un compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setIcon(QIcon("resources/icons/facebook-icon-png-745.png"))  # Ajout d'une icône pour le bouton inscription
        self.signup_button.setStyleSheet("""
            background-color: #28A745;
            color: white;
            padding: 12px;
            border-radius: 5px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        """)
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.setStyleSheet(self.signup_button.styleSheet() + """
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Espacement entre les widgets
        form_layout.setSpacing(15)

        # Ajouter le formulaire à la mise en page principale
        self.layout.addWidget(form_frame)

        # Variables de contrôle
        self.failed_attempts = 0
        self.max_attempts = 3  # Limite d'essais
    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load("resources/lang/en_US/ui/login_translated.qm")
        elif language == "fr":
            self.translator.load("resources/lang/fr_FR/ui/login_translated.qm")
        elif language == "tr":
            self.translator.load("resources/lang/tr_TR/ui/login_translated.qm")
        elif language == "ar":
            self.translator.load("resources/lang/ar_AR/ui/login_translated.qm")

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
        """Recharge les textes traduits dans l'interface."""
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

    def load_user_data(self):
        """Charge les données des utilisateurs depuis le fichier JSON."""
        try:
            with open(os.path.join(user_data_dir, 'resources', 'data','users.json'), 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.critical(self, self.tr("Erreur"), self.tr("Impossible de charger les données des utilisateurs."))
            return []

    def hash_password(self, password):
        """Hache le mot de passe avec SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(self, username, password):
        """Vérifie la validité des entrées de l'utilisateur."""
        if not username or not password:
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez remplir tous les champs."))
            return False

        if len(username) < 3:
            self.username_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le nom d'utilisateur doit comporter au moins 3 caractères."))
            return False
        else:
            self.username_input.setStyleSheet("border: 1px solid #ddd;")

        if len(password) < 6:
            self.password_input.setStyleSheet("border: 1px solid red;")
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Le mot de passe doit comporter au moins 6 caractères."))
            return False
        else:
            self.password_input.setStyleSheet("border: 1px solid #ddd;")

        return True

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not self.validate_input(username, password):
            return

        user_data = self.load_user_data()

        # Vérification des identifiants
        user_found = next((user for user in user_data if user['username'] == username), None)
        if user_found and user_found['password'] == self.hash_password(password):
            
            self.connection_successful.emit()  # Émettre le signal de réussite

            QMessageBox.information(self, self.tr("Connexion réussie"), self.tr("Bienvenue, {}!").format(username))
            self.failed_attempts = 0  # Réinitialiser le compteur d'échecs

            self.close()
        else:
            self.failed_attempts += 1
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Nom d'utilisateur ou mot de passe incorrect."))
            if self.failed_attempts >= self.max_attempts:
                self.login_button.setEnabled(False)
                QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Trop d'échecs de connexion. Veuillez réessayer plus tard."))

    def create_account(self):
        self.register_module = RegisterModule()  # Créez une instance de RegisterModule
        self.register_module.show()  # Affichez le module d'inscription

    def reset_password(self):
        QMessageBox.information(self, self.tr("Mot de passe oublié"), self.tr("Fonctionnalité non implémentée."))

    def open_nova360(self):
        self.hide()  # Masquer le module de connexion
        self.home_page = HomePage()  # Remplacez ceci par votre classe de page d'accueil
        self.home_page.show()  # Afficher la page d'accueil
