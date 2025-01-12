import json
import sys
import sqlite3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QWidget, QScrollArea, QMessageBox, QComboBox, QGraphicsOpacityEffect
)

class Nova360Ultimate(QMainWindow):
    def __init__(self, main_app=None):
        super().__init__()
        self.setWindowTitle("Leopardo - Expérience Ultime")
        self.setGeometry(100, 100, 1200, 800)
        self.main_app = main_app  # Stocke une référence à MainApp

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

        self.platforms = {
            "Facebook": ["Group Share", "Auto Comment", "Page Management"],
            "Twitter": ["Auto Tweet", "Hashtag Tracker", "Analytics"],
            "Instagram": ["Auto Post", "Story Scheduler", "Hashtag Analyzer"],
            # Ajouter d'autres plateformes ici...
        }

        # Database connection
        self.conn = sqlite3.connect('nova360.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.setup_ui()

    def create_tables(self):
        """Crée les tables si elles n'existen pas déjà."""
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
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la création de la table : {e}")

    def setup_ui(self):
        """Configuration de l'interface principale avec animations et engagement utilisateur."""
        main_layout = QVBoxLayout()

        # Titre principal avec animation de transparence
        self.title_label = QLabel("\u2728 Bienvenue sur Leopardo \u2728")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #007bff;")
        main_layout.addWidget(self.title_label)
        self.add_fade_animation(self.title_label, 2000)

        # Description motivante
        description = QLabel("\"Automatisez votre marketing comme jamais auparavant !\"")
        description.setFont(QFont("Arial", 16))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #6c757d;")
        main_layout.addWidget(description)

        # Animation GIF d'introduction
        gif_label = QLabel()
        gif = QMovie("welcome_animation.gif")  # Ajoutez un gif engageant ici
        gif_label.setMovie(gif)
        gif.start()
        main_layout.addWidget(gif_label)

        # Scroll Area pour choisir les plateformes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()

        for platform in self.platforms.keys():
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

        # Bouton de finalisation avec effet hover
        finalize_button = QPushButton("\U0001F680 Finaliser la Configuration")
        finalize_button.setFont(QFont("Arial", 16, QFont.Bold))
        finalize_button.setStyleSheet(
            "padding: 20px; background-color: #28a745; color: white; border-radius: 10px;"
            "hover { background-color: #218838; }"
        )
        finalize_button.clicked.connect(self.finalize_setup)
        main_layout.addWidget(finalize_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_modules(self, platform):
        """Afficher les modules pour une plateforme sélectionnée avec transitions."""
        self.user_data["bots"].setdefault(platform, [])

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel(f"\u2728 Modules disponibles pour {platform} \u2728")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        for module in self.platforms[platform]:
            button = QPushButton(module)
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(
                "padding: 15px; margin: 10px; background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 5px;"
            )
            button.clicked.connect(lambda _, m=module: self.add_module(platform, m))
            layout.addWidget(button)

        back_button = QPushButton("\u2B05 Retour")
        back_button.setFont(QFont("Arial", 14))
        back_button.setStyleSheet(
            "padding: 15px; background-color: #d9534f; color: white; border-radius: 5px;"
        )
        back_button.clicked.connect(self.setup_ui)
        layout.addWidget(back_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def add_module(self, platform, module):
        """Ajouter un module sélectionné."""
        if module not in self.user_data["bots"][platform]:
            self.user_data["bots"][platform].append(module)
            QMessageBox.information(self, "Module ajouté", f"\"{module}\" ajouté avec succès à {platform} !")

    def finalize_setup(self):
        """Finaliser la configuration et enregistrer les données dans la base de données SQLite."""
        try:
            # Sérialiser les données des bots et des modules
            bots_json = json.dumps(self.user_data["bots"])
            modules_json = json.dumps(self.user_data["modules"])

            # Insérer les données dans la base de données
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
            QMessageBox.information(
                self, "Succès", "\U0001F389 Vos paramètres ont été enregistrés avec succès !\U0001F389"
            )
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def add_fade_animation(self, widget, duration):
        """Ajouter une animation de fondu pour un widget."""
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        animation = QTimer()

        def fade():
            current_opacity = opacity_effect.opacity()
            if current_opacity > 0:
                opacity_effect.setOpacity(current_opacity - 0.01)
            else:
                animation.stop()

        animation.timeout.connect(fade)
        animation.start(duration // 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Nova360Ultimate()
    window.show()
    sys.exit(app.exec_())