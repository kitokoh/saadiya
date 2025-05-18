import hashlib  # Pour le hachage des mots de passe
import json
import os
import re
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox
)

from mail.mail_in_to_in import Mailer1  # Importer la classe Mailer1
from mail.mail_in_to_out import Mailer2  # Importer la classe Mailer1
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from translation import TranslatorManager  # Importer le gestionnaire de traductions

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout,QDialog, QWidget
import os
class RegisterModule(QDialog):
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
        self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))  # Spécifiez le chemin de l'icône

        self.setFixedSize(700, 500)
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

        # Champ "Licence" avec une liste déroulante
        self.licence_input = QComboBox(self)
        self.licence_input.addItems([
            self.tr("demo"),
            self.tr("annuelle"),
            self.tr("mensuelle"),
            self.tr("lifetime")
        ])  # Ajout des options
        self.licence_input.setCurrentText("demo")  # Sélection par défaut

        # Appliquer un style personnalisé tout en utilisant input_style
        self.licence_input.setStyleSheet(self.input_style() + """
            QComboBox {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #007BFF;  /* Bordure bleue pour un design soigné */
                background-color: #F8F9FA;  /* Fond clair */
                font-size: 14px;
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
            }

            QComboBox:hover {
                border-color: #0056b3;  /* Bordure bleue plus foncée lors du survol */
            }

            QComboBox:focus {
                border-color: #0056b3;  /* Bordure bleue foncée quand le champ est sélectionné */
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.4);  /* Ombre douce pour la mise en avant */
            }

            QComboBox::drop-down {
                border: none;  /* Retirer la bordure du menu déroulant */
                background-color: #FFFFFF;  /* Fond blanc pour le menu déroulant */
            }

            QComboBox::down-arrow {
                image: url('resources/icons/telgrampng.png');  /* Icône personnalisée pour la flèche */
            }
        """)

        # Ajouter le champ de sélection à la mise en page
        form_layout.addWidget(self.licence_input)

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
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/register_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/register_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/register_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/register_translated.qm")

        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','register_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','register_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','register_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','register_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','register_translated.qm'))

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
                'pt': 'pt',

            }

            # Vérifier si la langue système est supportée, sinon utiliser l'anglais par défaut
            selected_language = language_map.get(system_locale, 'en')

        self.switch_language(selected_language)

    def input_style(self):
        """Retourne le style CSS pour les champs de saisie."""
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 8px; /* Bordures arrondies pour un aspect moderne */
                border: 1px solid #007BFF; /* Bordure bleue par défaut */
                background-color: #FFFFFF; /* Fond blanc */
                font-size: 14px; /* Taille de police confortable */
                color: #333333; /* Texte sombre pour une meilleure lisibilité */
                margin-bottom: 20px; /* Espacement entre les champs */
                transition: border-color 0.3s ease, box-shadow 0.3s ease; /* Transition douce */
            }

            QLineEdit:focus {
                border: 1px solid #0056b3; /* Bordure bleue plus foncée lorsqu'en focus */
                box-shadow: 0 0 8px rgba(0, 86, 179, 0.6); /* Ombre pour accentuer l'état actif */
            }

            QLineEdit:disabled {
                background-color: #f2f2f2; /* Fond gris clair pour les champs désactivés */
                border: 1px solid #cccccc; /* Bordure grise pour les champs désactivés */
                color: #999999; /* Texte gris pour les champs désactivés */
            }

            QLineEdit::placeholder {
                color: #888888; /* Couleur grise pour le texte du placeholder */
                font-style: italic; /* Texte en italique pour le placeholder */
            }
        """


    def button_style(self):
        return """
            QPushButton {
                background: linear-gradient(45deg, #007BFF, #0056b3);
                color: blue;
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

            QPushButton:focus {
                outline: none;
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
           # QMessageBox.warning(self, self.tr("Erreur"), self.tr("Veuillez remplir tous les champs obligatoires."))
            QMessageBox.warning(
                self, 
                self.tr("⚠️ Warning - Missing Information"), 
                self.tr("Please fill in all required fields to proceed."))

            return

        if password != confirm_password:
         #   QMessageBox.warning(self, self.tr("Erreur"), self.tr("Les mots de passe ne correspondent pas."))
            QMessageBox.warning(
                    self, 
                    self.tr("⚠️ Error - Password Mismatch"), 
                    self.tr("The passwords entered do not match. Please check and try again.")
                )

            return

        if len(username) < 3:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username Too Short"),
                self.tr("The username must be at least 3 characters long. Please enter a longer username.")
            )
            return

        if len(password) < 6:
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Password Too Short"),
                self.tr("The password must be at least 6 characters long. Please choose a more secure password.")
            )
            return

        if not self.validate_email(email):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Invalid Email Address"),
                self.tr("The entered email address is invalid. Please enter a correct email address.")
            )
            return

        user_data = self.load_user_data()

        if self.user_exists(username, email, user_data):
            QMessageBox.warning(
                self,
                self.tr("⚠️ Error - Username or Email Already Taken"),
                self.tr("This username or email address is already in use. Please choose a different one.")
            )
            return


        # Chiffrement du mot de passe
        hashed_password = self.hash_password(password)

        # Enregistrer le nouvel utilisateur avec e-mail et mot de passe haché
        user_data.append({"username": username, "password": hashed_password, "email": email})
        self.save_user_data(user_data)

        # Envoi d'un e-mail de confirmation
        mailer = Mailer1()
        mailer.send_email_to_user(user_email=email,email_type= 'mail4')
        mailer2 = Mailer2()
        mailer2.send_email(email_type="admin_message2",extra_subject=None)  # Exemple d'envoi d'e-mail


       # QMessageBox.information(self, self.tr("Succès"), self.tr("Compte créé avec succès ! Vous pouvez maintenant vous connecter."))
        QMessageBox.information(
                    self, 
                    self.tr("🎉 Success - Welcome!"), 
                    self.tr("Your account has been created successfully!\n\n"
                            "✨ You’re now ready to explore our features and enhance your strategies.\n\n"
                            "👉 Log in now to begin your journey with us!"))
                
       
        self.clear_fields()
        self.accept()

        #self.close()  # Fermez le formulaire après la création réussie du compte

    def clear_fields(self):
        """Réinitialise les champs de saisie."""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.email_input.clear()


