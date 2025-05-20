import hashlib  # Pour le hachage des mots de passe
import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QFrame
)
from datetime import datetime, timedelta

from Home.home import HomePage
from mail.mail_in_to_in import Mailer1
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from ui.welcomeSyle import WelcomeDialog
from .carousel import CarouselWidget  # Assurez-vous que CarouselWidget est importé
from .register import RegisterModule

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Durée maximale de la session en minutes
SESSION_TIMEOUT = 144000  # 30 minutes


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
            border-radius: 15px;  /* Arrondir les coins du formulaire */
            padding: 30px;
            backdrop-filter: blur(10px);  /* Flou en arrière-plan */
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.2);  /* Ombre plus marquée pour un effet de profondeur */
        """)
        form_layout = QVBoxLayout(form_frame)

        # Titre du formulaire
        title_label = QLabel(self.tr("Connexion à Leopardo AI"))
        title_label.setFont(QFont("Roboto", 24, QFont.Bold))  # Police moderne et taille de police plus grande
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #333333;  /* Texte sombre pour un contraste optimal */
            margin-bottom: 20px;  /* Espacement sous le titre */
        """)
        # Frame contenant le formulaire
        form_frame = QFrame(self)
        form_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.95);  /* Fond blanc avec légère transparence */
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(8px);
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        """)
        form_layout = QVBoxLayout(form_frame)

        # Titre du formulaire
        title_label = QLabel(self.tr("Connexion  Leopardo AI"))
        title_label.setFont(QFont("Roboto", 26, QFont.Bold))  # Police moderne et imposante
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #2D74DA;
            margin-bottom: 10px;
        """)
        form_layout.addWidget(title_label)

        # Sous-titre commercial
        subtitle_label = QLabel(self.tr("Automatisez votre marketing avec une efficacité inégalée"))
        subtitle_label.setFont(QFont("Roboto", 13, QFont.Light))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            color: #777;  /* Gris clair pour un sous-titre élégant */
            margin-bottom: 15px;
            font-style: italic;
        """)
        form_layout.addWidget(subtitle_label)

        # Champ de saisie pour le nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet("""
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #2D74DA;  /* Bordure élégante bleue */
            background-color: #F5F8FA;
            font-size: 15px;
            color: #333;
            transition: all 0.3s ease-in-out;
        """)
        self.username_input.setStyleSheet(self.username_input.styleSheet() + """
            QLineEdit:focus {
                border-color: #1A59A0;  /* Bordure bleu foncé au focus */
                box-shadow: 0 0 8px rgba(26, 89, 160, 0.3);
            }
        """)
        form_layout.addWidget(self.username_input)

        # Champ de saisie pour le mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #2D74DA;
            background-color: #F5F8FA;
            font-size: 15px;
            color: #333;
            transition: all 0.3s ease-in-out;
        """)
        self.password_input.setStyleSheet(self.password_input.styleSheet() + """
            QLineEdit:focus {
                border-color: #1A59A0;
                box-shadow: 0 0 8px rgba(26, 89, 160, 0.3);
            }
        """)
        form_layout.addWidget(self.password_input)

        # Bouton de connexion
        self.login_button = QPushButton(self.tr("Se connecter"), self)
        self.login_button.setIcon(QIcon("resources/icons/house-key-icon-41543-Windows.ico"))
        self.login_button.setStyleSheet("""
            background-color: #2D74DA;
            color: white;
            padding: 14px 28px;
            border-radius: 40px;  /* Coins arrondis pour un bouton moderne */
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            border: 2px solid red;  /* Bordure visible bleue */
            transition: all 0.3s ease-in-out;
        """)
        self.login_button.setStyleSheet(self.login_button.styleSheet() + """
            QPushButton:hover {
                background-color: #1A59A0;
                transform: scale(1.05);
            }
        """)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)

        # Lien pour mot de passe oublié
        self.forgot_password_button = QPushButton(self.tr("Mot de passe oublié ?"), self)
        self.forgot_password_button.setStyleSheet("""
            background: transparent;
            color: #2D74DA;
            border: none;
            font-size: 14px;
            font-weight: bold;
            margin-top: 10px;
            text-decoration: underline;
            cursor: pointer;
        """)
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.reset_password)
        form_layout.addWidget(self.forgot_password_button)

        # Lien pour créer un compte
        self.signup_button = QPushButton(self.tr("Créer un compte"), self)
        self.signup_button.setIcon(QIcon("resources/icons/878952-Hornet-Secure.ico"))
        self.signup_button.setStyleSheet("""
            background-color: #28A745;
            color: white;
            padding: 14px 28px;
            border-radius: 40px;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
                                         
            border: 2px solid blue;
            transition: all 0.3s ease-in-out;
        """)
        self.signup_button.setStyleSheet(self.signup_button.styleSheet() + """
            QPushButton:hover {
                background-color: #218838;
                transform: scale(1.05);
            }
        """)
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Espacement et marges ajustées pour une interface plus compacte
        form_layout.setSpacing(10)  # Réduit l'espacement entre les éléments
        form_layout.setContentsMargins(20, 20, 20, 20)  # Marges internes réduites pour plus de compacité

        # Ajouter le formulaire à la mise en page principale
        self.layout.addWidget(form_frame)

                # Ajouter le formulaire à la mise en page principale
        self.layout.addWidget(form_frame)

        # Variables de contrôle
        self.failed_attempts = 0
        self.max_attempts = 3  # Limite d'essais
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

    def switch_language(self, language):
        """Permet de changer la langue."""
        # if language == "en":
        #     self.translator.load("resources/lang/en_US/ui/login_translated.qm")
        # elif language == "fr":
        #     self.translator.load("resources/lang/fr_FR/ui/login_translated.qm")
        # elif language == "tr":
        #     self.translator.load("resources/lang/tr_TR/ui/login_translated.qm")
        # elif language == "ar":
        #     self.translator.load("resources/lang/ar_AR/ui/login_translated.qm")


        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','login_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','login_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','login_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','login_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','login_translated.qm'))

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
                 'pt': 'pt',

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
            self.save_session(username)  # Sauvegarder la session

            self.connection_successful.emit()  # Émettre le signal de réussite

            # QMessageBox.information(self, self.tr("Connexion réussie"), self.tr("Bienvenue, {}!").format(username))
            # QMessageBox.information(
            #     self,
            #     self.tr("🎉 Successful Login!"),
            #     self.tr(
            #         "<h2 style='color:#2E86C1;'>Welcome, {}!</h2>"
            #         "<p style='font-size:14px; color:#4A4A4A;'>"
            #         "You've entered <strong>Saadiya.ai's Command Center</strong> — the heart of your automated marketing strategy.</p>"
            #         "<p style='font-size:13px; color:#4A4A4A;'>"
            #         "Here, you can design and schedule your marketing campaigns, hand the execution over to our intelligent AI-driven bots, "
            #         "and watch as your reach and influence expand effortlessly.</p>"
            #         "<br>"
            #         "<h3 style='color:#2E86C1;'>Next Steps</h3>"
            #         "<ul style='font-size:13px; color:#4A4A4A;'>"
            #         "<li><strong>Define Your Goals:</strong> Outline your marketing objectives to focus your strategy.</li>"
            #         "<li><strong>Schedule Campaigns:</strong> Set precise timing to engage your audience when it matters most.</li>"
            #         "<li><strong>Let Saadiya Execute:</strong> Our robots handle the rest, ensuring your brand grows while you focus on bigger visions.</li>"
            #         "</ul>"
            #         "<p style='font-size:13px; color:#4A4A4A;'>"
            #         "Ready to accelerate? Start now and let nova.ai take your brand to new heights!</p>"
            #     ).format(username)
            # )

            dialog = WelcomeDialog(username)
            dialog.exec_()
            mailer = Mailer1()
            mailer.send_email(email_type="mail1")
            QMessageBox.information(
                self,
                self.tr("🎉 Bienvenue chez Leopardo.ai!"),
                self.tr(
                    "<div style='background-color:#F0F8FF; padding:20px; border-radius:10px;'>"
                    "<h1 style='color:#2E86C1; font-size:24px; text-align:center;'>Bienvenue, {}</h1>"
                    "<p style='font-size:16px; color:#333333; text-align:center;'>"
                    "<strong>Votre Hub d'Automatisation Marketing Intelligent</strong>"
                    "</p><br>"
                    
                    "<div style='padding: 10px; border-left: 5px solid #2E86C1; margin: 10px 0;'>"
                    "<p style='font-size:14px; color:#555555; line-height:1.6;'>"
                    "Vous avez désormais accès à Leopardo.ai, la solution ultime pour automatiser et optimiser vos stratégies marketing.<br>"
                    "Programmez vos campagnes, définissez vos objectifs, et laissez nos robots intelligents s'occuper du reste."
                    "</p>"
                    "</div><br>"
                    
                    "<h3 style='color:#2E86C1; font-size:18px;'>🔑 Fonctionnalités Clés</h3>"
                    "<ul style='font-size:14px; color:#555555; padding-left: 40px;'>"
                    "<li style='margin-bottom:10px;'><strong>📅 Programmation Intelligente :</strong> Planifiez et automatisez vos publications sur plusieurs plateformes avec une précision optimale.</li>"
                    "<li style='margin-bottom:10px;'><strong>🤖 Engagement Automatisé :</strong> Interagissez avec votre audience grâce à des réponses et commentaires intelligents générés par l'IA.</li>"
                    "<li><strong>📊 Analyse et Reporting :</strong> Suivez les performances de vos campagnes en temps réel et ajustez vos stratégies pour un impact maximal.</li>"
                    "</ul><br>"
                    
                    "<p style='font-size:14px; color:#555555; text-align:center;'>"
                    "Prêt à révolutionner votre marketing? Commencez dès maintenant et laissez Leopardo.ai propulser votre marque vers de nouveaux sommets!"
                    "</p><br>"
                    
                    "<p style='font-size:12px; color:#888888; text-align:center;'>"
                    "© 2024 Leopardo Pro | "
                    "<a href='https://www.Leopardopro.com' style='color:#2E86C1; text-decoration:none;'>www.Leopardopro.com</a>"
                    "</p>"
                    "</div>"
                ).format(username)
            )

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

        if not self.is_session_active():
            return
        try:
            with open(os.path.join(user_data_dir, 'resources', 'session.json'), 'r') as file:
                session_data = json.load(file)
                if session_data.get('is_logged_in'):
                    username = session_data.get('username')
                    dialog = WelcomeDialog(username)
                    dialog.exec_()

                    QMessageBox.information(
                        self,
                        self.tr("🎉 Bienvenue chez Leopardo.ai!"),
                        self.tr(
                            "<div style='background-color:#F0F8FF; padding:20px; border-radius:10px;'>"
                            "<h1 style='color:#2E86C1; font-size:24px; text-align:center;'>Bienvenue, {}</h1>"
                            "<p style='font-size:16px; color:#333333; text-align:center;'>"
                            "<strong>Votre Hub d'Automatisation Marketing Intelligent</strong>"
                            "</p><br>"
                            
                            "<div style='padding: 10px; border-left: 5px solid #2E86C1; margin: 10px 0;'>"
                            "<p style='font-size:14px; color:#555555; line-height:1.6;'>"
                            "Vous avez désormais accès à Leopardo.ai, la solution ultime pour automatiser et optimiser vos stratégies marketing.<br>"
                            "Programmez vos campagnes, définissez vos objectifs, et laissez nos robots intelligents s'occuper du reste."
                            "</p>"
                            "</div><br>"
                            
                            "<h3 style='color:#2E86C1; font-size:18px;'>🔑 Fonctionnalités Clés</h3>"
                            "<ul style='font-size:14px; color:#555555; padding-left: 40px;'>"
                            "<li style='margin-bottom:10px;'><strong>📅 Programmation Intelligente :</strong> Planifiez et automatisez vos publications sur plusieurs plateformes avec une précision optimale.</li>"
                            "<li style='margin-bottom:10px;'><strong>🤖 Engagement Automatisé :</strong> Interagissez avec votre audience grâce à des réponses et commentaires intelligents générés par l'IA.</li>"
                            "<li><strong>📊 Analyse et Reporting :</strong> Suivez les performances de vos campagnes en temps réel et ajustez vos stratégies pour un impact maximal.</li>"
                            "</ul><br>"
                            
                            "<p style='font-size:14px; color:#555555; text-align:center;'>"
                            "Prêt à révolutionner votre marketing? Commencez dès maintenant et laissez Leopardo.ai propulser votre marque vers de nouveaux sommets!"
                            "</p><br>"
                            
                            "<p style='font-size:12px; color:#888888; text-align:center;'>"
                            "© 2024 Leopardo Pro | "
                            "<a href='https://www.Leopardopro.com' style='color:#2E86C1; text-decoration:none;'>www.Leopardopro.com</a>"
                            "</p>"
                            "</div>"
                        ).format(username)
                    )
                    self.connection_successful.emit()  # Passer directement à l'application
                    self.close()
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Pas de session, l'utilisateur doit se connecter
    def logout(self):
        session_file = os.path.join(user_data_dir, 'resources', 'session.json')
        if os.path.exists(session_file):
            os.remove(session_file)
        QMessageBox.information(self, self.tr("Déconnexion"), self.tr("Vous êtes maintenant déconnecté."))
        # Recharger ou rediriger vers l'interface de connexion

    def save_session(self, username):
        """Sauvegarde les informations de session au moment de la connexion."""
        now = datetime.now()
        session_data = {
            'username': username,
            'is_logged_in': True,
            'session_start': now.isoformat(),
            'last_active': now.isoformat(),
            'expiration_time': (now + timedelta(minutes=SESSION_TIMEOUT)).isoformat()
        }
        with open(os.path.join(user_data_dir, 'resources', 'data', 'session.json'), 'w') as file:
            json.dump(session_data, file)

    def update_last_active(self):
        """Met à jour le champ last_active et expiration_time de la session active."""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        try:
            with open(session_file, 'r') as file:
                session_data = json.load(file)
            session_data['last_active'] = datetime.now().isoformat()
            session_data['expiration_time'] = (datetime.now() + timedelta(minutes=SESSION_TIMEOUT)).isoformat()
            with open(session_file, 'w') as file:
                json.dump(session_data, file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def is_session_active(self):
        """Vérifie si la session est encore active en comparant l'heure actuelle avec last_active et expiration_time."""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        try:
            with open(session_file, 'r') as file:
                session_data = json.load(file)
                last_active = datetime.fromisoformat(session_data.get('last_active'))
                expiration_time = datetime.fromisoformat(session_data.get('expiration_time'))
                
                if datetime.now() > expiration_time:
                    self.logout()
                    QMessageBox.warning(self, self.tr("Session expirée"), self.tr("Votre session a expiré. Veuillez vous reconnecter."))
                    return False
                else:
                    self.update_last_active()
                    return True
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return False









































import hashlib  # Pour le hachage des mots de passe
import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QLinearGradient, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
)
from datetime import datetime, timedelta

