import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QTranslator

class FolderVisibilityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.tr("Gestion de la Visibilité des Dossiers"))

        layout = QVBoxLayout()

        self.label = QLabel(self.tr("Entrez le chemin du dossier à rendre invisible :"))
        layout.addWidget(self.label)

        self.folder_input = QLineEdit(self)
        self.folder_input.setText("C:\\bon")  # Chemin par défaut
        layout.addWidget(self.folder_input)

        self.check_button = QPushButton(self.tr("Vérifier et Rendre Invisible"), self)
        self.check_button.clicked.connect(self.check_and_hide_folder)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def check_and_hide_folder(self):
        folder_path = self.folder_input.text()
        
        if os.path.exists(folder_path):
            # Commande pour rendre le dossier caché et système
            os.system(f'attrib +h +s "{folder_path}"')
            QMessageBox.information(self, self.tr("Succès"), self.tr(f"Le dossier '{folder_path}' est maintenant invisible."))
        else:
            QMessageBox.critical(self, self.tr("Erreur"), self.tr(f"Le dossier '{folder_path}' n'existe pas."))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Gestion de la traduction
    translator = QTranslator(app)
    translator.load("your_translation_file.qm")  # Chargez votre fichier de traduction
    app.installTranslator(translator)

    # Création et affichage de l'application
    ex = FolderVisibilityApp()
    ex.show()

    sys.exit(app.exec_())
