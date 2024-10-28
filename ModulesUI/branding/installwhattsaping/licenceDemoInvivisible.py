import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)

class FileHiderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cacher le Fichier")

        layout = QVBoxLayout()

        self.label = QLabel("Cliquez sur le bouton pour cacher le fichier python.txt.")
        layout.addWidget(self.label)

        self.hide_button = QPushButton("Cacher le Fichier", self)
        self.hide_button.clicked.connect(self.hide_file)
        layout.addWidget(self.hide_button)

        self.setLayout(layout)

    def hide_file(self):
        file_path = r"C:\bon\python.txt"

        # Vérification si le fichier existe
        if os.path.exists(file_path):
            # Affichage des attributs actuels du fichier avant modification
            current_attributes = os.popen(f'attrib "{file_path}"').read()
            print(f"Attributs avant modification : {current_attributes.strip()}")

            # Essayer de rendre le fichier caché et système
            os.system(f'attrib +h +s "{file_path}"')

            # Affichage des attributs après modification pour vérifier le changement
            new_attributes = os.popen(f'attrib "{file_path}"').read()
            print(f"Attributs après modification : {new_attributes.strip()}")

            QMessageBox.information(self, "Succès", 
                                    "Le fichier python.txt est maintenant caché.")
        else:
            QMessageBox.critical(self, "Erreur", 
                                 "Le fichier python.txt n'existe pas dans C:\\bon!")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Création et affichage de l'application
    ex = FileHiderApp()
    ex.show()

    sys.exit(app.exec_())