import hashlib
import sqlite3
import os
import re
from datetime import datetime
from PyQt5.QtCore import Qt, QTranslator, QLocale, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                            QLabel, QMessageBox, QHBoxLayout, QComboBox, QWidget)
from PyQt5.QtWidgets import QFrame

# class RegisterModule(QDialog):

#     registration_success = pyqtSignal(str)  # Signal avec le nom d'utilisateur
    


#     def create_input_field(self, placeholder, icon_name, is_password):
#         """Crée un champ de saisie stylisé"""
#         frame = QFrame()
#         frame.setStyleSheet("""
#             QFrame {
#                 background-color: #F5F8FA;
#                 border-radius: 8px;
#                 border: 2px solid #2D74DA;
#             }
#         """)
        
#         layout = QHBoxLayout(frame)
#         layout.setContentsMargins(5, 5, 5, 5)
        
#         # Icône
#         icon_label = QLabel()
#         icon_label.setPixmap(QPixmap(f"resources/icons/{icon_name}").scaled(20, 20))
#         layout.addWidget(icon_label)
        
#         # Champ de saisie
#         field = QLineEdit()
#         field.setPlaceholderText(placeholder)
#         field.setStyleSheet("""
#             QLineEdit {
#                 border: none;
#                 background: transparent;
#                 font-size: 14px;
#                 padding: 5px;
#             }
#         """)
        
#         if is_password:
#             field.setEchoMode(QLineEdit.Password)
#             # Bouton pour afficher/masquer le mot de passe
#             toggle_btn = QPushButton()
#             toggle_btn.setIcon(QIcon("resources/icons/eye.png"))
#             toggle_btn.setStyleSheet("border: none; background: transparent;")
#             toggle_btn.setCheckable(True)
#             toggle_btn.toggled.connect(
#                 lambda state, f=field: f.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password))
#             layout.addWidget(field)
#             layout.addWidget(toggle_btn)
#         else:
#             layout.addWidget(field)
        
#         return frame

