# import os
# import sys
# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtGui import QIcon  # Importation correcte de QIcon

# class App(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.updateEnvFiles()  # Appel automatique de la mise à jour des fichiers .env

#         # Fermer l'application après 3 secondes
#         QtCore.QTimer.singleShot(30, self.close)  # 3000 ms = 3 secondes

#     def initUI(self):
#         self.setWindowTitle('Mise à Jour des Fichiers .env')
#         self.setGeometry(100, 100, 400, 300)

#         # Définir une icône (remplacez 'icon.png' par le chemin de votre icône)
#         self.setWindowIcon(QIcon('resources/icons/icon.png'))  # Mettez le chemin correct

#         # Layout principal
#         layout = QtWidgets.QVBoxLayout()

#         # Champ de journal
#         self.logTextEdit = QtWidgets.QTextEdit(self)
#         self.logTextEdit.setReadOnly(True)
#         layout.addWidget(self.logTextEdit)

#         self.setLayout(layout)

#     def updateEnvFiles(self):
#         base_dir = 'C:/bon'  # Chemin du dossier contenant les robots
#         log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "journalinstallation.txt")

#         self.log("Démarrage de la mise à jour des fichiers .env dans le dossier C:/bon.")

#         # Initialisation du fichier log
#         with open(log_file_path, 'a') as log_file:
#             log_file.write("\n===========================================\n")
#             log_file.write(f"Mise à jour commencée le {QtCore.QDate.currentDate().toString()} à {QtCore.QTime.currentTime().toString()}\n")

#         # Lister les dossiers robotX
#         folders = [folder for folder in os.listdir(base_dir) if folder.startswith('robot') and os.path.isdir(os.path.join(base_dir, folder))]

#         if not folders:
#             self.log("Aucun dossier 'robotX' trouvé dans C:/bon.")
#             return

#         self.log(f"{len(folders)} dossiers trouvés : {', '.join(folders)}.")

#         log_content = ""

#         # Boucle pour mettre à jour chaque dossier robotX
#         for folder_name in folders:
#             env_file = os.path.join(base_dir, folder_name, '.env')
#             if os.path.exists(env_file):
#                 with open(env_file, 'w') as f:
#                     robot_number = folder_name[5:]  # Extraction du numéro de robot
#                     f.write(f'CHROME_FOLDER="C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Profil {robot_number}"\n')
#                     f.write('WAIT_MIN=5\n')
#                     f.write('PROFILE=Default\n')
#                     f.write('PUBLISH_LABEL=Publier\n')
#                     f.write('VISIT_LABEL=Visiter\n')

#                 log_content += f"Fichier .env mis à jour pour {folder_name} à {QtCore.QTime.currentTime().toString()}.\n"
#             else:
#                 log_content += f"ERREUR : Le fichier .env pour {folder_name} n'a pas été trouvé.\n"

#         # Écrire le contenu du log dans le fichier
#         with open(log_file_path, 'a') as log_file:
#             log_file.write(log_content)
#             log_file.write(f"Mise à jour terminée à {QtCore.QTime.currentTime().toString()}.\n")

#         self.log("Toutes les mises à jour sont terminées.")

#     def log(self, message):
#         """Ajoute un message dans l'interface utilisateur"""
#         self.logTextEdit.append(message)

# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = App()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()
import os
import sys
from datetime import datetime

def update_env_files(base_dir='C:/bon'):
    log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "journalinstallation.txt")

    log("Démarrage de la mise à jour des fichiers .env dans le dossier C:/bon.")

    # Initialisation du fichier log
    with open(log_file_path, 'a') as log_file:
        log_file.write("\n===========================================\n")
        log_file.write(f"Mise à jour commencée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Lister les dossiers robotX
    folders = [folder for folder in os.listdir(base_dir) if folder.startswith('robot') and os.path.isdir(os.path.join(base_dir, folder))]

    if not folders:
        log("Aucun dossier 'robotX' trouvé dans C:/bon.")
        return

    log(f"{len(folders)} dossiers trouvés : {', '.join(folders)}.")

    log_content = ""

    # Boucle pour mettre à jour chaque dossier robotX
    for folder_name in folders:
        env_file = os.path.join(base_dir, folder_name, '.env')
        if os.path.exists(env_file):
            with open(env_file, 'w') as f:
                robot_number = folder_name[5:]  # Extraction du numéro de robot
                f.write(f'CHROME_FOLDER="C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Profil {robot_number}"\n')
                f.write('WAIT_MIN=5\n')
                f.write('PROFILE=Default\n')
                f.write('PUBLISH_LABEL=Publier\n')
                f.write('VISIT_LABEL=Visiter\n')

            log_content += f"Fichier .env mis à jour pour {folder_name} à {datetime.now().strftime('%H:%M:%S')}.\n"
        else:
            log_content += f"ERREUR : Le fichier .env pour {folder_name} n'a pas été trouvé.\n"

    # Écrire le contenu du log dans le fichier
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_content)
        log_file.write(f"Mise à jour terminée à {datetime.now().strftime('%H:%M:%S')}.\n")

    log("Toutes les mises à jour sont terminées.")

def log(message):
    """Affiche un message dans la console"""
    print(message)

def main():
    update_env_files()

if __name__ == '__main__':
    main()  # Appelle la fonction main si le script est exécuté directement
