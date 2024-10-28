# import sys
# import os
# import time
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QMessageBox, QVBoxLayout, QProgressBar
# )
# from PyQt5.QtCore import QTranslator, QTimer

# class FacebookRobotApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle(self.tr("Facebook Robot Pro - Masquer les Dossiers"))
#         self.setFixedSize(400, 150)  # Taille fixe pour un design propre

#         layout = QVBoxLayout()

#         self.label = QLabel(self.tr("Préparation à masquer les dossiers..."))
#         layout.addWidget(self.label)

#         # Création de la barre de progression
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 100)  # Plage de la barre de progression
#         layout.addWidget(self.progress_bar)

#         self.setLayout(layout)

#         # Masquage automatique lors du démarrage
#         QTimer.singleShot(1, self.hide_folders)
#         QTimer.singleShot(000, self.close)

#     def hide_folders(self):
#         # Chemin du dossier principal
#         base_folder = "C:\\bon"

#         # Vérification si le dossier principal existe
#         if os.path.exists(base_folder):
#             # Récupération des sous-dossiers et fichiers
#             items = [os.path.join(base_folder, item) for item in os.listdir(base_folder)]
#             total_items = len(items)

#             # Masquer le dossier principal
#             os.system(f'attrib +h +s "{base_folder}"')

#             # Masquage des sous-dossiers et fichiers avec mise à jour de la barre de progression
#             for index, item in enumerate(items):
#                 os.system(f'attrib +h +s "{item}"')
#                 progress = int((index + 1) / total_items * 100)
#                 self.progress_bar.setValue(progress)  # Mise à jour de la barre de progression
#                 QApplication.processEvents()  # Mise à jour de l'interface

#             self.log_action(f"Tous les dossiers dans {base_folder} sont maintenant masqués.")
#             #QMessageBox.information(self, self.tr("Dossier masqué"), 
#              #                       self.tr("Tous les dossiers dans C:\\bon sont masqués et prêts à l'emploi !"))
#         else:
#             self.log_action(f"Le dossier {base_folder} n'existe pas.")
#             QMessageBox.critical(self, self.tr("Erreur"), 
#                                  self.tr(f"Le dossier {base_folder} n'existe pas."))

#     def log_action(self, message):
#         # Chemin du dossier ressources pour le fichier de log
#         resources_folder = os.path.join(os.path.dirname(__file__), "ressources")
#         log_file = os.path.join(resources_folder, "journalInstallation.txt")

#         # Création du fichier de log s'il n'existe pas
#         if not os.path.exists(resources_folder):
#             os.makedirs(resources_folder)  # Crée le dossier ressources s'il n'existe pas

#         if not os.path.exists(log_file):
#             with open(log_file, 'w') as f:
#                 f.write("-- Journal des opérations de masquage démarré --\n")
        
#         with open(log_file, 'a') as f:
#             f.write(f"{message}\n")



# def main():
#     app = QApplication(sys.argv)

#     # Gestion de la traduction
#     translator = QTranslator(app)
#     translator.load("your_translation_file.qm")  # Chargez votre fichier de traduction
#     app.installTranslator(translator)

#     # Création et affichage de l'application
#     ex = FacebookRobotApp()
#     ex.show()

#     sys.exit(app.exec_()) 
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement
import os
import time

def hide_folders(base_folder):
    # Vérification si le dossier principal existe
    if os.path.exists(base_folder):
        # Récupération des sous-dossiers et fichiers
        items = [os.path.join(base_folder, item) for item in os.listdir(base_folder)]
        total_items = len(items)

        # Masquer le dossier principal
        os.system(f'attrib +h +s "{base_folder}"')

        # Masquage des sous-dossiers et fichiers avec mise à jour de la progression
        for index, item in enumerate(items):
            os.system(f'attrib +h +s "{item}"')
            progress = int((index + 1) / total_items * 100)
            print(f"Progression : {progress}%")  # Affiche la progression
            time.sleep(0.1)  # Pause pour simuler le temps d'exécution

        log_action(f"Tous les dossiers dans {base_folder} sont maintenant masqués.")
    else:
        log_action(f"Le dossier {base_folder} n'existe pas.")
        print(f"Erreur : Le dossier {base_folder} n'existe pas.")

def log_action(message):
    # Chemin du dossier ressources pour le fichier de log
    resources_folder = "ressources"
    log_file = os.path.join(resources_folder, "journalInstallation.txt")

    # Création du fichier de log s'il n'existe pas
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)  # Crée le dossier ressources s'il n'existe pas

    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write("-- Journal des opérations de masquage démarré --\n")
    
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")

def main():
    base_folder = "C:\\bon"  # Chemin du dossier à masquer
    hide_folders(base_folder)

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