#     def get_combo_style(self):
#         """Retourne le style CSS pour la combo box"""
#         return """
#             QComboBox {
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 2px solid #2D74DA;
#                 background-color: #F5F8FA;
#                 font-size: 14px;
#             }
#             QComboBox:hover {
#                 border-color: #1A59A0;
#             }
#             QComboBox::drop-down {
#                 border: none;
#                 width: 30px;
#             }
#             QComboBox::down-arrow {
#                 image: url('resources/icons/telgrampng.png');
#             }
#         """

#     def get_button_style(self):
#         """Retourne le style CSS pour les boutons"""
#         return """
#             QPushButton {
#                 background-color: #2D74DA;
#                 color: white;
#                 padding: 12px;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 font-weight: bold;
#                 border: 2px solid #1A59A0;
#             }
#             QPushButton:hover {
#                 background-color: #1A59A0;
#             }
#             QPushButton:pressed {
#                 background-color: #154273;
#             }
#         """


#     def init_translations(self):
#         """Initialise le système de traduction"""
#         self.translator = QTranslator()
#         self.translator_manager = TranslatorManager()
#         self.translator_manager.load_translations()
        
#         # Charger la langue par défaut
#         settings_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "settings.json")
#         if os.path.exists(settings_path):
#             with open(settings_path) as f:
#                 lang = json.load(f).get('language', 'fr')
#                 self.switch_language(lang)

#     def switch_language(self, language):
#         """Change la langue de l'interface"""
#         translations_path = os.path.join(
#             os.path.expanduser("~"), 
#             "AppData", "Roaming", "saadiya", 
#             "resources", "lang", 
#             f"{language}_{language.upper()}", 
#             "ui", "register_translated.qm"
#         )
        
#         if os.path.exists(translations_path):
#             self.translator.load(translations_path)
#             QApplication.instance().installTranslator(self.translator)
#             self.retranslate_ui()

#     def retranslate_ui(self):
#         """Retraduit l'interface"""
#         self.setWindowTitle(self.tr("Créer un compte"))
#         # Mettre à jour les autres éléments textuels si nécessaire

#     def validate_inputs(self):
#         """Valide tous les champs du formulaire"""
#         username = self.username_input.findChild(QLineEdit).text().strip()
#         password = self.password_input.findChild(QLineEdit).text()
#         confirm_password = self.confirm_password_input.findChild(QLineEdit).text()
#         email = self.email_input.findChild(QLineEdit).text().strip()
#         license_type = self.license_combo.currentText()
        
#         errors = []
        
#         # Validation du nom d'utilisateur
#         if len(username) < 3:
#             errors.append(self.tr("Le nom d'utilisateur doit contenir au moins 3 caractères"))
#         elif not re.match(r'^[a-zA-Z0-9_]+$', username):
#             errors.append(self.tr("Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores"))
        
#         # Validation du mot de passe
#         if len(password) < 8:
#             errors.append(self.tr("Le mot de passe doit contenir au moins 8 caractères"))
#         elif password != confirm_password:
#             errors.append(self.tr("Les mots de passe ne correspondent pas"))
        
#         # Validation de l'email
#         if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
#             errors.append(self.tr("L'adresse email n'est pas valide"))
        
#         # Vérification des doublons dans la DB
#         try:
#             self.cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
#             if self.cursor.fetchone():
#                 errors.append(self.tr("Ce nom d'utilisateur ou email est déjà utilisé"))
#         except sqlite3.Error as e:
#             errors.append(self.tr("Erreur de vérification des données"))
#             print(f"Erreur DB: {e}")
        
#         if errors:
#             QMessageBox.warning(self, self.tr("Erreurs de validation"), "\n".join(errors))
#             return False
        
#         return True

#     def handle_registration(self):
#         """Gère le processus d'inscription"""
#         if not self.validate_inputs():
#             return
            
#         username = self.username_input.findChild(QLineEdit).text().strip()
#         password = self.password_input.findChild(QLineEdit).text()
#         email = self.email_input.findChild(QLineEdit).text().strip()
#         license_type = self.license_combo.currentText()
        
#         try:
#             # Hachage du mot de passe
#             hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
            
#             # Création du token de vérification
#             verification_token = hashlib.sha256(f"{username}{email}{datetime.now()}".encode()).hexdigest()
            
#             # Insertion dans la DB
#             self.cursor.execute("""
#                 INSERT INTO users (username, password_hash, email, license_type, verification_token)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (username, hashed_pwd, email, license_type, verification_token))
            
