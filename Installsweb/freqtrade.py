import sys
import os
import subprocess
import platform
import sqlite3
import shutil
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, 
                           QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
                           QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
                           QAction)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QTextCursor

class CommandWorker(QThread):
    output_signal = pyqtSignal(str, str)  # text, color
    
    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.process = None
        
    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                bufsize=1
            )
            
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip(), "white")
                
                err = self.process.stderr.readline()
                if err:
                    self.output_signal.emit(err.strip(), "red")
                    
        except Exception as e:
            self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            
    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                if platform.system() == "Windows":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], check=True)
                else:
                    self.process.terminate()
                    self.process.wait()
            except Exception as e:
                self.output_signal.emit(f"Error stopping process: {str(e)}", "red")

class FreqtradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade Manager Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(QSize(800, 600))
        
        # Chemins importants
        self.base_dir = self.get_base_dir()
        self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
        self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
        self.config_dir = os.path.join(self.base_dir, "user_data")
        
        # Variables d'état
        self.installation_in_progress = False
        self.freqtrade_running = False
        self.current_worker = None
        
        # Initialisation de la base de données
        self.init_db()
        
        # Vérification des dépendances
        self.check_dependencies()
        
        # Initialisation de l'interface
        self.init_ui()
        self.init_tray_icon()
        self.init_menu_bar()
        
        # Style
        self.set_style()
        
        # Mise à jour de l'état initial
        self.update_ui_state()

    def get_base_dir(self):
        """Détermine le répertoire de base approprié selon le système d'exploitation"""
        if platform.system() == "Windows":
            return os.path.join(os.environ.get("APPDATA", "C:\\"), "Freqtrade")
        else:
            return os.path.join(os.path.expanduser("~"), ".freqtrade_manager")

    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Table des installations
            c.execute('''CREATE TABLE IF NOT EXISTS installations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          version TEXT,
                          path TEXT,
                          install_date TEXT,
                          status TEXT,
                          details TEXT)''')
            
            # Table des exécutions
            c.execute('''CREATE TABLE IF NOT EXISTS executions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          start_time TEXT,
                          end_time TEXT,
                          command TEXT,
                          status TEXT,
                          output TEXT)''')
            
            # Table des configurations
            c.execute('''CREATE TABLE IF NOT EXISTS configurations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          path TEXT,
                          last_used TEXT)''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

    def log_installation(self, version, status, details=""):
        """Journalise l'installation dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO installations (version, path, install_date, status, details) VALUES (?, ?, ?, ?, ?)",
                      (version, self.freqtrade_dir, datetime.now().isoformat(), status, details))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log installation: {str(e)}")

    def log_execution(self, command, status, output=""):
        """Journalise l'exécution dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            if status == "Démarré":
                c.execute("INSERT INTO executions (start_time, command, status) VALUES (?, ?, ?)",
                          (datetime.now().isoformat(), command, status))
            else:
                # Mettre à jour la dernière exécution
                c.execute("UPDATE executions SET end_time=?, status=?, output=? WHERE id=(SELECT MAX(id) FROM executions)",
                          (datetime.now().isoformat(), status, output))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log execution: {str(e)}")

    def check_dependencies(self):
        """Vérifie les dépendances requises"""
        self.git_installed = self.check_command_available("git --version")
        self.python_installed = self.check_command_available("python --version") or self.check_command_available("python3 --version")
        self.docker_installed = self.check_command_available("docker --version")
        self.freqtrade_installed = self.check_freqtrade_installation()
        
    def check_command_available(self, command):
        """Vérifie si une commande système est disponible"""
        try:
            subprocess.run(command, shell=True, check=True, 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except:
            return False
            
    def check_freqtrade_installation(self):
        """Vérifie si Freqtrade est déjà installé"""
        if not os.path.exists(self.freqtrade_dir):
            return False
            
        try:
            # Vérifier si freqtrade est installé et fonctionnel
            result = subprocess.run(["freqtrade", "--version"], 
                                  cwd=self.freqtrade_dir,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            return result.returncode == 0
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
        
        # Onglet Configuration
        self.setup_config_tab()
        
        # Onglet Exécution
        self.setup_execution_tab()
        
        # Onglet Historique
        self.setup_history_tab()
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")

    def setup_install_tab(self):
        """Configure l'onglet d'installation"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Installation Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Vérification des dépendances
        deps_group = QGroupBox("Vérification des dépendances")
        deps_layout = QVBoxLayout()
        
        self.git_status = QLabel(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
        self.python_status = QLabel(f"Python: {'Installé' if self.python_installed else 'Manquant'}")
        self.docker_status = QLabel(f"Docker: {'Installé' if self.docker_installed else 'Manquant'}")
        self.freqtrade_status = QLabel(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        
        deps_layout.addWidget(self.git_status)
        deps_layout.addWidget(self.python_status)
        deps_layout.addWidget(self.docker_status)
        deps_layout.addWidget(self.freqtrade_status)
        
        deps_group.setLayout(deps_layout)
        layout.addWidget(deps_group)
        
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
        self.docker_check = QCheckBox("Installer Docker (si manquant)")
        self.docker_check.setChecked(True)
        options_layout.addWidget(self.docker_check)
        
        self.plot_check = QCheckBox("Installer les dépendances de visualisation")
        self.plot_check.setChecked(True)
        options_layout.addWidget(self.plot_check)
        
        self.ta_check = QCheckBox("Installer les dépendances d'analyse technique")
        self.ta_check.setChecked(True)
        options_layout.addWidget(self.ta_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Bouton d'installation
        self.install_btn = QPushButton("Installer Freqtrade" if not self.freqtrade_installed else "Mettre à jour Freqtrade")
        self.install_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.install_btn.clicked.connect(self.start_installation)
        layout.addWidget(self.install_btn)
        
        # Bouton de réparation
        self.repair_btn = QPushButton("Réparer l'installation")
        self.repair_btn.setStyleSheet("background-color: #f39c12; color: white;")
        self.repair_btn.clicked.connect(self.repair_installation)
        layout.addWidget(self.repair_btn)
        
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

    def setup_config_tab(self):
        """Configure l'onglet de configuration"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Configuration Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Configuration existante
        config_group = QGroupBox("Configurations existantes")
        config_layout = QVBoxLayout()
        
        self.config_combo = QComboBox()
        self.load_configurations()
        config_layout.addWidget(self.config_combo)
        
        btn_layout = QHBoxLayout()
        self.use_config_btn = QPushButton("Utiliser cette configuration")
        self.use_config_btn.clicked.connect(self.use_selected_config)
        btn_layout.addWidget(self.use_config_btn)
        
        self.edit_config_btn = QPushButton("Éditer")
        self.edit_config_btn.clicked.connect(self.edit_selected_config)
        btn_layout.addWidget(self.edit_config_btn)
        
        config_layout.addLayout(btn_layout)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Nouvelle configuration
        new_config_group = QGroupBox("Nouvelle configuration")
        new_config_layout = QVBoxLayout()
        
        self.new_config_name = QLineEdit()
        self.new_config_name.setPlaceholderText("Nom de la configuration")
        new_config_layout.addWidget(self.new_config_name)
        
        self.config_path_input = QLineEdit()
        self.config_path_input.setPlaceholderText("Chemin du fichier de configuration")
        new_config_layout.addWidget(self.config_path_input)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_config_file)
        new_config_layout.addWidget(browse_btn)
        
        self.create_config_btn = QPushButton("Créer configuration")
        self.create_config_btn.clicked.connect(self.create_new_config)
        new_config_layout.addWidget(self.create_config_btn)
        
        new_config_group.setLayout(new_config_layout)
        layout.addWidget(new_config_group)
        
        # Documentation
        doc_btn = QPushButton("Ouvrir la documentation Freqtrade")
        doc_btn.clicked.connect(self.open_documentation)
        layout.addWidget(doc_btn)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Configuration")

    def setup_execution_tab(self):
        """Configure l'onglet d'exécution"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Exécution Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Boutons d'exécution
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Démarrer Freqtrade")
        self.start_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.start_btn.clicked.connect(self.start_freqtrade)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Arrêter Freqtrade")
        self.stop_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_freqtrade)
        btn_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("Redémarrer")
        self.restart_btn.setStyleSheet("background-color: #f39c12; color: white;")
        self.restart_btn.setEnabled(False)
        self.restart_btn.clicked.connect(self.restart_freqtrade)
        btn_layout.addWidget(self.restart_btn)
        
        layout.addLayout(btn_layout)
        
        # Options d'exécution
        exec_group = QGroupBox("Options d'exécution")
        exec_layout = QVBoxLayout()
        
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Trade", "Backtest", "Hyperopt", "Plot", "Edge", "Download Data"])
        self.mode_combo.currentTextChanged.connect(self.update_mode_options)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        exec_layout.addLayout(mode_layout)
        
        # Options spécifiques au mode
        self.mode_options_stack = QWidget()
        self.mode_options_layout = QVBoxLayout(self.mode_options_stack)
        
        # Options pour le mode Trade
        self.trade_options = QWidget()
        trade_options_layout = QVBoxLayout(self.trade_options)
        
        strategy_layout = QHBoxLayout()
        strategy_label = QLabel("Stratégie:")
        self.strategy_input = QLineEdit("SampleStrategy")
        strategy_layout.addWidget(strategy_label)
        strategy_layout.addWidget(self.strategy_input)
        trade_options_layout.addLayout(strategy_layout)
        
        self.db_check = QCheckBox("Utiliser la base de données")
        self.db_check.setChecked(True)
        trade_options_layout.addWidget(self.db_check)
        
        self.trade_options.setLayout(trade_options_layout)
        self.mode_options_layout.addWidget(self.trade_options)
        
        # Options pour le mode Backtest
        self.backtest_options = QWidget()
        backtest_options_layout = QVBoxLayout(self.backtest_options)
        
        bt_strategy_layout = QHBoxLayout()
        bt_strategy_label = QLabel("Stratégie:")
        self.bt_strategy_input = QLineEdit("SampleStrategy")
        bt_strategy_layout.addWidget(bt_strategy_label)
        bt_strategy_layout.addWidget(self.bt_strategy_input)
        backtest_options_layout.addLayout(bt_strategy_layout)
        
        timerange_layout = QHBoxLayout()
        timerange_label = QLabel("Plage de temps:")
        self.timerange_input = QLineEdit()
        self.timerange_input.setPlaceholderText("YYYYMMDD-YYYYMMDD")
        timerange_layout.addWidget(timerange_label)
        timerange_layout.addWidget(self.timerange_input)
        backtest_options_layout.addLayout(timerange_layout)
        
        self.backtest_options.setLayout(backtest_options_layout)
        self.mode_options_layout.addWidget(self.backtest_options)
        
        # Ajouter d'autres options pour les autres modes...
        
        exec_layout.addWidget(self.mode_options_stack)
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
        
        # Filtres
        filter_layout = QHBoxLayout()
        
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(["Tous", "Installations", "Exécutions"])
        self.filter_type_combo.currentIndexChanged.connect(self.update_history)
        filter_layout.addWidget(self.filter_type_combo)
        
        self.refresh_history_btn = QPushButton("Actualiser")
        self.refresh_history_btn.clicked.connect(self.update_history)
        filter_layout.addWidget(self.refresh_history_btn)
        
        layout.addLayout(filter_layout)
        
        # Tableau d'historique
        self.history_table = QTextEdit()
        self.history_table.setReadOnly(True)
        layout.addWidget(self.history_table)
        
        self.update_history()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Historique")

    def init_menu_bar(self):
        """Initialise la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self.open_documentation)
        help_menu.addAction(docs_action)
        
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

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
        
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Gère les clics sur l'icône de la barre système"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

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
            QLabel[status="error"] {
                color: #e74c3c;
                font-weight: bold;
            }
            QLabel[status="success"] {
                color: #27ae60;
                font-weight: bold;
            }
        """)

    def update_ui_state(self):
        """Met à jour l'état de l'interface en fonction des dépendances"""
        self.git_status.setText(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
        self.python_status.setText(f"Python: {'Installé' if self.python_installed else 'Manquant'}")
        self.docker_status.setText(f"Docker: {'Installé' if self.docker_installed else 'Manquant'}")
        self.freqtrade_status.setText(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        
        # Activer/désactiver les boutons en fonction des dépendances
        self.install_btn.setEnabled(self.git_installed and self.python_installed)
        self.start_btn.setEnabled(self.freqtrade_installed)
        
        # Mettre à jour les styles en fonction de l'état
        for label, condition in [(self.git_status, self.git_installed),
                                (self.python_status, self.python_installed),
                                (self.docker_status, self.docker_installed),
                                (self.freqtrade_status, self.freqtrade_installed)]:
            label.setProperty("status", "success" if condition else "error")
            label.style().unpolish(label)
            label.style().polish(label)

    def start_installation(self):
        """Lance le processus d'installation"""
        if self.installation_in_progress:
            QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
            return
            
        # Vérifier les prérequis
        if not self.git_installed:
            QMessageBox.critical(self, "Erreur", "Git est requis pour installer Freqtrade")
            return
            
        if not self.python_installed:
            QMessageBox.critical(self, "Erreur", "Python est requis pour installer Freqtrade")
            return
            
        self.installation_in_progress = True
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
            elif platform.system() == "Linux":
                commands.extend([
                    "sudo apt-get update",
                    "sudo apt-get install -y docker.io docker-compose",
                    "sudo systemctl enable --now docker",
                    "sudo usermod -aG docker $USER"
                ])
            elif platform.system() == "Darwin":
                commands.extend([
                    "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
                    "brew install --cask docker"
                ])
        
        # Commandes Freqtrade
        if not os.path.exists(self.freqtrade_dir):
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git {self.freqtrade_dir}")
        else:
            commands.append(f"cd {self.freqtrade_dir} && git fetch --all")
            
        commands.extend([
            f"cd {self.freqtrade_dir} && git checkout {version}",
            f"cd {self.freqtrade_dir} && git pull",
            f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
            f"cd {self.freqtrade_dir} && python -m pip install -e .",
            f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt"
        ])
        
        # Dépendances optionnelles
        if self.plot_check.isChecked():
            commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt")
            
        if self.ta_check.isChecked():
            commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt")
        
        return commands

    def execute_next_command(self):
        """Exécute la prochaine commande dans la séquence"""
        if self.current_command < len(self.commands):
            cmd = self.commands[self.current_command]
            self.output.append(f"> {cmd}")
            
            try:
                # Créer un worker pour exécuter la commande
                self.current_worker = CommandWorker(cmd, self.base_dir)
                self.current_worker.output_signal.connect(self.handle_command_output)
                self.current_worker.finished.connect(self.command_finished)
                self.current_worker.start()
                
            except Exception as e:
                self.output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
                self.installation_failed()
                
        else:
            # Installation terminée avec succès
            self.installation_completed()

    def handle_command_output(self, text, color):
        """Affiche la sortie de la commande"""
        if color == "red":
            self.output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.output.append(text)
        
        # Faire défiler vers le bas
        self.output.moveCursor(QTextCursor.End)

    def command_finished(self):
        """Appelé lorsqu'une commande est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if self.current_command < len(self.commands):
            # Passer à la commande suivante
            QTimer.singleShot(100, self.execute_next_command)
        else:
            # Installation terminée avec succès
            self.installation_completed()

    def installation_completed(self):
        """Appelé lorsque l'installation est terminée avec succès"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)
        self.freqtrade_installed = True
        self.update_ui_state()
        
        version = self.version_combo.currentText()
        self.log_installation(version, "Succès", "Installation terminée avec succès")
        
        QMessageBox.information(self, "Succès", "Installation terminée avec succès!")
        
        # Vérifier si Docker a été installé
        if self.docker_check.isChecked():
            self.docker_installed = self.check_command_available("docker --version")
            self.update_ui_state()

    def installation_failed(self):
        """Appelé lorsque l'installation échoue"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)
        
        version = self.version_combo.currentText()
        self.log_installation(version, "Échec", "Échec de l'installation")
        
        QMessageBox.critical(self, "Erreur", "L'installation a échoué. Consultez la sortie pour plus de détails.")

    def repair_installation(self):
        """Tente de réparer une installation existante"""
        reply = QMessageBox.question(self, "Réparer", 
                                   "Voulez-vous vraiment réparer l'installation Freqtrade?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Réinstaller les dépendances
            commands = [
                f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
                f"cd {self.freqtrade_dir} && python -m pip install -e .",
                f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt",
                f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt",
                f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt"
            ]
            
            self.installation_in_progress = True
            self.output.clear()
            self.current_command = 0
            self.commands = commands
            self.progress.setMaximum(len(commands))
            self.execute_next_command()

    def start_freqtrade(self):
        """Démarre Freqtrade"""
        if self.freqtrade_running:
            QMessageBox.warning(self, "Déjà en cours", "Freqtrade est déjà en cours d'exécution")
            return
            
        mode = self.mode_combo.currentText().lower().replace(" ", "_")
        strategy = self.strategy_input.text()
        
        # Construire la commande de base
        cmd = f"cd {self.freqtrade_dir} && freqtrade {mode} --strategy {strategy}"
        
        # Ajouter des options spécifiques au mode
        if mode == "backtest":
            timerange = self.timerange_input.text()
            if timerange:
                cmd += f" --timerange {timerange}"
        
        try:
            self.exec_output.clear()
            self.freqtrade_running = True
            self.update_execution_buttons()
            
            self.current_worker = CommandWorker(cmd, self.freqtrade_dir)
            self.current_worker.output_signal.connect(self.handle_execution_output)
            self.current_worker.finished.connect(self.execution_finished)
            self.current_worker.start()
            
            self.log_execution(cmd, "Démarré")
            
        except Exception as e:
            self.exec_output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.freqtrade_running = False
            self.update_execution_buttons()

    def handle_execution_output(self, text, color):
        """Affiche la sortie de l'exécution de Freqtrade"""
        if color == "red":
            self.exec_output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.exec_output.append(text)
        
        # Faire défiler vers le bas
        self.exec_output.moveCursor(QTextCursor.End)

    def stop_freqtrade(self):
        """Arrête Freqtrade"""
        if not self.freqtrade_running:
            return
            
        if self.current_worker:
            self.current_worker.stop()
            
        self.freqtrade_running = False
        self.update_execution_buttons()
        self.log_execution("", "Arrêté")

    def restart_freqtrade(self):
        """Redémarre Freqtrade"""
        self.stop_freqtrade()
        QTimer.singleShot(1000, self.start_freqtrade)

    def execution_finished(self):
        """Appelé lorsque l'exécution de Freqtrade est terminée"""
        self.freqtrade_running = False
        self.update_execution_buttons()
        
        # Capturer la sortie finale
        output = self.exec_output.toPlainText()
        self.log_execution("", "Terminé", output)

    def update_execution_buttons(self):
        """Met à jour l'état des boutons d'exécution"""
        self.start_btn.setEnabled(not self.freqtrade_running)
        self.stop_btn.setEnabled(self.freqtrade_running)
        self.restart_btn.setEnabled(self.freqtrade_running)

    def update_mode_options(self):
        """Met à jour les options affichées en fonction du mode sélectionné"""
        mode = self.mode_combo.currentText()
        
        # Masquer toutes les options
        for i in range(self.mode_options_layout.count()):
            widget = self.mode_options_layout.itemAt(i).widget()
            if widget:
                widget.hide()
        
        # Afficher les options appropriées
        if mode == "Trade":
            self.trade_options.show()
        elif mode == "Backtest":
            self.backtest_options.show()
        # Ajouter d'autres conditions pour les autres modes...

    def load_configurations(self):
        """Charge les configurations depuis la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT name FROM configurations ORDER BY last_used DESC")
            configs = c.fetchall()
            
            self.config_combo.clear()
            for config in configs:
                self.config_combo.addItem(config[0])
                
            conn.close()
        except Exception as e:
            print(f"Failed to load configurations: {str(e)}")

    def use_selected_config(self):
        """Utilise la configuration sélectionnée"""
        config_name = self.config_combo.currentText()
        if not config_name:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT path FROM configurations WHERE name=?", (config_name,))
            path = c.fetchone()[0]
            
            # Mettre à jour la date d'utilisation
            c.execute("UPDATE configurations SET last_used=? WHERE name=?", 
                     (datetime.now().isoformat(), config_name))
            conn.commit()
            conn.close()
            
            # Copier le fichier de configuration vers le répertoire user_data
            os.makedirs(os.path.join(self.config_dir, "configs"), exist_ok=True)
            dest_path = os.path.join(self.config_dir, "configs", "config.json")
            shutil.copy2(path, dest_path)
            
            QMessageBox.information(self, "Succès", f"Configuration {config_name} appliquée avec succès!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'appliquer la configuration: {str(e)}")

    def edit_selected_config(self):
        """Ouvre la configuration sélectionnée pour édition"""
        config_name = self.config_combo.currentText()
        if not config_name:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT path FROM configurations WHERE name=?", (config_name,))
            path = c.fetchone()[0]
            conn.close()
            
            # Ouvrir le fichier avec l'éditeur par défaut
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")

    def browse_config_file(self):
        """Ouvre un dialogue pour sélectionner un fichier de configuration"""
        path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier de configuration", 
                                            "", "JSON Files (*.json);;All Files (*)")
        if path:
            self.config_path_input.setText(path)

    def create_new_config(self):
        """Crée une nouvelle configuration"""
        name = self.new_config_name.text().strip()
        path = self.config_path_input.text().strip()
        
        if not name or not path:
            QMessageBox.warning(self, "Champs manquants", "Veuillez remplir tous les champs")
            return
            
        if not os.path.exists(path):
            QMessageBox.warning(self, "Fichier introuvable", "Le fichier de configuration spécifié n'existe pas")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Vérifier si le nom existe déjà
            c.execute("SELECT 1 FROM configurations WHERE name=?", (name,))
            if c.fetchone():
                QMessageBox.warning(self, "Nom existant", "Une configuration avec ce nom existe déjà")
                return
                
            # Insérer la nouvelle configuration
            c.execute("INSERT INTO configurations (name, path, last_used) VALUES (?, ?, ?)",
                     (name, path, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Succès", "Configuration créée avec succès!")
            self.load_configurations()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer la configuration: {str(e)}")

    def update_history(self):
        """Met à jour l'historique des exécutions"""
        filter_type = self.filter_type_combo.currentText()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            history_text = ""
            
            if filter_type in ["Tous", "Installations"]:
                c.execute("SELECT * FROM installations ORDER BY install_date DESC LIMIT 10")
                installations = c.fetchall()
                
                history_text += "<h2>Dernières Installations</h2><table border='1'><tr><th>Date</th><th>Version</th><th>Statut</th><th>Détails</th></tr>"
                
                for install in installations:
                    history_text += f"<tr><td>{install[3]}</td><td>{install[1]}</td><td>{install[4]}</td><td>{install[5] or ''}</td></tr>"
                
                history_text += "</table>"
            
            if filter_type in ["Tous", "Exécutions"]:
                c.execute("SELECT * FROM executions ORDER BY start_time DESC LIMIT 20")
                executions = c.fetchall()
                
                history_text += "<h2>Dernières Exécutions</h2><table border='1'><tr><th>Date</th><th>Commande</th><th>Statut</th></tr>"
                
                for exec_ in executions:
                    history_text += f"<tr><td>{exec_[1]}</td><td>{exec_[3]}</td><td>{exec_[4]}</td></tr>"
                
                history_text += "</table>"
            
            self.history_table.setHtml(history_text)
            conn.close()
            
        except Exception as e:
            self.history_table.setPlainText(f"Erreur lors du chargement de l'historique: {str(e)}")

    def open_documentation(self):
        """Ouvre la documentation Freqtrade dans le navigateur"""
        webbrowser.open("https://www.freqtrade.io/en/latest/")

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h1>Freqtrade Manager Pro</h1>
        <p>Version 1.0.0</p>
        <p>Un gestionnaire graphique pour Freqtrade, le bot de trading algorithmique open-source.</p>
        <p>Développé avec Python et PyQt5</p>
        <p>© 2023 - Tous droits réservés</p>
        """
        QMessageBox.about(self, "À propos", about_text)

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.freqtrade_running:
            reply = QMessageBox.question(
                self, "Freqtrade en cours",
                "Freqtrade est toujours en cours d'exécution. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
            else:
                self.stop_freqtrade()
                
        if self.installation_in_progress:
            reply = QMessageBox.question(
                self, "Installation en cours",
                "Une installation est en cours. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        # Fermer proprement
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
            
        event.accept()


    def get_install_commands(self, version):
        """Retourne les commandes d'installation appropriées"""
        commands = []
        
        # Vérifier et créer le répertoire de base
        if not os.path.exists(self.base_dir):
            try:
                os.makedirs(self.base_dir, exist_ok=True)
                self.output.append(f"Création du répertoire: {self.base_dir}")
            except Exception as e:
                self.output.append(f"<font color='red'>ERREUR: Impossible de créer {self.base_dir}: {str(e)}</font>")
                return commands
        
        # Installation Docker si nécessaire
        if self.docker_check.isChecked() and not self.docker_installed:
            if platform.system() == "Windows":
                commands.extend([
                    f"cd /d {self.base_dir}",
                    "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile docker_installer.exe",
                    "Start-Process -Wait -FilePath .\\docker_installer.exe -ArgumentList 'install --quiet'",
                    "Remove-Item docker_installer.exe"
                ])
        
        # Commandes Freqtrade - d'abord cloner le dépôt si nécessaire
        if not os.path.exists(self.freqtrade_dir):
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git {self.freqtrade_dir}")
        else:
            commands.append(f"cd {self.freqtrade_dir} && git fetch --all")
        
        # Vérifier que le répertoire freqtrade existe avant d'ajouter les autres commandes
        if os.path.exists(self.freqtrade_dir):
            commands.extend([
                f"cd {self.freqtrade_dir} && git checkout {version}",
                f"cd {self.freqtrade_dir} && git pull",
                f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
                f"cd {self.freqtrade_dir} && python -m pip install -e .",
                f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt"
            ])
            
            # Dépendances optionnelles
            if self.plot_check.isChecked():
                plot_req = os.path.join(self.freqtrade_dir, "requirements-plot.txt")
                if os.path.exists(plot_req):
                    commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt")
                else:
                    self.output.append(f"<font color='orange'>Avertissement: Fichier {plot_req} introuvable</font>")
            
            if self.ta_check.isChecked():
                ta_req = os.path.join(self.freqtrade_dir, "requirements-ft.txt")
                if os.path.exists(ta_req):
                    commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt")
                else:
                    self.output.append(f"<font color='orange'>Avertissement: Fichier {ta_req} introuvable</font>")
        else:
            self.output.append(f"<font color='red'>ERREUR: Répertoire Freqtrade introuvable à {self.freqtrade_dir}</font>")
        
        return commands
    def execute_next_command(self):
        if self.current_command < len(self.commands):
            cmd = self.commands[self.current_command]
            self.output.append(f"> {cmd}")
            
            # Vérifier les commandes cd
            if cmd.startswith("cd ") and "&&" in cmd:
                path = cmd.split("&&")[0].replace("cd ", "").strip()
                if not os.path.exists(path):
                    self.output.append(f"<font color='red'>ERREUR: Le répertoire {path} n'existe pas</font>")
                    self.installation_failed()
                    return
            # ...


    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade Manager Pro")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(QSize(800, 600))
        
        # Chemins importants
        self.base_dir = self.get_base_dir()
        self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
        self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
        self.config_dir = os.path.join(self.base_dir, "user_data")
        
        # Variables d'état
        self.installation_in_progress = False
        self.freqtrade_running = False
        self.current_worker = None
        
        # Initialisation de la base de données
        self.init_db()
        
        # Vérification des dépendances
        self.check_dependencies()
        
        # Initialisation de l'interface
        self.init_ui()
        self.init_tray_icon()
        self.init_menu_bar()
        
        # Style
        self.set_style()
        
        # Mise à jour de l'état initial
        self.update_ui_state()

    def get_base_dir(self):
        """Détermine le répertoire de base approprié selon le système d'exploitation"""
        if platform.system() == "Windows":
            base = os.path.join(os.environ.get("APPDATA", "C:\\"), "Freqtrade")
            # Créer le répertoire s'il n'existe pas
            os.makedirs(base, exist_ok=True)
            return base
        else:
            base = os.path.join(os.path.expanduser("~"), ".freqtrade_manager")
            os.makedirs(base, exist_ok=True)
            return base

    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Table des installations
            c.execute('''CREATE TABLE IF NOT EXISTS installations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          version TEXT,
                          path TEXT,
                          install_date TEXT,
                          status TEXT,
                          details TEXT)''')
            
            # Table des exécutions
            c.execute('''CREATE TABLE IF NOT EXISTS executions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          start_time TEXT,
                          end_time TEXT,
                          command TEXT,
                          status TEXT,
                          output TEXT)''')
            
            # Table des configurations
            c.execute('''CREATE TABLE IF NOT EXISTS configurations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          path TEXT,
                          last_used TEXT)''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

    def check_dependencies(self):
        """Vérifie les dépendances requises de manière plus robuste"""
        self.git_installed = self.check_command_available(["git", "--version"])
        self.python_installed = self.check_command_available(["python", "--version"]) or \
                                self.check_command_available(["python3", "--version"])
        self.docker_installed = self.check_command_available(["docker", "--version"])
        self.freqtrade_installed = self.check_freqtrade_installation()
        
    def check_command_available(self, command):
        """Vérifie si une commande système est disponible de manière plus robuste"""
        try:
            subprocess.run(command, check=True, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          timeout=10)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False
            
    def check_freqtrade_installation(self):
        """Vérifie si Freqtrade est déjà installé de manière plus robuste"""
        if not os.path.exists(self.freqtrade_dir):
            return False
            
        try:
            # Vérifier si freqtrade est installé et fonctionnel
            result = subprocess.run(["freqtrade", "--version"], 
                                  cwd=self.freqtrade_dir,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=30)
            return result.returncode == 0
        except:
            return False

    def get_install_commands(self, version):
        """Retourne les commandes d'installation appropriées avec des vérifications"""
        commands = []
        
        # 1. Vérifier et créer les répertoires nécessaires
        commands.append(f"@echo Création des répertoires nécessaires")
        commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
        commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
        # 2. Installation des dépendances système si manquantes
        if not self.git_installed:
            if platform.system() == "Windows":
                commands.append("@echo Installation de Git...")
                commands.append("winget install --id Git.Git -e --source winget")
            elif platform.system() == "Linux":
                commands.append("@echo Installation de Git...")
                commands.append("sudo apt-get update && sudo apt-get install -y git")
            elif platform.system() == "Darwin":
                commands.append("@echo Installation de Git...")
                commands.append("brew install git")
        
        if not self.python_installed:
            if platform.system() == "Windows":
                commands.append("@echo Installation de Python...")
                commands.append("winget install Python.Python.3 --silent")
            elif platform.system() == "Linux":
                commands.append("@echo Installation de Python...")
                commands.append("sudo apt-get update && sudo apt-get install -y python3 python3-pip")
            elif platform.system() == "Darwin":
                commands.append("@echo Installation de Python...")
                commands.append("brew install python")
        
        # 3. Installation Docker si nécessaire
        if self.docker_check.isChecked() and not self.docker_installed:
            if platform.system() == "Windows":
                commands.append("@echo Installation de Docker...")
                commands.extend([
                    f"cd /d \"{self.base_dir}\"",
                    "curl -Lo docker_installer.exe https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
                    "start /wait docker_installer.exe install --quiet",
                    "del docker_installer.exe"
                ])
            elif platform.system() == "Linux":
                commands.append("@echo Installation de Docker...")
                commands.extend([
                    "sudo apt-get update",
                    "sudo apt-get install -y docker.io docker-compose",
                    "sudo systemctl enable --now docker",
                    "sudo usermod -aG docker $USER"
                ])
            elif platform.system() == "Darwin":
                commands.append("@echo Installation de Docker...")
                commands.extend([
                    "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
                    "brew install --cask docker"
                ])
        
        # 4. Commandes Freqtrade avec vérifications
        if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
            commands.append("@echo Clonage du dépôt Freqtrade...")
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\" || echo Échec du clonage")
        else:
            commands.append("@echo Mise à jour du dépôt Freqtrade...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && git fetch --all || echo Échec de la mise à jour")
            
        commands.extend([
            f"@echo Installation de Freqtrade version {version}",
            f"cd \"{self.freqtrade_dir}\" && git checkout {version} || echo Échec du checkout",
            f"cd \"{self.freqtrade_dir}\" && git pull || echo Échec du pull",
            f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip || echo Échec de la mise à jour de pip",
            f"cd \"{self.freqtrade_dir}\" && python -m pip install -e . || echo Échec de l'installation",
            f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-common.txt || echo Échec de l'installation des dépendances"
        ])
        
        # 5. Dépendances optionnelles
        if self.plot_check.isChecked():
            commands.append("@echo Installation des dépendances de visualisation...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-plot.txt || echo Échec de l'installation des dépendances de visualisation")
            
        if self.ta_check.isChecked():
            commands.append("@echo Installation des dépendances d'analyse technique...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-ft.txt || echo Échec de l'installation des dépendances d'analyse technique")
        
        return commands

    def start_installation(self):
        """Lance le processus d'installation avec gestion des erreurs améliorée"""
        if self.installation_in_progress:
            QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
            return
            
        # Créer les répertoires de base si nécessaire
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            os.makedirs(self.freqtrade_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer les répertoires: {str(e)}")
            return
            
        self.installation_in_progress = True
        self.install_btn.setEnabled(False)
        self.output.clear()
        
        # Préparer les commandes d'installation
        version = self.version_combo.currentText()
        commands = self.get_install_commands(version)
        
        # Exécuter les commandes une par une
        self.current_command = 0
        self.commands = commands
        self.progress.setMaximum(len(commands))
        self.execute_next_command()

    def execute_next_command(self):
        """Exécute la prochaine commande avec gestion des erreurs améliorée"""
        if self.current_command >= len(self.commands):
            self.installation_completed()
            return
            
        cmd = self.commands[self.current_command]
        
        # Gestion spéciale des commandes echo
        if cmd.startswith("@echo "):
            self.output.append(f"<font color='blue'>{cmd[6:]}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_command)
            return
            
        self.output.append(f"> {cmd}")
        
        try:
            # Créer un worker pour exécuter la commande
            self.current_worker = CommandWorker(cmd, self.base_dir)
            self.current_worker.output_signal.connect(self.handle_command_output)
            self.current_worker.finished.connect(self.command_finished)
            self.current_worker.start()
            
        except Exception as e:
            self.output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
            # Continuer avec la commande suivante malgré l'erreur
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_command)

    def installation_completed(self):
        """Appelé lorsque l'installation est terminée"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)
        
        # Vérifier à nouveau les dépendances
        self.check_dependencies()
        self.update_ui_state()
        
        version = self.version_combo.currentText()
        self.log_installation(version, "Terminé", "Processus d'installation terminé")
        
        # Vérifier si l'installation a réussi
        if self.freqtrade_installed:
            QMessageBox.information(self, "Succès", "Installation terminée avec succès!")
            self.install_btn.setText("Mettre à jour Freqtrade")
        else:
            QMessageBox.warning(self, "Avertissement", 
                               "Le processus d'installation est terminé mais Freqtrade n'est peut-être pas correctement installé. "
                               "Consultez la sortie pour plus de détails.")

    # ... (le reste du code reste inchangé)


    def get_install_commands(self, version):
        """Retourne les commandes d'installation améliorées"""
        commands = []
        
        # 1. Création des répertoires
        commands.append(f"@echo Création des répertoires nécessaires")
        commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
        commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
        # 2. Clonage ou mise à jour du dépôt
        if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
            commands.append(f"@echo Clonage du dépôt Freqtrade...")
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\" || exit 1")
        else:
            commands.append(f"@echo Mise à jour du dépôt Freqtrade...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && git fetch --all || exit 1")
        
        # 3. Checkout et pull
        commands.append(f"@echo Sélection de la version {version}")
        commands.append(f"cd \"{self.freqtrade_dir}\" && git checkout {version} || exit 1")
        commands.append(f"cd \"{self.freqtrade_dir}\" && git pull || exit 1")
        
        # 4. Installation standard (au lieu de -e .)
        commands.append(f"@echo Installation des dépendances principales...")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip || exit 1")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install . || exit 1")
        
        # 5. Installation des dépendances supplémentaires
        commands.append(f"@echo Installation des dépendances communes...")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-common.txt || exit 1")
        
        if self.plot_check.isChecked():
            commands.append(f"@echo Installation des dépendances de visualisation...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-plot.txt || exit 1")
            
        if self.ta_check.isChecked():
            commands.append(f"@echo Installation des dépendances d'analyse technique...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-ft.txt || exit 1")
        
        return commands
    def installation_completed(self):
        """Vérifie que l'installation a réussi"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)
        
        # Vérification finale
        success = self.check_freqtrade_installation()
        self.freqtrade_installed = success
        self.update_ui_state()
        
        version = self.version_combo.currentText()
        if success:
            self.log_installation(version, "Succès", "Installation terminée avec succès")
            QMessageBox.information(self, "Succès", 
                                "Freqtrade a été installé avec succès!\n\n"
                                f"Répertoire : {self.freqtrade_dir}")
            self.install_btn.setText("Mettre à jour Freqtrade")
        else:
            self.log_installation(version, "Échec", "Installation incomplète")
            QMessageBox.warning(self, "Avertissement",
                            "L'installation semble incomplète.\n"
                            "Veuillez vérifier la sortie pour les erreurs.")

    def get_install_commands(self, version):
        """Commandes d'installation optimisées pour Windows"""
        commands = []
        
        # 1. Installer les prérequis système
        commands.append("@echo Installation des outils de compilation...")
        commands.append("winget install Python.Python.3 --silent")
        commands.append("winget install Git.Git --silent")
        commands.append("winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"")
        
        # 2. Configuration de l'environnement
        commands.append("@echo Configuration de l'environnement...")
        commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
        commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
        # 3. Clonage du dépôt
        if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
            commands.append("@echo Clonage du dépôt Freqtrade...")
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\"")
        
        # 4. Mise à jour
        commands.append("@echo Mise à jour du dépôt...")
        commands.append(f"cd \"{self.freqtrade_dir}\" && git checkout {version} && git pull")
        
        # 5. Installation avec wheel précompilé
        commands.append("@echo Installation des dépendances...")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip setuptools wheel")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install numpy --only-binary=:all:")
        commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install . --use-pep517")
        
        return commands


