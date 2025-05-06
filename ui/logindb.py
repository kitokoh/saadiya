import hashlib
import os
import sqlite3
from datetime import datetime, timedelta

from PyQt5.QtCore import Qt, QTranslator, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QMessageBox, QHBoxLayout, QFrame)

from Home.home import HomePage
from mail.mail_in_to_in import Mailer1
from translation import TranslatorManager
from ui.welcomeSyle import WelcomeDialog
from .carousel import CarouselWidget
from .register import RegisterModule

# Configuration des chemins
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
DB_PATH = os.path.join(user_data_dir, 'resources', 'data', 'leopardo.db')
SESSION_TIMEOUT = 144000  # 30 minutes en secondes

class DatabaseManager:
    """Gère la connexion à la base de données SQLite et les opérations CRUD."""
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas."""
        cursor = self.conn.cursor()
        
        # Table des utilisateurs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Table des sessions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        
        # Table des préférences
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en',
            theme TEXT DEFAULT 'light',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        
        self.conn.commit()

    def get_user(self, username):
        """Récupère un utilisateur par son nom d'utilisateur."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    def add_user(self, username, hashed_password, email=None):
        """Ajoute un nouvel utilisateur à la base de données."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, hashed_password, email)
            )
            user_id = cursor.lastrowid
            # Ajouter des préférences par défaut
            cursor.execute(
                "INSERT INTO preferences (user_id) VALUES (?)",
                (user_id,)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def create_session(self, user_id):
        """Crée une nouvelle session pour l'utilisateur."""
        cursor = self.conn.cursor()
        # D'abord désactiver toutes les sessions existantes pour cet utilisateur
        cursor.execute(
            "UPDATE sessions SET is_active = 0 WHERE user_id = ?",
            (user_id,)
        )
        
        # Créer une nouvelle session
        session_token = hashlib.sha256(f"{user_id}{datetime.now()}".encode()).hexdigest()
        expires_at = datetime.now() + timedelta(minutes=SESSION_TIMEOUT)
        
        cursor.execute(
            """INSERT INTO sessions 
            (user_id, session_token, expires_at) 
            VALUES (?, ?, ?)""",
            (user_id, session_token, expires_at)
        )
        self.conn.commit()
        return session_token

    def get_active_session(self, user_id):
        """Récupère la session active d'un utilisateur."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT id, session_token, expires_at 
            FROM sessions 
            WHERE user_id = ? AND is_active = 1 
            AND expires_at > datetime('now')""",
            (user_id,)
        )
        return cursor.fetchone()

    def update_session_activity(self, session_id):
        """Met à jour le timestamp de dernière activité d'une session."""
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE sessions 
            SET last_activity = datetime('now') 
            WHERE id = ?""",
            (session_id,)
        )
        self.conn.commit()

    def close_session(self, session_id):
        """Ferme une session spécifique."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE sessions SET is_active = 0 WHERE id = ?",
            (session_id,)
        )
        self.conn.commit()

    def get_user_preferences(self, user_id):
        """Récupère les préférences d'un utilisateur."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT language, theme FROM preferences WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchone()

    def update_user_preferences(self, user_id, language=None, theme=None):
        """Met à jour les préférences d'un utilisateur."""
        cursor = self.conn.cursor()
        updates = []
        params = []
        
        if language:
            updates.append("language = ?")
            params.append(language)
        if theme:
            updates.append("theme = ?")
            params.append(theme)
        
        if updates:
            params.append(user_id)
            query = f"UPDATE preferences SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, params)
            self.conn.commit()

    def __del__(self):
        self.conn.close()


