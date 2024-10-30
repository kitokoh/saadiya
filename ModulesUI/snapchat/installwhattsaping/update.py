import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTranslator, QLocale
user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "saadiya")

class UpdateApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de l'interface
        self.setWindowTitle("FacebookRobotPro - Mise à jour des instances")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Bienvenue dans le programme de mise à jour des instances.")
        layout.addWidget(self.label)

        self.update_button = QtWidgets.QPushButton("Mettre à jour toutes les instances")
        self.update_button.clicked.connect(self.update_instances)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

        # Fichier de log
        self.logfile = os.path.join(user_data_dir, "resources", "journalInstallation.txt")

        # Vérification des droits d'administrateur
        if not self.check_admin_rights():
            QMessageBox.critical(self, "Erreur", "Ce programme doit être exécuté en tant qu'administrateur.")
            sys.exit(1)

        # Création du fichier de log s'il n'existe pas
        if not os.path.exists(self.logfile):
            with open(self.logfile, "a") as log:
                log.write("-- Journal de mise à jour lancé --\n")
                log.write(f"{QtCore.QDate.currentDate().toString()} {QtCore.QTime.currentTime().toString()} : Début de la mise à jour\n")

    def check_admin_rights(self):
        try:
            subprocess.check_output('openfiles', shell=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def update_instances(self):
        confirmation = QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment mettre à jour toutes les instances ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.No:
            return

        instance_index = 1
        while True:
            foldername = f"C:\\bon\\robot{instance_index}"
            if os.path.exists(foldername):
                self.log_and_update_instance(foldername, instance_index)
                instance_index += 1
            else:
                self.log_all_updated(instance_index)
                break

    def log_and_update_instance(self, foldername, index):
        # Met à jour le dépôt GitHub
        os.chdir(foldername)
        log_message = f"robot{index} mise à jour en cours...\n"
        self.log_to_file(log_message)

        try:
            subprocess.check_call('git pull origin main', shell=True)
            log_message = f"{QtCore.QDate.currentDate().toString()} {QtCore.QTime.currentTime().toString()} : robot{index} mis à jour avec succès\n"
            self.log_to_file(log_message)

            # Mise à jour des dépendances
            if os.path.exists(f"env{index}\\Scripts\\activate"):
                subprocess.call(f"env{index}\\Scripts\\activate && pip install --upgrade -r requirements.txt", shell=True)
                log_message = f"{QtCore.QDate.currentDate().toString()} {QtCore.QTime.currentTime().toString()} : Dépendances de robot{index} mises à jour\n"
                self.log_to_file(log_message)
        except subprocess.CalledProcessError:
            log_message = f"Échec de la mise à jour de robot{index}\n"
            self.log_to_file(log_message)

    def log_all_updated(self, instance_index):
        log_message = "Toutes les instances ont été mises à jour avec succès.\n"
        self.log_to_file(log_message)
       # QMessageBox.information(self, "Succès", "Mise à jour terminée.")

    def log_to_file(self, message):
        with open(self.logfile, "a") as log:
            log.write(message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Configuration de la traduction
    translator = QTranslator()
    locale = QLocale.system().name()
    translator.load(f"translations_{locale}.qm")  # Assurez-vous d'avoir le fichier de traduction
    app.installTranslator(translator)

    main_window = UpdateApp()
    main_window.show()
    sys.exit(app.exec_())