import sys
import os
import subprocess
import platform
import sqlite3
import shutil
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, 
                           QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
                           QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
                           QAction)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QTextCursor

class CommandWorker(QThread):
    output_signal = pyqtSignal(str, str)  # text, color
    
    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.process = None
        
    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                bufsize=1
            )
            
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip(), "white")
                
                err = self.process.stderr.readline()
                if err:
                    self.output_signal.emit(err.strip(), "red")
                    
        except Exception as e:
            self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            
    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                if platform.system() == "Windows":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], check=True)
                else:
                    self.process.terminate()
                    self.process.wait()
            except Exception as e:
                self.output_signal.emit(f"Error stopping process: {str(e)}", "red")

if __name__ == "__main__":
    # Vérifier et installer les dépendances PyQt5 si nécessaire
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            from PyQt5.QtWidgets import QApplication
        except:
            print("PyQt5 est requis. Veuillez l'installer manuellement avec: pip install PyQt5")
            sys.exit(1)
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre principale
    window = FreqtradeManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())
if __name__ == "__main__":
    # Vérifier et installer les dépendances si nécessaire
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            from PyQt5.QtWidgets import QApplication
        except:
            print("PyQt5 est requis. Veuillez l'installer manuellement avec: pip install PyQt5")
            sys.exit(1)
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Vérifier la présence de git et python
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("Git et Python sont requis pour ce programme")
    
    # Créer et afficher la fenêtre principale
    window = FreqtradeManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())