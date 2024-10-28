import os 
import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class LogWorker(QThread):
    log_signal = pyqtSignal(str)

    def run(self):
        """Gère la création des dossiers et journalise les actions"""
        user_folder = r"C:\bon"  # Répertoire spécifique
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "AI-FB-Robot")
        log_file = os.path.join('..\\resources', 'journalInstallation.txt')

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Démarrer la journalisation
        self.log_signal.emit(f"[INFO] - Script démarré le {current_time}\n")

        # Vérifier et créer le dossier "bon"
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            self.log_signal.emit(f"[INFO] - Le dossier 'bon' a été créé avec succès.\n")
            self.log_to_file(log_file, f"[INFO] - Dossier 'bon' créé avec succès le {current_time}\n")
        else:
            self.log_signal.emit(f"[INFO] - Le dossier 'bon' existe déjà.\n")
            self.log_to_file(log_file, f"[INFO] - Dossier 'bon' existant vérifié le {current_time}\n")

        # Vérifier et créer le dossier "AI-FB-Robot" dans "Downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
            self.log_signal.emit(f"[INFO] - Le dossier 'AI-FB-Robot' a été créé avec succès.\n")
            self.log_to_file(log_file, f"[INFO] - Dossier 'AI-FB-Robot' créé avec succès le {current_time}\n")
        else:
            self.log_signal.emit(f"[INFO] - Le dossier 'AI-FB-Robot' existe déjà.\n")
            self.log_to_file(log_file, f"[INFO] - Dossier 'AI-FB-Robot' existant vérifié le {current_time}\n")

        # Fin du script
        self.log_signal.emit(f"[INFO] - Script terminé le {current_time}\n")
        self.log_to_file(log_file, f"[INFO] - Script terminé le {current_time}\n")

    def log_to_file(self, log_file, message):
        """Écrit le message dans le fichier de journalisation"""
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(message)


class FolderManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("AI FB Robot - Gestion des Dossiers et Journalisation")
        self.setGeometry(700, 400, 600, 500)
        self.setWindowIcon(QIcon("robot_icon.png"))  # Icône personnalisée

        # Mise en page principale
        self.layout = QVBoxLayout()

        # Ajout d'un titre stylisé
        title_label = QLabel("AI FB Robot - Gestion des Dossiers", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.layout.addWidget(title_label)

        # Texte d'information
        self.info_label = QLabel("Traitement en cours, veuillez patienter...", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Zone de texte pour afficher le journal
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        # Appliquer la mise en page
        self.setLayout(self.layout)

        # Démarrer la gestion des dossiers
        self.start_logging()

    def start_logging(self):
        """Commence le processus de journalisation sans intervention de l'utilisateur"""
        self.log_worker = LogWorker()
        self.log_worker.log_signal.connect(self.update_log_output)
        self.log_worker.finished.connect(self.show_completion_message)
        self.log_worker.start()

    def update_log_output(self, message):
        """Affiche le message dans la zone de texte"""
        self.log_output.append(message)

    def show_completion_message(self):
        """Affiche une boîte de dialogue de succès lorsque la gestion est terminée"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Succès")
        #msg_box.setText("Les dossiers ont été gérés avec succès. Consultez le fichier journal.")
        #msg_box.setIcon(QMessageBox.Information)
        #msg_box.exec_()

        # Créer un timer pour fermer l'application après 2 secondes
        QTimer.singleShot(1000, self.close)  # 2000 ms = 2 secondes


def main():
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = FolderManagerApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
