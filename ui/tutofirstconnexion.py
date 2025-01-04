import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")
config_file = os.path.join(user_data_dir, "resources", "settings.json")

class TutorialApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Vérifiez si c'est la première utilisation
        self.is_first_use = self.check_first_use()

        # Configuration de l'interface
        self.init_ui()

        if self.is_first_use:
            self.start_tutorial()

    def init_ui(self):
        self.setWindowTitle("Mon Application")
        self.setGeometry(100, 100, 800, 600)

        # Créer un label pour afficher un texte de base
        label = QLabel("Bienvenue dans l'application !", self)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def check_first_use(self):
        """Vérifie si c'est la première fois que l'application est lancée."""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                settings = json.load(f)
                return settings.get("first_use", True)
        else:
            # Si le fichier n'existe pas, c'est la première utilisation
            return True

    def start_tutorial(self):
        """Affiche une série de boîtes de dialogue pour guider l'utilisateur."""
        self.show_welcome_message()
        self.show_feature_highlight()

        # Après la fin du tutoriel, marquer l'application comme non première utilisation
        self.mark_tutorial_completed()

    def show_welcome_message(self):
        """Affiche le message de bienvenue."""
        welcome_msg = QMessageBox(self)
        welcome_msg.setIcon(QMessageBox.Information)
        welcome_msg.setWindowTitle("Bienvenue")
        welcome_msg.setText("Bienvenue dans notre application ! Nous allons vous guider à travers les fonctionnalités principales.")
        welcome_msg.setStandardButtons(QMessageBox.Ok)
        welcome_msg.exec_()

    def show_feature_highlight(self):
        """Affiche une info-bulle pour une fonctionnalité clé."""
        feature_msg = QMessageBox(self)
        feature_msg.setIcon(QMessageBox.Information)
        feature_msg.setWindowTitle("Fonctionnalité clé")
        feature_msg.setText("Cette application vous permet de gérer vos médias et groupes de manière simplifiée. Cliquez sur le bouton pour commencer.")
        feature_msg.setStandardButtons(QMessageBox.Ok)
        feature_msg.exec_()

    def mark_tutorial_completed(self):
        """Marque que la visite guidée est terminée pour cette installation."""
        settings = {"first_use": False}
        if not os.path.exists(os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        with open(config_file, 'w') as f:
            json.dump(settings, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TutorialApp()
    window.show()
    sys.exit(app.exec_())
