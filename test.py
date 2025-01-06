import json
from PyQt5.QtWidgets import (
    QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QProgressBar, QWidget, QApplication
)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.settings_file = "settings.json"  # Chemin vers le fichier JSON
        self.load_settings()

        duplicate_features = [
            ("Twitter Bot", "resources/icons/aquicon-icon-18708-Windows.ico", "#1DA1F2", self.open_twitter, "twitter_bot"),
            ("LinkedIn Pro", "resources/icons/aquicon-icon-18717-Windows.ico", "#0077B5", self.open_linkedin, "linkedin_bot"),
            ("Pinterest Bot", "resources/icons/subscribe-png-574-Windows.ico", "#BD081C", self.open_pinterest, "pinterest_bot"),
            ("Snapchat Bot", "resources/icons/snapchat-icon-1707-Windows.ico", "#FFFC00", self.open_snapchat, "snapchat_bot"),
            ("TikTok Pro", "resources/icons/camera-icon-59-Windows.ico", "#010101", self.open_tiktok, "tiktok_bot"),
            ("Reddit Bot", "resources/icons/camera-icon-59-Windows.ico", "#FF4500", self.open_reddit, "reddit_bot"),
            ("YouTube Pro", "resources/icons/youtube-logo-png-3580-Windows.ico", "#FF0000", self.open_youtube, "youtube_bot"),
        ]

        duplicate_layout = QHBoxLayout()

        self.buttons = {}
        for text, icon, color, func, setting_key in duplicate_features:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setIcon(QIcon(QPixmap(icon).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
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
                    border: 2px solid #AAAAAA;
                    margin: -2px;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    border: 2px solid #888888;
                    padding: 12px;
                }}
            """)

            # Vérifie si le module est activé ou non
            button.setEnabled(self.settings.get(setting_key, False))
            button.clicked.connect(lambda _, f=func, k=setting_key: self.handle_button_click(f, k))

            self.buttons[setting_key] = button
            duplicate_layout.addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(duplicate_layout)
        self.setLayout(main_layout)

    def load_settings(self):
        """Charge les paramètres depuis le fichier JSON."""
        try:
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = {}

    def save_settings(self):
        """Enregistre les paramètres dans le fichier JSON."""
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def handle_button_click(self, func, setting_key):
        """Gère le clic sur un bouton."""
        if self.settings.get(setting_key, False):
            func()
        else:
            self.show_activation_popup(setting_key)

    def show_activation_popup(self, setting_key):
        """Affiche un popup pour activer un module."""
        reply = QMessageBox.question(
            self, "Activation requise",
            f"Le module '{setting_key}' est désactivé. Voulez-vous l'activer ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.activate_module(setting_key)

    def activate_module(self, setting_key):
        """Active un module avec une barre de progression."""
        progress_dialog = QProgressBar(self)
        progress_dialog.setRange(0, 100)
        progress_dialog.setValue(0)
        progress_dialog.show()

        def update_progress():
            value = progress_dialog.value() + 10
            if value > 100:
                progress_dialog.close()
                self.settings[setting_key] = True
                self.save_settings()
                self.buttons[setting_key].setEnabled(True)
            else:
                progress_dialog.setValue(value)

        timer = QTimer(self)
        timer.timeout.connect(update_progress)
        timer.start(300)

    def lighten_color(self, color):
        """Éclaircit une couleur en hexadécimal."""
        r = min(int(color[1:3], 16) + 30, 255)
        g = min(int(color[3:5], 16) + 30, 255)
        b = min(int(color[5:], 16) + 30, 255)
        return f"#{r:02X}{g:02X}{b:02X}"

    # Exemple de fonctions pour les boutons
    def open_twitter(self):
        print("Twitter Bot activé")

    def open_linkedin(self):
        print("LinkedIn Bot activé")

    def open_pinterest(self):
        print("Pinterest Bot activé")

    def open_snapchat(self):
        print("Snapchat Bot activé")

    def open_tiktok(self):
        print("TikTok Bot activé")

    def open_reddit(self):
        print("Reddit Bot activé")

    def open_youtube(self):
        print("YouTube Bot activé")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