#             self.conn.commit()
            
#             # Envoi des emails
#             Mailer1().send_email_to_user(
#                 user_email=email,
#                 email_type='welcome',
#                 extra_data={'username': username, 'token': verification_token}
#             )
            
#             Mailer2().send_email(
#                 email_type="new_user_notification",
#                 extra_subject=f"Nouvel utilisateur: {username}"
#             )
            
#             # Message de succès
#             QMessageBox.information(
#                 self, 
#                 self.tr("🎉 Inscription réussie !"), 
#                 self.tr("""Votre compte a été créé avec succès !
                
# Un email de confirmation vous a été envoyé à {email}.

# Vous pouvez maintenant vous connecter et commencer à utiliser Leopardo AI.""").format(email=email)
#             )
            
#             self.registration_success.emit(username)
#             self.accept()
            
#         except sqlite3.Error as e:
#             QMessageBox.critical(
#                 self, 
#                 self.tr("Erreur"), 
#                 self.tr("Une erreur est survenue lors de la création du compte. Veuillez réessayer.")
#             )
#             print(f"Erreur DB: {e}")

#     def clear_form(self):
#         """Réinitialise le formulaire"""
#         self.username_input.findChild(QLineEdit).clear()
#         self.password_input.findChild(QLineEdit).clear()
#         self.confirm_password_input.findChild(QLineEdit).clear()
#         self.email_input.findChild(QLineEdit).clear()
#         self.license_combo.setCurrentIndex(0)

#     def closeEvent(self, event):
#         """Gère la fermeture de la fenêtre"""
#         self.conn.close()
#         super().closeEvent(event)




#     registration_success = pyqtSignal(str)  # Signal avec le nom d'utilisateur
    
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # Configuration DB
#         self.db_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "data", "users.db")
        
#         # Initialisation dans le bon ordre
#         self.init_db()  # Doit être appelé en premier
#         self.init_ui()
#         self.init_translations()

#     def init_db(self):
#         """Initialise la base de données SQLite"""
#         try:
#             os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
#             self.conn = sqlite3.connect(self.db_path)
#             self.cursor = self.conn.cursor()
            
#             # Création des tables si elles n'existent pas
#             # Création des tables si elles n'existent pas
#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT UNIQUE NOT NULL,
#                     password_hash TEXT NOT NULL,
#                     email TEXT UNIQUE NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     last_login TIMESTAMP,
#                     is_active BOOLEAN DEFAULT 1,
#                     failed_attempts INTEGER DEFAULT 0,
#                     verification_token TEXT,
#                     license_type TEXT NOT NULL,
#                     license_expiration TIMESTAMP,
#                     is_verified BOOLEAN DEFAULT 0,
#                     is_locked BOOLEAN DEFAULT 0,
#                     lockout_time TIMESTAMP,
#                     last_active TIMESTAMP


#                 )
#             """)


#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS licenses (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT UNIQUE NOT NULL,
#                     duration_days INTEGER,
#                     price REAL,
#                     features TEXT
#                 )
#             """)
            


#             self.cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS sessions (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER REFERENCES users(id),
#                     session_token TEXT UNIQUE NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     expires_at TIMESTAMP NOT NULL,
#                     is_valid BOOLEAN DEFAULT 1,
#                     session_timeout INTEGER DEFAULT 14400,
#                     session_start TIMESTAMP,
#                     session_end TIMESTAMP,  
#                     session_valid BOOLEAN DEFAULT 1,
#                     session_expiration TIMESTAMP,
#                     session_last_active TIMESTAMP
#                 )
#             """)       

#             # Insertion des licences par défaut si nécessaire
#             self.cursor.execute("SELECT COUNT(*) FROM licenses")
#             if self.cursor.fetchone()[0] == 0:
#                 licenses = [
#                     ("demo", 7, 0.0, "Fonctionnalités de base"),
#                     ("mensuelle", 30, 9.99, "Accès complet mensuel"),
#                     ("annuelle", 365, 99.99, "Accès complet annuel"),
#                     ("lifetime", None, 299.99, "Accès permanent")
#                 ]
#                 self.cursor.executemany(
#                     "INSERT INTO licenses (name, duration_days, price, features) VALUES (?, ?, ?, ?)",
#                     licenses
#                 )
            
