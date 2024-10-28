# import sys
# import os
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
# )

# class FileUnhiderApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Rendre le Fichier Visible")

#         layout = QVBoxLayout()

#         self.label = QLabel("Cliquez sur le bouton pour rendre le fichier python.txt visible.")
#         layout.addWidget(self.label)

#         self.unhide_button = QPushButton("Rendre le Fichier Visible", self)
#         self.unhide_button.clicked.connect(self.unhide_file)
#         layout.addWidget(self.unhide_button)

#         self.setLayout(layout)

#     def unhide_file(self):
#         file_path = r"C:\bon\python.txt"

#         # Vérification si le fichier existe
#         if os.path.exists(file_path):
#             # Affichage des attributs actuels du fichier avant modification
#             current_attributes = os.popen(f'attrib "{file_path}"').read()
#             print(f"Attributs avant modification : {current_attributes.strip()}")

#             # Essayer de rendre le fichier visible (enlever les attributs caché et système)
#             os.system(f'attrib -h -s "{file_path}"')

#             # Affichage des attributs après modification pour vérifier le changement
#             new_attributes = os.popen(f'attrib "{file_path}"').read()
#             print(f"Attributs après modification : {new_attributes.strip()}")

#             #QMessageBox.information(self, "Succès", 
#              #                       "Le fichier python.txt est maintenant visible.")
#         else:
#             QMessageBox.critical(self, "Erreur", 
#                                  "Le fichier python.txt n'existe pas dans C:\\bon!")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     # Création et affichage de l'application
#     ex = FileUnhiderApp()
#     ex.show()

#     sys.exit(app.exec_())
import os

def unhide_file(file_path):
    # Vérification si le fichier existe
    if os.path.exists(file_path):
        # Affichage des attributs actuels du fichier avant modification
        current_attributes = os.popen(f'attrib "{file_path}"').read()
        print(f"Attributs avant modification : {current_attributes.strip()}")

        # Essayer de rendre le fichier visible (enlever les attributs caché et système)
        os.system(f'attrib -h -s "{file_path}"')

        # Affichage des attributs après modification pour vérifier le changement
        new_attributes = os.popen(f'attrib "{file_path}"').read()
        print(f"Attributs après modification : {new_attributes.strip()}")
    else:
        print(f"Erreur : Le fichier {file_path} n'existe pas dans C:\\bon!")

def main():
    file_path = r"C:\bon\python.txt"  # Chemin du fichier à rendre visible
    unhide_file(file_path)

if __name__ == '__main__':
    main()  # Appelle la fonction main si le script est exécuté directement
