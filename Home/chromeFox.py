import sqlite3
import sys
import os
import webbrowser
import subprocess
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QRadioButton, QButtonGroup, QDialog, QCheckBox, QFormLayout, QLineEdit, 
    QMessageBox, QGroupBox, QScrollArea, QComboBox, QFrame, QSizePolicy
)
import sqlite3
import sys
import os
import webbrowser
import subprocess
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QRadioButton, QButtonGroup, QDialog, QCheckBox, QFormLayout, QLineEdit, 
    QMessageBox, QGroupBox, QScrollArea, QComboBox, QFrame, QSizePolicy
)
from imports import DB_PATH_Home
class SecureBrowserConnect1(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 1000)
        self.setWindowTitle("Connexion Premium - Multi-Comptes")
        self.setWindowIcon(QIcon(":/icons/lock.png"))
        self.social_accounts = {}  # Initialisation précoce
        self.chrome_profiles = self.detect_chrome_profiles()  # Initialisation avant setup_ui
        self.init_db()
        self.setup_ui()

    def detect_chrome_profiles(self):
        """Détecte les profils Chrome disponibles"""
        profiles = ["Default"]  # Valeur par défaut
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        
        try:
            if os.path.exists(chrome_path):
                for item in os.listdir(chrome_path):
                    if item.startswith("Profile ") or item == "Default":
                        profiles.append(item)
        except Exception as e:
            print(f"Erreur détection profils Chrome: {str(e)}")
        
        return list(set(profiles))  # Élimine les doublons

    def init_db(self):
        roaming_path = os.getenv('APPDATA')
        resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
        # db_path = os.path.join(resources_folder, 'modules.db')
        db_path = DB_PATH_Home
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)

        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                active INTEGER DEFAULT 0,
                color TEXT DEFAULT '#FFFFFF'
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM modules")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO modules (name, active, color) VALUES (?, ?, ?)", [
                ("Facebook", 1, "#1877F2"),
                ("LinkedIn", 1, "#0A66C2"),
                ("WhatsApp", 1, "#25D366"),
                ("Instagram", 1, "#E4405F"),
                ("YouTube", 0, "#FF0000"),
                ("Pinterest", 0, "#E60023"),
                ("TikTok", 0, "#000000"),
                ("Twitter", 0, "#1DA1F2"),
            ])
        self.conn.commit()

    def setup_ui(self):
        # ... (le reste du code setup_ui reste inchangé)
        
        # Dans la section navigateur, utiliser self.chrome_profiles qui est maintenant initialisé
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.chrome_profiles)
        self.profile_combo.setCurrentText("Default")
        self.profile_combo.setEnabled(False)

        # ... (le reste du code)