from Home.home import HomePage
from mail.mail_in_to_in import Mailer1
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from ui.welcomeSyle import WelcomeDialog
from .carousel import CarouselWidget  # Assurez-vous que CarouselWidget est importé
from .register import RegisterModule

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

# Durée maximale de la session en minutes
SESSION_TIMEOUT = 144000  # 30 minutes


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
        
        # Configuration de la fenêtre principale
        self.setWindowTitle("Leopardo AI - Connexion")
        self.setWindowIcon(QIcon("resources/icons/logo.ico"))
        self.setMinimumSize(900, 600)
        
        # Mise en page principale avec fond dégradé
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Appliquer un fond dégradé
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#1a2a6c"))
        gradient.setColorAt(1, QColor("#b21f1f"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Carrousel d'images (côté gauche)
        self.carousel_widget = CarouselWidget()
        self.carousel_widget.setFixedWidth(450)
        self.layout.addWidget(self.carousel_widget)

        # Section du formulaire (côté droit)
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 0;
            }
        """)
        form_container.setFixedWidth(450)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)
        
        # Logo et titre
        logo_label = QLabel()
        logo_pixmap = QPixmap("resources/icons/logo.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(self.tr("Connexion"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        subtitle_label = QLabel(self.tr("Plateforme d'automatisation marketing intelligente"))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                margin-bottom: 30px;
            }
        """)
        
        form_layout.addWidget(logo_label)
        form_layout.addWidget(title_label)
        form_layout.addWidget(subtitle_label)
        
        # Champ email/nom d'utilisateur
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self.tr("Email ou nom d'utilisateur"))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f7fa;
                border: 2px solid #dfe6e9;
                border-radius: 5px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2d3436;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        
        # Champ mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        
        # Bouton de connexion
        self.login_button = QPushButton(self.tr("Se connecter"))
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
        """)
        self.login_button.clicked.connect(self.login)
        
        # Lien mot de passe oublié
        self.forgot_password_button = QPushButton(self.tr("Mot de passe oublié ?"))
        self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3498db;
                border: none;
                font-size: 13px;
                text-align: right;
                padding: 5px;
            }
            QPushButton:hover {
                color: #2980b9;
                text-decoration: underline;
            }
        """)
        self.forgot_password_button.clicked.connect(self.reset_password)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                color: #dfe6e9;
                margin: 15px 0;
            }
        """)
        
        # Bouton création de compte
        self.signup_button = QPushButton(self.tr("Créer un compte"))
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        self.signup_button.clicked.connect(self.create_account)
        
        # Ajout des widgets au layout
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.forgot_password_button, 0, Qt.AlignRight)
        form_layout.addWidget(separator)
        form_layout.addWidget(self.signup_button)
        
        # Ajouter un espace flexible pour pousser le contenu vers le haut
        form_layout.insertStretch(0, 1)
        
        # Footer
        footer_label = QLabel(self.tr("© 2024 Leopardo AI - Tous droits réservés"))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 11px;
                margin-top: 30px;
            }
        """)
        form_layout.addWidget(footer_label)
        
        self.layout.addWidget(form_container)

        # Variables de contrôle
        self.failed_attempts = 0
        self.max_attempts = 3  # Limite d'essais

    # [Le reste des méthodes reste inchangé...]
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

    def switch_language(self, language):
        """Permet de changer la langue."""
        if language == "en":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','en_US','ui','login_translated.qm'))
        elif language == "fr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','fr_FR','ui','login_translated.qm'))
        elif language == "tr":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','tr_TR','ui','login_translated.qm'))
        elif language == "ar":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','ar_SA','ui','login_translated.qm'))
        elif language == "pt":
            self.translator.load(os.path.join(user_data_dir, 'resources', 'lang','pt_BR','ui','login_translated.qm'))

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
        pass

    def init_language(self):
        """Initialise la langue par défaut à celle du système ou à celle choisie par l'utilisateur."""
        if os.path.exists(os.path.join(user_data_dir, 'resources', 'settings.json')):
            with open(os.path.join(user_data_dir, 'resources', 'settings.json'), 'r') as f:
                preferences = json.load(f)
                selected_language = preferences.get('language', 'en')
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {
                'en': 'en',
                'fr': 'fr',
                'tr': 'tr',
                'ar': 'ar',
                'pt': 'pt',
            }
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
            self.save_session(username)  # Sauvegarder la session

            self.connection_successful.emit()  # Émettre le signal de réussite

            dialog = WelcomeDialog(username)
            dialog.exec_()
            mailer = Mailer1()
            mailer.send_email(email_type="mail1")
            QMessageBox.information(
                self,
                self.tr("🎉 Bienvenue chez Leopardo.ai!"),
                self.tr(
                    "<div style='background-color:#F0F8FF; padding:20px; border-radius:10px;'>"
                    "<h1 style='color:#2E86C1; font-size:24px; text-align:center;'>Bienvenue, {}</h1>"
                    "<p style='font-size:16px; color:#333333; text-align:center;'>"
                    "<strong>Votre Hub d'Automatisation Marketing Intelligent</strong>"
                    "</p><br>"
                    
                    "<div style='padding: 10px; border-left: 5px solid #2E86C1; margin: 10px 0;'>"
                    "<p style='font-size:14px; color:#555555; line-height:1.6;'>"
                    "Vous avez désormais accès à Leopardo.ai, la solution ultime pour automatiser et optimiser vos stratégies marketing.<br>"
                    "Programmez vos campagnes, définissez vos objectifs, et laissez nos robots intelligents s'occuper du reste."
                    "</p>"
                    "</div><br>"
                    
                    "<h3 style='color:#2E86C1; font-size:18px;'>🔑 Fonctionnalités Clés</h3>"
                    "<ul style='font-size:14px; color:#555555; padding-left: 40px;'>"
                    "<li style='margin-bottom:10px;'><strong>📅 Programmation Intelligente :</strong> Planifiez et automatisez vos publications sur plusieurs plateformes avec une précision optimale.</li>"
                    "<li style='margin-bottom:10px;'><strong>🤖 Engagement Automatisé :</strong> Interagissez avec votre audience grâce à des réponses et commentaires intelligents générés par l'IA.</li>"
                    "<li><strong>📊 Analyse et Reporting :</strong> Suivez les performances de vos campagnes en temps réel et ajustez vos stratégies pour un impact maximal.</li>"
                    "</ul><br>"
                    
                    "<p style='font-size:14px; color:#555555; text-align:center;'>"
                    "Prêt à révolutionner votre marketing? Commencez dès maintenant et laissez Leopardo.ai propulser votre marque vers de nouveaux sommets!"
                    "</p><br>"
                    
                    "<p style='font-size:12px; color:#888888; text-align:center;'>"
                    "© 2024 Leopardo Pro | "
                    "<a href='https://www.Leopardopro.com' style='color:#2E86C1; text-decoration:none;'>www.Leopardopro.com</a>"
                    "</p>"
                    "</div>"
                ).format(username)
            )

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

        if not self.is_session_active():
            return
        try:
            with open(os.path.join(user_data_dir, 'resources', 'session.json'), 'r') as file:
                session_data = json.load(file)
                if session_data.get('is_logged_in'):
                    username = session_data.get('username')
                    dialog = WelcomeDialog(username)
                    dialog.exec_()

                    QMessageBox.information(
                        self,
                        self.tr("🎉 Bienvenue chez Leopardo.ai!"),
                        self.tr(
                            "<div style='background-color:#F0F8FF; padding:20px; border-radius:10px;'>"
                            "<h1 style='color:#2E86C1; font-size:24px; text-align:center;'>Bienvenue, {}</h1>"
                            "<p style='font-size:16px; color:#333333; text-align:center;'>"
                            "<strong>Votre Hub d'Automatisation Marketing Intelligent</strong>"
                            "</p><br>"
                            
                            "<div style='padding: 10px; border-left: 5px solid #2E86C1; margin: 10px 0;'>"
                            "<p style='font-size:14px; color:#555555; line-height:1.6;'>"
                            "Vous avez désormais accès à Leopardo.ai, la solution ultime pour automatiser et optimiser vos stratégies marketing.<br>"
                            "Programmez vos campagnes, définissez vos objectifs, et laissez nos robots intelligents s'occuper du reste."
                            "</p>"
                            "</div><br>"
                            
                            "<h3 style='color:#2E86C1; font-size:18px;'>🔑 Fonctionnalités Clés</h3>"
                            "<ul style='font-size:14px; color:#555555; padding-left: 40px;'>"
                            "<li style='margin-bottom:10px;'><strong>📅 Programmation Intelligente :</strong> Planifiez et automatisez vos publications sur plusieurs plateformes avec une précision optimale.</li>"
                            "<li style='margin-bottom:10px;'><strong>🤖 Engagement Automatisé :</strong> Interagissez avec votre audience grâce à des réponses et commentaires intelligents générés par l'IA.</li>"
                            "<li><strong>📊 Analyse et Reporting :</strong> Suivez les performances de vos campagnes en temps réel et ajustez vos stratégies pour un impact maximal.</li>"
                            "</ul><br>"
                            
                            "<p style='font-size:14px; color:#555555; text-align:center;'>"
                            "Prêt à révolutionner votre marketing? Commencez dès maintenant et laissez Leopardo.ai propulser votre marque vers de nouveaux sommets!"
                            "</p><br>"
                            
                            "<p style='font-size:12px; color:#888888; text-align:center;'>"
                            "© 2024 Leopardo Pro | "
                            "<a href='https://www.Leopardopro.com' style='color:#2E86C1; text-decoration:none;'>www.Leopardopro.com</a>"
                            "</p>"
                            "</div>"
                        ).format(username)
                    )
                    self.connection_successful.emit()  # Passer directement à l'application
                    self.close()
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Pas de session, l'utilisateur doit se connecter
            
    def logout(self):
        session_file = os.path.join(user_data_dir, 'resources', 'session.json')
        if os.path.exists(session_file):
            os.remove(session_file)
        QMessageBox.information(self, self.tr("Déconnexion"), self.tr("Vous êtes maintenant déconnecté."))
        # Recharger ou rediriger vers l'interface de connexion

    def save_session(self, username):
        """Sauvegarde les informations de session au moment de la connexion."""
        now = datetime.now()
        session_data = {
            'username': username,
            'is_logged_in': True,
            'session_start': now.isoformat(),
            'last_active': now.isoformat(),
            'expiration_time': (now + timedelta(minutes=SESSION_TIMEOUT)).isoformat()
        }
        with open(os.path.join(user_data_dir, 'resources', 'data', 'session.json'), 'w') as file:
            json.dump(session_data, file)

    def update_last_active(self):
        """Met à jour le champ last_active et expiration_time de la session active."""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        try:
            with open(session_file, 'r') as file:
                session_data = json.load(file)
            session_data['last_active'] = datetime.now().isoformat()
            session_data['expiration_time'] = (datetime.now() + timedelta(minutes=SESSION_TIMEOUT)).isoformat()
            with open(session_file, 'w') as file:
                json.dump(session_data, file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def is_session_active(self):
        """Vérifie si la session est encore active en comparant l'heure actuelle avec last_active et expiration_time."""
        session_file = os.path.join(user_data_dir, 'resources', 'data', 'session.json')
        try:
            with open(session_file, 'r') as file:
                session_data = json.load(file)
                last_active = datetime.fromisoformat(session_data.get('last_active'))
                expiration_time = datetime.fromisoformat(session_data.get('expiration_time'))
                
                if datetime.now() > expiration_time:
                    self.logout()
                    QMessageBox.warning(self, self.tr("Session expirée"), self.tr("Votre session a expiré. Veuillez vous reconnecter."))
                    return False
                else:
                    self.update_last_active()
                    return True
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return False





# import hashlib
# import sqlite3
# import os
# from datetime import datetime, timedelta
# from PyQt5.QtCore import Qt, QTranslator, QLocale, pyqtSignal
# from PyQt5.QtGui import QFont, QIcon, QPixmap
# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
#                             QLabel, QMessageBox, QHBoxLayout, QFrame, QCheckBox)
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QInputDialog

# class LoginModule(QWidget):
#     connection_successful = pyqtSignal(str)  # Signal avec username
    
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.failed_attempts = 0
#         self.max_attempts = 5
#         self.lockout_time = None
#         self.session_timeout = 1440  # 24h en minutes
        
#         # Initialisation DB
#         self.db_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "data", "users.db")
#         self.init_db()
        
#         # UI Setup
#         self.init_ui()
#         self.init_translations()
#         self.check_existing_session()

#     def init_db(self):
#         """Initialise la base de données SQLite"""
#         os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
#         self.conn = sqlite3.connect(self.db_path)
#         self.cursor = self.conn.cursor()
        
#         # Création des tables si elles n'existent pas
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 password_hash TEXT NOT NULL,
#                 email TEXT UNIQUE NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 last_login TIMESTAMP,
#                 is_active BOOLEAN DEFAULT 1,
#                 failed_attempts INTEGER DEFAULT 0,
#                 verification_token TEXT,
#                 license_type TEXT NOT NULL,
#                 license_expiration TIMESTAMP,
#                 is_verified BOOLEAN DEFAULT 0,
#                 is_locked BOOLEAN DEFAULT 0,
#                 lockout_time TIMESTAMP,
#                 last_active TIMESTAMP


#             )
#         """)


#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS licenses (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT UNIQUE NOT NULL,
#                 duration_days INTEGER,
#                 price REAL,
#                 features TEXT
#             )
#         """)
        


#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS sessions (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER REFERENCES users(id),
#                 session_token TEXT UNIQUE NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 expires_at TIMESTAMP NOT NULL,
#                 is_valid BOOLEAN DEFAULT 1,
#                 session_timeout INTEGER DEFAULT 14400,
#                 session_start TIMESTAMP,
#                 session_end TIMESTAMP,  
#                 session_valid BOOLEAN DEFAULT 1,
#                 session_expiration TIMESTAMP,
#                 session_last_active TIMESTAMP
#             )
#         """)
        
#         self.conn.commit()

#     def init_ui(self):
#         """Initialise l'interface utilisateur"""
#         self.setWindowTitle(self.tr("Connexion - Leopardo AI"))
#         self.setWindowIcon(QIcon('resources/icons/house-key-icon-41543-Windows.ico'))
#         self.setStyleSheet("background-color: #F5F5F5;")
#         self.setFixedSize(800, 500)
        
#         # Layout principal
#         main_layout = QHBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)
        
#         # Carrousel d'images (50% de l'espace)
#         self.carousel = CarouselWidget()
#         main_layout.addWidget(self.carousel, stretch=1)
        
#         # Formulaire de connexion (50% de l'espace)
#         form_frame = QFrame()
#         form_frame.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.95);
#                 border-radius: 12px;
#             }
#         """)
        
#         form_layout = QVBoxLayout(form_frame)
#         form_layout.setContentsMargins(40, 40, 40, 40)
#         form_layout.setSpacing(20)
        
#         # Titre
#         title = QLabel(self.tr("Connexion à Leopardo AI"))
#         title.setStyleSheet("""
#             font-size: 26px;
#             font-weight: bold;
#             color: #2D74DA;
#         """)
#         title.setAlignment(Qt.AlignCenter)
#         form_layout.addWidget(title)
        
#         # Champs de formulaire
#         self.username_input = self.create_input_field(self.tr("Nom d'utilisateur"), "user.png")
#         self.password_input = self.create_input_field(self.tr("Mot de passe"), "lock.png", True)
        
#         form_layout.addWidget(self.username_input)
#         form_layout.addWidget(self.password_input)
        
#         # Bouton de connexion
#         self.login_btn = QPushButton(self.tr("Se connecter"))
#         self.login_btn.setIcon(QIcon("resources/icons/house-key-icon-41543-Windows.ico"))
#         self.login_btn.setStyleSheet(self.get_button_style())
#         self.login_btn.clicked.connect(self.handle_login)
#         form_layout.addWidget(self.login_btn)
        
#         # Options
#         options_layout = QHBoxLayout()
        
#         self.remember_me = QCheckBox(self.tr("Se souvenir de moi"))
#         self.remember_me.setStyleSheet("color: #34495e;")
        
#         forgot_pwd = QPushButton(self.tr("Mot de passe oublié ?"))
#         forgot_pwd.setStyleSheet("""
#             QPushButton {
#                 color: #3498db;
#                 border: none;
#                 text-decoration: underline;
#             }
#         """)
#         forgot_pwd.clicked.connect(self.handle_password_recovery)
        
#         options_layout.addWidget(self.remember_me)
#         options_layout.addStretch()
#         options_layout.addWidget(forgot_pwd)
#         form_layout.addLayout(options_layout)
        
#         # Séparateur
#         separator = QFrame()
#         separator.setFrameShape(QFrame.HLine)
#         separator.setStyleSheet("color: #ecf0f1;")
#         form_layout.addWidget(separator)
        
#         # Bouton d'inscription
#         signup_btn = QPushButton(self.tr("Créer un compte"))
#         signup_btn.setIcon(QIcon("resources/icons/878952-Hornet-Secure.ico"))
#         signup_btn.setStyleSheet(self.get_button_style(primary=False))
#         signup_btn.clicked.connect(self.show_register_form)
#         form_layout.addWidget(signup_btn)
        
#         main_layout.addWidget(form_frame, stretch=1)
        
#         # Timer pour verrouillage
#         self.lockout_timer = QTimer()
#         self.lockout_timer.timeout.connect(self.check_lockout_status)

#     def create_input_field(self, placeholder, icon_name, is_password=False):
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

#     def get_button_style(self, primary=True):
#         """Retourne le style CSS pour les boutons"""
#         if primary:
#             return """
#                 QPushButton {
#                     background-color: #2D74DA;
#                     color: white;
#                     padding: 14px 28px;
#                     border-radius: 40px;
#                     font-size: 16px;
#                     font-weight: bold;
#                     border: 2px solid #1A59A0;
#                 }
#                 QPushButton:hover {
#                     background-color: #1A59A0;
#                 }
#                 QPushButton:disabled {
#                     background-color: #95a5a6;
#                 }
#             """
#         else:
#             return """
#                 QPushButton {
#                     background-color: #28A745;
#                     color: white;
#                     padding: 14px 28px;
#                     border-radius: 40px;
#                     font-size: 16px;
#                     font-weight: bold;
#                     border: 2px solid #218838;
#                 }
#                 QPushButton:hover {
#                     background-color: #218838;
#                 }
#             """

#     def init_translations(self):
#         """Initialise le système de traduction"""
#         self.translator = QTranslator()
#         self.translator_manager = TranslatorManager()
#         self.translator_manager.load_translations()
        
#         # Charger la langue par défaut
#         if os.path.exists(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "settings.json")):
#             with open(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "settings.json")) as f:
#                 lang = json.load(f).get('language', 'fr')
#                 self.switch_language(lang)

#     def switch_language(self, language):
#         """Change la langue de l'interface"""
#         if language == "fr":
#             self.translator.load(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "resources", "lang", "fr_FR", "ui", "login_translated.qm"))
#         elif language == "en":
#             self.translator.load(os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya", "resources", "lang", "en_US", "ui", "login_translated.qm"))
        
#         QApplication.instance().installTranslator(self.translator)
#         self.retranslate_ui()

#     def retranslate_ui(self):
#         """Retraduit l'interface"""
#         # Implémentez la mise à jour des textes si nécessaire
#         pass

#     def check_existing_session(self):
#         """Vérifie s'il existe une session valide"""
#         try:
#             self.cursor.execute("""
#                 SELECT u.username, s.expires_at 
#                 FROM sessions s
#                 JOIN users u ON s.user_id = u.id
#                 WHERE s.is_valid = 1 AND s.expires_at > datetime('now')
#                 ORDER BY s.created_at DESC
#                 LIMIT 1
#             """)
#             session = self.cursor.fetchone()
            
#             if session:
#                 username, expires_at = session
#                 if datetime.now() < datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S"):
#                     self.login_success.emit(username)
#         except sqlite3.Error as e:
#             print(f"Erreur DB: {e}")

#     def handle_login(self):
#         """Gère la tentative de connexion"""
#         if self.lockout_time and datetime.now() < self.lockout_time:
#             remaining = (self.lockout_time - datetime.now()).seconds // 60
#             QMessageBox.warning(self, self.tr("Compte verrouillé"),
#                               self.tr(f"Trop de tentatives. Réessayez dans {remaining} minutes."))
#             return
        
#         username = self.username_input.findChild(QLineEdit).text().strip()
#         password = self.password_input.findChild(QLineEdit).text()
        
#         if not self.validate_credentials(username, password):
#             self.failed_attempts += 1
#             if self.failed_attempts >= self.max_attempts:
#                 self.lockout_time = datetime.now() + timedelta(minutes=15)
#                 self.lockout_timer.start(60000)
#                 self.login_btn.setEnabled(False)
#                 self.update_failed_attempts(username)
#             return
            
#         if self.authenticate_user(username, password):
#             self.create_user_session(username)
#             self.show_welcome_message(username)
#             self.login_success.emit(username)
#             self.close()

#     def validate_credentials(self, username, password):
#         """Valide le format des identifiants"""
#         errors = []
        
#         if len(username) < 3:
#             errors.append(self.tr("Nom d'utilisateur trop court"))
            
#         if len(password) < 6:
#             errors.append(self.tr("Mot de passe trop court"))
            
#         if errors:
#             QMessageBox.warning(self, self.tr("Erreur de validation"), "\n".join(errors))
#             return False
            
#         return True

#     def authenticate_user(self, username, password):
#         """Authentifie l'utilisateur avec la DB"""
#         try:
#             hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
            
#             self.cursor.execute("""
#                 SELECT id, password_hash, is_active 
#                 FROM users 
#                 WHERE username = ? 
#                 LIMIT 1
#             """, (username,))
#             user = self.cursor.fetchone()
            
#             if not user:
#                 QMessageBox.warning(self, self.tr("Échec de connexion"),
#                                   self.tr("Identifiants incorrects"))
#                 return False
                
#             user_id, db_hash, is_active = user
            
#             if not is_active:
#                 QMessageBox.warning(self, self.tr("Compte désactivé"),
#                                   self.tr("Votre compte a été désactivé. Contactez le support."))
#                 return False
                
#             if db_hash != hashed_pwd:
#                 QMessageBox.warning(self, self.tr("Échec de connexion"),
#                                   self.tr("Identifiants incorrects"))
#                 return False
                
#             # Réinitialiser les tentatives échouées
#             self.cursor.execute("""
#                 UPDATE users 
#                 SET failed_attempts = 0, last_login = datetime('now')
#                 WHERE id = ?
#             """, (user_id,))
#             self.conn.commit()
            
#             return True
            
#         except sqlite3.Error as e:
#             print(f"Erreur DB: {e}")
#             return False

#     def update_failed_attempts(self, username):
#         """Met à jour le compteur de tentatives échouées"""
#         try:
#             self.cursor.execute("""
#                 UPDATE users 
#                 SET failed_attempts = failed_attempts + 1
#                 WHERE username = ?
#             """, (username,))
#             self.conn.commit()
#         except sqlite3.Error as e:
#             print(f"Erreur DB: {e}")

#     def create_user_session(self, username):
#         """Crée une session utilisateur dans la DB"""
#         try:
#             # Récupérer l'ID utilisateur
#             self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
#             user_id = self.cursor.fetchone()[0]
            
#             # Créer un token de session
#             session_token = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()
#             expires_at = (datetime.now() + timedelta(minutes=self.session_timeout)).strftime("%Y-%m-%d %H:%M:%S")
            
#             # Insérer la session
#             self.cursor.execute("""
#                 INSERT INTO sessions (user_id, session_token, expires_at)
#                 VALUES (?, ?, ?)
#             """, (user_id, session_token, expires_at))
            
#             self.conn.commit()
            
#             # Envoyer un email de notification
#             Mailer1().send_email(email_type="mail1")
            
#         except sqlite3.Error as e:
#             print(f"Erreur DB: {e}")

#     def show_welcome_message(self, username):
#         """Affiche le message de bienvenue"""
#         dialog = WelcomeDialog(username)
#         dialog.exec_()
        
#         QMessageBox.information(
#             self,
#             self.tr("🎉 Bienvenue chez Leopardo.ai!"),
#             self.tr(
#                 "<div style='background-color:#F0F8FF; padding:20px; border-radius:10px;'>"
#                 "<h1 style='color:#2E86C1; font-size:24px; text-align:center;'>Bienvenue, {}</h1>"
#                 # ... (votre message HTML existant) ...
#                 "</div>"
#             ).format(username)
#         )

#     def check_lockout_status(self):
#         """Vérifie si le verrouillage doit être levé"""
#         if self.lockout_time and datetime.now() >= self.lockout_time:
#             self.lockout_time = None
#             self.failed_attempts = 0
#             self.login_btn.setEnabled(True)
#             self.lockout_timer.stop()

#     def handle_password_recovery(self):
#         """Gère la récupération de mot de passe"""
#         email, ok = QInputDialog.getText(self, 
#                                        self.tr("Récupération de mot de passe"),
#                                        self.tr("Entrez votre email:"))
        
#         if ok and email:
#             try:
#                 self.cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
#                 if self.cursor.fetchone():
#                     # Envoyer un email de réinitialisation (simulé)
#                     Mailer1().send_email_to_user(user_email=email, email_type='password_reset')
#                     QMessageBox.information(self, self.tr("Succès"), 
#                                           self.tr("Un email de réinitialisation a été envoyé."))
#                 else:
#                     QMessageBox.warning(self, self.tr("Erreur"), 
#                                       self.tr("Aucun compte associé à cet email."))
#             except sqlite3.Error as e:
#                 print(f"Erreur DB: {e}")

#     def show_register_form(self):
#         """Affiche le formulaire d'inscription"""
#         self.register_module = RegisterModule()
#         self.register_module.show()
#         self.close()

#     def closeEvent(self, event):
#         """Gère la fermeture de la fenêtre"""
#         self.lockout_timer.stop()
#         self.conn.close()
#         super().closeEvent(event)

