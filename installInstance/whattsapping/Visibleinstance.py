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
#         self.setWindowTitle(self.tr("Facebook Robot Pro - Rendre les Dossiers Visibles"))
#         self.setFixedSize(400, 150)  # Taille fixe pour un design propre

#         layout = QVBoxLayout()

#         self.label = QLabel(self.tr("Préparation à rendre les dossiers visibles..."))
#         layout.addWidget(self.label)

#         # Création de la barre de progression
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setRange(0, 100)  # Plage de la barre de progression
#         layout.addWidget(self.progress_bar)

#         self.setLayout(layout)

#         # Rendre les dossiers visibles automatiquement lors du démarrage
#         QTimer.singleShot(1000, self.show_folders)
#         QTimer.singleShot(3000, self.close)

#     def show_folders(self):
#         # Chemin du dossier principal
#         base_folder = "C:\\bon"

#         # Vérification si le dossier principal existe
#         if os.path.exists(base_folder):
#             # Récupération des sous-dossiers et fichiers
#             items = [os.path.join(base_folder, item) for item in os.listdir(base_folder)]
#             total_items = len(items)

#             # Rendre visible le dossier principal
#             os.system(f'attrib -h -s "{base_folder}"')

#             # Rendre visibles les sous-dossiers et fichiers avec mise à jour de la barre de progression
#             for index, item in enumerate(items):
#                 os.system(f'attrib -h -s "{item}"')
#                 progress = int((index + 1) / total_items * 100)
#                 self.progress_bar.setValue(progress)  # Mise à jour de la barre de progression
#                 QApplication.processEvents()  # Mise à jour de l'interface

#             self.log_action(f"Tous les dossiers dans {base_folder} sont maintenant visibles.")
#             QMessageBox.information(self, self.tr("Dossiers visibles"), 
#                                     self.tr("Tous les dossiers dans bon sont maintenant visibles et accessibles !"))
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
#                 f.write("-- Journal des opérations de rendu visible démarré --\n")
        
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
import sys
import time

def show_folders():
    # Chemin du dossier principal
    base_folder = "C:\\bon"

    # Vérification si le dossier principal existe
    if os.path.exists(base_folder):
        # Récupération des sous-dossiers et fichiers
        items = [os.path.join(base_folder, item) for item in os.listdir(base_folder)]
        total_items = len(items)

        # Rendre visible le dossier principal
        os.system(f'attrib -h -s "{base_folder}"')

        # Rendre visibles les sous-dossiers et fichiers
        for index, item in enumerate(items):
            os.system(f'attrib -h -s "{item}"')
            progress = int((index + 1) / total_items * 100)
            print(f"Progression : {progress}% - {item} rendu visible")
            time.sleep(0.1)  # Simuler un léger délai pour la progression

        log_action(f"Tous les dossiers dans {base_folder} sont maintenant visibles.")
        print("Tous les dossiers dans 'bon' sont maintenant visibles et accessibles !")
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
            f.write("-- Journal des opérations de rendu visible démarré --\n")
    
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")

def main():
    print("Préparation à rendre les dossiers visibles...")
    time.sleep(1)  # Simuler un délai avant de commencer
    show_folders()

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
