# import os
# import json
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QVBoxLayout, QWidget
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QTimer

# class RobotApp(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Configuration de la fenêtre
#         self.setWindowTitle("AI-FB-Robot - Gestion des Dossiers")
#         self.setGeometry(200, 200, 600, 400)

#         # Définir l'icône de la fenêtre
#         self.setWindowIcon(QIcon(os.path.join('resources', 'Creative-Freedom-Shimmer-Folder-New.ico')))

#         # Création des éléments d'interface
#         self.create_widgets()

#         # Chemin vers le fichier journal d'installation
#         self.log_file_path = os.path.join('resources', 'journalInstallation.txt')

#         # Exécute la création des dossiers et fichiers au démarrage
#         self.create_robot_directories()

#     def create_widgets(self):
#         layout = QVBoxLayout()

#         # Label d'informations
#         self.info_label = QLabel("L'opération est en cours...")
#         layout.addWidget(self.info_label)

#         # Set main widget
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#     def log_execution(self, message):
#         """Enregistre un message dans le fichier journalInstallation."""
#         with open(self.log_file_path, 'a') as log_file:
#             log_file.write(message + '\n')

#     def create_robot_directories(self):
#         # Définir le chemin du dossier Téléchargements
#         download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot")

#         # Créer le dossier AI-FB-Robot dans Téléchargements
#         if not os.path.exists(download_dir):
#             os.makedirs(download_dir)
#             self.log_execution(f"Dossier créé : {download_dir}")
#             #QMessageBox.information(self, "Dossier Créé", f"Dossier {download_dir} créé.")

#         # Créer les sous-dossiers media et text
#         media_dir = os.path.join(download_dir, "media")
#         text_dir = os.path.join(download_dir, "text")

#         os.makedirs(media_dir, exist_ok=True)
#         os.makedirs(text_dir, exist_ok=True)

#         # Vérifier et compter les dossiers roboti dans C:\bon
#         robot_dirs = [d for d in os.listdir('C:\\bon') if d.startswith('robot') and os.path.isdir(os.path.join('C:\\bon', d))]
#         robot_count = len(robot_dirs)

#         # Si aucun dossier n'est trouvé
#         if robot_count == 0:
#             self.log_execution("Aucun dossier roboti trouvé dans C:\\bon.")
#             QMessageBox.warning(self, "Erreur", "Aucun dossier roboti trouvé dans C:\\bon.")
#             self.info_label.setText("Opération terminée.")
#             self.schedule_closing()
#             return

#         # Si un seul dossier est trouvé
#         if robot_count == 1:
#             robot_dir = robot_dirs[0]
#             with open(os.path.join(text_dir, 'data.json'), 'w') as f:
#                 json.dump({}, f)
#             with open(os.path.join(text_dir, 'log.txt'), 'w') as f:
#                 f.write(f"Log du dossier {robot_dir}\n")
#             with open(os.path.join(media_dir, 'media.txt'), 'w') as f:
#                 f.write("Fichier média associé\n")
#             self.log_execution(f"Fichiers créés pour le dossier robot : {robot_dir}")
#             #QMessageBox.information(self, "Création Réussie", "Fichiers créés pour le dossier robot.")
#         else:
#             # Créer des sous-dossiers et fichiers pour chaque dossier robot
#             for i, robot_dir in enumerate(robot_dirs):
#                 os.makedirs(os.path.join(media_dir, f'media{i+1}'), exist_ok=True)
#                 os.makedirs(os.path.join(text_dir, f'text{i+1}'), exist_ok=True)
#                 with open(os.path.join(text_dir, f'text{i+1}', 'data.json'), 'w') as f:
#                     json.dump({}, f)
#                 with open(os.path.join(text_dir, f'text{i+1}', f'text{i+1}.log'), 'w') as f:
#                     f.write(f"Log de text{i+1}\n")
#                 self.log_execution(f"Fichiers créés pour le dossier robot : {robot_dir}")
#             self.log_execution(f"Fichiers créés pour {robot_count} dossiers roboti.")
#             #QMessageBox.information(self, "Création Réussie", f"Fichiers créés pour {robot_count} dossiers roboti.")

#         #self.info_label.setText("Opération terminée.")
#         self.schedule_closing()

#     def schedule_closing(self):
#         """Planifie la fermeture de l'application après 3 secondes."""
#         QTimer.singleShot(00, self.close_application)  # 3000 ms = 3 secondes

#     def close_application(self):
#         """Ferme l'application."""
#         self.close()

# # Application
# def main():
#     app = QApplication([])
#     window = RobotApp()
#     window.show()
#     app.exec_()
        
# if __name__ == "__main__":
#     main()
    
import os
import json

class RobotApp:
    def __init__(self):
        # Chemin vers le fichier journal d'installation
        self.log_file_path = os.path.join('resources', 'journalInstallation.txt')

        # Exécute la création des dossiers et fichiers au démarrage
        self.create_robot_directories()

    def log_execution(self, message):
        """Enregistre un message dans le fichier journalInstallation."""
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(message + '\n')

    def create_robot_directories(self):
        # Définir le chemin du dossier Téléchargements
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot")

        # Créer le dossier AI-FB-Robot dans Téléchargements
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            self.log_execution(f"Dossier créé : {download_dir}")
            print(f"Dossier {download_dir} créé.")

        # Créer les sous-dossiers media et text
        media_dir = os.path.join(download_dir, "media")
        text_dir = os.path.join(download_dir, "text")

        os.makedirs(media_dir, exist_ok=True)
        os.makedirs(text_dir, exist_ok=True)

        # Vérifier et compter les dossiers roboti dans C:\bon
        robot_dirs = [d for d in os.listdir('C:\\bon') if d.startswith('robot') and os.path.isdir(os.path.join('C:\\bon', d))]
        robot_count = len(robot_dirs)

        # Si aucun dossier n'est trouvé
        if robot_count == 0:
            self.log_execution("Aucun dossier roboti trouvé dans C:\\bon.")
            print("Aucun dossier roboti trouvé dans C:\\bon.")
            return

        # Si un seul dossier est trouvé
        if robot_count == 1:
            robot_dir = robot_dirs[0]
            with open(os.path.join(text_dir, 'data.json'), 'w') as f:
                json.dump({}, f)
            with open(os.path.join(text_dir, 'log.txt'), 'w') as f:
                f.write(f"Log du dossier {robot_dir}\n")
            with open(os.path.join(media_dir, 'media.txt'), 'w') as f:
                f.write("Fichier média associé\n")
            self.log_execution(f"Fichiers créés pour le dossier robot : {robot_dir}")
            print(f"Fichiers créés pour le dossier robot : {robot_dir}")
        else:
            # Créer des sous-dossiers et fichiers pour chaque dossier robot
            for i, robot_dir in enumerate(robot_dirs):
                os.makedirs(os.path.join(media_dir, f'media{i+1}'), exist_ok=True)
                os.makedirs(os.path.join(text_dir, f'text{i+1}'), exist_ok=True)
                with open(os.path.join(text_dir, f'text{i+1}', 'data.json'), 'w') as f:
                    json.dump({}, f)
                with open(os.path.join(text_dir, f'text{i+1}', f'text{i+1}.log'), 'w') as f:
                    f.write(f"Log de text{i+1}\n")
                self.log_execution(f"Fichiers créés pour le dossier robot : {robot_dir}")
            self.log_execution(f"Fichiers créés pour {robot_count} dossiers roboti.")
            print(f"Fichiers créés pour {robot_count} dossiers roboti.")

# Application
def main():
    app = RobotApp()

if __name__ == "__main__":
    main()
