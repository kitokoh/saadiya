from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                            QTextEdit, QProgressBar, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
import sys
import os
import platform
import subprocess
import webbrowser
import requests

DOCKER_COMPOSE_URL = "https://raw.githubusercontent.com/invoiceninja/invoiceninja/master/docker-compose.yml"

class InvoiceNinjaInstaller(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        # Widgets
        self.title_label = QLabel("Invoice Ninja Installer")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        self.install_btn = QPushButton("Lancer l'installation")
        self.install_btn.clicked.connect(self.start_installation)

        self.open_btn = QPushButton("Ouvrir Invoice Ninja")
        self.open_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000"))
        self.open_btn.setEnabled(False)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.install_btn)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_output)

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel { 
                color: #333333; 
                font-size: 16px; 
                padding: 10px; 
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled { background-color: #555555; }
            QTextEdit {
                background-color: white;
                color: #333333;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-family: Consolas;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                color: #333333;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2E7D32);
                border-radius: 5px;
            }
        """)

    def start_installation(self):
        self.install_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_output.clear()

        self.thread = InstallerThread()
        self.thread.log_signal.connect(self.update_log)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.finished_signal.connect(self.installation_finished)
        self.thread.start()

    def update_log(self, message):
        self.log_output.append(message)

    def installation_finished(self, success):
        self.progress_bar.setValue(100)
        self.open_btn.setEnabled(success)
        if success:
            QMessageBox.information(self, "Succès", "Invoice Ninja est prêt ! Cliquez sur 'Ouvrir'.")
        else:
            QMessageBox.critical(self, "Erreur", "Installation échouée. Consultez les logs.")


class InstallerThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)

    def run(self):
        try:
            # Vérification/Installation de Docker (Linux uniquement)
            if platform.system() == "Linux":
                self.log_signal.emit("🔍 Vérification de Docker...")
                try:
                    subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    self.log_signal.emit("⚠️ Docker non installé. Installation en cours...")
                    subprocess.run(["sudo", "apt-get", "update"], check=True)
                    subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"], check=True)
                    subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
                    subprocess.run(["sudo", "systemctl", "enable", "docker"], check=True)
                    self.log_signal.emit("✅ Docker installé avec succès.")

            # Téléchargement du docker-compose.yml
            self.log_signal.emit("\n📥 Téléchargement de la configuration Docker...")
            response = requests.get(DOCKER_COMPOSE_URL)
            with open("docker-compose.yml", "wb") as f:
                f.write(response.content)
            self.log_signal.emit("✅ Fichier docker-compose.yml téléchargé.")

            # Lancement des conteneurs
            self.log_signal.emit("\n🚀 Démarrage d'Invoice Ninja...")
            process = subprocess.Popen(
                ["docker-compose", "up", "-d"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_signal.emit(output.strip())
            
            self.finished_signal.emit(process.returncode == 0)

        except Exception as e:
            self.log_signal.emit(f"❌ Erreur critique : {str(e)}")
            self.finished_signal.emit(False)


if __name__ == "__main__":
    # Pour tester l'installateur seul
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InvoiceNinjaInstaller()
    window.show()
    sys.exit(app.exec_())