class LoginModule(QWidget):
    connection_successful = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialisation de la base de données
        self.db = DatabaseManager()
        
        # Initialisation du traducteur
        self.translator = QTranslator()
        self.init_language()
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Variables de contrôle
        self.failed_attempts = 0
        self.max_attempts = 3

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        self.layout = QHBoxLayout(self)
        self.setStyleSheet("background-color: #F5F5F5;")

        # Carrousel d'images
        self.carousel_widget = CarouselWidget()
        self.layout.addWidget(self.carousel_widget)

        # Section du formulaire de connexion
        form_frame = QFrame(self)
        form_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(8px);
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        """)
        form_layout = QVBoxLayout(form_frame)

        # Titre du formulaire
        title_label = QLabel(self.tr("Connexion  Leopardo AI"))
        title_label.setFont(QFont("Roboto", 26, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #2D74DA;
            margin-bottom: 10px;
        """)
        form_layout.addWidget(title_label)

        # Sous-titre
        subtitle_label = QLabel(self.tr("Automatisez votre marketing avec une efficacité inégalée"))
        subtitle_label.setFont(QFont("Roboto", 13, QFont.Light))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            color: #777;
            margin-bottom: 15px;
            font-style: italic;
        """)
        form_layout.addWidget(subtitle_label)

        # Champ nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.tr("Nom d'utilisateur"))
        self.username_input.setStyleSheet("""
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #2D74DA;
            background-color: #F5F8FA;
            font-size: 15px;
            color: #333;
            transition: all 0.3s ease-in-out;
        """)
        form_layout.addWidget(self.username_input)

        # Champ mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.tr("Mot de passe"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        form_layout.addWidget(self.password_input)

        # Bouton de connexion
        self.login_button = QPushButton(self.tr("Se connecter"), self)
        self.login_button.setIcon(QIcon("resources/icons/house-key-icon-41543-Windows.ico"))
        self.login_button.setStyleSheet(self.button_style())
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)

        # Lien mot de passe oublié
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
        self.forgot_password_button.clicked.connect(self.reset_password)
        form_layout.addWidget(self.forgot_password_button)

        # Bouton création de compte
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
        self.signup_button.clicked.connect(self.create_account)
        form_layout.addWidget(self.signup_button)

        # Ajout du formulaire à la mise en page
        self.layout.addWidget(form_frame)

    def button_style(self):
        return """
            QPushButton {
                background-color: #2D74DA;
                color: white;
                padding: 14px 28px;
                border-radius: 40px;
                font-size: 16px;
                font-weight: bold;
                text-transform: uppercase;
                border: 2px solid red;
                transition: all 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: #1A59A0;
                transform: scale(1.05);
            }
        """

    def hash_password(self, password):
        """Hache le mot de passe avec SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(self, username, password):
        """Valide les entrées de l'utilisateur."""
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
        """Gère le processus de connexion."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not self.validate_input(username, password):
            return

        user = self.db.get_user(username)
        if user and user[2] == self.hash_password(password):
            # Créer une nouvelle session
            self.db.create_session(user[0])
            
            # Afficher le message de bienvenue
            dialog = WelcomeDialog(username)
            dialog.exec_()
            
            # Envoyer l'email de notification
            mailer = Mailer1()
            mailer.send_email(email_type="mail1")
            
            # Afficher le message de bienvenue stylisé
            self.show_welcome_message(username)
            
            # Émettre le signal de connexion réussie
            self.connection_successful.emit()
            self.close()
        else:
            self.failed_attempts += 1
            QMessageBox.warning(self, self.tr("Erreur"), self.tr("Nom d'utilisateur ou mot de passe incorrect."))
            if self.failed_attempts >= self.max_attempts:
                self.login_button.setEnabled(False)
                QMessageBox.warning(self, self.tr("Avertissement"), self.tr("Trop d'échecs de connexion. Veuillez réessayer plus tard."))

    def show_welcome_message(self, username):
        """Affiche un message de bienvenue stylisé."""
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

    def create_account(self):
        """Ouvre le module d'inscription."""
        self.register_module = RegisterModule(self.db)
        self.register_module.show()

    def reset_password(self):
        """Gère la réinitialisation du mot de passe."""
        QMessageBox.information(self, self.tr("Mot de passe oublié"), self.tr("Fonctionnalité non implémentée."))

    def init_language(self):
        """Initialise la langue par défaut."""
        preferences = self.db.get_user_preferences(1)  # Supposons que l'ID 1 est pour les préférences globales
        if preferences:
            self.switch_language(preferences[0])
        else:
            system_locale = QLocale.system().name()[:2]
            language_map = {'en': 'en', 'fr': 'fr', 'tr': 'tr', 'ar': 'ar', 'pt': 'pt'}
            selected_language = language_map.get(system_locale, 'en')
            self.switch_language(selected_language)

    def switch_language(self, language):
        """Change la langue de l'interface."""
        translation_path = os.path.join(user_data_dir, 'resources', 'lang', language, 'ui', 'login_translated.qm')
        if os.path.exists(translation_path):
            self.translator.load(translation_path)
            QApplication.instance().installTranslator(self.translator)
            self.retranslate_ui()

    def retranslate_ui(self):
        """Retraduit l'interface après un changement de langue."""
        # Implémentez la mise à jour des textes ici
        pass

    def logout(self):
        """Gère la déconnexion de l'utilisateur."""
        # Implémentez la logique de déconnexion ici
        pass

if __name__ == "__main__":
    app = QApplication([])
    login = LoginModule()
    login.show()
    app.exec_()

    