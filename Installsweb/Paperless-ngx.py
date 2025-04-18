import os
import sys
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QProgressBar, QPushButton, QLabel, QMessageBox, 
                            QTextEdit, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
import qdarktheme


class InstallThread(QThread):
    progress_update = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cancelled = False

    def run(self):
        try:
            self.log_signal.emit("Début de l'installation de Paperless-ngx...")
            
            # Vérification des prérequis
            self.progress_update.emit(5, "Vérification des prérequis")
            if not self.check_prerequisites():
                self.finished_signal.emit(False, "Prérequis non satisfaits")
                return
            
            # Clone du dépôt
            if not self.cancelled:
                self.progress_update.emit(10, "Clonage du dépôt Paperless-ngx")
                self.clone_repo()
            
            # Installation Docker
            if not self.cancelled:
                self.progress_update.emit(30, "Installation de Docker")
                self.install_docker()
            
            # Configuration
            if not self.cancelled:
                self.progress_update.emit(60, "Configuration de Paperless-ngx")
                self.configure_paperless()
            
            # Lancement
            if not self.cancelled:
                self.progress_update.emit(80, "Lancement de Paperless-ngx")
                self.start_paperless()
            
            if not self.cancelled:
                self.progress_update.emit(100, "Installation terminée!")
                self.finished_signal.emit(True, "Installation terminée avec succès!")
            
        except Exception as e:
            self.log_signal.emit(f"Erreur: {str(e)}")
            self.finished_signal.emit(False, f"Erreur lors de l'installation: {str(e)}")

    def check_prerequisites(self):
        try:
            # Vérifier Git
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            self.log_signal.emit("Git est installé")
            
            # Vérifier Python
            subprocess.run(["python3", "--version"], check=True, capture_output=True)
            self.log_signal.emit("Python 3 est installé")
            
            return True
        except subprocess.CalledProcessError:
            self.log_signal.emit("Certains prérequis ne sont pas installés")
            return False

    def clone_repo(self):
        if not os.path.exists("paperless-ngx"):
            self.log_signal.emit("Clonage du dépôt paperless-ngx...")
            subprocess.run(["git", "clone", "https://github.com/paperless-ngx/paperless-ngx.git"], 
                          check=True, capture_output=True)
            self.log_signal.emit("Dépôt cloné avec succès")
        else:
            self.log_signal.emit("Le dépôt paperless-ngx existe déjà")

    def install_docker(self):
        system = platform.system()
        self.log_signal.emit(f"Installation de Docker pour {system}...")
        
        if system == "Linux":
            # Installation Docker sur Linux
            commands = [
                ["sudo", "apt-get", "update"],
                ["sudo", "apt-get", "install", "-y", "docker.io", "docker-compose"],
                ["sudo", "systemctl", "enable", "--now", "docker"],
                ["sudo", "usermod", "-aG", "docker", os.getenv("USER")]
            ]
            
            for cmd in commands:
                if self.cancelled:
                    return
                subprocess.run(cmd, check=True)
                
        elif system == "Windows":
            # Télécharger Docker Desktop pour Windows
            subprocess.run(["winget", "install", "-e", "--id", "Docker.DockerDesktop"], check=True)
        elif system == "Darwin":
            # Télécharger Docker Desktop pour Mac
            subprocess.run(["brew", "install", "--cask", "docker"], check=True)
        
        self.log_signal.emit("Docker installé avec succès")

    def configure_paperless(self):
        self.log_signal.emit("Configuration de Paperless-ngx...")
        os.chdir("paperless-ngx")
        
        # Copier le fichier de configuration exemple
        if not os.path.exists("docker-compose.env"):
            subprocess.run(["cp", "docker-compose.env.example", "docker-compose.env"], check=True)
            self.log_signal.emit("Fichier de configuration créé")
        
        # Modifier les paramètres par défaut si nécessaire
        # (ici vous pourriez ajouter des modifications automatiques)
        
        self.log_signal.emit("Configuration terminée")

    def start_paperless(self):
        self.log_signal.emit("Lancement de Paperless-ngx via Docker...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        self.log_signal.emit("Paperless-ngx est en cours de démarrage...")
        
        # Attendre que le service soit opérationnel
        subprocess.run(["docker-compose", "exec", "-T", "webserver", "manage.py", "migrate"], check=True)
        self.log_signal.emit("Migration de la base de données terminée")

    def cancel(self):
        self.cancelled = True
        self.log_signal.emit("Installation annulée par l'utilisateur")


class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Installateur Paperless-ngx")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon.fromTheme("system-software-install"))
        
        # Style et thème
        qdarktheme.setup_theme()
        
        self.init_ui()
        self.install_thread = None

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # En-tête
        header = QLabel("Installateur Paperless-ngx")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("margin: 20px 0; color: #2b79c2;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("""
        Paperless-ngx est un système moderne de gestion de documents (DMS) qui vous permet
        de numériser, indexer et archiver tous vos documents papier.
        """)
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("margin: 0 30px 20px 30px;")
        layout.addWidget(desc)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3a3a3a;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2b79c2;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Label d'état
        self.status_label = QLabel("Prêt à installer")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-style: italic; margin: 10px 0;")
        layout.addWidget(self.status_label)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        self.install_button = QPushButton("Commencer l'installation")
        self.install_button.setIcon(QIcon.fromTheme("system-run"))
        self.install_button.clicked.connect(self.start_installation)
        self.install_button.setStyleSheet("""
            QPushButton {
                background-color: #2b79c2;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a8ad2;
            }
        """)
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.cancel_button.clicked.connect(self.cancel_installation)
        self.cancel_button.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.install_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Journal d'installation
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #252525;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 5px;
                font-family: monospace;
            }
        """)
        layout.addWidget(self.log_output)
        
        # Pied de page
        footer = QLabel("© 2023 - Installateur Paperless-ngx")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer.setStyleSheet("color: #7a7a7a; margin-top: 10px;")
        layout.addWidget(footer)

    def start_installation(self):
        self.install_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.log_output.clear()
        
        self.install_thread = InstallThread()
        self.install_thread.progress_update.connect(self.update_progress)
        self.install_thread.finished_signal.connect(self.installation_finished)
        self.install_thread.log_signal.connect(self.log_message)
        self.install_thread.start()

    def cancel_installation(self):
        if self.install_thread and self.install_thread.isRunning():
            self.install_thread.cancel()
            self.cancel_button.setEnabled(False)
            self.status_label.setText("Installation annulée")

    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def installation_finished(self, success, message):
        self.install_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Résultat de l'installation")
        
        if success:
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText("Installation terminée avec succès!")
            msg_box.setInformativeText("""
            Paperless-ngx a été installé avec succès.
            
            Vous pouvez y accéder via:
            http://localhost:8000
            
            Identifiants par défaut:
            Utilisateur: admin
            Mot de passe: admin
            """)
        else:
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText("Erreur lors de l'installation")
            msg_box.setInformativeText(message)
        
        msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Style supplémentaire
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = InstallerWindow()
    window.show()
    
    sys.exit(app.exec())