import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class InstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vérification et Installation de Python et Git')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Vérification des installations...', self)
        layout.addWidget(self.label)

        self.install_button = QPushButton('Installer Python et Git', self)
        self.install_button.clicked.connect(self.check_and_install)
        layout.addWidget(self.install_button)

        self.setLayout(layout)

        self.check_installations()

    def check_installations(self):
        self.python_installed = self.is_python_installed()
        self.git_installed = self.is_git_installed()

        if self.python_installed and self.git_installed:
            self.label.setText('Python et Git sont déjà installés.')
            self.install_button.setEnabled(False)
        else:
            self.label.setText('Python ou Git ne sont pas installés. Cliquez sur le bouton pour les installer.')

    def is_python_installed(self):
        try:
            subprocess.check_output(['python', '--version'])
            return True
        except:
            return False

    def is_git_installed(self):
        try:
            subprocess.check_output(['git', '--version'])
            return True
        except:
            return False

    def check_and_install(self):
        if not self.python_installed:
            self.install_python()
        if not self.git_installed:
            self.install_git()

        self.check_installations()

    def install_python(self):
        if self.is_admin():
            try:
                subprocess.run(['winget', 'install', 'Python.Python.3'], check=True)
                QMessageBox.information(self, 'Succès', 'Python a été installé avec succès.')
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'installation de Python: {e}')
        else:
            self.run_as_admin(['winget', 'install', 'Python.Python.3'])

    def install_git(self):
        if self.is_admin():
            try:
                subprocess.run(['winget', 'install', 'Git.Git'], check=True)
                QMessageBox.information(self, 'Succès', 'Git a été installé avec succès.')
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'installation de Git: {e}')
        else:
            self.run_as_admin(['winget', 'install', 'Git.Git'])

    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def run_as_admin(self, command):
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", command[0], ' '.join(command[1:]), None, 1)
        else:
            QMessageBox.warning(self, 'Erreur', 'Cette fonctionnalité est uniquement disponible sur Windows.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InstallerApp()
    ex.show()
    sys.exit(app.exec_())