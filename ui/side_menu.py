from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRect, QEasingCurve
from translation import TranslatorManager  # Importer le gestionnaire de traductions
from imports import *
class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
                # Initialiser le traducteur
        self.translator = QTranslator()
        self.init_language()  # Initialisation de la langue après la création des actions

        self.setVisible(False)
                # Initialiser et charger les traductions
        self.translator_manager = TranslatorManager()
        self.translator_manager.load_translations()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 80, 200, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #4CAF50; /* Couleur de fond principale */
                border: 1px solid #388E3C; /* Bordure pour un meilleur contraste */
                border-radius: 10px; /* Coins arrondis */
            }
            QPushButton {
                background-color: #66BB6A; /* Couleur des boutons */
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
                border-radius: 5px; /* Coins arrondis pour les boutons */
            }
            QPushButton:hover {
                background-color: #81C784; /* Couleur au survol */
            }
        """)

        layout = QVBoxLayout(self)
        side_buttons = [
            (self.tr("Accueil"), "resources/icons/home-icon.png"),
            (self.tr("Paramètres"), "resources/icons/settings-icon.png"),
            (self.tr("Aide"), "resources/icons/help-icon.png"),
            (self.tr("À propos"), "resources/icons/info-icon.png"),
            (self.tr("Quitter"), "resources/icons/exit-icon.png"),
        ]

        for text, icon in side_buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            button.setIconSize(QPixmap(icon).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation).size())
            layout.addWidget(button)
