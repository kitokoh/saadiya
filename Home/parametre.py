import json
import os
import sys
import sqlite3
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QMovie, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QScrollArea, QMessageBox, QLineEdit, QFormLayout, QComboBox,
    QGraphicsOpacityEffect, QCheckBox, QListWidget, QListWidgetItem
)


class Nova360Ultimate(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.setWindowTitle("Leopardo - Ultimate Experience")
        self.setGeometry(100, 100, 1200, 800)
        self.main_app = main_app  # Référence à l'application principale

        # Données utilisateur
        self.user_data = {
            "bots": {},
            "modules": {},
            "info": {
                "name": "",
                "email": "",
                "role": ""
            }
        }

        # Plateformes et modules disponibles
        self.platforms = {
            "Faceboo": ["Group Share", "Auto Comment", "Page Management"],
            "Twitter": ["Auto Tweet", "Hashtag Tracker", "Analytics"],
            "Instagram": ["Auto Post", "Story Scheduler", "Hashtag Analyzer"],
            # Ajouter d'autres plateformes ici...
        }

        # Chemin de la base de données
        self.db_path = self.get_database_path()
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Charger les préférences utilisateur si elles existent
        self.load_user_preferences()

        # Configuration de l'interface utilisateur
        self.setup_ui()

    def get_database_path(self):
        """Retourne le chemin de la base de données."""
        roaming_path = os.path.join(os.getenv('APPDATA'), "saadiya", "resources")
        os.makedirs(roaming_path, exist_ok=True)
        return os.path.join(roaming_path, "nova360.db")

    def create_tables(self):
        """Crée les tables si elles n'existent pas déjà."""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    role TEXT,
                    bots TEXT,
                    modules TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def load_user_preferences(self):
        """Charge les préférences utilisateur depuis la base de données."""
        try:
            self.cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result:
                self.user_data["info"]["name"] = result[1]
                self.user_data["info"]["email"] = result[2]
                self.user_data["info"]["role"] = result[3]
                self.user_data["bots"] = json.loads(result[4])
                self.user_data["modules"] = json.loads(result[5])
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Warning", f"Failed to load user preferences: {e}")

    def setup_ui(self):
        """Configure l'interface utilisateur."""
        main_layout = QVBoxLayout()

        # Titre principal avec animation
        self.title_label = QLabel("\u2728 Welcome to Leopardo \u2728")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #007bff;")
        main_layout.addWidget(self.title_label)
        self.add_fade_animation(self.title_label, 2000)

        # Description
        description = QLabel("\"Automate your marketing like never before!\"")
        description.setFont(QFont("Arial", 16))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #6c757d;")
        main_layout.addWidget(description)

        # Animation GIF
        gif_label = QLabel()
        gif = QMovie("welcome_animation.gif")  # Assurez-vous d'avoir ce fichier
        gif_label.setMovie(gif)
        gif.start()
        main_layout.addWidget(gif_label)

        # Formulaire pour les informations utilisateur
        user_form = QFormLayout()
        self.name_input = QLineEdit(self.user_data["info"]["name"])
        self.email_input = QLineEdit(self.user_data["info"]["email"])
        self.role_input = QComboBox()
        self.role_input.addItems(["Admin", "User", "Guest"])
        self.role_input.setCurrentText(self.user_data["info"]["role"])

        user_form.addRow("Name:", self.name_input)
        user_form.addRow("Email:", self.email_input)
        user_form.addRow("Role:", self.role_input)
        main_layout.addLayout(user_form)

        # Scroll Area pour les plateformes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout()

        # Afficher uniquement les plateformes non configurées
        for platform in self.platforms.keys():
            if platform not in self.user_data["bots"]:
                button = QPushButton(f"\u25B6 {platform}")
                button.setFont(QFont("Arial", 14))
                button.setStyleSheet(
                    "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #007bff; border-radius: 10px;"
                )
                button.clicked.connect(lambda _, p=platform: self.show_modules(p))
                content_layout.addWidget(button)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Bouton de finalisation
        finalize_button = QPushButton("\U0001F680 Finalize Configuration")
        finalize_button.setFont(QFont("Arial", 16, QFont.Bold))
        finalize_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
            "hover { background-color: #218838; }"
        )
        finalize_button.clicked.connect(self.finalize_setup)
        main_layout.addWidget(finalize_button)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_modules(self, platform):
        """Affiche les modules pour une plateforme sélectionnée."""
        self.current_platform = platform
        self.user_data["bots"].setdefault(platform, [])

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel(f"\u2728 Available Modules for {platform} \u2728")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Liste des modules avec des cases à cocher
        self.module_list = QListWidget()
        for module in self.platforms[platform]:
            item = QListWidgetItem(module)
            item.setCheckState(Qt.Unchecked)
            if module in self.user_data["bots"][platform]:
                item.setCheckState(Qt.Checked)
            self.module_list.addItem(item)
        layout.addWidget(self.module_list)

        # Bouton pour confirmer les choix
        confirm_button = QPushButton("\U0001F44D Confirm Selection")
        confirm_button.setFont(QFont("Arial", 14))
        confirm_button.setStyleSheet(
            "padding: 15px; background-color: #007bff; color: white; border-radius: 5px;"
        )
        confirm_button.clicked.connect(self.save_modules)
        layout.addWidget(confirm_button)

        # Bouton pour revenir au menu principal
        back_button = QPushButton("\u2B05 Back")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(
            "padding: 15px; background-color: #d9534f; color: white; border-radius: 5px;"
        )
        back_button.clicked.connect(self.setup_ui)
        layout.addWidget(back_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def save_modules(self):
        """Sauvegarde les modules sélectionnés pour la plateforme actuelle."""
        selected_modules = []
        for index in range(self.module_list.count()):
            item = self.module_list.item(index)
            if item.checkState() == Qt.Checked:
                selected_modules.append(item.text())

        self.user_data["bots"][self.current_platform] = selected_modules
        self.show_summary()

    def show_summary(self):
        """Affiche un résumé des choix de l'utilisateur."""
        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("\u2728 Your Selections \u2728")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Afficher les choix
        summary_label = QLabel()
        summary_text = ""
        for platform, modules in self.user_data["bots"].items():
            summary_text += f"<b>{platform}:</b><br>"
            for module in modules:
                summary_text += f" - {module}<br>"
            summary_text += "<br>"
        summary_label.setText(summary_text)
        summary_label.setFont(QFont("Arial", 14))
        layout.addWidget(summary_label)

        # Bouton pour terminer
        finish_button = QPushButton("\U0001F680 Finish")
        finish_button.setFont(QFont("Arial", 16, QFont.Bold))
        finish_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
        )
        finish_button.clicked.connect(self.setup_ui)
        layout.addWidget(finish_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def finalize_setup(self):
        """Finalise la configuration et enregistre les données."""
        try:
            self.user_data["info"]["name"] = self.name_input.text()
            self.user_data["info"]["email"] = self.email_input.text()
            self.user_data["info"]["role"] = self.role_input.currentText()

            bots_json = json.dumps(self.user_data["bots"])
            modules_json = json.dumps(self.user_data["modules"])

            self.cursor.execute('''
                INSERT INTO users (name, email, role, bots, modules)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.user_data["info"]["name"],
                self.user_data["info"]["email"],
                self.user_data["info"]["role"],
                bots_json,
                modules_json
            ))
            self.conn.commit()
            QMessageBox.information(self, "Success", "\U0001F389 Settings saved successfully!\U0001F389")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")

    def add_fade_animation(self, widget, duration):
        """Ajoute une animation de fondu."""
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Nova360Ultimate()
    window.show()
    sys.exit(app.exec_())