import os
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class FolderVisibilityApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de l'interface
        self.setWindowTitle("Vérification de la visibilité du dossier")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Bienvenue dans l'application de vérification de dossier.")
        layout.addWidget(self.label)

        self.check_folder_button = QtWidgets.QPushButton("Vérifier et rendre le dossier visible")
        self.check_folder_button.clicked.connect(self.check_and_make_visible)
        layout.addWidget(self.check_folder_button)

        self.setLayout(layout)

    def check_and_make_visible(self):
        folder_path = "C:\\bon"

        # Vérifie si le dossier existe
        if os.path.exists(folder_path):
            self.toggle_folder_visibility(folder_path)
        else:
            QMessageBox.critical(self, "Erreur", "Le dossier C:\\bon n'existe pas!")

    def toggle_folder_visibility(self, folder_path):
        # Enlève les attributs caché et système
        os.system(f'attrib -h -s "{folder_path}"')
        QMessageBox.information(self, "Succès", "Le dossier C:\\bon est maintenant visible.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = FolderVisibilityApp()
    main_window.show()
    sys.exit(app.exec_())
