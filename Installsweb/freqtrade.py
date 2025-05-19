import sys
import os
import subprocess
import platform
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, 
                           QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
                           QFileDialog, QLineEdit, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont

class FreqtradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade Manager Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(QSize(800, 600))
        
        # Chemins importants
        self.base_dir = os.path.join("C:\\", "Freqtrade")
        self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
        self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
        
        # Initialisation de la base de données
        self.init_db()
        
        # Vérification de l'installation existante
        self.installed = self.check_installation()
        self.docker_installed = self.check_docker()
        
        # Initialisation de l'interface
        self.init_ui()
        self.init_tray_icon()
        
        # Style
        self.set_style()

    def init_db(self):
        """Initialise la base de données SQLite"""
        os.makedirs(self.base_dir, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Table des installations
        c.execute('''CREATE TABLE IF NOT EXISTS installations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      version TEXT,
                      path TEXT,
                      install_date TEXT,
                      status TEXT)''')
        
        # Table des exécutions
        c.execute('''CREATE TABLE IF NOT EXISTS executions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      start_time TEXT,
                      end_time TEXT,
                      command TEXT,
                      status TEXT)''')
        
        conn.commit()
        conn.close()

    def log_installation(self, version, status):
        """Journalise l'installation dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO installations (version, path, install_date, status) VALUES (?, ?, ?, ?)",
                  (version, self.freqtrade_dir, datetime.now().isoformat(), status))
        conn.commit()
        conn.close()

    def log_execution(self, command, status):
        """Journalise l'exécution dans la base de données"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO executions (start_time, command, status) VALUES (?, ?, ?)",
                  (datetime.now().isoformat(), command, status))
        conn.commit()
        conn.close()

    def check_installation(self):
        """Vérifie si Freqtrade est déjà installé"""
        return os.path.exists(os.path.join(self.freqtrade_dir, "setup.py"))

    def check_docker(self):
        """Vérifie si Docker est installé"""
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            return True
        except:
            return False

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Création des onglets
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Onglet Installation
        self.setup_install_tab()
        
        # Onglet Exécution
        self.setup_execution_tab()
        
        # Onglet Historique
        self.setup_history_tab()
        
        # Barre de statut
        self.statusBar().showMessage("Prêt")

    def setup_install_tab(self):
        """Configure l'onglet d'installation"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Installation Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Options d'installation
        options_group = QGroupBox("Options d'installation")
        options_layout = QVBoxLayout()
        
        # Version à installer
        version_layout = QHBoxLayout()
        version_label = QLabel("Version:")
        self.version_combo = QComboBox()
        self.version_combo.addItems(["stable", "develop"])
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_combo)
        options_layout.addLayout(version_layout)
        
        # Options
        self.docker_check = QCheckBox("Installer Docker")
        self.docker_check.setChecked(True)
        self.docker_check.setEnabled(not self.docker_installed)
        options_layout.addWidget(self.docker_check)
        
        self.plot_check = QCheckBox("Installer les dépendances de visualisation")
        self.plot_check.setChecked(True)
        options_layout.addWidget(self.plot_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Bouton d'installation
        self.install_btn = QPushButton("Installer Freqtrade" if not self.installed else "Mettre à jour Freqtrade")
        self.install_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.install_btn.clicked.connect(self.start_installation)
        layout.addWidget(self.install_btn)
        
        # Barre de progression
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Console de sortie
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 10))
        layout.addWidget(self.output)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Installation")

    def setup_execution_tab(self):
        """Configure l'onglet d'exécution"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Exécution Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Boutons d'exécution
        self.start_btn = QPushButton("Démarrer Freqtrade")
        self.start_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.start_btn.setEnabled(self.installed)
        self.start_btn.clicked.connect(self.start_freqtrade)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Arrêter Freqtrade")
        self.stop_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_freqtrade)
        layout.addWidget(self.stop_btn)
        
        # Options d'exécution
        exec_group = QGroupBox("Options d'exécution")
        exec_layout = QVBoxLayout()
        
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Trade", "Backtest", "Hyperopt", "Plot"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        exec_layout.addLayout(mode_layout)
        
        strategy_layout = QHBoxLayout()
        strategy_label = QLabel("Stratégie:")
        self.strategy_input = QLineEdit("SampleStrategy")
        strategy_layout.addWidget(strategy_label)
        strategy_layout.addWidget(self.strategy_input)
        exec_layout.addLayout(strategy_layout)
        
        exec_group.setLayout(exec_layout)
        layout.addWidget(exec_group)
        
        # Console d'exécution
        self.exec_output = QTextEdit()
        self.exec_output.setReadOnly(True)
        self.exec_output.setFont(QFont("Consolas", 10))
        layout.addWidget(self.exec_output)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Exécution")

    def setup_history_tab(self):
        """Configure l'onglet d'historique"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Historique des Exécutions</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Tableau d'historique
        self.history_table = QTextEdit()
        self.history_table.setReadOnly(True)
        layout.addWidget(self.history_table)
        
        self.update_history()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Historique")

    def set_style(self):
        """Applique le style à l'application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                padding: 5px;
                border-radius: 4px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #3498db;
                color: white;
            }
            QTabWidget::pane {
                border-top: 2px solid #bdc3c7;
            }
            QTabBar::tab {
                padding: 8px;
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)

    def start_installation(self):
        """Lance le processus d'installation"""
        self.install_btn.setEnabled(False)
        self.output.clear()
        
        # Créer le répertoire si nécessaire
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Préparer les commandes d'installation
        version = self.version_combo.currentText()
        commands = self.get_install_commands(version)
        
        # Exécuter les commandes une par une
        self.current_command = 0
        self.commands = commands
        self.progress.setMaximum(len(commands))
        self.execute_next_command()

    def get_install_commands(self, version):
        """Retourne les commandes d'installation appropriées"""
        commands = []
        
        # Installation Docker si nécessaire
        if self.docker_check.isChecked() and not self.docker_installed:
            if platform.system() == "Windows":
                commands.extend([
                    f"cd /d {self.base_dir}",
                    "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile docker_installer.exe",
                    "Start-Process -Wait -FilePath .\\docker_installer.exe -ArgumentList 'install --quiet'",
                    "Remove-Item docker_installer.exe"
                ])
            else:
                commands.extend([
                    "sudo apt-get update",
                    "sudo apt-get install -y docker.io docker-compose",
                    "sudo systemctl enable --now docker",
                    "sudo usermod -aG docker $USER"
                ])
        
        # Commandes Freqtrade
        commands.extend([
            f"cd /d {self.base_dir}",
            f"git clone https://github.com/freqtrade/freqtrade.git" if not os.path.exists(self.freqtrade_dir) else f"cd {self.freqtrade_dir} && git pull",
            f"cd {self.freqtrade_dir} && git checkout {version}",
            f"cd {self.freqtrade_dir} && python -m pip install -e .",
            f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt"
        ])
        
        # Dépendances optionnelles
        if self.plot_check.isChecked():
            commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt")
        
        return commands

    def execute_next_command(self):
        """Exécute la prochaine commande dans la séquence"""
        if self.current_command < len(self.commands):
            cmd = self.commands[self.current_command]
            self.output.append(f"> {cmd}")
            
            try:
                # Exécuter la commande
                process = subprocess.run(
                    cmd,
                    cwd=self.base_dir,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Afficher la sortie
                if process.stdout:
                    self.output.append(process.stdout)
                if process.stderr:
                    self.output.append(f"<font color='orange'>{process.stderr}</font>")
                
                # Passer à la commande suivante
                self.current_command += 1
                self.progress.setValue(self.current_command)
                QTimer.singleShot(100, self.execute_next_command)
                
            except subprocess.CalledProcessError as e:
                self.output.append(f"<font color='red'>ERREUR: {e.stderr}</font>")
                self.install_btn.setEnabled(True)
                self.log_installation(self.version_combo.currentText(), "Échec")
        else:
            # Installation terminée
            self.install_btn.setText("Mettre à jour Freqtrade")
            self.start_btn.setEnabled(True)
            self.install_btn.setEnabled(True)
            self.installed = True
            self.log_installation(self.version_combo.currentText(), "Succès")
            QMessageBox.information(self, "Succès", "Installation terminée avec succès!")

    def start_freqtrade(self):
        """Démarre Freqtrade"""
        mode = self.mode_combo.currentText().lower()
        strategy = self.strategy_input.text()
        
        if mode == "trade":
            cmd = f"cd {self.freqtrade_dir} && freqtrade trade --strategy {strategy}"
        elif mode == "backtest":
            cmd = f"cd {self.freqtrade_dir} && freqtrade backtesting --strategy {strategy}"
        elif mode == "hyperopt":
            cmd = f"cd {self.freqtrade_dir} && freqtrade hyperopt --strategy {strategy}"
        elif mode == "plot":
            cmd = f"cd {self.freqtrade_dir} && freqtrade plot-dataframe --strategy {strategy}"
        
        try:
            self.freqtrade_process = subprocess.Popen(
                cmd,
                cwd=self.freqtrade_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.log_execution(cmd, "Démarré")
            
            # Lire la sortie en temps réel
            QTimer.singleShot(100, self.read_freqtrade_output)
            
        except Exception as e:
            self.exec_output.append(f"<font color='red'>ERREUR: {str(e)}</font>")

    def read_freqtrade_output(self):
        """Lit la sortie de Freqtrade en temps réel"""
        if hasattr(self, 'freqtrade_process'):
            stdout = self.freqtrade_process.stdout.readline()
            stderr = self.freqtrade_process.stderr.readline()
            
            if stdout:
                self.exec_output.append(stdout.strip())
            if stderr:
                self.exec_output.append(f"<font color='orange'>{stderr.strip()}</font>")
            
            if self.freqtrade_process.poll() is None:
                QTimer.singleShot(100, self.read_freqtrade_output)
            else:
                self.stop_btn.setEnabled(False)
                self.start_btn.setEnabled(True)
                self.log_execution("", "Terminé")

    def stop_freqtrade(self):
        """Arrête Freqtrade"""
        if hasattr(self, 'freqtrade_process'):
            self.freqtrade_process.terminate()
            self.stop_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.log_execution("", "Arrêté")

    def update_history(self):
        """Met à jour l'historique des exécutions"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM executions ORDER BY start_time DESC LIMIT 50")
        executions = c.fetchall()
        
        c.execute("SELECT * FROM installations ORDER BY install_date DESC LIMIT 10")
        installations = c.fetchall()
        
        history_text = "<h2>Dernières Installations</h2><ul>"
        for install in installations:
            history_text += f"<li>{install[2]} - {install[1]} ({install[4]})</li>"
        history_text += "</ul><h2>Dernières Exécutions</h2><ul>"
        
        for exec_ in executions:
            history_text += f"<li>{exec_[2]} - {exec_[4]}</li>"
        history_text += "</ul>"
        
        self.history_table.setHtml(history_text)
        conn.close()

    def init_tray_icon(self):
        """Initialise l'icône de la barre système"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("system-run"))
        
        tray_menu = QMenu()
        open_action = tray_menu.addAction("Ouvrir")
        open_action.triggered.connect(self.show)
        
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Vérifier et installer les dépendances si nécessaire
    try:
        from PyQt5 import QtWidgets
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"])
    
    window = FreqtradeManager()
    window.show()
    sys.exit(app.exec_())