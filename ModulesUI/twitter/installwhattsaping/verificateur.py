# import os
# import sys
# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtWidgets import QMessageBox

# class ReportApp(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         # Configuration de l'interface
#         self.setWindowTitle("Rapport d'installation AI-FB-Robot")
#         self.setGeometry(100, 100, 400, 300)

#         # Layout
#         layout = QtWidgets.QVBoxLayout()

#         self.label = QtWidgets.QLabel("Bienvenue dans l'application de rapport d'installation.")
#         layout.addWidget(self.label)

#         self.setLayout(layout)

#         # Appeler la génération du rapport directement
#         self.generate_report()

#     def generate_report(self):
#         bon_dir = "C:\\bon"
#         ai_fb_robot_dir = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot")
#         log_file = os.path.join(os.path.expanduser("~"), "Desktop", "journalinstallation.txt")

#         # Création du fichier log s'il n'existe pas
#         if not os.path.exists(log_file):
#             with open(log_file, "a") as log:
#                 log.write("===============================\n")
#                 log.write("Rapport d'installation\n")
#                 log.write("===============================\n\n")

#         # Démarrage du rapport pour 'bonDir'
#         self.log_directory_report(bon_dir, log_file)
#         self.log_directory_report(ai_fb_robot_dir, log_file)

#         # Fin du script
#         with open(log_file, "a") as log:
#             log.write("Script terminé. Les informations ont été enregistrées dans \"{}\".\n".format(log_file))

#         #QMessageBox.information(self, "Succès", "Le rapport a été généré avec succès.")

#         # Fermer l'application après 2 secondes
#         QtCore.QTimer.singleShot(20, self.close)

#     def log_directory_report(self, directory, log_file):
#         with open(log_file, "a") as log:
#             log.write("Démarrage du rapport pour le répertoire {}\n".format(directory))
#             if os.path.exists(directory):
#                 folder_count = sum(os.path.isdir(os.path.join(directory, name)) for name in os.listdir(directory))
#                 for name in os.listdir(directory):
#                     path = os.path.join(directory, name)
#                     if os.path.isdir(path):
#                         log.write("Sous-dossier trouvé : {}\n".format(name))
#                 if folder_count > 0:
#                     log.write("Total des sous-dossiers trouvés dans {} : {}\n".format(directory, folder_count))
#                 else:
#                     log.write("Aucun sous-dossier trouvé dans {}\n".format(directory))
#             else:
#                 log.write("Le répertoire {} n'existe pas !\n".format(directory))
#             log.write("\n")


# def main():
#     app = QtWidgets.QApplication(sys.argv)

#     main_window = ReportApp()
#     main_window.show()

#     # Exécuter l'application et quitter après la fermeture
#     sys.exit(app.exec_())
    
# if __name__ == "__main__":
#     main()  # Appelle la fonction main si le script est exécuté directement
import os
import sys
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

def generate_report():
    bon_dir = "C:\\bon"
    ai_fb_robot_dir = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot")
    log_file =os.path.join(user_data_dir, "resources", "journalInstallation.txt")

    # Création du fichier log s'il n'existe pas
    if not os.path.exists(log_file):
        with open(log_file, "a") as log:
            log.write("===============================\n")
            log.write("Rapport d'installation\n")
            log.write("===============================\n\n")

    # Démarrage du rapport pour 'bonDir'
    log_directory_report(bon_dir, log_file)
    log_directory_report(ai_fb_robot_dir, log_file)

    # Fin du script
    with open(log_file, "a") as log:
        log.write("Script terminé. Les informations ont été enregistrées dans \"{}\".\n".format(log_file))

    print("Le rapport a été généré avec succès.")
    print("Les informations ont été enregistrées dans \"{}\".".format(log_file))


def log_directory_report(directory, log_file):
    with open(log_file, "a") as log:
        log.write("Démarrage du rapport pour le répertoire {}\n".format(directory))
        if os.path.exists(directory):
            folder_count = sum(os.path.isdir(os.path.join(directory, name)) for name in os.listdir(directory))
            for name in os.listdir(directory):
                path = os.path.join(directory, name)
                if os.path.isdir(path):
                    log.write("Sous-dossier trouvé : {}\n".format(name))
            if folder_count > 0:
                log.write("Total des sous-dossiers trouvés dans {} : {}\n".format(directory, folder_count))
            else:
                log.write("Aucun sous-dossier trouvé dans {}\n".format(directory))
        else:
            log.write("Le répertoire {} n'existe pas !\n".format(directory))
        log.write("\n")


def main():
    generate_report()

if __name__ == "__main__":
    main()  # Appelle la fonction main si le script est exécuté directement
