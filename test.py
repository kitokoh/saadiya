import os
import sys
import json
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QCheckBox, QFrame)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices, QIcon, QPixmap

# Configuration des chemins
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "LeopardoAI")
os.makedirs(user_data_dir, exist_ok=True)

class LocalAuth:
    """Système d'authentification locale avec SQLite"""
    def __init__(self):
        self.db_path = os.path.join(user_data_dir, "users.db")
        self.init_db()
    
    def init_db(self):
        """Initialise la base de données SQLite"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    email_verified BOOLEAN DEFAULT 0,
                    license_type TEXT DEFAULT 'trial',
                    license_expiry TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            conn.commit()
    
    def hash_password(self, password, salt=None):
        """Hash un mot de passe avec salt"""
        if not salt:
            salt = secrets.token_hex(16)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000), salt
    
    def create_user(self, username, email, password, license_type='trial'):
        """Crée un nouvel utilisateur local"""
        password_hash, salt = self.hash_password(password)
        license_expiry = datetime.now() + timedelta(days=180)  # 6 mois
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """INSERT INTO users 
                    (username, email, password_hash, salt, license_type, license_expiry)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (username, email, password_hash, salt, license_type, license_expiry)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError as e:
                if "username" in str(e):
                    raise ValueError("Nom d'utilisateur déjà utilisé")
                elif "email" in str(e):
                    raise ValueError("Email déjà utilisé")
                raise ValueError("Erreur de création de compte")
    
    def verify_user(self, username_or_email, password):
        """Vérifie les identifiants d'un utilisateur"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, password_hash, salt FROM users 
                WHERE username = ? OR email = ?""",
                (username_or_email, username_or_email)
            )
            result = cursor.fetchone()
            
            if not result:
                raise ValueError("Identifiants incorrects")
            
            user_id, stored_hash, salt = result
            input_hash, _ = self.hash_password(password, salt)
            
            if input_hash != stored_hash:
                raise ValueError("Identifiants incorrects")
            
            # Mettre à jour la dernière connexion
            cursor.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now(), user_id)
            )
            conn.commit()
            
            return user_id
    
    def create_session(self, user_id, remember_me=False):
        """Crée une nouvelle session"""
        session_token = secrets.token_urlsafe(64)
        expires_at = datetime.now() + timedelta(days=180 if remember_me else 7)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)",
                (user_id, session_token, expires_at)
            )
            conn.commit()
        
        return session_token, expires_at
    
    def validate_session(self, session_token):
        """Valide une session existante"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT user_id, expires_at FROM sessions 
                WHERE session_token = ? AND expires_at > ?""",
                (session_token, datetime.now())
            )
            result = cursor.fetchone()
            
            if not result:
                return None
                
            user_id, expires_at = result
            return user_id

class FirebaseAuth:
    """Wrapper pour l'authentification Firebase avec gestion des erreurs"""
    def __init__(self):
        self.initialized = False
        self.initialize()
    
    def initialize(self):
        """Initialise Firebase si les credentials sont disponibles"""
        cred_path = os.path.join(user_data_dir, "firebase_credentials.json")
        
        if not os.path.exists(cred_path):
            return False
        
        try:
            import firebase_admin
            from firebase_admin import credentials, auth
            from firebase_admin import exceptions as firebase_exceptions
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            self.auth = auth
            self.exceptions = firebase_exceptions
            self.initialized = True
            return True
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            return False
    
    def create_user(self, email, password, display_name=None):
        """Crée un utilisateur Firebase"""
        if not self.initialized:
            raise RuntimeError("Firebase non initialisé")
        
        try:
            user = self.auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return user.uid
        except self.exceptions.FirebaseError as e:
            print(f"Firebase error: {e}")
            raise ValueError(self._translate_firebase_error(e))
    
    def _translate_firebase_error(self, error):
        """Traduit les erreurs Firebase en messages utilisateur"""
        if "email-already-exists" in str(error):
            return "Cet email est déjà utilisé"
        elif "invalid-email" in str(error):
            return "Email invalide"
        elif "weak-password" in str(error):
            return "Mot de passe trop faible (min 6 caractères)"
        else:
            return "Erreur d'authentification Firebase"

