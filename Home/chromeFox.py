import sys
import sqlite3
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton,
    QButtonGroup, QDialog, QCheckBox, QFormLayout, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt



class SecureBrowserConnect(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 800)
        self.setWindowTitle("Connexion Sécurisée")
        self.setWindowIcon(QIcon("lock_icon.png"))  # Custom icon
        self.init_db()
        self.setup_ui()

    def init_db(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect("modules.db")
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                active INTEGER DEFAULT 0
            )
        """)
        # Add default modules if the table is empty
        cursor.execute("SELECT COUNT(*) FROM modules")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO modules (name, active) VALUES (?, ?)", [
                ("Facebook", 1),
                ("LinkedIn", 0),
                ("WhatsApp", 0),
                ("Instagram", 0),
                ("YouTube", 0),
                ("Pinterest", 0),
                ("TikTok", 0),
                ("WordPress", 0),
            ])
        self.conn.commit()

    def setup_ui(self):
        # Main layout configuration
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Global style for the UI
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;  /* Dark blue */
                color: #ffffff;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #00bcd4;  /* Cyan */
                color: #1e1e2f;  /* Dark blue */
                border-radius: 10px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5dcff3;  /* Light cyan */
            }
            QPushButton:pressed {
                background-color: #008ba3;  /* Darker cyan */
            }
            QRadioButton {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00bcd4;
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        # Title section
        title = QLabel("Connexion Sécurisée")
        title.setFont(QFont("Arial", 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);")
        #main_layout.addWidget(title)

        # Subtitle section
        subtitle = QLabel("Bienvenue ! Connectez-vous à vos services préférés en toute sécurité.")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #dddddd;")
        #main_layout.addWidget(subtitle)

        # Browser selection layout
        browser_layout = QHBoxLayout()
        browser_label = QLabel("Navigateur :")
        browser_label.setFont(QFont("Arial", 16))

        self.chrome_radio = QRadioButton("Chrome")
        self.chrome_radio.setFont(QFont("Arial", 14))
        self.chrome_radio.setChecked(True)

        self.firefox_radio = QRadioButton("Firefox")
        self.firefox_radio.setFont(QFont("Arial", 14))

        # Grouping the radio buttons
        browser_group = QButtonGroup(self)
        browser_group.addButton(self.chrome_radio)
        browser_group.addButton(self.firefox_radio)

        # Button to configure modules
        config_button = QPushButton("Configurer Modules")
        config_button.setFont(QFont("Arial", 14))
        config_button.clicked.connect(self.open_module_config)

        # Adding widgets to the browser layout
        browser_layout.addWidget(browser_label)
        browser_layout.addWidget(self.chrome_radio)
        browser_layout.addWidget(self.firefox_radio)
        browser_layout.addStretch()
        browser_layout.addWidget(config_button)

        main_layout.addLayout(browser_layout)

        # Section for dynamic buttons
        self.buttons_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_layout)

        # Load active modules dynamically
        self.load_active_modules()


    def load_active_modules(self):
        # Clear old widgets
        for i in reversed(range(self.buttons_layout.count())):
            item = self.buttons_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        # Define module URLs
        module_urls = {
            "Facebook": "https://www.facebook.com",
            "LinkedIn": "https://www.linkedin.com",
            "WhatsApp": "https://web.whatsapp.com",
            "Instagram": "https://www.instagram.com",
            "YouTube": "https://www.youtube.com",
            "Pinterest": "https://www.pinterest.com",
            "TikTok": "https://www.tiktok.com",
            "WordPress": "https://wordpress.com"
        }
        # Fetch active modules from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, active FROM modules WHERE active = 1")
        active_modules = cursor.fetchall()

        for name, active in active_modules:
            social_widget = QWidget()
            social_layout = QHBoxLayout(social_widget)

            label = QLabel(f"{name}")
            label.setFont(QFont("Arial", 18))
            label.setStyleSheet("color: #80deea;")

            connect_button = QPushButton("Se connecter")
        #    connect_button.clicked.connect(lambda _, u=module_urls.get(name, "#"): self.open_browser(u))
            if name == "LinkedIn":
                 connect_button.clicked.connect(self.show_linkedin_modal)

#                connect_button.clicked.connect(self.show_linkedin_modal)
            else:
                connect_button.clicked.connect(lambda _, u=module_urls.get(name, "#"): self.open_browser(u))


                    
            status_indicator = QLabel("🔴")
            status_indicator.setFont(QFont("Arial", 20))

            social_layout.addWidget(label)
            social_layout.addWidget(connect_button)
            social_layout.addWidget(status_indicator)

            self.buttons_layout.addWidget(social_widget)

    def open_browser(self, url):
        browser = "chrome" if self.chrome_radio.isChecked() else "firefox"

        try:
            if browser == "chrome":
                webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(url)
            elif browser == "firefox":
                webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s").open(url)
        except webbrowser.Error as e:
            self.show_error(f"{browser.capitalize()} non trouvé. Assurez-vous qu'il est installé.\n{str(e)}")
    def show_linkedin_modal(self):
        print("show_linkedin_modal called")  # Débogage
        modal = LinkedInModal(self)
        modal.exec_()
    # def show_linkedin_modal(self):
    #     # Modal window for LinkedIn
    #     modal = QDialog(self)
    #     modal.setWindowTitle("LinkedIn Configuration")
    #     modal.exec_()

    def open_module_config(self):
        # Open modal dialog to configure modules
        config_dialog = ModuleConfigDialog(self.conn, self)
        config_dialog.accepted.connect(self.load_active_modules)
        config_dialog.exec_()

    def show_error(self, message):
        QMessageBox.critical(self, "Erreur", message)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())


class ModuleConfigDialog(QDialog):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.parent = parent

        self.setWindowTitle("Configurer Modules")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Activer/Désactiver Modules")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00bcd4;")  # Cyan
        layout.addWidget(title)

        # Form layout for checkboxes
        self.form_layout = QFormLayout()
        self.checkboxes = {}

        self.load_modules()
        layout.addLayout(self.form_layout)

        # Save button
        save_button = QPushButton("Enregistrer")
        save_button.setStyleSheet("""
            QPushButton {
                background: #00e676;  /* Vert */
                color: black;
                border-radius: 10px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #66ffa6;  /* Vert clair */
            }
        """)
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

    def load_modules(self):
        """
        Charge les modules depuis la base de données et les affiche sous forme de cases à cocher.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name, active FROM modules")
            modules = cursor.fetchall()

            if not modules:
                empty_label = QLabel("Aucun module trouvé.")
                empty_label.setStyleSheet("color: #ff9800;")  # Orange
                empty_label.setAlignment(Qt.AlignCenter)
                self.form_layout.addRow(empty_label)
                return

            for name, active in modules:
                checkbox = QCheckBox(name)
                checkbox.setChecked(bool(active))
                checkbox.setStyleSheet("color: white;")  # Blanc
                self.checkboxes[name] = checkbox
                self.form_layout.addRow(name, checkbox)

        except Exception as e:
            error_label = QLabel(f"Erreur lors du chargement des modules: {e}")
            error_label.setStyleSheet("color: #f44336;")  # Rouge
            error_label.setAlignment(Qt.AlignCenter)
            self.form_layout.addRow(error_label)

    def save_config(self):
        """
        Sauvegarde l'état des modules dans la base de données.
        """
        try:
            cursor = self.conn.cursor()
            for name, checkbox in self.checkboxes.items():
                active = 1 if checkbox.isChecked() else 0
                cursor.execute("UPDATE modules SET active = ? WHERE name = ?", (active, name))
            self.conn.commit()
            QMessageBox.information(self, "Succès", "Configuration sauvegardée avec succès !")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {e}")



