import os
import shutil
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
import datetime


class FileCopyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("FB Robot - Copie de Fichiers Media")
        self.setGeometry(700, 400, 600, 400)
        self.setWindowIcon(QIcon("../resources/robot_icon.png"))  # Icône personnalisée

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Ajout d'un titre stylisé
        title_label = QLabel("FB Robot - Copie de Fichiers Media", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.layout.addWidget(title_label)

        # Texte d'information
        self.info_label = QLabel("Les fichiers media sont en cours de copie...", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Barre de progression pour visualiser la copie
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # Appliquer la mise en page
        self.setLayout(self.layout)

        # Exécution automatique de la copie
        QTimer.singleShot(1000, self.copy_files)

    def copy_files(self):
        """Copier les fichiers media spécifiés du répertoire source vers le dossier de destination"""
        source_folder = os.path.join(os.getcwd(), "../resources/demoData")  # Répertoire resources/demoData
        destination_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot", "media", "media1")
        files_to_copy = ["1.mp4", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]

        log_file = os.path.join(os.getcwd(), "copy_log.txt")
        self.log_message(log_file, "Démarrage de la copie de fichiers...")

        # Créer le dossier de destination s'il n'existe pas
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            self.log_message(log_file, f"Création du dossier : {destination_folder}")

        # Démarrer la copie avec la barre de progression
        progress_step = 100 // len(files_to_copy)
        progress = 0

        for file in files_to_copy:
            source_file = os.path.join(source_folder, file)
            dest_file = os.path.join(destination_folder, file)

            if os.path.exists(source_file):
                try:
                    shutil.copy(source_file, dest_file)
                    progress += progress_step
                    self.progress_bar.setValue(progress)
                    self.log_message(log_file, f"{file} copié vers {destination_folder}")
                except Exception as e:
                    self.log_message(log_file, f"Erreur lors de la copie de {file} : {str(e)}")
            else:
                self.log_message(log_file, f"{file} n'existe pas dans {source_folder}")

        self.progress_bar.setValue(100)  # Complétion de la barre de progression
       # self.show_message("Opération terminée", "Tous les fichiers media ont été traités.")
        QTimer.singleShot(3000, self.close)  # Fermer la fenêtre après 3 secondes

    def log_message(self, log_file, message):
        """Enregistrer un message dans un fichier de journalisation"""
        with open(log_file, 'a') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")

    def show_message(self, title, message):
        """Afficher un message d'information dans une boîte de dialogue"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()


def main():
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = FileCopyApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