class AuthWindow(QMainWindow):
    """Fenêtre principale d'authentification"""
    login_success = pyqtSignal(int)  # user_id
    
    def __init__(self):
        super().__init__()
        self.local_auth = LocalAuth()
        self.firebase_auth = FirebaseAuth()
        self.current_user = None
        
        self.setWindowTitle("Leopardo AI - Authentification")
        self.setFixedSize(800, 600)
        
        self.init_ui()
        self.check_existing_session()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left Panel - Branding
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #2D74DA;")
        left_panel.setFixedWidth(350)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 60, 40, 60)
        
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(":/icons/logo").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Leopardo AI")
        title_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("Solution complète d'automatisation marketing")
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addStretch()
        
        # Right Panel - Login Form
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 80, 60, 80)
        
        form_title = QLabel("Connectez-vous")
        form_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email ou nom d'utilisateur")
        self.username_input.setStyleSheet("padding: 12px; border: 1px solid #ddd; border-radius: 4px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        
        self.remember_check = QCheckBox("Se souvenir de moi")
        self.remember_check.setStyleSheet("color: #666;")
        
        login_btn = QPushButton("Connexion")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D74DA;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563C2;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        
        right_layout.addWidget(form_title)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.username_input)
        right_layout.addWidget(self.password_input)
        right_layout.addWidget(self.remember_check)
        right_layout.addWidget(login_btn)
        right_layout.addStretch()
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        self.setCentralWidget(main_widget)
    
    def check_existing_session(self):
        """Vérifie s'il existe une session valide"""
        session_file = os.path.join(user_data_dir, "session.json")
        if os.path.exists(session_file):
            try:
                with open(session_file) as f:
                    session_data = json.load(f)
                    user_id = self.local_auth.validate_session(session_data["token"])
                    if user_id:
                        self.login_success.emit(user_id)
                        self.close()
            except Exception as e:
                print(f"Erreur de lecture de session: {e}")
    
    def handle_login(self):
        """Gère la tentative de connexion"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Champs manquants", "Veuillez remplir tous les champs")
            return
        
        try:
            # Tentative de connexion locale
            user_id = self.local_auth.verify_user(username, password)
            
            # Création de session
            session_token, expires_at = self.local_auth.create_session(
                user_id, 
                self.remember_check.isChecked()
            )
            
            # Sauvegarde de la session
            self.save_session(session_token, expires_at)
            
            # Synchronisation avec Firebase si disponible
            if self.firebase_auth.initialized:
                self.sync_with_firebase(user_id, username, password)
            
            self.login_success.emit(user_id)
            self.close()
            
        except ValueError as e:
            QMessageBox.warning(self, "Erreur de connexion", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue: {e}")
    
    def save_session(self, token, expires_at):
        """Sauvegarde les infos de session"""
        session_data = {
            "token": token,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.now().isoformat()
        }
        
        session_file = os.path.join(user_data_dir, "session.json")
        with open(session_file, "w") as f:
            json.dump(session_data, f)
    
    def sync_with_firebase(self, user_id, username, password):
        """Synchronise le compte local avec Firebase"""
        try:
            with sqlite3.connect(self.local_auth.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT email FROM users WHERE id = ?", 
                    (user_id,)
                )
                email = cursor.fetchone()[0]
                
                # Créer ou mettre à jour le compte Firebase
                firebase_uid = self.firebase_auth.create_user(email, password, username)
                
                # Mettre à jour la référence Firebase dans la base locale
                cursor.execute(
                    "UPDATE users SET firebase_uid = ? WHERE id = ?",
                    (firebase_uid, user_id)
                )
                conn.commit()
                
        except Exception as e:
            print(f"Échec de la synchronisation Firebase: {e}")

def main():
    app = QApplication(sys.argv)
    
    # Vérifier et créer le répertoire d'application
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    
    # Vérifier la présence des credentials Firebase
    firebase_cred_path = os.path.join(user_data_dir, "firebase_credentials.json")
    if not os.path.exists(firebase_cred_path):
        # Donner des instructions pour obtenir les credentials
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Configuration requise")
        msg.setText(
            "Pour activer toutes les fonctionnalités, veuillez:\n\n"
            "1. Aller sur la console Firebase\n"
            "2. Télécharger le fichier de configuration\n"
            "3. Le placer dans:\n"
            f"{firebase_cred_path}"
        )
        msg.addButton(QPushButton("Ouvrir la console Firebase"), QMessageBox.ActionRole)
        msg.addButton(QPushButton("Continuer sans Firebase"), QMessageBox.RejectRole)
        
        result = msg.exec_()
        
        if result == QMessageBox.ActionRole:
            QDesktopServices.openUrl(QUrl("https://console.firebase.google.com/"))
    
    # Démarrer l'application
    auth_window = AuthWindow()
    auth_window.show()
    
    def on_login_success(user_id):
        print(f"Utilisateur connecté: {user_id}")
        # Ici vous ouvririez votre application principale
    
    auth_window.login_success.connect(on_login_success)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()