class SecureBrowserConnect(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 1000)
        self.setWindowTitle("Connexion Premium - Multi-Comptes")
        self.setWindowIcon(QIcon(":/icons/lock.png"))
        self.social_accounts = {}  # Initialisation précoce
        self.chrome_profiles = self.detect_chrome_profiles()  # Initialisation avant setup_ui
        self.init_db()
        self.setup_ui()

    def __initL__(self):
        super().__init__()
        self.setFixedSize(900, 1000)
        self.setWindowTitle("Connexion Premium - Multi-Comptes")
        self.setWindowIcon(QIcon(":/icons/lock.png"))
        self.init_db()
        self.setup_ui()
        self.social_accounts = {}
        self.chrome_profiles = self.detect_chrome_profiles()
    def detect_chrome_profiles(self):
        """Détecte les profils Chrome disponibles"""
        profiles = ["Default"]  # Valeur par défaut
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        
        try:
            if os.path.exists(chrome_path):
                for item in os.listdir(chrome_path):
                    if item.startswith("Profile ") or item == "Default":
                        profiles.append(item)
        except Exception as e:
            print(f"Erreur détection profils Chrome: {str(e)}")
        
        return list(set(profiles))  # Élimine les doublons

    def init_db(self):
        roaming_path = os.getenv('APPDATA')
        resources_folder = os.path.join(roaming_path, 'saadiya', 'resources')
        # db_path = os.path.join(resources_folder, 'modules1.db')
        db_path = DB_PATH_Home
        if not os.path.exists(resources_folder):
            os.makedirs(resources_folder)

        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                active INTEGER DEFAULT 0,
                color TEXT DEFAULT '#FFFFFF'
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM modules")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO modules (name, active, color) VALUES (?, ?, ?)", [
                ("Facebook", 1, "#1877F2"),
                ("LinkedIn", 1, "#0A66C2"),
                ("WhatsApp", 1, "#25D366"),
                ("Instagram", 1, "#E4405F"),
                ("YouTube", 0, "#FF0000"),
                ("Pinterest", 0, "#E60023"),
                ("TikTok", 0, "#000000"),
                ("Twitter", 0, "#1DA1F2"),
            ])
        self.conn.commit()

    def setup_ui(self):
        # Configuration du style blanc premium
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                font-size: 16px;
                color: #555555;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 14px;
                min-width: 120px;
                border: 1px solid transparent;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QComboBox, QLineEdit {
                border: 1px solid #DDDDDD;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                min-height: 36px;
                background-color: #FAFAFA;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #DDDDDD;
                border-left-style: solid;
            }
            QScrollBar:vertical {
                border: none;
                background: #F5F5F5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                min-height: 20px;
                border-radius: 5px;
            }
            QRadioButton {
                spacing: 8px;
                font-size: 14px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header avec logo et titre
        header = QHBoxLayout()
        header.setSpacing(15)
        
        # Logo (remplacer par votre propre logo)
        logo = QLabel()
        logo.setPixmap(QIcon(":/icons/shield.png").pixmap(48, 48))
        header.addWidget(logo)
        
        title = QLabel("Connexion Premium")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #333333;")
        header.addWidget(title)
        header.addStretch()
        
        main_layout.addLayout(header)

        # Section navigateur
        browser_group = QGroupBox("Paramètres du Navigateur")
        browser_layout = QHBoxLayout(browser_group)
        
        # Sélection du navigateur
        browser_label = QLabel("Navigateur:")
        browser_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        self.chrome_radio = QRadioButton("Chrome")
        self.chrome_radio.setChecked(True)
        self.firefox_radio = QRadioButton("Firefox")
        
        # Sélection du profil Chrome
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(self.chrome_profiles)
        self.profile_combo.setCurrentText("Profil 1")
        self.profile_combo.setEnabled(False)  # Désactivé par défaut
        
        # Configurer la réactivité
        self.chrome_radio.toggled.connect(lambda: self.profile_combo.setEnabled(self.chrome_radio.isChecked()))
        
        browser_layout.addWidget(browser_label)
        browser_layout.addWidget(self.chrome_radio)
        browser_layout.addWidget(self.firefox_radio)
        browser_layout.addWidget(QLabel("Profil Chrome:"))
        browser_layout.addWidget(self.profile_combo)
        browser_layout.addStretch()
        
        config_button = QPushButton("Configurer")
        config_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333333;
                border: 1px solid #DDDDDD;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        config_button.clicked.connect(self.open_module_config)
        browser_layout.addWidget(config_button)
        
        main_layout.addWidget(browser_group)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #EEEEEE;")
        main_layout.addWidget(separator)

        # Zone de défilement pour les comptes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll.setWidget(scroll_content)
        
        main_layout.addWidget(scroll)

        # Charger les modules actifs
        self.load_active_modules()

    def detect_chrome_profiles(self):
        """Détecte les profils Chrome disponibles"""
        profiles = []
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        
        if os.path.exists(chrome_path):
            for item in os.listdir(chrome_path):
                if item.startswith("Profile ") or item == "Default":
                    profiles.append(item)
        
        return profiles if profiles else ["Default"]

    def check_accounts(self, social_name):
        """Vérifie les comptes disponibles pour un réseau social donné"""
        accounts = []
        
        # Mapping des dossiers
        folder_map = {
            "Facebook": "cbon",
            "WhatsApp": "wabon",
            "Instagram": "instabon"
        }
        
        folder_name = folder_map.get(social_name, None)
        if not folder_name:
            return [social_name]  # Retourne le nom de base si pas de dossier spécifique
        
        # Chemin du dossier dans AppData/Roaming
        roaming_path = os.getenv('APPDATA')
        target_folder = os.path.join(roaming_path, 'saadiya', folder_name)
        
        # Vérifier si le dossier existe
        if not os.path.exists(target_folder):
            return [social_name]
        
        # Vérifier les robots disponibles (de 1 à 10)
        for i in range(1, 11):
            robot_name = f"robot{i}"
            robot_path = os.path.join(target_folder, robot_name)
            if os.path.exists(robot_path):
                accounts.append(f"{social_name} {i}")
        
        return accounts if accounts else [social_name]

    def load_active_modules(self):
        # Effacer les widgets existants
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # URLs des réseaux sociaux
        module_urls = {
            "Facebook": "https://www.facebook.com",
            "LinkedIn": "https://www.linkedin.com",
            "WhatsApp": "https://web.whatsapp.com",
            "Instagram": "https://www.instagram.com",
            "YouTube": "https://www.youtube.com",
            "Pinterest": "https://www.pinterest.com",
            "TikTok": "https://www.tiktok.com",
            "Twitter": "https://twitter.com"
        }

        # Récupérer les modules actifs avec leurs couleurs
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, active, color FROM modules WHERE active = 1 ORDER BY name")
        active_modules = cursor.fetchall()

        for name, active, color in active_modules:
            accounts = self.check_accounts(name)
            
            # Créer un groupe pour ce réseau social
            group = QGroupBox(name)
            group.setStyleSheet(f"QGroupBox {{ color: {color}; }}")
            
            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(10)
            
            # Menu déroulant pour les comptes
            account_combo = QComboBox()
            account_combo.addItems(accounts)
            
            # Bouton de connexion avec la couleur du réseau social
            connect_btn = QPushButton("Se connecter")
            connect_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: {self.adjust_color(color, 20)};
                }}
                QPushButton:pressed {{
                    background-color: {self.adjust_color(color, -20)};
                }}
            """)
            
            # Connecter le bouton à la fonction d'ouverture
            if name == "LinkedIn":
                connect_btn.clicked.connect(self.show_linkedin_modal)
            else:
                connect_btn.clicked.connect(
                    lambda _, u=module_urls.get(name, "#"), n=name, c=account_combo: 
                    self.open_browser(u, n, c.currentText()))
            
            group_layout.addWidget(account_combo)
            group_layout.addWidget(connect_btn)
            
            self.scroll_layout.addWidget(group)

        # Ajouter un espace stretch à la fin
        self.scroll_layout.addStretch()

    def adjust_color(self, hex_color, amount):
        """Ajuste la luminosité d'une couleur hexadécimale"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        new_rgb = []
        for channel in rgb:
            new_channel = max(0, min(255, channel + amount))
            new_rgb.append(new_channel)
        
        return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

    def open_browser(self, url, social_name, account):
        """Ouvre le navigateur avec l'URL spécifiée pour le compte sélectionné"""
        try:
            if self.chrome_radio.isChecked():
                # Ouvrir Chrome avec le profil spécifique
                profile = self.profile_combo.currentText()
                chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
                
                # Personnaliser l'URL si nécessaire
                if "facebook" in url.lower() and account.lower() != "facebook":
                    account_num = account.split()[-1]
                    profile_url = f"https://www.facebook.com/profile.php?id={account_num}"
                else:
                    profile_url = url
                
                # Commande pour ouvrir Chrome avec le profil spécifique
                subprocess.Popen([
                    chrome_path,
                    f"--profile-directory={profile}",
                    profile_url
                ])
                
            else:
                # Ouvrir Firefox normalement
                webbrowser.get("firefox").open(url)
                
            self.show_status_message(f"Connexion à {account} réussie!")
            
        except Exception as e:
            self.show_error(f"Erreur d'ouverture: {str(e)}")

    def show_linkedin_modal(self):
        modal = LinkedInModal(self)
        if modal.exec_() == QDialog.Accepted:
            self.show_status_message("Connexion LinkedIn réussie!")

    def open_module_config(self):
        config_dialog = ModuleConfigDialog(self.conn, self)
        config_dialog.accepted.connect(self.load_active_modules)
        config_dialog.exec_()

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Erreur")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
        """)
        msg.exec_()

    def show_status_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Succès")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
        """)
        msg.exec_()

