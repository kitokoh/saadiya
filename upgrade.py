import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QVBoxLayout, QWidget
)


def check_if_paid():
    # Dossiers à vérifier
    folders_to_check = [
        "c:\\bon\\robot1", "c:\\wabon\\robot1", "c:\\xbon\\robot1", "c:\\instabon\\robot1",
        "c:\\inbon\\robot", "c:\\bon\\ytbon\\robot1"
    ]

    # Modifier les dossiers pour les systèmes non-Windows
    if sys.platform == "darwin":  # macOS
        folders_to_check = [
            f"/Users/{os.getlogin()}/Documents/{folder.replace('\\', '/')}" for folder in folders_to_check
        ]
    elif sys.platform == "linux":  # Linux
        folders_to_check = [
            f"/home/{os.getlogin()}/{folder.replace('\\', '/')}" for folder in folders_to_check
        ]

    # Vérifier si "python.txt" existe dans l'un des dossiers
    for folder in folders_to_check:
        file_path = os.path.join(folder, "python.txt")
        if os.path.isfile(file_path):
            return True

    return False

class SpecialOfferWindow(QMainWindow):
    def __init__(self,main_app=None):
        super().__init__()
        self.setWindowTitle("Offre Spéciale")
        self.setGeometry(200, 200, 500, 400)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.main_app = main_app  # Stocke une référence à MainApp

        # Design principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Message d'offre spéciale
        label = QLabel("Vous utilisez actuellement la version gratuite. Passez à la version payante pour profiter de fonctionnalités exclusives et améliorées !")
        label.setFont(QFont("Arial", 12))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #333;")
        layout.addWidget(label)

        # Bouton pour passer au plan payant
        upgrade_button = QPushButton("Passer au plan payant")
        upgrade_button.setFont(QFont("Arial", 14, QFont.Bold))
        upgrade_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px; border-radius: 8px;"
            "border: none;"
        )
        upgrade_button.setCursor(Qt.PointingHandCursor)
        upgrade_button.clicked.connect(self.on_upgrade_click)
        layout.addWidget(upgrade_button)

        # Bouton pour fermer la fenêtre
        close_button = QPushButton("Fermer")
        close_button.setFont(QFont("Arial", 12))
        close_button.setStyleSheet(
            "background-color: #dc3545; color: white; padding: 8px; border-radius: 8px;"
            "border: none;"
        )
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Espacement
        layout.setSpacing(20)

    def on_upgrade_click(self):
        QMessageBox.information(self, "Merci !", "Merci de votre intérêt pour notre plan payant !")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not check_if_paid():
        # Afficher la fenêtre d'offre spéciale si le fichier n'existe pas
        window = SpecialOfferWindow()
        window.show()
    else:
        QMessageBox.information(None, "Vérification réussie", "Version payante détectée !")

    sys.exit(app.exec_())