class LinkedInModal(QDialog):
    """
    Modal futuriste pour la connexion LinkedIn.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setWindowTitle("Connexion LinkedIn")
        self.setFixedSize(450, 350)
        self.setStyleSheet("background-color: #1e1e2f; color: #ffffff;")  # Fond sombre futuriste
        self.setup_ui()

    def setup_ui(self):
        """
        Configure l'interface utilisateur.
        """
        layout = QVBoxLayout(self)

        # Titre
        title = QLabel("🔗 Connexion LinkedIn")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4caf50; margin-bottom: 20px;")  # Vert brillant
        layout.addWidget(title)

        # Formulaire
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 10, 20, 10)
        form_layout.setSpacing(15)

        # Champ Nom d'utilisateur
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d44; color: #ffffff;
                padding: 10px; border-radius: 8px; border: 2px solid #4caf50;
            }
            QLineEdit:focus {
                border: 2px solid #00e676;
            }
        """)
        form_layout.addRow("Nom d'utilisateur :", self.username_input)

        # Champ Mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d44; color: #ffffff;
                padding: 10px; border-radius: 8px; border: 2px solid #4caf50;
            }
            QLineEdit:focus {
                border: 2px solid #00e676;
            }
        """)
        form_layout.addRow("Mot de passe :", self.password_input)

        layout.addLayout(form_layout)

        # Bouton Enregistrer
        save_button = QPushButton("🔒 Connexion")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #00e676; color: black;
                border-radius: 10px; padding: 12px;
                font-size: 16px; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66ffa6;
            }
            QPushButton:pressed {
                background-color: #00c853;
            }
        """)
        save_button.clicked.connect(self.save_credentials)
        layout.addWidget(save_button)

    def save_credentials(self):
        """
        Enregistre les données après validation.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            QMessageBox.information(
                self,
                "Succès",
                "Connexion réussie ! Bienvenue sur LinkedIn.",
                QMessageBox.Ok
            )
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez remplir tous les champs avant de continuer.",
                QMessageBox.Ok
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SecureBrowserConnect()
    window.show()
    sys.exit(app.exec_())
