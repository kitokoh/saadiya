# content/content.py
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Section des boutons du milieu
        self.create_feature_buttons()
        self.create_duplicate_buttons()
        self.create_footer()

    def create_feature_buttons(self):
        # Layout pour les icônes et boutons du milieu
        middle_layout = QHBoxLayout()

        # Liste des fonctionnalités avec leurs icônes et couleur
        features = [
            ("FB Robot Pro", "resources/icons/facebook-icon-png-770.png", "#E91E63"),
            ("WhatsApping", "resources/icons/whatsapp-512.png", "#4CAF50"),
            ("Blogging", "resources/icons/article-marketing-3-512.gif", "#4CAF50"),
            ("Insta Pro", "resources/icons/pink-message-icon-12055.png", "#4CAF50"),
            ("Ads Pro", "resources/icons/promotion-icon-png-3422.png", "#4CAF50"),
            ("Branding", "resources/icons/robotic-process-automation.png", "#4CAF50"),
            ("Emailing", "resources/icons/pink-message-icon-12045.png", "#4CAF50"),
        ]

        # Ajouter des boutons avec animation et icônes dynamiques
        for text, icon, color in features:
            button = self.create_button(text, icon, color)
            middle_layout.addWidget(button)

        self.main_layout.addLayout(middle_layout)

    def create_duplicate_buttons(self):
        duplicate_layout = QHBoxLayout()

        duplicate_features = [
            ("Twitter Bot", "resources/icons/twitter-icon.png", "#1DA1F2"),
            ("LinkedIn Pro", "resources/icons/linkedin-icon.png", "#0077B5"),
            ("Pinterest Bot", "resources/icons/pinterest-icon.png", "#BD081C"),
            ("Snapchat Bot", "resources/icons/snapchat-icon.png", "#FFFC00"),
            ("TikTok Pro", "resources/icons/tiktok-icon.png", "#010101"),
            ("Reddit Bot", "resources/icons/reddit-icon.png", "#FF4500"),
            ("YouTube Pro", "resources/icons/youtube-icon.png", "#FF0000"),
        ]

        for text, icon, color in duplicate_features:
            button = self.create_button(text, icon, color)
            duplicate_layout.addWidget(button)

        self.main_layout.addLayout(duplicate_layout)

    def create_button(self, text, icon_path, color):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14))  # Taille de police réduite
        button.setIcon(QIcon(QPixmap(icon_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: 2px solid #CCCCCC;
                border-radius: 15px;
                padding: 10px;
                min-width: 150px;
                min-height: 150px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
                transform: scale(1.05); 
            }}
            QPushButton:pressed {{
                background-color: {color};
            }}
        """)
        button.clicked.connect(lambda _, btn=text: self.show_message(btn))
        return button

    def lighten_color(self, color):
        # Fonction pour éclaircir une couleur
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def show_message(self, button_text):
        # Afficher un message lorsque l'un des boutons est cliqué
        QMessageBox.information(self, "Info", f"Vous avez cliqué sur {button_text}!")


