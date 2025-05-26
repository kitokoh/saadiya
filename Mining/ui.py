import sys
import json
import psutil  # Pour la surveillance du CPU
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QWidget, QFileDialo, QTabWidget, QFormLayout, QSpinBox,
    QComboBox, QCheckBox, QSlider, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor


class UltimateMoneroMiningMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monero Mining Monitor")
        self.setGeometry(100, 100, 1000, 800)
        self.config_data = {}  # Dictionnaire pour stocker les données JSON
        self.current_file = "config.json"  # Chemin du fichier JSON

        # Initialisation de l'interface
        self.initUI()
        self.apply_styles()

        # Charger le fichier JSON au démarrage
        self.load_json()

        # Timer pour la mise à jour des statistiques
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_live_stats)
        self.stats_timer.start(2000)  # Rafraîchir toutes les 2 secondes

    def initUI(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Barre d'outils supérieure
        toolbar_layout = QHBoxLayout()
        self.load_button = QPushButton("🔄 Recharger")
        self.load_button.clicked.connect(self.load_json)
        toolbar_layout.addWidget(self.load_button)

        self.save_button = QPushButton("💾 Sauvegarder")
        self.save_button.clicked.connect(self.save_json)
        toolbar_layout.addWidget(self.save_button)

        main_layout.addLayout(toolbar_layout)

        # Onglets pour organiser les sections
        self.tabs = QTabWidget()
        self.init_stats_tab()
        self.init_config_tab()
        main_layout.addWidget(self.tabs)

        # Widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def init_stats_tab(self):
        stats_tab = QWidget()
        layout = QVBoxLayout()

        # Titre
        title_label = QLabel("Statistiques en Temps Réel")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title_label)

        # Hasrate
        self.hashrate_label = QLabel("Hashrate : 0 H/s")
        layout.addWidget(self.hashrate_label)

        # Température du CPU
        self.cpu_temp_label = QLabel("Température CPU : N/A")
        layout.addWidget(self.cpu_temp_label)

        # Utilisation du CPU
        self.cpu_usage_label = QLabel("Utilisation CPU : 0%")
        layout.addWidget(self.cpu_usage_label)

        # Barre de progression pour l'utilisation du CPU
        self.cpu_usage_progress = QProgressBar()
        self.cpu_usage_progress.setRange(0, 100)
        layout.addWidget(self.cpu_usage_progress)

        # Shares acceptés
        self.shares_label = QLabel("Shares acceptés : 0")
        layout.addWidget(self.shares_label)

        stats_tab.setLayout(layout)
        self.tabs.addTab(stats_tab, "📊 Statistiques")

    def init_config_tab(self):
        config_tab = QWidget()
        layout = QFormLayout()

        # Titre
        title_label = QLabel("Configuration du Mineur")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addRow(title_label)

        # URL du pool
        self.pool_url_input = QLineEdit()
        layout.addRow("URL du pool :", self.pool_url_input)

        # Adresse du portefeuille
        self.wallet_address_input = QLineEdit()
        layout.addRow("Adresse du portefeuille :", self.wallet_address_input)

        # Rig ID
        self.rig_id_input = QLineEdit()
        layout.addRow("Rig ID :", self.rig_id_input)

        # Limite d'utilisation du CPU
        self.cpu_limit_slider = QSlider(Qt.Horizontal)
        self.cpu_limit_slider.setRange(0, 100)
        self.cpu_limit_slider.setValue(100)
        self.cpu_limit_slider.valueChanged.connect(self.update_cpu_limit)
        layout.addRow("Limite d'utilisation du CPU :", self.cpu_limit_slider)

        config_tab.setLayout(layout)
        self.tabs.addTab(config_tab, "⚙️ Configuration")

    def apply_styles(self):
        # Appliquer un style moderne
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QPushButton {
                background-color: #4C566A;
                color: #ECEFF4;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QLabel, QLineEdit, QSlider {
                color: #ECEFF4;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #4C566A;
                background-color: #3B4252;
            }
            QTabBar::tab {
                background-color: #4C566A;
                color: #ECEFF4;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #5E81AC;
            }
            QProgressBar {
                background-color: #4C566A;
                color: #ECEFF4;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #88C0D0;
                border-radius: 5px;
            }
        """)

    def load_json(self):
        try:
            with open(self.current_file, "r") as file:
                self.config_data = json.load(file)
            self.update_ui()
            QMessageBox.information(self, "Succès", "Fichier JSON chargé avec succès !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement du fichier : {str(e)}")

    def save_json(self):
        try:
            with open(self.current_file, "w") as file:
                json.dump(self.config_data, file, indent=4)
            QMessageBox.information(self, "Succès", "Fichier JSON sauvegardé avec succès !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {str(e)}")

    def update_ui(self):
        # Mettre à jour les champs avec les données JSON
        if "pools" in self.config_data and len(self.config_data["pools"]) > 0:
            pool = self.config_data["pools"][0]
            self.pool_url_input.setText(pool.get("url", ""))
            self.wallet_address_input.setText(pool.get("user", ""))
            self.rig_id_input.setText(pool.get("rig-id", ""))

    def update_live_stats(self):
        # Mettre à jour les statistiques en temps réel
        cpu_usage = psutil.cpu_percent()
        self.cpu_usage_label.setText(f"Utilisation CPU : {cpu_usage}%")
        self.cpu_usage_progress.setValue(int(cpu_usage))

        # Température du CPU (avec gestion des erreurs)
        try:
            temps = psutil.sensors_temperatures()
            if "coretemp" in temps:
                self.cpu_temp_label.setText(f"Température CPU : {temps['coretemp'][0].current}°C")
            else:
                self.cpu_temp_label.setText("Température CPU : N/A")
        except Exception as e:
            self.cpu_temp_label.setText("Température CPU : N/A")

        # Simuler un hashrate et des shares
        self.hashrate_label.setText(f"Hashrate : {1000 + (id(self) % 1000)} H/s")
        self.shares_label.setText(f"Shares acceptés : {100 + (id(self) % 50)}")

    def update_cpu_limit(self, value):
        # Mettre à jour la limite d'utilisation du CPU
        self.cpu_usage_label.setText(f"Utilisation CPU : {value}%")
        # Ici, vous pouvez ajouter la logique pour limiter l'utilisation du CPU

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Quitter", "Êtes-vous sûr de vouloir quitter ? Les modifications non sauvegardées seront perdues.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UltimateMoneroMiningMonitor()
    window.show()
    sys.exit(app.exec_())