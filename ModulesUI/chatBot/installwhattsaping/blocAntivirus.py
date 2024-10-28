import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar, QTimer
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

# Thread pour simuler les actions du script
class TaskThread(QThread):
    update_progress = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        # Simuler la désactivation de Windows Defender
        self.update_progress.emit(25, "Désactivation de Windows Defender...")
        time.sleep(2)

        # Simuler l'attente de 30 minutes (utilisé 5 secondes pour la démonstration)
        for i in range(30):
            time.sleep(1)
            self.update_progress.emit(25 + int(50 * (i + 1) / 30), f"Attente de {30 - i} secondes...")

        # Simuler la réactivation de Windows Defender
        self.update_progress.emit(90, "Réactivation de Windows Defender...")
        time.sleep(2)
        self.update_progress.emit(100, "Windows Defender réactivé avec succès.")

class AdminCheckWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion de Windows Defender")
        self.setGeometry(680, 390, 400, 200)
        self.setWindowIcon(QIcon("shield.png"))  # Icône de protection pour plus de style

        # Création de la mise en page principale
        self.layout = QVBoxLayout()

        # Label pour afficher les messages d'état
        self.status_label = QLabel("Veuillez démarrer l'opération en tant qu'administrateur.", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Barre de progression pour montrer les étapes du processus
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        # Bouton pour démarrer le processus
        self.start_button = QPushButton("Démarrer", self)
        self.start_button.clicked.connect(self.start_task)
        self.layout.addWidget(self.start_button)

        # Appliquer la mise en page
        self.setLayout(self.layout)

        # Initialiser le thread de la tâche
        self.task_thread = TaskThread()
        self.task_thread.update_progress.connect(self.update_status)

    def start_task(self):
        # Vérifier si le script est exécuté en tant qu'administrateur
        if not self.is_admin():
            QMessageBox.critical(self, "Erreur", "Ce script doit être exécuté en tant qu'administrateur.")
            return
        
        self.start_button.setEnabled(False)
        self.task_thread.start()

    def update_status(self, progress, message):
        self.progress_bar.setValue(progress)
        self.status_label.setText(message)

    def is_admin(self):
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

def main():
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre
    window = AdminCheckWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
