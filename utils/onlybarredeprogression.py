import sys
import subprocess
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import Qt, QTimer

class BackgroundInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.check_and_install()

    def initUI(self):
        # Configuration de la fenêtre
        self.setWindowTitle('Installation en arrière-plan')
        self.setGeometry(100, 100, 400, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # Fenêtre toujours visible et sans bordure

        # Layout
        layout = QVBoxLayout()

        # Barre de progression
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Label pour les messages d'avancement
        self.status_label = QLabel('Vérification des installations...', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def check_and_install(self):
        # Vérifier et installer Python et Git
        self.update_progress(10, 'Vérification de Python...')
        if not self.is_python_installed():
            self.update_progress(20, 'Installation de Python...')
            self.install_python()
        else:
            self.update_progress(30, 'Python est déjà installé.')

        self.update_progress(40, 'Vérification de Git...')
        if not self.is_git_installed():
            self.update_progress(50, 'Installation de Git...')
            self.install_git()
        else:
            self.update_progress(60, 'Git est déjà installé.')

        self.update_progress(100, 'Installation terminée.')
        QTimer.singleShot(3000, self.close)  # Fermer la fenêtre après 3 secondes

    def update_progress(self, value, message):
        """Met à jour la barre de progression et le message."""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        QApplication.processEvents()  # Forcer la mise à jour de l'interface

    def is_python_installed(self):
        """Vérifie si Python est installé."""
        try:
            subprocess.check_output(['python', '--version'], stderr=subprocess.STDOUT)
            return True
        except:
            return False

    def is_git_installed(self):
        """Vérifie si Git est installé."""
        try:
            subprocess.check_output(['git', '--version'], stderr=subprocess.STDOUT)
            return True
        except:
            return False

    def install_python(self):
        """Installe Python en utilisant winget."""
        if self.is_admin():
            try:
                subprocess.run(['winget', 'install', 'Python.Python.3'], check=True)
                self.update_progress(30, 'Python installé avec succès.')
            except subprocess.CalledProcessError as e:
                self.update_progress(30, f'Erreur lors de l\'installation de Python: {e}')
        else:
            self.run_as_admin(['winget', 'install', 'Python.Python.3'])

    def install_git(self):
        """Installe Git en utilisant winget."""
        if self.is_admin():
            try:
                subprocess.run(['winget', 'install', 'Git.Git'], check=True)
                self.update_progress(80, 'Git installé avec succès.')
            except subprocess.CalledProcessError as e:
                self.update_progress(80, f'Erreur lors de l\'installation de Git: {e}')
        else:
            self.run_as_admin(['winget', 'install', 'Git.Git'])

    def is_admin(self):
        """Vérifie si l'application est exécutée avec les droits administrateur."""
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def run_as_admin(self, command):
        """Relance l'application avec les droits administrateur (Windows uniquement)."""
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", command[0], ' '.join(command[1:]), None, 1)
        else:
            self.update_progress(100, 'Cette fonctionnalité est uniquement disponible sur Windows.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = BackgroundInstaller()
    installer.show()
    sys.exit(app.exec_())