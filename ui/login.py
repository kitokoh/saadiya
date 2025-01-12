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

