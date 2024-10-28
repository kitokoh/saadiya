import sys
import os
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class FolderVisibilityApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Gestionnaire de Visibilité de Dossiers")
        self.setGeometry(680, 390, 400, 200)
        self.setWindowIcon(QIcon("folder_visible.png"))  # Icône personnalisée pour la visibilité du dossier

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Label d'information
        self.info_label = QLabel("Cliquez pour vérifier et rendre visible le dossier.", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Bouton pour rendre visible le dossier
        self.show_button = QPushButton("Vérifier et Rendre Visible", self)
        self.show_button.clicked.connect(self.show_folder)
        self.layout.addWidget(self.show_button)

        # Appliquer la mise en page
        self.setLayout(self.layout)

    def show_folder(self):
        folder_path = "C:\\bon"

        # Vérifier si le dossier existe
        if os.path.exists(folder_path):
            try:
                # Rendre le dossier visible en retirant les attributs +h et +s
                ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x80)  # Attribut pour le rendre visible
                self.info_label.setText("Le dossier C:\\bon est maintenant visible.")
                QMessageBox.information(self, "Succès", "Le dossier C:\\bon est maintenant visible.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de rendre le dossier visible : {str(e)}")
        else:
            self.info_label.setText("Le dossier C:\\bon n'existe pas.")
            QMessageBox.warning(self, "Erreur", "Le dossier C:\\bon n'existe pas.")

def main():
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre
    window = FolderVisibilityApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
