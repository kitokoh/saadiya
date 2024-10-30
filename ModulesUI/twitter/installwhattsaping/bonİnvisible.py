# import sys
# import os
# import ctypes
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# class FolderHiderApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Configuration de la fenêtre principale
#         self.setWindowTitle("Gestionnaire de Dossiers Cachés")
#         self.setGeometry(680, 390, 400, 200)
#         self.setWindowIcon(QIcon("folder.png"))  # Icône pour un style visuel attractif

#         # Mise en page principale
#         self.layout = QVBoxLayout()

#         # Label d'information
#         self.info_label = QLabel("Cliquez pour vérifier et cacher le dossier.", self)
#         self.info_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.info_label)

#         # Bouton pour cacher le dossier
#         self.hide_button = QPushButton("Vérifier et Cacher", self)
#         self.hide_button.clicked.connect(self.hide_folder)
#         self.layout.addWidget(self.hide_button)

#         # Appliquer la mise en page
#         self.setLayout(self.layout)

#     def hide_folder(self):
#         folder_path = "C:\\bon"

#         # Vérifier si le dossier existe
#         if os.path.exists(folder_path):
#             try:
#                 # Cacher le dossier avec les attributs +h et +s
#                 ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x02 | 0x04)
#                 self.info_label.setText("Le dossier C:\\bon est maintenant caché.")
#                 #QMessageBox.information(self, "Succès", "Le dossier C:\\bon est maintenant caché.")
#             except Exception as e:
#                 QMessageBox.critical(self, "Erreur", f"Impossible de cacher le dossier : {str(e)}")
#         else:
#             self.info_label.setText("Le dossier C:\\bon n'existe pas.")
#             QMessageBox.warning(self, "Erreur", "Le dossier C:\\bon n'existe pas.")

# def main():
#     app = QApplication(sys.argv)
    
#     # Créer et afficher la fenêtre
#     window = FolderHiderApp()
#     window.show()

#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()
import os
import ctypes

def hide_folder():
    """Vérifie si le dossier existe et le cache."""
    folder_path = "C:\\bon"

    # Vérifier si le dossier existe
    if os.path.exists(folder_path):
        try:
            # Cacher le dossier avec les attributs +h (hidden) et +s (system)
            ctypes.windll.kernel32.SetFileAttributesW(folder_path, 0x02 | 0x04)
            print(f"Le dossier {folder_path} est maintenant caché.")
        except Exception as e:
            print(f"Erreur : Impossible de cacher le dossier. Détails : {str(e)}")
    else:
        print(f"Erreur : Le dossier {folder_path} n'existe pas.")

def main():
    """Point d'entrée principal du script."""
    hide_folder()

if __name__ == "__main__":
    main()
