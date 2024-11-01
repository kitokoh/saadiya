# import os
# import shutil
# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox, QProgressBar
# )
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QIcon, QFont


# class FileCopyApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Configuration de la fenêtre principale
#         self.setWindowTitle("FB Robot - Copie du Fichier")
#         self.setGeometry(700, 400, 500, 300)
#         self.setWindowIcon(QIcon("robot_icon.png"))  # Icône personnalisée

#         # Mise en page principale
#         self.layout = QVBoxLayout()

#         # Ajout d'une police plus moderne et d'un titre stylisé
#         title_label = QLabel("FB Robot - Copie de Fichier", self)
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setFont(QFont("Arial", 18, QFont.Bold))
#         self.layout.addWidget(title_label)

#         # Texte d'information
#         self.info_label = QLabel("La copie du fichier est en cours...", self)
#         self.info_label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.info_label)

#         # Barre de progression pour visualiser la copie
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setValue(0)
#         self.layout.addWidget(self.progress_bar)

#         # Appliquer la mise en page
#         self.setLayout(self.layout)

#         # Démarrer automatiquement la copie du fichier
#         self.copy_file()

#     def copy_file(self):
#         """Copier le fichier cle.exe du répertoire courant vers le Bureau de l'utilisateur"""
#         desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#         self.source_folder = os.path.join(os.getcwd(), "resources", "tools")  # Dossier source modifié

#         source_file = os.path.join(self.source_folder, "cle.exe")
#         dest_file = os.path.join(desktop_path, "FB-Robot.exe")

#         # Démarrer la copie
#         self.progress_bar.setValue(25)  # Barre de progression partielle

#         if os.path.exists(source_file):
#             try:
#                 shutil.copy(source_file, dest_file)
#                 self.progress_bar.setValue(75)  # Avancement de la progression

#                 # Vérification du succès de la copie
#                 if os.path.exists(dest_file):
#                     self.progress_bar.setValue(100)  # Progression complète
#                     #self.show_message("Succès", "La copie de cle.exe vers le Bureau a réussi !")
#                 else:
#                     self.show_message("Échec", "La copie a échoué. Le fichier n'a pas été trouvé sur le Bureau.")
#             except Exception as e:
#                 self.show_message("Erreur", f"Une erreur est survenue lors de la copie : {str(e)}")
#         else:
#             self.show_message("Erreur", "Le fichier source cle.exe n'a pas été trouvé dans le répertoire courant.")

#         # Fermer l'application après 1 seconde
#         QTimer.singleShot(10, self.close)

#     def show_message(self, title, message):
#         """Afficher un message d'information dans une boîte de dialogue"""
#         msg_box = QMessageBox(self)
#         msg_box.setWindowTitle(title)
#         msg_box.setText(message)
#         msg_box.setIcon(QMessageBox.Information)
#         msg_box.exec_()


# def main():
#     app = QApplication(sys.argv)

#     # Créer et afficher la fenêtre principale
#     window = FileCopyApp()
#     window.show()

#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
import os
import shutil
from pathlib import Path

user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

def copy_file():
    """Copier cle.exe depuis resources/tools vers le Bureau sous le nom FB-Robot.exe."""
    print("Début de la fonction copy_file...")

    # Obtenir le chemin du bureau de l'utilisateur
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")    
    print(f"Chemin du bureau récupéré : {desktop_path}")

    # Chemin du fichier source cle.exe
    current_dir = os.getcwd()
    source_file = os.path.join(user_data_dir, "resources", "tools", "wacle.exe")
    source_file2 = os.path.join(user_data_dir, "resources", "tools", "wastart2.exe")

    print(f"Chemin du fichier source : {source_file}")

    # Chemin du fichier destination sur le bureau
    dest_file = os.path.join(desktop_path, "WA-Robot.exe")
    dest_file2 = os.path.join(desktop_path, "WA-Robot-Multi.exe")

    # Vérification du fichier source
    if not os.path.exists(source_file):
        print(f"Erreur : Le fichier source cle.exe est introuvable à l'emplacement {source_file}.")
        return
    
    print("Fichier source trouvé, préparation à la copie...")

    # Copier le fichier vers le bureau
    try:
        shutil.copy(source_file, dest_file)
        print(f"Succès : Le fichier a été copié sur le bureau sous le nom FB-Robot.exe.")
        shutil.copy(source_file2, dest_file2)
        print(f"Succès : Le fichier a été copié sur le bureau sous le nom FB-Robot.exe.")

    except Exception as e:
        print(f"Erreur lors de la copie : {str(e)}")

def main():
    """Point d'entrée principal du script."""
    print("Lancement de la copie du fichier cle.exe vers le bureau...")
    copy_file()

if __name__ == "__main__":
    main()