#             self.conn.commit()
            
#         except sqlite3.Error as e:
#             print(f"Erreur lors de l'initialisation de la base de données: {e}")
#             # Fallback: recréer la connexion
#             self.conn = sqlite3.connect(self.db_path)
#             self.cursor = self.conn.cursor()

#     def init_ui(self):
#         """Initialise l'interface utilisateur"""
#         self.setWindowTitle(self.tr("Créer un compte"))
#         self.setWindowIcon(QIcon('resources/icons/878952-Hornet-Secure.ico'))
#         self.setFixedSize(700, 500)
        
#         # Layout principal
#         main_layout = QHBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
        
#         # Image de fond (50%)
#         self.image_label = QLabel()
#         self.image_label.setPixmap(QPixmap("resources/images/7.jpg").scaled(
#             350, 500, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
#         main_layout.addWidget(self.image_label)
        
#         # Formulaire (50%)
#         form_frame = QFrame()
#         form_frame.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.95);
#                 border-radius: 10px;
#             }
#         """)
        
#         form_layout = QVBoxLayout(form_frame)
#         form_layout.setContentsMargins(30, 30, 30, 30)
#         form_layout.setSpacing(15)
        
#         # Titre
#         title = QLabel(self.tr("Créer un compte"))
#         title.setStyleSheet("""
#             font-size: 24px;
#             font-weight: bold;
#             color: #2c3e50;
#         """)
#         title.setAlignment(Qt.AlignCenter)
#         form_layout.addWidget(title)
        
#         # Champs de formulaire
#         fields = [
#             (self.tr("Nom d'utilisateur"), "user.png", False),
#             (self.tr("Mot de passe"), "lock.png", True),
#             (self.tr("Confirmer le mot de passe"), "lock.png", True),
#             (self.tr("Adresse e-mail"), "email.png", False)
#         ]
        
#         self.username_input = self.create_input_field(*fields[0])
#         self.password_input = self.create_input_field(*fields[1])
#         self.confirm_password_input = self.create_input_field(*fields[2])
#         self.email_input = self.create_input_field(*fields[3])
        
#         form_layout.addWidget(self.username_input)
#         form_layout.addWidget(self.password_input)
#         form_layout.addWidget(self.confirm_password_input)
#         form_layout.addWidget(self.email_input)
        
#         # Liste déroulante des licences
#         self.license_combo = QComboBox()
#         self.license_combo.setStyleSheet(self.get_combo_style())
#         self.populate_license_combo()  # Appelé après l'initialisation de la DB
#         form_layout.addWidget(self.license_combo)
        
#         # Bouton d'inscription
#         self.register_btn = QPushButton(self.tr("Créer un compte"))
#         self.register_btn.setStyleSheet(self.get_button_style())
#         self.register_btn.clicked.connect(self.handle_registration)
#         form_layout.addWidget(self.register_btn)
        
#         main_layout.addWidget(form_frame)

#     def populate_license_combo(self):
#         """Remplit la liste déroulante des licences"""
#         try:
#             # Vérification que le curseur est bien initialisé
#             if not hasattr(self, 'cursor') or not self.cursor:
#                 self.init_db()  # Réinitialisation si nécessaire
                
#             self.cursor.execute("SELECT name FROM licenses ORDER BY price")
#             licenses = self.cursor.fetchall()
            
#             self.license_combo.clear()
#             for license in licenses:
#                 self.license_combo.addItem(license[0])
            
#             # Sélection par défaut sur "demo"
#             index = self.license_combo.findText("demo")
#             if index >= 0:
#                 self.license_combo.setCurrentIndex(index)
                
#         except sqlite3.Error as e:
#             print(f"Erreur lors du chargement des licences: {e}")
#             # Solution de repli avec des valeurs par défaut
#             self.license_combo.clear()
#             self.license_combo.addItems(["demo", "mensuelle", "annuelle", "lifetime"])
#             self.license_combo.setCurrentIndex(0)
            
#             # Tentative de réparation de la base de données
#             try:
#                 self.init_db()
#             except Exception as e:
#                 print(f"Échec de la réinitialisation de la base de données: {e}")

#     # ... (le reste des méthodes reste inchangé)