class ModuleConfigDialog(QDialog):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle("Configuration des Modules")
        self.setFixedSize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
        """)

        # Titre
        title = QLabel("Configuration des Réseaux Sociaux")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #555555; margin-bottom: 20px;")
        layout.addWidget(title)

        # Description
        desc = QLabel("Activez ou désactivez les réseaux sociaux disponibles dans l'application")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #777777; margin-bottom: 20px;")
        layout.addWidget(desc)

        # Zone de défilement
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Récupérer tous les modules
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, active, color FROM modules ORDER BY name")
        modules = cursor.fetchall()

        self.checkboxes = {}
        for name, active, color in modules:
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(5, 5, 5, 5)
            
            cb = QCheckBox(name)
            cb.setChecked(bool(active))
            cb.setStyleSheet(f"""
                QCheckBox {{
                    color: #333333;
                    font-size: 14px;
                    spacing: 10px;
                }}
                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                }}
            """)
            
            # Aperçu de la couleur
            color_label = QLabel()
            color_label.setFixedSize(20, 20)
            color_label.setStyleSheet(f"background-color: {color}; border: 1px solid #DDDDDD;")
            
            item_layout.addWidget(cb)
            item_layout.addWidget(color_label)
            item_layout.addStretch()
            
            scroll_layout.addWidget(item)
            self.checkboxes[name] = cb
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333333;
                border: 1px solid #DDDDDD;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def save_config(self):
        try:
            cursor = self.conn.cursor()
            for name, checkbox in self.checkboxes.items():
                active = 1 if checkbox.isChecked() else 0
                cursor.execute("UPDATE modules SET active = ? WHERE name = ?", (active, name))
            self.conn.commit()
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Configuration sauvegardée avec succès!")
            msg.setWindowTitle("Succès")
            msg.exec_()
            
            self.accept()
        except Exception as e:
            self.show_error(f"Erreur lors de la sauvegarde: {str(e)}")

    def show_error(self, message):
        QMessageBox.critical(self, "Erreur", message)

class LinkedInModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connexion LinkedIn")
        self.setFixedSize(450, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
        """)

        # Logo LinkedIn
        logo = QLabel()
        logo.setPixmap(QIcon(":/icons/linkedin.png").pixmap(48, 48))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Titre
        title = QLabel("Connexion à LinkedIn")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #0A66C2; margin-bottom: 20px;")
        layout.addWidget(title)

        # Formulaire
        form = QFormLayout()
        form.setSpacing(15)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email ou téléphone")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form.addRow("Email/Téléphone:", self.email_input)
        form.addRow("Mot de passe:", self.password_input)
        
        layout.addLayout(form)

        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333333;
                border: 1px solid #DDDDDD;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        login_btn = QPushButton("Se connecter")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0A66C2;
                color: white;
            }
            QPushButton:hover {
                background-color: #084d94;
            }
        """)
        login_btn.clicked.connect(self.attempt_login)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(login_btn)
        layout.addLayout(btn_layout)

    def attempt_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Champs manquants", "Veuillez remplir tous les champs")
            return
            
        # Simulation de connexion réussie
        QMessageBox.information(self, "Succès", "Connexion réussie à LinkedIn!")
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Définir la palette de couleurs pour un thème clair
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(240, 240, 240))
    palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = SecureBrowserConnect()
    window.show()
    sys.exit(app.exec_())