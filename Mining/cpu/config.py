import sys
import psutil
import time
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFormLayout, QGroupBox
)
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


# Thread pour exécuter le processus de minage
class MiningThread(QThread):
    update_log_signal = pyqtSignal(str)  # Signal pour mettre à jour les logs

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None
        self.is_running = False

    def run(self):
        self.is_running = True
        self.process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        while self.is_running:
            output = self.process.stdout.readline()
            if output:
                self.update_log_signal.emit(output.strip())
            if self.process.poll() is not None:  # Vérifie si le processus est terminé
                break
        self.is_running = False

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.is_running = False


# Fenêtre principale de l'application
class MiningApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Monero Mining Manager")
        self.setGeometry(100, 100, 800, 600)

        # Variables
        self.mining_thread = None
        self.mining_command = []
        self.cpu_threshold = 70  # Seuil de température par défaut
        self.cpu_usage_threshold = 80  # Seuil d'utilisation du CPU par défaut

        # Layout principal
        layout = QVBoxLayout()

        # Formulaire de configuration
        config_group = QGroupBox("Configuration du minage")
        config_layout = QFormLayout()

        self.pool_address_input = QLineEdit("pool.minexmr.com:5555")
        config_layout.addRow("Adresse du pool:", self.pool_address_input)

        self.wallet_input = QLineEdit("Votre adresse de portefeuille Monero")
        config_layout.addRow("Portefeuille Monero:", self.wallet_input)

        self.threads_input = QLineEdit(str(psutil.cpu_count(logical=True)))
        config_layout.addRow("Nombre de threads:", self.threads_input)

        self.cpu_threshold_input = QLineEdit(str(self.cpu_threshold))
        config_layout.addRow("Seuil de température CPU (°C):", self.cpu_threshold_input)

        self.cpu_usage_input = QLineEdit(str(self.cpu_usage_threshold))
        config_layout.addRow("Seuil d'utilisation CPU (%):", self.cpu_usage_input)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Boutons de contrôle
        self.start_button = QPushButton("Démarrer le minage")
        self.start_button.clicked.connect(self.start_mining)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Arrêter le minage")
        self.stop_button.clicked.connect(self.stop_mining)
        layout.addWidget(self.stop_button)

        # Affichage des logs
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        # Conteneur principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer pour la surveillance système
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.monitor_system)
        self.monitor_timer.start(5000)  # Vérifie toutes les 5 secondes

    def start_mining(self):
        # Récupérer les paramètres de configuration
        pool_address = self.pool_address_input.text()
        wallet = self.wallet_input.text()
        threads = self.threads_input.text()
        self.cpu_threshold = int(self.cpu_threshold_input.text())
        self.cpu_usage_threshold = int(self.cpu_usage_input.text())

        # Construire la commande de minage
        self.mining_command = [
            "xmrig",  # Remplacez par le chemin de votre exécutable xmrig
            "-o", pool_address,
            "-u", wallet,
            "-t", threads
        ]

        # Démarrer le thread de minage
        self.mining_thread = MiningThread(self.mining_command)
        self.mining_thread.update_log_signal.connect(self.update_log)
        self.mining_thread.start()

        self.log_output.append("Démarrage du minage...")

    def stop_mining(self):
        if self.mining_thread:
            self.mining_thread.stop()
            self.mining_thread.wait()
            self.log_output.append("Minage arrêté.")

    def update_log(self, message):
        self.log_output.append(message)

    def monitor_system(self):
        if not self.mining_thread or not self.mining_thread.is_running:
            return

        # Surveiller la température du CPU
        cpu_temp = self.get_cpu_temperature()
        if cpu_temp > self.cpu_threshold:
            self.log_output.append(f"Alerte : Température CPU élevée ({cpu_temp}°C). Réduction de l'intensité du minage.")
            self.adjust_mining_intensity(False)

        # Surveiller l'utilisation du CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > self.cpu_usage_threshold:
            self.log_output.append(f"Alerte : Utilisation CPU élevée ({cpu_usage}%). Réduction de l'intensité du minage.")
            self.adjust_mining_intensity(False)

    def get_cpu_temperature(self):
        # Exemple pour Linux (utilisez psutil ou d'autres méthodes pour Windows)
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            return temps["coretemp"][0].current
        return 0  # Retourne 0 si la température ne peut pas être lue

    def adjust_mining_intensity(self, increase):
        # Placeholder pour ajuster l'intensité du minage
        if increase:
            self.log_output.append("Augmentation de l'intensité du minage.")
        else:
            self.log_output.append("Réduction de l'intensité du minage.")


# Point d'entrée de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiningApp()
    window.show()
    sys.exit(app.exec_())