# import sys
# import os
# import shutil
# from PyQt5.QtWidgets import QApplication, QMessageBox
# from PyQt5.QtCore import QTimer

# class FileCopyApp:
#     def __init__(self):
#         # Configuration des chemins
#         self.source_folder = os.path.join(os.getcwd(), "resources", "demoData")  # Dossier source pour les fichiers media
#         self.destination_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "media", "media1")
        
#         # Dossier source pour data.json
#         self.data_json_source = os.path.join(self.source_folder, "data.json")
#         # Dossier de destination pour data.json
#         self.data_json_destination_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "text")
        
#         # Vérifie si le dossier de destination existe, sinon le crée
#         if not os.path.exists(self.destination_folder):
#             os.makedirs(self.destination_folder)
        
#         # Vérifie si le dossier de destination 'text' existe pour data.json, sinon le crée
#         if not os.path.exists(self.data_json_destination_folder):
#             os.makedirs(self.data_json_destination_folder)

#         # Liste des fichiers à copier
#         self.files_to_copy = ["1.mp4", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]

#         # Exécution de la tâche
#         self.copy_files()
#         self.copy_data_json()

#         # Affiche une boîte de message pour informer que l'opération est terminée
#         #self.show_message("Opération terminée.")

#         # Démarre une minuterie pour fermer l'application après 1 seconde
#         QTimer.singleShot(000, QApplication.instance().quit)  # Ferme l'application après 1 seconde

#     def copy_files(self):
#         """Copie les fichiers media spécifiés"""
#         for file_name in self.files_to_copy:
#             source_file = os.path.join(self.source_folder, file_name)
#             if os.path.exists(source_file):
#                 shutil.copy(source_file, self.destination_folder)
#                 print(f"{file_name} copié vers {self.destination_folder}")
#             else:
#                 print(f"{file_name} n'existe pas dans {self.source_folder}")

#     def copy_data_json(self):
#         """Copie le fichier data.json vers le dossier text"""
#         if os.path.exists(self.data_json_source):
#             shutil.copy(self.data_json_source, self.data_json_destination_folder)
#             print(f"data.json copié vers {self.data_json_destination_folder}")
#         else:
#             print(f"data.json n'existe pas dans {self.source_folder}")

#     def show_message(self, message):
#         msg = QMessageBox()
#         msg.setWindowTitle("Info")
#         msg.setText(message)
#         msg.setStandardButtons(QMessageBox.Ok)
#         msg.exec_()

# def main():
#     app = QApplication(sys.argv)
#     FileCopyApp()
#     sys.exit(app.exec_())
        
# if __name__ == "__main__":
#     main()
import os
import shutil
import time

class FileCopyApp:
    def __init__(self):
        # Configuration des chemins
        self.source_folder = os.path.join(os.getcwd(), "resources", "demoData")  # Dossier source pour les fichiers media
        self.destination_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "media", "media1")
        
        # Dossier source pour data.json
        self.data_json_source = os.path.join(self.source_folder, "data.json")
        # Dossier de destination pour data.json
        self.data_json_destination_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "text")
        
        # Vérifie si le dossier de destination existe, sinon le crée
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)
        
        # Vérifie si le dossier de destination 'text' existe pour data.json, sinon le crée
        if not os.path.exists(self.data_json_destination_folder):
            os.makedirs(self.data_json_destination_folder)

        # Liste des fichiers à copier
        self.files_to_copy = ["1.mp4", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]

        # Exécution de la tâche
        self.copy_files()
        self.copy_data_json()

        # Affiche un message de confirmation
        self.show_message("Opération terminée.")

    def copy_files(self):
        """Copie les fichiers media spécifiés"""
        for file_name in self.files_to_copy:
            source_file = os.path.join(self.source_folder, file_name)
            if os.path.exists(source_file):
                shutil.copy(source_file, self.destination_folder)
                print(f"{file_name} copié vers {self.destination_folder}")
            else:
                print(f"{file_name} n'existe pas dans {self.source_folder}")

    def copy_data_json(self):
        """Copie le fichier data.json vers le dossier text"""
        if os.path.exists(self.data_json_source):
            shutil.copy(self.data_json_source, self.data_json_destination_folder)
            print(f"data.json copié vers {self.data_json_destination_folder}")
        else:
            print(f"data.json n'existe pas dans {self.source_folder}")

    def show_message(self, message):
        """Affiche un message de confirmation dans la console"""
        print(message)

# Fonction principale
def main():
    FileCopyApp()
    time.sleep(1)  # Attend 1 seconde avant de terminer le programme

if __name__ == "__main__":
    main()
