import json
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout,QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from mail.mail_in_to_in import Mailer1  # Importer la classe Mailer1
from mail.mail_in_to_out import Mailer2  # Importer la classe Mailer1

import hashlib  # Pour le hachage des mots de passe
from translation import TranslatorManager  # Importer le gestionnaire de traductions
import os
from PyQt5.QtGui import QFont, QPixmap, QIcon


from translation import TranslatorManager  # Importer le gestionnaire de traductions
from PyQt5.QtCore import Qt, QTranslator, QLocale
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
        self.setWindowIcon(QIcon('resources/icons/robot-icons-30497.png'))  # Spécifiez le chemin de l'icône

        self.setFixedSize(700, 500)
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
                image: url('resources/icons/arrow-down.png');  /* Icône personnalisée pour la flèche */
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
