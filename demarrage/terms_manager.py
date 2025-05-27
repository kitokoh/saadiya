import sys
import sqlite3
import hashlib
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QTextBrowser, 
                            QCheckBox, QPushButton, QFrame, QLabel, QMessageBox,
                            QHBoxLayout, QSpacerItem, QSizePolicy, QAction)
from PyQt5.QtCore import Qt, QDateTime, QTimer, QPropertyAnimation, QRect, QByteArray
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog
import socket
import platform
from cryptography.fernet import Fernet
import json
from datetime import datetime
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QTextDocument
from PyQt5.QtPrintSupport import QPrinter

class TermsManager:
    """Classe pour gérer le chiffrement et la configuration"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager()
        return cls._instance
    
    def _init_manager(self):
        self.config_path = Path.home() / ".leopardo" / "config"
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        # Charger ou générer la clé de chiffrement
        self.key_file = self.config_path / "encryption.key"
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
        else:
            key = self.key_file.read_bytes()
        
        self.cipher = Fernet(key)
    
    def encrypt_data(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        return self.cipher.decrypt(encrypted_data).decode()
    
    @property
    def terms_version(self):
        return "2.3.1"  # À remplacer par votre système de versionning

class TermsDialog(QDialog):
    def __init__(self, parent=None, user_id=None, force_show=False):
        super().__init__()
        self.manager = TermsManager()
        self.user_id = user_id or "guest"
        self.setup_ui()
        self.setup_db()
        
        # Vérifier si l'utilisateur a déjà accepté les dernières conditions
        if not force_show and self.check_already_accepted():
            self.accept()
            return
            
        self.exec_()
    
    def setup_ui(self):
        self.setWindowTitle("Conditions d'Utilisation - Léopardo AI")
        self.setWindowIcon(QIcon("leopardo_icon.png"))
        self.resize(900, 700)
        
        # Détecter le thème système
        self.dark_mode = self.is_dark_mode()
        self.apply_style()
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # En-tête avec animation
        self.header = QFrame()
        self.header.setObjectName("header")
        header_layout = QVBoxLayout()
        
        self.title = QLabel("Conditions d'Utilisation de Léopardo AI")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        
        self.subtitle = QLabel(f"Version {self.manager.terms_version} - {QDateTime.currentDateTime().toString('dd/MM/yyyy')}")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.subtitle)
        self.header.setLayout(header_layout)
        layout.addWidget(self.header)
        
        # Texte des conditions
        self.terms_browser = QTextBrowser()
        self.terms_browser.setOpenExternalLinks(True)
        self.load_terms_content()
        layout.addWidget(self.terms_browser)
        
        # Case à cocher avec animation
        self.accept_checkbox = QCheckBox("J'ai lu et j'accepte les conditions d'utilisation")
        self.accept_checkbox.setObjectName("acceptCheckbox")
        self.accept_checkbox.stateChanged.connect(self.toggle_accept_button)
        layout.addWidget(self.accept_checkbox)
        
        # Boutons
        button_frame = QFrame()
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        # Bouton Imprimer
        self.print_button = QPushButton("Imprimer")
        self.print_button.setObjectName("printButton")
        self.print_button.clicked.connect(self.print_terms)
        button_layout.addWidget(self.print_button)
        
        # Bouton Refuser
        self.decline_button = QPushButton("Refuser et Quitter")
        self.decline_button.setObjectName("declineButton")
        self.decline_button.clicked.connect(self.reject)
        button_layout.addWidget(self.decline_button)
        
        # Bouton Accepter
        self.accept_button = QPushButton("Accepter et Continuer")
        self.accept_button.setObjectName("acceptButton")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.on_accept)
        button_layout.addWidget(self.accept_button)
        
        button_frame.setLayout(button_layout)
        layout.addWidget(button_frame)
        
        self.setLayout(layout)
        
        # Menu contextuel
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        print_action = QAction("Imprimer les conditions", self)
        print_action.triggered.connect(self.print_terms)
        self.addAction(print_action)
        
        # Animation d'apparition
        self.start_animation()
    
    def apply_style(self):
        base_style = """
            QDialog {
                background-color: $BG_COLOR;
            }
            QTextBrowser {
                background-color: $TEXT_BG;
                color: $TEXT_COLOR;
                border: 1px solid $BORDER_COLOR;
                border-radius: 8px;
                padding: 12px;
                font-size: 12px;
            }
            QCheckBox {
                font-size: 14px;
                padding: 12px 0;
                color: $TEXT_COLOR;
            }
            QPushButton {
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton#printButton {
                background-color: $PRINT_BG;
                color: $PRINT_COLOR;
            }
            QPushButton#printButton:hover {
                background-color: $PRINT_BG_HOVER;
            }
            QPushButton#declineButton {
                background-color: $DECLINE_BG;
                color: $DECLINE_COLOR;
            }
            QPushButton#declineButton:hover {
                background-color: $DECLINE_BG_HOVER;
            }
            QPushButton#acceptButton {
                background-color: $ACCEPT_BG;
                color: $ACCEPT_COLOR;
            }
            QPushButton#acceptButton:hover {
                background-color: $ACCEPT_BG_HOVER;
            }
            QPushButton#acceptButton:disabled {
                background-color: $ACCEPT_BG_DISABLED;
            }
            QFrame#header {
                background-color: $HEADER_BG;
                border-radius: 8px;
                padding: 15px;
            }
            QLabel#title {
                color: $TITLE_COLOR;
                font-size: 18px;
                font-weight: bold;
            }
            QLabel#subtitle {
                color: $SUBTITLE_COLOR;
                font-size: 12px;
                margin-top: 5px;
            }
        """
        
        if self.dark_mode:
            style = base_style.replace("$BG_COLOR", "#1e1e2e") \
                             .replace("$TEXT_BG", "#2e2e3e") \
                             .replace("$TEXT_COLOR", "#e0e0e0") \
                             .replace("$BORDER_COLOR", "#3e3e4e") \
                             .replace("$PRINT_BG", "#3e3e4e") \
                             .replace("$PRINT_COLOR", "#ffffff") \
                             .replace("$PRINT_BG_HOVER", "#4e4e5e") \
                             .replace("$DECLINE_BG", "#7f1d1d") \
                             .replace("$DECLINE_COLOR", "#ffffff") \
                             .replace("$DECLINE_BG_HOVER", "#991b1b") \
                             .replace("$ACCEPT_BG", "#1e3a8a") \
                             .replace("$ACCEPT_COLOR", "#ffffff") \
                             .replace("$ACCEPT_BG_HOVER", "#1e40af") \
                             .replace("$ACCEPT_BG_DISABLED", "#64748b") \
                             .replace("$HEADER_BG", "#4338ca") \
                             .replace("$TITLE_COLOR", "#ffffff") \
                             .replace("$SUBTITLE_COLOR", "#d4d4d8")
        else:
            style = base_style.replace("$BG_COLOR", "#f5f7fa") \
                             .replace("$TEXT_BG", "#ffffff") \
                             .replace("$TEXT_COLOR", "#111827") \
                             .replace("$BORDER_COLOR", "#d1d5db") \
                             .replace("$PRINT_BG", "#e5e7eb") \
                             .replace("$PRINT_COLOR", "#111827") \
                             .replace("$PRINT_BG_HOVER", "#d1d5db") \
                             .replace("$DECLINE_BG", "#ef4444") \
                             .replace("$DECLINE_COLOR", "#ffffff") \
                             .replace("$DECLINE_BG_HOVER", "#dc2626") \
                             .replace("$ACCEPT_BG", "#4f46e5") \
                             .replace("$ACCEPT_COLOR", "#ffffff") \
                             .replace("$ACCEPT_BG_HOVER", "#4338ca") \
                             .replace("$ACCEPT_BG_DISABLED", "#a5b4fc") \
                             .replace("$HEADER_BG", "#4f46e5") \
                             .replace("$TITLE_COLOR", "#ffffff") \
                             .replace("$SUBTITLE_COLOR", "#e5e7eb")
        
        self.setStyleSheet(style)
    
    def is_dark_mode(self):
        """Détecte si le système est en mode sombre"""
        palette = self.palette()
        return palette.window().color().lightness() < 128
    
    def start_animation(self):
        """Animation d'apparition de la fenêtre"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
    
    def load_terms_content(self):
        """Charge le contenu des conditions directement depuis une chaîne HTML"""
        terms_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    color: #4f46e5;
                    border-bottom: 2px solid #4f46e5;
                    padding-bottom: 8px;
                    margin-top: 24px;
                }}
                h2 {{
                    color: #4338ca;
                    margin-top: 20px;
                }}
                h3 {{
                    color: #3730a3;
                }}
                ul, ol {{
                    padding-left: 24px;
                }}
                li {{
                    margin-bottom: 8px;
                }}
                strong {{
                    color: #111827;
                }}
                .version {{
                    background-color: #e0e7ff;
                    color: #3730a3;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                .highlight {{
                    background-color: #fef3c7;
                    padding: 2px 4px;
                    border-radius: 4px;
                }}
                .note {{
                    border-left: 4px solid #4f46e5;
                    padding-left: 12px;
                    margin: 16px 0;
                    font-style: italic;
                    color: #6b7280;
                }}
            </style>
        </head>
        <body>
            <h1>Conditions d'Utilisation de Léopardo AI</h1>
            
            <p><strong>Version <span class="version">{self.manager.terms_version}</span> - Date d'effet : {QDateTime.currentDateTime().toString('dd/MM/yyyy')}</strong></p>
            
            <div class="note">
                En utilisant Léopardo AI, vous acceptez ces conditions d'utilisation. 
                Veuillez les lire attentivement avant d'utiliser notre application.
            </div>
            
            <h2>1. Acceptation des Conditions</h2>
            <p>En accédant ou en utilisant Léopardo AI, vous acceptez d'être lié par ces conditions. 
            Si vous n'acceptez pas toutes ces conditions, vous ne pouvez pas utiliser notre application.</p>
            
            <h2>2. Description du Service</h2>
            <p>Léopardo AI est une plateforme tout-en-un pour les professionnels du marketing offrant :</p>
            <ul>
                <li>Gestion et planification des publications sur les réseaux sociaux</li>
                <li>Organisation centralisée des médias marketing</li>
                <li>Bibliothèque de descriptions réutilisables</li>
                <li>Module de gestion des prospects (pre-CRM)</li>
                <li>Fonctionnalités de publication assistée</li>
                <li>Stockage <span class="highlight">100% local</span> de vos données</li>
            </ul>
            
            <h2>3. Compte Utilisateur</h2>
            <p>Pour accéder à certaines fonctionnalités, vous devrez créer un compte. Vous êtes responsable :</p>
            <ul>
                <li>De la confidentialité de vos identifiants</li>
                <li>De l'exactitude des informations fournies</li>
                <li>De toutes les activités sur votre compte</li>
            </ul>
            
            <h2>4. Protection des Données</h2>
            <p>Nous accordons une importance particulière à la protection de vos données :</p>
            <ul>
                <li>Toutes vos données restent stockées sur votre appareil</li>
                <li>Aucune donnée marketing n'est collectée par nos serveurs</li>
                <li>Les données sensibles sont chiffrées</li>
            </ul>
            
            <h2>5. Responsabilités</h2>
            <p>Vous vous engagez à :</p>
            <ul>
                <li>Respecter les lois en vigueur et les conditions des plateformes sociales</li>
                <li>Ne pas publier de contenu illégal, diffamatoire ou nuisible</li>
                <li>Superviser les publications automatisées</li>
            </ul>
            
            <h2>6. Tarification et Paiement</h2>
            <p>L'application propose différents plans :</p>
            <ul>
                <li><strong>Standard</strong> : 19€/mois (fonctionnalités de base)</li>
                <li><strong>Pro</strong> : 39€/mois (fonctionnalités avancées + support prioritaire)</li>
                <li><strong>Entreprise</strong> : Sur devis (solutions personnalisées)</li>
            </ul>
            
            <h2>7. Modifications des Conditions</h2>
            <p>Nous pouvons modifier ces conditions. Les utilisateurs seront notifiés et devront 
            accepter les nouvelles conditions pour continuer à utiliser le service.</p>
            
            <h2>8. Contact</h2>
            <p>Pour toute question concernant ces conditions :</p>
            <ul>
                <li>Email : legal@leopardo.ai</li>
                <li>Support dans l'application</li>
            </ul>
            
            <div class="note">
                En acceptant ces conditions, vous reconnaissez avoir lu, compris et accepté 
                l'intégralité de ce document. Cette acceptation sera enregistrée avec la date 
                et l'heure de votre consentement.
            </div>
        </body>
        </html>
        """
        
        self.terms_browser.setHtml(terms_html)
    
    def setup_db(self):
        """Initialise la base de données chiffrée"""
        db_path = Path.home() / ".leopardo" / "user_data.db"
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        
        # Créer les tables si elles n'existent pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms_acceptance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                acceptance_date TEXT NOT NULL,
                terms_version TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                encrypted_data BLOB
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT NOT NULL,
                change_date TEXT NOT NULL,
                changes_summary TEXT
            )
        """)
        
        self.conn.commit()
    
    def check_already_accepted(self):
        """Vérifie si l'utilisateur a déjà accepté la dernière version"""
        self.cursor.execute("""
            SELECT 1 FROM terms_acceptance 
            WHERE user_id = ? AND terms_version = ?
            ORDER BY acceptance_date DESC 
            LIMIT 1
        """, (self.user_id, self.manager.terms_version))
        
        return self.cursor.fetchone() is not None
    
    def get_system_info(self):
        """Récupère les informations système pour l'audit"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "127.0.0.1"
        
        user_agent = f"{platform.system()} {platform.release()}; {platform.machine()}"
        
        return ip_address, user_agent
    
    def toggle_accept_button(self, state):
        """Active/désactive le bouton d'acceptation avec animation"""
        self.accept_button.setEnabled(state == Qt.Checked)
        
        if state == Qt.Checked:
            anim = QPropertyAnimation(self.accept_button, b"geometry")
            anim.setDuration(200)
            anim.setStartValue(QRect(self.accept_button.x(), self.accept_button.y(), 
                               self.accept_button.width(), self.accept_button.height()))
            anim.setEndValue(QRect(self.accept_button.x()-5, self.accept_button.y()-5, 
                             self.accept_button.width()+10, self.accept_button.height()+10))
            anim.start()
    
    def print_terms(self):
        """Imprime les conditions d'utilisation"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QDialog.Accepted:
            document = QTextDocument()
            document.setHtml(self.terms_browser.toHtml())
            document.print_(printer)
    
    def on_accept(self):
        """Enregistre l'acceptation dans la base de données"""
        acceptance_date = QDateTime.currentDateTime().toString(Qt.ISODate)
        ip_address, user_agent = self.get_system_info()
        
        # Données supplémentaires à stocker (chiffrées)
        extra_data = {
            "screen_resolution": f"{self.width()}x{self.height()}",
            "color_scheme": "dark" if self.dark_mode else "light",
            "system_language": "fr"  # À adapter
        }
        
        encrypted_data = self.manager.encrypt_data(json.dumps(extra_data))
        
        try:
            self.cursor.execute("""
                INSERT INTO terms_acceptance 
                (user_id, acceptance_date, terms_version, ip_address, user_agent, encrypted_data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.user_id, acceptance_date, self.manager.terms_version, 
                 ip_address, user_agent, encrypted_data))
            
            self.conn.commit()
            
            # Animation de succès
            self.animate_acceptance()
            
            # Fermer après l'animation
            QTimer.singleShot(1000, self.accept)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement : {str(e)}")
    
    def animate_acceptance(self):
        """Animation lorsque l'utilisateur accepte"""
        self.accept_button.setText("✓ Accepté !")
        
        # Animation de couleur
        anim = QPropertyAnimation(self.accept_button, b"styleSheet")
        anim.setDuration(1000)
        anim.setStartValue(f"background-color: {'#10b981' if self.dark_mode else '#059669'};")
        anim.setEndValue(self.styleSheet())
        anim.start()
    
    def closeEvent(self, event):
        """Ferme proprement la connexion à la base de données"""
        self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Définir une police moderne
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Inter")
    app.setFont(font)
    
    # Exemple d'utilisation
    dialog = TermsDialog(user_id="test_user", force_show=True)
    
    if dialog.result() == QDialog.Accepted:
        print("Conditions acceptées")
    else:
        print("Conditions refusées")
        sys.exit()