# import sys
# import os
# import subprocess
# import platform
# import sqlite3
# import shutil
# import webbrowser
# from datetime import datetime
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
#                            QVBoxLayout, QWidget, QLabel, QTextEdit,
#                            QMessageBox, QProgressBar, QCheckBox, 
#                            QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
#                            QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
#                            QAction)
# from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
# from PyQt5.QtGui import QIcon, QFont, QTextCursor

# class CommandWorker(QThread):
#     output_signal = pyqtSignal(str, str)  # text, color
    
#     def __init__(self, command, cwd=None):
#         super().__init__()
#         self.command = command
#         self.cwd = cwd or os.getcwd()
#         self.process = None
        
#     def run(self):
#         try:
#             self.process = subprocess.Popen(
#                 self.command,
#                 cwd=self.cwd,
#                 shell=True,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 universal_newlines=True,
#                 bufsize=1
#             )
            
#             while True:
#                 output = self.process.stdout.readline()
#                 if output == '' and self.process.poll() is not None:
#                     break
#                 if output:
#                     self.output_signal.emit(output.strip(), "white")
                
#                 err = self.process.stderr.readline()
#                 if err:
#                     self.output_signal.emit(err.strip(), "red")
                    
#         except Exception as e:
#             self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            
#     def stop(self):
#         if self.process and self.process.poll() is None:
#             try:
#                 if platform.system() == "Windows":
#                     subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], check=True)
#                 else:
#                     self.process.terminate()
#                     self.process.wait()
#             except Exception as e:
#                 self.output_signal.emit(f"Error stopping process: {str(e)}", "red")

# class FreqtradeManager(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Configuration de base
#         self.setWindowTitle("Freqtrade Manager Pro")
#         self.setGeometry(100, 100, 900, 700)
#         self.setMinimumSize(QSize(800, 600))
        
#         # Chemins importants
#         self.base_dir = self.get_base_dir()
#         self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
#         self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
#         self.config_dir = os.path.join(self.base_dir, "user_data")
        
#         # Variables d'état
#         self.installation_in_progress = False
#         self.freqtrade_running = False
#         self.current_worker = None
        
#         # Initialisation de la base de données
#         self.init_db()
        
#         # Vérification des dépendances
#         self.check_dependencies()
        
#         # Initialisation de l'interface
#         self.init_ui()
#         self.init_tray_icon()
#         self.init_menu_bar()
        
#         # Style
#         self.set_style()
        
#         # Mise à jour de l'état initial
#         self.update_ui_state()

#     def get_base_dir(self):
#         """Détermine le répertoire de base approprié selon le système d'exploitation"""
#         if platform.system() == "Windows":
#             return os.path.join(os.environ.get("APPDATA", "C:\\"), "Freqtrade")
#         else:
#             return os.path.join(os.path.expanduser("~"), ".freqtrade_manager")

#     def init_db(self):
#         """Initialise la base de données SQLite"""
#         try:
#             os.makedirs(self.base_dir, exist_ok=True)
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
            
#             # Table des installations
#             c.execute('''CREATE TABLE IF NOT EXISTS installations
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           version TEXT,
#                           path TEXT,
#                           install_date TEXT,
#                           status TEXT,
#                           details TEXT)''')
            
#             # Table des exécutions
#             c.execute('''CREATE TABLE IF NOT EXISTS executions
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           start_time TEXT,
#                           end_time TEXT,
#                           command TEXT,
#                           status TEXT,
#                           output TEXT)''')
            
#             # Table des configurations
#             c.execute('''CREATE TABLE IF NOT EXISTS configurations
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           name TEXT UNIQUE,
#                           path TEXT,
#                           last_used TEXT)''')
            
#             conn.commit()
#             conn.close()
#         except Exception as e:
#             QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

#     def log_installation(self, version, status, details=""):
#         """Journalise l'installation dans la base de données"""
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
#             c.execute("INSERT INTO installations (version, path, install_date, status, details) VALUES (?, ?, ?, ?, ?)",
#                       (version, self.freqtrade_dir, datetime.now().isoformat(), status, details))
#             conn.commit()
#             conn.close()
#         except Exception as e:
#             print(f"Failed to log installation: {str(e)}")

#     def log_execution(self, command, status, output=""):
#         """Journalise l'exécution dans la base de données"""
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
            
#             if status == "Démarré":
#                 c.execute("INSERT INTO executions (start_time, command, status) VALUES (?, ?, ?)",
#                           (datetime.now().isoformat(), command, status))
#             else:
#                 # Mettre à jour la dernière exécution
#                 c.execute("UPDATE executions SET end_time=?, status=?, output=? WHERE id=(SELECT MAX(id) FROM executions)",
#                           (datetime.now().isoformat(), status, output))
            
#             conn.commit()
#             conn.close()
#         except Exception as e:
#             print(f"Failed to log execution: {str(e)}")

#     def check_dependencies(self):
#         """Vérifie les dépendances requises"""
#         self.git_installed = self.check_command_available("git --version")
#         self.python_installed = self.check_command_available("python --version") or self.check_command_available("python3 --version")
#         self.docker_installed = self.check_command_available("docker --version")
#         self.freqtrade_installed = self.check_freqtrade_installation()
        
#     def check_command_available(self, command):
#         """Vérifie si une commande système est disponible"""
#         try:
#             subprocess.run(command, shell=True, check=True, 
#                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             return True
#         except:
#             return False
            
#     def check_freqtrade_installation(self):
#         """Vérifie si Freqtrade est déjà installé"""
#         if not os.path.exists(self.freqtrade_dir):
#             return False
            
#         try:
#             # Vérifier si freqtrade est installé et fonctionnel
#             result = subprocess.run(["freqtrade", "--version"], 
#                                   cwd=self.freqtrade_dir,
#                                   stdout=subprocess.PIPE, 
#                                   stderr=subprocess.PIPE,
#                                   text=True)
#             return result.returncode == 0
#         except:
#             return False

#     def init_ui(self):
#         """Initialise l'interface utilisateur"""
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
        
#         self.main_layout = QVBoxLayout()
#         self.central_widget.setLayout(self.main_layout)
        
#         # Création des onglets
#         self.tabs = QTabWidget()
#         self.main_layout.addWidget(self.tabs)
        
#         # Onglet Installation
#         self.setup_install_tab()
        
#         # Onglet Configuration
#         self.setup_config_tab()
        
#         # Onglet Exécution
#         self.setup_execution_tab()
        
#         # Onglet Historique
#         self.setup_history_tab()
        
# #         # Barre de statut
# #         self.status_bar = self.statusBar()
# #         self.status_bar.showMessage("Prêt")

#     def setup_install_tab(self):
#         """Configure l'onglet d'installation"""
#         tab = QWidget()
#         layout = QVBoxLayout()
        
#         # Header
#         header = QLabel("<h1>Installation Freqtrade</h1>")
#         header.setAlignment(Qt.AlignCenter)
#         layout.addWidget(header)
        
#         # Vérification des dépendances
#         deps_group = QGroupBox("Vérification des dépendances")
#         deps_layout = QVBoxLayout()
        
#         self.git_status = QLabel(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
#         self.python_status = QLabel(f"Python: {'Installé' if self.python_installed else 'Manquant'}")
#         self.docker_status = QLabel(f"Docker: {'Installé' if self.docker_installed else 'Manquant'}")
#         self.freqtrade_status = QLabel(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        
#         deps_layout.addWidget(self.git_status)
#         deps_layout.addWidget(self.python_status)
#         deps_layout.addWidget(self.docker_status)
#         deps_layout.addWidget(self.freqtrade_status)
        
# #         deps_group.setLayout(deps_layout)
# #         layout.addWidget(deps_group)
        
#         # Options d'installation
#         options_group = QGroupBox("Options d'installation")
#         options_layout = QVBoxLayout()
        
#         # Version à installer
#         version_layout = QHBoxLayout()
#         version_label = QLabel("Version:")
#         self.version_combo = QComboBox()
#         self.version_combo.addItems(["stable", "develop"])
#         version_layout.addWidget(version_label)
#         version_layout.addWidget(self.version_combo)
#         options_layout.addLayout(version_layout)
        
#         # Options
#         self.docker_check = QCheckBox("Installer Docker (si manquant)")
#         self.docker_check.setChecked(True)
#         options_layout.addWidget(self.docker_check)
        
# #         self.plot_check = QCheckBox("Installer les dépendances de visualisation")
# #         self.plot_check.setChecked(True)
# #         options_layout.addWidget(self.plot_check)
        
#         self.ta_check = QCheckBox("Installer les dépendances d'analyse technique")
#         self.ta_check.setChecked(True)
#         options_layout.addWidget(self.ta_check)
        
# #         options_group.setLayout(options_layout)
# #         layout.addWidget(options_group)
        
#         # Bouton d'installation
#         self.install_btn = QPushButton("Installer Freqtrade" if not self.freqtrade_installed else "Mettre à jour Freqtrade")
#         self.install_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
#         self.install_btn.clicked.connect(self.start_installation)
#         layout.addWidget(self.install_btn)
        
#         # Bouton de réparation
#         self.repair_btn = QPushButton("Réparer l'installation")
#         self.repair_btn.setStyleSheet("background-color: #f39c12; color: white;")
#         self.repair_btn.clicked.connect(self.repair_installation)
#         layout.addWidget(self.repair_btn)
        
# #         # Barre de progression
# #         self.progress = QProgressBar()
# #         layout.addWidget(self.progress)
        
# #         # Console de sortie
# #         self.output = QTextEdit()
# #         self.output.setReadOnly(True)
# #         self.output.setFont(QFont("Consolas", 10))
# #         layout.addWidget(self.output)
        
# #         tab.setLayout(layout)
# #         self.tabs.addTab(tab, "Installation")

#     def setup_config_tab(self):
#         """Configure l'onglet de configuration"""
#         tab = QWidget()
#         layout = QVBoxLayout()
        
#         # Header
#         header = QLabel("<h1>Configuration Freqtrade</h1>")
#         header.setAlignment(Qt.AlignCenter)
#         layout.addWidget(header)
        
#         # Configuration existante
#         config_group = QGroupBox("Configurations existantes")
#         config_layout = QVBoxLayout()
        
#         self.config_combo = QComboBox()
#         self.load_configurations()
#         config_layout.addWidget(self.config_combo)
        
#         btn_layout = QHBoxLayout()
#         self.use_config_btn = QPushButton("Utiliser cette configuration")
#         self.use_config_btn.clicked.connect(self.use_selected_config)
#         btn_layout.addWidget(self.use_config_btn)
        
#         self.edit_config_btn = QPushButton("Éditer")
#         self.edit_config_btn.clicked.connect(self.edit_selected_config)
#         btn_layout.addWidget(self.edit_config_btn)
        
#         config_layout.addLayout(btn_layout)
#         config_group.setLayout(config_layout)
#         layout.addWidget(config_group)
        
#         # Nouvelle configuration
#         new_config_group = QGroupBox("Nouvelle configuration")
#         new_config_layout = QVBoxLayout()
        
#         self.new_config_name = QLineEdit()
#         self.new_config_name.setPlaceholderText("Nom de la configuration")
#         new_config_layout.addWidget(self.new_config_name)
        
#         self.config_path_input = QLineEdit()
#         self.config_path_input.setPlaceholderText("Chemin du fichier de configuration")
#         new_config_layout.addWidget(self.config_path_input)
        
#         browse_btn = QPushButton("Parcourir...")
#         browse_btn.clicked.connect(self.browse_config_file)
#         new_config_layout.addWidget(browse_btn)
        
#         self.create_config_btn = QPushButton("Créer configuration")
#         self.create_config_btn.clicked.connect(self.create_new_config)
#         new_config_layout.addWidget(self.create_config_btn)
        
#         new_config_group.setLayout(new_config_layout)
#         layout.addWidget(new_config_group)
        
#         # Documentation
#         doc_btn = QPushButton("Ouvrir la documentation Freqtrade")
#         doc_btn.clicked.connect(self.open_documentation)
#         layout.addWidget(doc_btn)
        
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Configuration")

#     def setup_execution_tab(self):
#         """Configure l'onglet d'exécution"""
#         tab = QWidget()
#         layout = QVBoxLayout()
        
#         # Header
#         header = QLabel("<h1>Exécution Freqtrade</h1>")
#         header.setAlignment(Qt.AlignCenter)
#         layout.addWidget(header)
        
#         # Boutons d'exécution
#         btn_layout = QHBoxLayout()
        
#         self.start_btn = QPushButton("Démarrer Freqtrade")
#         self.start_btn.setStyleSheet("background-color: #3498db; color: white;")
#         self.start_btn.clicked.connect(self.start_freqtrade)
#         btn_layout.addWidget(self.start_btn)
        
#         self.stop_btn = QPushButton("Arrêter Freqtrade")
#         self.stop_btn.setStyleSheet("background-color: #e74c3c; color: white;")
#         self.stop_btn.setEnabled(False)
#         self.stop_btn.clicked.connect(self.stop_freqtrade)
#         btn_layout.addWidget(self.stop_btn)
        
#         self.restart_btn = QPushButton("Redémarrer")
#         self.restart_btn.setStyleSheet("background-color: #f39c12; color: white;")
#         self.restart_btn.setEnabled(False)
#         self.restart_btn.clicked.connect(self.restart_freqtrade)
#         btn_layout.addWidget(self.restart_btn)
        
#         layout.addLayout(btn_layout)
        
#         # Options d'exécution
#         exec_group = QGroupBox("Options d'exécution")
#         exec_layout = QVBoxLayout()
        
#         mode_layout = QHBoxLayout()
#         mode_label = QLabel("Mode:")
#         self.mode_combo = QComboBox()
#         self.mode_combo.addItems(["Trade", "Backtest", "Hyperopt", "Plot", "Edge", "Download Data"])
#         self.mode_combo.currentTextChanged.connect(self.update_mode_options)
#         mode_layout.addWidget(mode_label)
#         mode_layout.addWidget(self.mode_combo)
#         exec_layout.addLayout(mode_layout)
        
#         # Options spécifiques au mode
#         self.mode_options_stack = QWidget()
#         self.mode_options_layout = QVBoxLayout(self.mode_options_stack)
        
#         # Options pour le mode Trade
#         self.trade_options = QWidget()
#         trade_options_layout = QVBoxLayout(self.trade_options)
        
#         strategy_layout = QHBoxLayout()
#         strategy_label = QLabel("Stratégie:")
#         self.strategy_input = QLineEdit("SampleStrategy")
#         strategy_layout.addWidget(strategy_label)
#         strategy_layout.addWidget(self.strategy_input)
#         trade_options_layout.addLayout(strategy_layout)
        
#         self.db_check = QCheckBox("Utiliser la base de données")
#         self.db_check.setChecked(True)
#         trade_options_layout.addWidget(self.db_check)
        
#         self.trade_options.setLayout(trade_options_layout)
#         self.mode_options_layout.addWidget(self.trade_options)
        
#         # Options pour le mode Backtest
#         self.backtest_options = QWidget()
#         backtest_options_layout = QVBoxLayout(self.backtest_options)
        
#         bt_strategy_layout = QHBoxLayout()
#         bt_strategy_label = QLabel("Stratégie:")
#         self.bt_strategy_input = QLineEdit("SampleStrategy")
#         bt_strategy_layout.addWidget(bt_strategy_label)
#         bt_strategy_layout.addWidget(self.bt_strategy_input)
#         backtest_options_layout.addLayout(bt_strategy_layout)
        
#         timerange_layout = QHBoxLayout()
#         timerange_label = QLabel("Plage de temps:")
#         self.timerange_input = QLineEdit()
#         self.timerange_input.setPlaceholderText("YYYYMMDD-YYYYMMDD")
#         timerange_layout.addWidget(timerange_label)
#         timerange_layout.addWidget(self.timerange_input)
#         backtest_options_layout.addLayout(timerange_layout)
        
#         self.backtest_options.setLayout(backtest_options_layout)
#         self.mode_options_layout.addWidget(self.backtest_options)
        
# #         # Ajouter d'autres options pour les autres modes...
        
#         exec_layout.addWidget(self.mode_options_stack)
#         exec_group.setLayout(exec_layout)
#         layout.addWidget(exec_group)
        
#         # Console d'exécution
#         self.exec_output = QTextEdit()
#         self.exec_output.setReadOnly(True)
#         self.exec_output.setFont(QFont("Consolas", 10))
#         layout.addWidget(self.exec_output)
        
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Exécution")

#     def setup_history_tab(self):
#         """Configure l'onglet d'historique"""
#         tab = QWidget()
#         layout = QVBoxLayout()
        
#         # Header
#         header = QLabel("<h1>Historique des Exécutions</h1>")
#         header.setAlignment(Qt.AlignCenter)
#         layout.addWidget(header)
        
#         # Filtres
#         filter_layout = QHBoxLayout()
        
#         self.filter_type_combo = QComboBox()
#         self.filter_type_combo.addItems(["Tous", "Installations", "Exécutions"])
#         self.filter_type_combo.currentIndexChanged.connect(self.update_history)
#         filter_layout.addWidget(self.filter_type_combo)
        
#         self.refresh_history_btn = QPushButton("Actualiser")
#         self.refresh_history_btn.clicked.connect(self.update_history)
#         filter_layout.addWidget(self.refresh_history_btn)
        
#         layout.addLayout(filter_layout)
        
#         # Tableau d'historique
#         self.history_table = QTextEdit()
#         self.history_table.setReadOnly(True)
#         layout.addWidget(self.history_table)
        
#         self.update_history()
        
#         tab.setLayout(layout)
#         self.tabs.addTab(tab, "Historique")

#     def init_menu_bar(self):
#         """Initialise la barre de menu"""
#         menubar = self.menuBar()
        
#         # Menu Fichier
#         file_menu = menubar.addMenu("Fichier")
        
#         exit_action = QAction("Quitter", self)
#         exit_action.setShortcut("Ctrl+Q")
#         exit_action.triggered.connect(self.close)
#         file_menu.addAction(exit_action)
        
#         # Menu Aide
#         help_menu = menubar.addMenu("Aide")
        
#         docs_action = QAction("Documentation", self)
#         docs_action.triggered.connect(self.open_documentation)
#         help_menu.addAction(docs_action)
        
#         about_action = QAction("À propos", self)
#         about_action.triggered.connect(self.show_about)
#         help_menu.addAction(about_action)

#     def init_tray_icon(self):
#         """Initialise l'icône de la barre système"""
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon.fromTheme("system-run"))
        
#         tray_menu = QMenu()
#         open_action = tray_menu.addAction("Ouvrir")
#         open_action.triggered.connect(self.show)
        
#         exit_action = tray_menu.addAction("Quitter")
#         exit_action.triggered.connect(self.close)
        
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()
        
#         self.tray_icon.activated.connect(self.tray_icon_activated)

#     def tray_icon_activated(self, reason):
#         """Gère les clics sur l'icône de la barre système"""
#         if reason == QSystemTrayIcon.DoubleClick:
#             self.show()

#     def set_style(self):
#         """Applique le style à l'application"""
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #f5f6fa;
#             }
#             QGroupBox {
#                 border: 1px solid #ddd;
#                 border-radius: 4px;
#                 margin-top: 10px;
#                 padding-top: 15px;
#             }
#             QGroupBox::title {
#                 subcontrol-origin: margin;
#                 left: 10px;
#                 padding: 0 3px;
#             }
#             QTextEdit {
#                 background-color: #2c3e50;
#                 color: #ecf0f1;
#                 border: 1px solid #34495e;
#                 border-radius: 4px;
#                 padding: 5px;
#             }
#             QPushButton {
#                 padding: 5px;
#                 border-radius: 4px;
#                 min-height: 25px;
#             }
#             QPushButton:hover {
#                 background-color: #3498db;
#                 color: white;
#             }
#             QTabWidget::pane {
#                 border-top: 2px solid #bdc3c7;
#             }
#             QTabBar::tab {
#                 padding: 8px;
#                 background: #ecf0f1;
#                 border: 1px solid #bdc3c7;
#                 border-bottom: none;
#                 border-top-left-radius: 4px;
#                 border-top-right-radius: 4px;
#             }
#             QTabBar::tab:selected {
#                 background: #3498db;
#                 color: white;
#             }
#             QLabel[status="error"] {
#                 color: #e74c3c;
#                 font-weight: bold;
#             }
#             QLabel[status="success"] {
#                 color: #27ae60;
#                 font-weight: bold;
#             }
#         """)

#     def update_ui_state(self):
#         """Met à jour l'état de l'interface en fonction des dépendances"""
#         self.git_status.setText(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
#         self.python_status.setText(f"Python: {'Installé' if self.python_installed else 'Manquant'}")
#         self.docker_status.setText(f"Docker: {'Installé' if self.docker_installed else 'Manquant'}")
#         self.freqtrade_status.setText(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        
#         # Activer/désactiver les boutons en fonction des dépendances
#         self.install_btn.setEnabled(self.git_installed and self.python_installed)
#         self.start_btn.setEnabled(self.freqtrade_installed)
        
#         # Mettre à jour les styles en fonction de l'état
#         for label, condition in [(self.git_status, self.git_installed),
#                                 (self.python_status, self.python_installed),
#                                 (self.docker_status, self.docker_installed),
#                                 (self.freqtrade_status, self.freqtrade_installed)]:
#             label.setProperty("status", "success" if condition else "error")
#             label.style().unpolish(label)
#             label.style().polish(label)

#     def start_installation(self):
#         """Lance le processus d'installation"""
#         if self.installation_in_progress:
#             QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
#             return
            
#         # Vérifier les prérequis
#         if not self.git_installed:
#             QMessageBox.critical(self, "Erreur", "Git est requis pour installer Freqtrade")
#             return
            
#         if not self.python_installed:
#             QMessageBox.critical(self, "Erreur", "Python est requis pour installer Freqtrade")
#             return
            
#         self.installation_in_progress = True
#         self.install_btn.setEnabled(False)
#         self.output.clear()
        
#         # Créer le répertoire si nécessaire
#         os.makedirs(self.base_dir, exist_ok=True)
        
#         # Préparer les commandes d'installation
#         version = self.version_combo.currentText()
#         commands = self.get_install_commands(version)
        
#         # Exécuter les commandes une par une
#         self.current_command = 0
#         self.commands = commands
#         self.progress.setMaximum(len(commands))
#         self.execute_next_command()

#     def get_install_commands(self, version):
#         """Retourne les commandes d'installation appropriées"""
#         commands = []
        
#         # Installation Docker si nécessaire
#         if self.docker_check.isChecked() and not self.docker_installed:
#             if platform.system() == "Windows":
#                 commands.extend([
#                     f"cd /d {self.base_dir}",
#                     "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile docker_installer.exe",
#                     "Start-Process -Wait -FilePath .\\docker_installer.exe -ArgumentList 'install --quiet'",
#                     "Remove-Item docker_installer.exe"
#                 ])
#             elif platform.system() == "Linux":
#                 commands.extend([
#                     "sudo apt-get update",
#                     "sudo apt-get install -y docker.io docker-compose",
#                     "sudo systemctl enable --now docker",
#                     "sudo usermod -aG docker $USER"
#                 ])
#             elif platform.system() == "Darwin":
#                 commands.extend([
#                     "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
#                     "brew install --cask docker"
#                 ])
        
#         # Commandes Freqtrade
#         if not os.path.exists(self.freqtrade_dir):
#             commands.append(f"git clone https://github.com/freqtrade/freqtrade.git {self.freqtrade_dir}")
#         else:
#             commands.append(f"cd {self.freqtrade_dir} && git fetch --all")
            
#         commands.extend([
#             f"cd {self.freqtrade_dir} && git checkout {version}",
#             f"cd {self.freqtrade_dir} && git pull",
#             f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
#             f"cd {self.freqtrade_dir} && python -m pip install -e .",
#             f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt"
#         ])
        
#         # Dépendances optionnelles
#         if self.plot_check.isChecked():
#             commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt")
            
#         if self.ta_check.isChecked():
#             commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt")
        
#         return commands

#     def execute_next_command(self):
#         """Exécute la prochaine commande dans la séquence"""
#         if self.current_command < len(self.commands):
#             cmd = self.commands[self.current_command]
#             self.output.append(f"> {cmd}")
            
#             try:
#                 # Créer un worker pour exécuter la commande
#                 self.current_worker = CommandWorker(cmd, self.base_dir)
#                 self.current_worker.output_signal.connect(self.handle_command_output)
#                 self.current_worker.finished.connect(self.command_finished)
#                 self.current_worker.start()
                
#             except Exception as e:
#                 self.output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
#                 self.installation_failed()
                
#         else:
#             # Installation terminée avec succès
#             self.installation_completed()

#     def handle_command_output(self, text, color):
#         """Affiche la sortie de la commande"""
#         if color == "red":
#             self.output.append(f"<font color='{color}'>{text}</font>")
#         else:
#             self.output.append(text)
        
#         # Faire défiler vers le bas
#         self.output.moveCursor(QTextCursor.End)

#     def command_finished(self):
#         """Appelé lorsqu'une commande est terminée"""
#         self.current_command += 1
#         self.progress.setValue(self.current_command)
        
#         if self.current_command < len(self.commands):
#             # Passer à la commande suivante
#             QTimer.singleShot(100, self.execute_next_command)
#         else:
#             # Installation terminée avec succès
#             self.installation_completed()

#     def installation_completed(self):
#         """Appelé lorsque l'installation est terminée avec succès"""
#         self.installation_in_progress = False
#         self.install_btn.setEnabled(True)
#         self.freqtrade_installed = True
#         self.update_ui_state()
        
#         version = self.version_combo.currentText()
#         self.log_installation(version, "Succès", "Installation terminée avec succès")
        
#         QMessageBox.information(self, "Succès", "Installation terminée avec succès!")
        
#         # Vérifier si Docker a été installé
#         if self.docker_check.isChecked():
#             self.docker_installed = self.check_command_available("docker --version")
#             self.update_ui_state()

#     def installation_failed(self):
#         """Appelé lorsque l'installation échoue"""
#         self.installation_in_progress = False
#         self.install_btn.setEnabled(True)
        
#         version = self.version_combo.currentText()
#         self.log_installation(version, "Échec", "Échec de l'installation")
        
#         QMessageBox.critical(self, "Erreur", "L'installation a échoué. Consultez la sortie pour plus de détails.")

#     def repair_installation(self):
#         """Tente de réparer une installation existante"""
#         reply = QMessageBox.question(self, "Réparer", 
#                                    "Voulez-vous vraiment réparer l'installation Freqtrade?",
#                                    QMessageBox.Yes | QMessageBox.No)
        
#         if reply == QMessageBox.Yes:
#             # Réinstaller les dépendances
#             commands = [
#                 f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
#                 f"cd {self.freqtrade_dir} && python -m pip install -e .",
#                 f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt",
#                 f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt",
#                 f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt"
#             ]
            
#             self.installation_in_progress = True
#             self.output.clear()
#             self.current_command = 0
#             self.commands = commands
#             self.progress.setMaximum(len(commands))
#             self.execute_next_command()

#     def start_freqtrade(self):
#         """Démarre Freqtrade"""
#         if self.freqtrade_running:
#             QMessageBox.warning(self, "Déjà en cours", "Freqtrade est déjà en cours d'exécution")
#             return
            
#         mode = self.mode_combo.currentText().lower().replace(" ", "_")
#         strategy = self.strategy_input.text()
        
#         # Construire la commande de base
#         cmd = f"cd {self.freqtrade_dir} && freqtrade {mode} --strategy {strategy}"
        
#         # Ajouter des options spécifiques au mode
#         if mode == "backtest":
#             timerange = self.timerange_input.text()
#             if timerange:
#                 cmd += f" --timerange {timerange}"
        
#         try:
#             self.exec_output.clear()
#             self.freqtrade_running = True
#             self.update_execution_buttons()
            
#             self.current_worker = CommandWorker(cmd, self.freqtrade_dir)
#             self.current_worker.output_signal.connect(self.handle_execution_output)
#             self.current_worker.finished.connect(self.execution_finished)
#             self.current_worker.start()
            
#             self.log_execution(cmd, "Démarré")
            
#         except Exception as e:
#             self.exec_output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
#             self.freqtrade_running = False
#             self.update_execution_buttons()

#     def handle_execution_output(self, text, color):
#         """Affiche la sortie de l'exécution de Freqtrade"""
#         if color == "red":
#             self.exec_output.append(f"<font color='{color}'>{text}</font>")
#         else:
#             self.exec_output.append(text)
        
#         # Faire défiler vers le bas
#         self.exec_output.moveCursor(QTextCursor.End)

#     def stop_freqtrade(self):
#         """Arrête Freqtrade"""
#         if not self.freqtrade_running:
#             return
            
#         if self.current_worker:
#             self.current_worker.stop()
            
#         self.freqtrade_running = False
#         self.update_execution_buttons()
#         self.log_execution("", "Arrêté")

#     def restart_freqtrade(self):
#         """Redémarre Freqtrade"""
#         self.stop_freqtrade()
#         QTimer.singleShot(1000, self.start_freqtrade)

#     def execution_finished(self):
#         """Appelé lorsque l'exécution de Freqtrade est terminée"""
#         self.freqtrade_running = False
#         self.update_execution_buttons()
        
#         # Capturer la sortie finale
#         output = self.exec_output.toPlainText()
#         self.log_execution("", "Terminé", output)

#     def update_execution_buttons(self):
#         """Met à jour l'état des boutons d'exécution"""
#         self.start_btn.setEnabled(not self.freqtrade_running)
#         self.stop_btn.setEnabled(self.freqtrade_running)
#         self.restart_btn.setEnabled(self.freqtrade_running)

#     def update_mode_options(self):
#         """Met à jour les options affichées en fonction du mode sélectionné"""
#         mode = self.mode_combo.currentText()
        
#         # Masquer toutes les options
#         for i in range(self.mode_options_layout.count()):
#             widget = self.mode_options_layout.itemAt(i).widget()
#             if widget:
#                 widget.hide()
        
#         # Afficher les options appropriées
#         if mode == "Trade":
#             self.trade_options.show()
#         elif mode == "Backtest":
#             self.backtest_options.show()
#         # Ajouter d'autres conditions pour les autres modes...

#     def load_configurations(self):
#         """Charge les configurations depuis la base de données"""
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
#             c.execute("SELECT name FROM configurations ORDER BY last_used DESC")
#             configs = c.fetchall()
            
#             self.config_combo.clear()
#             for config in configs:
#                 self.config_combo.addItem(config[0])
                
#             conn.close()
#         except Exception as e:
#             print(f"Failed to load configurations: {str(e)}")

#     def use_selected_config(self):
#         """Utilise la configuration sélectionnée"""
#         config_name = self.config_combo.currentText()
#         if not config_name:
#             return
            
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
#             c.execute("SELECT path FROM configurations WHERE name=?", (config_name,))
#             path = c.fetchone()[0]
            
#             # Mettre à jour la date d'utilisation
#             c.execute("UPDATE configurations SET last_used=? WHERE name=?", 
#                      (datetime.now().isoformat(), config_name))
#             conn.commit()
#             conn.close()
            
#             # Copier le fichier de configuration vers le répertoire user_data
#             os.makedirs(os.path.join(self.config_dir, "configs"), exist_ok=True)
#             dest_path = os.path.join(self.config_dir, "configs", "config.json")
#             shutil.copy2(path, dest_path)
            
#             QMessageBox.information(self, "Succès", f"Configuration {config_name} appliquée avec succès!")
            
#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Impossible d'appliquer la configuration: {str(e)}")
#     def edit_selected_config(self):
#         """Ouvre la configuration sélectionnée pour édition"""
#         config_name = self.config_combo.currentText()
#         if not config_name:
#             return
            
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
#             c.execute("SELECT path FROM configurations WHERE name=?", (config_name,))
#             path = c.fetchone()[0]
#             conn.close()
            
#             # Ouvrir le fichier avec l'éditeur par défaut
#             if platform.system() == "Windows":
#                 os.startfile(path)
#             elif platform.system() == "Darwin":
#                 subprocess.run(["open", path])
#             else:
#                 subprocess.run(["xdg-open", path])
                
#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")

#     def browse_config_file(self):
#         """Ouvre un dialogue pour sélectionner un fichier de configuration"""
#         path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier de configuration", 
#                                             "", "JSON Files (*.json);;All Files (*)")
#         if path:
#             self.config_path_input.setText(path)

#     def create_new_config(self):
#         """Crée une nouvelle configuration"""
#         name = self.new_config_name.text().strip()
#         path = self.config_path_input.text().strip()
        
#         if not name or not path:
#             QMessageBox.warning(self, "Champs manquants", "Veuillez remplir tous les champs")
#             return
            
#         if not os.path.exists(path):
#             QMessageBox.warning(self, "Fichier introuvable", "Le fichier de configuration spécifié n'existe pas")
#             return
            
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
            
#             # Vérifier si le nom existe déjà
#             c.execute("SELECT 1 FROM configurations WHERE name=?", (name,))
#             if c.fetchone():
#                 QMessageBox.warning(self, "Nom existant", "Une configuration avec ce nom existe déjà")
#                 return
                
#             # Insérer la nouvelle configuration
#             c.execute("INSERT INTO configurations (name, path, last_used) VALUES (?, ?, ?)",
#                      (name, path, datetime.now().isoformat()))
#             conn.commit()
#             conn.close()
            
#             QMessageBox.information(self, "Succès", "Configuration créée avec succès!")
#             self.load_configurations()
            
#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Impossible de créer la configuration: {str(e)}")

#     def update_history(self):
#         """Met à jour l'historique des exécutions"""
#         filter_type = self.filter_type_combo.currentText()
        
#         try:
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
            
#             history_text = ""
            
#             if filter_type in ["Tous", "Installations"]:
#                 c.execute("SELECT * FROM installations ORDER BY install_date DESC LIMIT 10")
#                 installations = c.fetchall()
                
#                 history_text += "<h2>Dernières Installations</h2><table border='1'><tr><th>Date</th><th>Version</th><th>Statut</th><th>Détails</th></tr>"
                
#                 for install in installations:
#                     history_text += f"<tr><td>{install[3]}</td><td>{install[1]}</td><td>{install[4]}</td><td>{install[5] or ''}</td></tr>"
                
#                 history_text += "</table>"
            
#             if filter_type in ["Tous", "Exécutions"]:
#                 c.execute("SELECT * FROM executions ORDER BY start_time DESC LIMIT 20")
#                 executions = c.fetchall()
                
#                 history_text += "<h2>Dernières Exécutions</h2><table border='1'><tr><th>Date</th><th>Commande</th><th>Statut</th></tr>"
                
#                 for exec_ in executions:
#                     history_text += f"<tr><td>{exec_[1]}</td><td>{exec_[3]}</td><td>{exec_[4]}</td></tr>"
                
#                 history_text += "</table>"
            
#             self.history_table.setHtml(history_text)
#             conn.close()
            
#         except Exception as e:
#             self.history_table.setPlainText(f"Erreur lors du chargement de l'historique: {str(e)}")

#     def open_documentation(self):
#         """Ouvre la documentation Freqtrade dans le navigateur"""
#         webbrowser.open("https://www.freqtrade.io/en/latest/")

#     def show_about(self):
#         """Affiche la boîte de dialogue À propos"""
#         about_text = """
#         <h1>Freqtrade Manager Pro</h1>
#         <p>Version 1.0.0</p>
#         <p>Un gestionnaire graphique pour Freqtrade, le bot de trading algorithmique open-source.</p>
#         <p>Développé avec Python et PyQt5</p>
#         <p>© 2023 - Tous droits réservés</p>
#         """
#         QMessageBox.about(self, "À propos", about_text)

#     def closeEvent(self, event):
#         """Gère la fermeture de l'application"""
#         if self.freqtrade_running:
#             reply = QMessageBox.question(
#                 self, "Freqtrade en cours",
#                 "Freqtrade est toujours en cours d'exécution. Voulez-vous vraiment quitter?",
#                 QMessageBox.Yes | QMessageBox.No
#             )
            
#             if reply == QMessageBox.No:
#                 event.ignore()
#                 return
#             else:
#                 self.stop_freqtrade()
                
#         if self.installation_in_progress:
#             reply = QMessageBox.question(
#                 self, "Installation en cours",
#                 "Une installation est en cours. Voulez-vous vraiment quitter?",
#                 QMessageBox.Yes | QMessageBox.No
#             )
            
#             if reply == QMessageBox.No:
#                 event.ignore()
#                 return
                
#         # Fermer proprement
#         if hasattr(self, 'tray_icon'):
#             self.tray_icon.hide()
            
#         event.accept()


#     def get_install_commands(self, version):
#         """Retourne les commandes d'installation appropriées"""
#         commands = []
        
#         # Vérifier et créer le répertoire de base
#         if not os.path.exists(self.base_dir):
#             try:
#                 os.makedirs(self.base_dir, exist_ok=True)
#                 self.output.append(f"Création du répertoire: {self.base_dir}")
#             except Exception as e:
#                 self.output.append(f"<font color='red'>ERREUR: Impossible de créer {self.base_dir}: {str(e)}</font>")
#                 return commands
        
#         # Installation Docker si nécessaire
#         if self.docker_check.isChecked() and not self.docker_installed:
#             if platform.system() == "Windows":
#                 commands.extend([
#                     f"cd /d {self.base_dir}",
#                     "Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile docker_installer.exe",
#                     "Start-Process -Wait -FilePath .\\docker_installer.exe -ArgumentList 'install --quiet'",
#                     "Remove-Item docker_installer.exe"
#                 ])
        
#         # Commandes Freqtrade - d'abord cloner le dépôt si nécessaire
#         if not os.path.exists(self.freqtrade_dir):
#             commands.append(f"git clone https://github.com/freqtrade/freqtrade.git {self.freqtrade_dir}")
#         else:
#             commands.append(f"cd {self.freqtrade_dir} && git fetch --all")
        
#         # Vérifier que le répertoire freqtrade existe avant d'ajouter les autres commandes
#         if os.path.exists(self.freqtrade_dir):
#             commands.extend([
#                 f"cd {self.freqtrade_dir} && git checkout {version}",
#                 f"cd {self.freqtrade_dir} && git pull",
#                 f"cd {self.freqtrade_dir} && python -m pip install --upgrade pip",
#                 f"cd {self.freqtrade_dir} && python -m pip install -e .",
#                 f"cd {self.freqtrade_dir} && python -m pip install -r requirements-common.txt"
#             ])
            
#             # Dépendances optionnelles
#             if self.plot_check.isChecked():
#                 plot_req = os.path.join(self.freqtrade_dir, "requirements-plot.txt")
#                 if os.path.exists(plot_req):
#                     commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-plot.txt")
#                 else:
#                     self.output.append(f"<font color='orange'>Avertissement: Fichier {plot_req} introuvable</font>")
            
#             if self.ta_check.isChecked():
#                 ta_req = os.path.join(self.freqtrade_dir, "requirements-ft.txt")
#                 if os.path.exists(ta_req):
#                     commands.append(f"cd {self.freqtrade_dir} && python -m pip install -r requirements-ft.txt")
#                 else:
#                     self.output.append(f"<font color='orange'>Avertissement: Fichier {ta_req} introuvable</font>")
#         else:
#             self.output.append(f"<font color='red'>ERREUR: Répertoire Freqtrade introuvable à {self.freqtrade_dir}</font>")
        
#         return commands
#     def execute_next_command(self):
#         if self.current_command < len(self.commands):
#             cmd = self.commands[self.current_command]
#             self.output.append(f"> {cmd}")
            
#             # Vérifier les commandes cd
#             if cmd.startswith("cd ") and "&&" in cmd:
#                 path = cmd.split("&&")[0].replace("cd ", "").strip()
#                 if not os.path.exists(path):
#                     self.output.append(f"<font color='red'>ERREUR: Le répertoire {path} n'existe pas</font>")
#                     self.installation_failed()
#                     return
#             # ...


#     def __init__(self):
#         super().__init__()
        
#         # Configuration de base
#         self.setWindowTitle("Freqtrade Manager Pro")
#         self.setGeometry(100, 100, 900, 700)
#         self.setMinimumSize(QSize(800, 600))
        
#         # Chemins importants
#         self.base_dir = self.get_base_dir()
#         self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
#         self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
#         self.config_dir = os.path.join(self.base_dir, "user_data")
        
#         # Variables d'état
#         self.installation_in_progress = False
#         self.freqtrade_running = False
#         self.current_worker = None
        
#         # Initialisation de la base de données
#         self.init_db()
        
#         # Vérification des dépendances
#         self.check_dependencies()
        
#         # Initialisation de l'interface
#         self.init_ui()
#         self.init_tray_icon()
#         self.init_menu_bar()
        
#         # Style
#         self.set_style()
        
#         # Mise à jour de l'état initial
#         self.update_ui_state()

#     def get_base_dir(self):
#         """Détermine le répertoire de base approprié selon le système d'exploitation"""
#         if platform.system() == "Windows":
#             base = os.path.join(os.environ.get("APPDATA", "C:\\"), "Freqtrade")
#             # Créer le répertoire s'il n'existe pas
#             os.makedirs(base, exist_ok=True)
#             return base
#         else:
#             base = os.path.join(os.path.expanduser("~"), ".freqtrade_manager")
#             os.makedirs(base, exist_ok=True)
#             return base

#     def init_db(self):
#         """Initialise la base de données SQLite"""
#         try:
#             os.makedirs(self.base_dir, exist_ok=True)
#             conn = sqlite3.connect(self.db_path)
#             c = conn.cursor()
            
#             # Table des installations
#             c.execute('''CREATE TABLE IF NOT EXISTS installations
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           version TEXT,
#                           path TEXT,
#                           install_date TEXT,
#                           status TEXT,
#                           details TEXT)''')
            
#             # Table des exécutions
#             c.execute('''CREATE TABLE IF NOT EXISTS executions
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           start_time TEXT,
#                           end_time TEXT,
#                           command TEXT,
#                           status TEXT,
#                           output TEXT)''')
            
#             # Table des configurations
#             c.execute('''CREATE TABLE IF NOT EXISTS configurations
#                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                           name TEXT UNIQUE,
#                           path TEXT,
#                           last_used TEXT)''')
            
#             conn.commit()
#             conn.close()
#         except Exception as e:
#             QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

#     def check_dependencies(self):
#         """Vérifie les dépendances requises de manière plus robuste"""
#         self.git_installed = self.check_command_available(["git", "--version"])
#         self.python_installed = self.check_command_available(["python", "--version"]) or \
#                                 self.check_command_available(["python3", "--version"])
#         self.docker_installed = self.check_command_available(["docker", "--version"])
#         self.freqtrade_installed = self.check_freqtrade_installation()
        
#     def check_command_available(self, command):
#         """Vérifie si une commande système est disponible de manière plus robuste"""
#         try:
#             subprocess.run(command, check=True, 
#                           stdout=subprocess.PIPE, 
#                           stderr=subprocess.PIPE,
#                           timeout=10)
#             return True
#         except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
#             return False
            
#     def check_freqtrade_installation(self):
#         """Vérifie si Freqtrade est déjà installé de manière plus robuste"""
#         if not os.path.exists(self.freqtrade_dir):
#             return False
            
#         try:
#             # Vérifier si freqtrade est installé et fonctionnel
#             result = subprocess.run(["freqtrade", "--version"], 
#                                   cwd=self.freqtrade_dir,
#                                   stdout=subprocess.PIPE, 
#                                   stderr=subprocess.PIPE,
#                                   text=True,
#                                   timeout=30)
#             return result.returncode == 0
#         except:
#             return False

#     def get_install_commands(self, version):
#         """Retourne les commandes d'installation appropriées avec des vérifications"""
#         commands = []
        
#         # 1. Vérifier et créer les répertoires nécessaires
#         commands.append(f"@echo Création des répertoires nécessaires")
#         commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
#         commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
#         # 2. Installation des dépendances système si manquantes
#         if not self.git_installed:
#             if platform.system() == "Windows":
#                 commands.append("@echo Installation de Git...")
#                 commands.append("winget install --id Git.Git -e --source winget")
#             elif platform.system() == "Linux":
#                 commands.append("@echo Installation de Git...")
#                 commands.append("sudo apt-get update && sudo apt-get install -y git")
#             elif platform.system() == "Darwin":
#                 commands.append("@echo Installation de Git...")
#                 commands.append("brew install git")
        
#         if not self.python_installed:
#             if platform.system() == "Windows":
#                 commands.append("@echo Installation de Python...")
#                 commands.append("winget install Python.Python.3 --silent")
#             elif platform.system() == "Linux":
#                 commands.append("@echo Installation de Python...")
#                 commands.append("sudo apt-get update && sudo apt-get install -y python3 python3-pip")
#             elif platform.system() == "Darwin":
#                 commands.append("@echo Installation de Python...")
#                 commands.append("brew install python")
        
#         # 3. Installation Docker si nécessaire
#         if self.docker_check.isChecked() and not self.docker_installed:
#             if platform.system() == "Windows":
#                 commands.append("@echo Installation de Docker...")
#                 commands.extend([
#                     f"cd /d \"{self.base_dir}\"",
#                     "curl -Lo docker_installer.exe https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
#                     "start /wait docker_installer.exe install --quiet",
#                     "del docker_installer.exe"
#                 ])
#             elif platform.system() == "Linux":
#                 commands.append("@echo Installation de Docker...")
#                 commands.extend([
#                     "sudo apt-get update",
#                     "sudo apt-get install -y docker.io docker-compose",
#                     "sudo systemctl enable --now docker",
#                     "sudo usermod -aG docker $USER"
#                 ])
#             elif platform.system() == "Darwin":
#                 commands.append("@echo Installation de Docker...")
#                 commands.extend([
#                     "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
#                     "brew install --cask docker"
#                 ])
        
#         # 4. Commandes Freqtrade avec vérifications
#         if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
#             commands.append("@echo Clonage du dépôt Freqtrade...")
#             commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\" || echo Échec du clonage")
#         else:
#             commands.append("@echo Mise à jour du dépôt Freqtrade...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && git fetch --all || echo Échec de la mise à jour")
            
#         commands.extend([
#             f"@echo Installation de Freqtrade version {version}",
#             f"cd \"{self.freqtrade_dir}\" && git checkout {version} || echo Échec du checkout",
#             f"cd \"{self.freqtrade_dir}\" && git pull || echo Échec du pull",
#             f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip || echo Échec de la mise à jour de pip",
#             f"cd \"{self.freqtrade_dir}\" && python -m pip install -e . || echo Échec de l'installation",
#             f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-common.txt || echo Échec de l'installation des dépendances"
#         ])
        
#         # 5. Dépendances optionnelles
#         if self.plot_check.isChecked():
#             commands.append("@echo Installation des dépendances de visualisation...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-plot.txt || echo Échec de l'installation des dépendances de visualisation")
            
#         if self.ta_check.isChecked():
#             commands.append("@echo Installation des dépendances d'analyse technique...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-ft.txt || echo Échec de l'installation des dépendances d'analyse technique")
        
#         return commands

#     def start_installation(self):
#         """Lance le processus d'installation avec gestion des erreurs améliorée"""
#         if self.installation_in_progress:
#             QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
#             return
            
#         # Créer les répertoires de base si nécessaire
#         try:
#             os.makedirs(self.base_dir, exist_ok=True)
#             os.makedirs(self.freqtrade_dir, exist_ok=True)
#         except Exception as e:
#             QMessageBox.critical(self, "Erreur", f"Impossible de créer les répertoires: {str(e)}")
#             return
            
#         self.installation_in_progress = True
#         self.install_btn.setEnabled(False)
#         self.output.clear()
        
#         # Préparer les commandes d'installation
#         version = self.version_combo.currentText()
#         commands = self.get_install_commands(version)
        
#         # Exécuter les commandes une par une
#         self.current_command = 0
#         self.commands = commands
#         self.progress.setMaximum(len(commands))
#         self.execute_next_command()

#     def execute_next_command(self):
#         """Exécute la prochaine commande avec gestion des erreurs améliorée"""
#         if self.current_command >= len(self.commands):
#             self.installation_completed()
#             return
            
#         cmd = self.commands[self.current_command]
        
#         # Gestion spéciale des commandes echo
#         if cmd.startswith("@echo "):
#             self.output.append(f"<font color='blue'>{cmd[6:]}</font>")
#             self.current_command += 1
#             self.progress.setValue(self.current_command)
#             QTimer.singleShot(100, self.execute_next_command)
#             return
            
#         self.output.append(f"> {cmd}")
        
#         try:
#             # Créer un worker pour exécuter la commande
#             self.current_worker = CommandWorker(cmd, self.base_dir)
#             self.current_worker.output_signal.connect(self.handle_command_output)
#             self.current_worker.finished.connect(self.command_finished)
#             self.current_worker.start()
            
#         except Exception as e:
#             self.output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
#             # Continuer avec la commande suivante malgré l'erreur
#             self.current_command += 1
#             self.progress.setValue(self.current_command)
#             QTimer.singleShot(100, self.execute_next_command)

#     def installation_completed(self):
#         """Appelé lorsque l'installation est terminée"""
#         self.installation_in_progress = False
#         self.install_btn.setEnabled(True)
        
#         # Vérifier à nouveau les dépendances
#         self.check_dependencies()
#         self.update_ui_state()
        
#         version = self.version_combo.currentText()
#         self.log_installation(version, "Terminé", "Processus d'installation terminé")
        
#         # Vérifier si l'installation a réussi
#         if self.freqtrade_installed:
#             QMessageBox.information(self, "Succès", "Installation terminée avec succès!")
#             self.install_btn.setText("Mettre à jour Freqtrade")
#         else:
#             QMessageBox.warning(self, "Avertissement", 
#                                "Le processus d'installation est terminé mais Freqtrade n'est peut-être pas correctement installé. "
#                                "Consultez la sortie pour plus de détails.")

#     # ... (le reste du code reste inchangé)


#     def get_install_commands(self, version):
#         """Retourne les commandes d'installation améliorées"""
#         commands = []
        
#         # 1. Création des répertoires
#         commands.append(f"@echo Création des répertoires nécessaires")
#         commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
#         commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
#         # 2. Clonage ou mise à jour du dépôt
#         if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
#             commands.append(f"@echo Clonage du dépôt Freqtrade...")
#             commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\" || exit 1")
#         else:
#             commands.append(f"@echo Mise à jour du dépôt Freqtrade...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && git fetch --all || exit 1")
        
#         # 3. Checkout et pull
#         commands.append(f"@echo Sélection de la version {version}")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && git checkout {version} || exit 1")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && git pull || exit 1")
        
#         # 4. Installation standard (au lieu de -e .)
#         commands.append(f"@echo Installation des dépendances principales...")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip || exit 1")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install . || exit 1")
        
#         # 5. Installation des dépendances supplémentaires
#         commands.append(f"@echo Installation des dépendances communes...")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-common.txt || exit 1")
        
#         if self.plot_check.isChecked():
#             commands.append(f"@echo Installation des dépendances de visualisation...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-plot.txt || exit 1")
            
#         if self.ta_check.isChecked():
#             commands.append(f"@echo Installation des dépendances d'analyse technique...")
#             commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install -r requirements-ft.txt || exit 1")
        
#         return commands
#     def installation_completed(self):
#         """Vérifie que l'installation a réussi"""
#         self.installation_in_progress = False
#         self.install_btn.setEnabled(True)
        
#         # Vérification finale
#         success = self.check_freqtrade_installation()
#         self.freqtrade_installed = success
#         self.update_ui_state()
        
#         version = self.version_combo.currentText()
#         if success:
#             self.log_installation(version, "Succès", "Installation terminée avec succès")
#             QMessageBox.information(self, "Succès", 
#                                 "Freqtrade a été installé avec succès!\n\n"
#                                 f"Répertoire : {self.freqtrade_dir}")
#             self.install_btn.setText("Mettre à jour Freqtrade")
#         else:
#             self.log_installation(version, "Échec", "Installation incomplète")
#             QMessageBox.warning(self, "Avertissement",
#                             "L'installation semble incomplète.\n"
#                             "Veuillez vérifier la sortie pour les erreurs.")

#     def get_install_commands(self, version):
#         """Commandes d'installation optimisées pour Windows"""
#         commands = []
        
#         # 1. Installer les prérequis système
#         commands.append("@echo Installation des outils de compilation...")
#         commands.append("winget install Python.Python.3 --silent")
#         commands.append("winget install Git.Git --silent")
#         commands.append("winget install Microsoft.VisualStudio.2022.BuildTools --silent --override \"--wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended\"")
        
#         # 2. Configuration de l'environnement
#         commands.append("@echo Configuration de l'environnement...")
#         commands.append(f"mkdir \"{self.base_dir}\" 2>nul || echo Répertoire existe déjà")
#         commands.append(f"mkdir \"{self.freqtrade_dir}\" 2>nul || echo Répertoire existe déjà")
        
#         # 3. Clonage du dépôt
#         if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
#             commands.append("@echo Clonage du dépôt Freqtrade...")
#             commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\"")
        
#         # 4. Mise à jour
#         commands.append("@echo Mise à jour du dépôt...")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && git checkout {version} && git pull")
        
#         # 5. Installation avec wheel précompilé
#         commands.append("@echo Installation des dépendances...")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install --upgrade pip setuptools wheel")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install numpy --only-binary=:all:")
#         commands.append(f"cd \"{self.freqtrade_dir}\" && python -m pip install . --use-pep517")
        
#         return commands


# import sys
# import os
# import subprocess
# import platform
# import sqlite3
# import shutil
# import webbrowser
# from datetime import datetime
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
#                            QVBoxLayout, QWidget, QLabel, QTextEdit,
#                            QMessageBox, QProgressBar, QCheckBox, 
#                            QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
#                            QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
#                            QAction)
# from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
# from PyQt5.QtGui import QIcon, QFont, QTextCursor

# class CommandWorker(QThread):
#     output_signal = pyqtSignal(str, str)  # text, color
    
#     def __init__(self, command, cwd=None):
#         super().__init__()
#         self.command = command
#         self.cwd = cwd or os.getcwd()
#         self.process = None
        
#     def run(self):
#         try:
#             self.process = subprocess.Popen(
#                 self.command,
#                 cwd=self.cwd,
#                 shell=True,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 universal_newlines=True,
#                 bufsize=1
#             )
            
#             while True:
#                 output = self.process.stdout.readline()
#                 if output == '' and self.process.poll() is not None:
#                     break
#                 if output:
#                     self.output_signal.emit(output.strip(), "white")
                
#                 err = self.process.stderr.readline()
#                 if err:
#                     self.output_signal.emit(err.strip(), "red")
                    
#         except Exception as e:
#             self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            
#     def stop(self):
#         if self.process and self.process.poll() is None:
#             try:
#                 if platform.system() == "Windows":
#                     subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], check=True)
#                 else:
#                     self.process.terminate()
#                     self.process.wait()
#             except Exception as e:
#                 self.output_signal.emit(f"Error stopping process: {str(e)}", "red")

# if __name__ == "__main__":
#     # Vérifier et installer les dépendances PyQt5 si nécessaire
#     try:
#         from PyQt5.QtWidgets import QApplication
#     except ImportError:
#         try:
#             subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
#             from PyQt5.QtWidgets import QApplication
#         except:
#             print("PyQt5 est requis. Veuillez l'installer manuellement avec: pip install PyQt5")
#             sys.exit(1)
    
#     # Créer l'application
#     app = QApplication(sys.argv)
    
#     # Créer et afficher la fenêtre principale
#     window = FreqtradeManager()
#     window.show()
    
#     # Exécuter l'application
#     sys.exit(app.exec_())
# if __name__ == "__main__":
#     # Vérifier et installer les dépendances si nécessaire
#     try:
#         from PyQt5.QtWidgets import QApplication
#     except ImportError:
#         try:
#             subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
#             from PyQt5.QtWidgets import QApplication
#         except:
#             print("PyQt5 est requis. Veuillez l'installer manuellement avec: pip install PyQt5")
#             sys.exit(1)
    
#     # Créer l'application
#     app = QApplication(sys.argv)
    
#     # Vérifier la présence de git et python
#     try:
#         subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     except:
#         print("Git et Python sont requis pour ce programme")
    
#     # Créer et afficher la fenêtre principale
#     window = FreqtradeManager()
#     window.show()
    
#     # Exécuter l'application
#     sys.exit(app.exec_())





import sys
import os
import subprocess
import platform
import sqlite3
import shutil
import webbrowser
import json
import venv
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, 
                           QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
                           QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
                           QAction, QTreeWidget, QTreeWidgetItem, QHeaderView,
                           QInputDialog, QSplitter, QPlainTextEdit)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal, QProcess, QByteArray
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QColor, QTextCharFormat
from PyQt5.QtWidgets import QStackedWidget, QStyleFactory

class CommandWorker(QThread):
    output_signal = pyqtSignal(str, str)  # text, color
    finished_signal = pyqtSignal(bool)  # success
    
    def __init__(self, command, cwd=None, env=None):
        super().__init__()
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.env = env or os.environ.copy()
        self.process = None
        self._is_running = True
        
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
                bufsize=1,
                env=self.env
            )
            
            while self._is_running:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip(), "white")
                
                err = self.process.stderr.readline()
                if err:
                    self.output_signal.emit(err.strip(), "red")
            
            return_code = self.process.poll()
            self.finished_signal.emit(return_code == 0)
                    
        except Exception as e:
            self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            self.finished_signal.emit(False)
            
    def stop(self):
        self._is_running = False
        if self.process and self.process.poll() is None:
            try:
                if platform.system() == "Windows":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.process.pid)], check=True)
                else:
                    self.process.terminate()
                    self.process.wait()
            except Exception as e:
                self.output_signal.emit(f"Error stopping process: {str(e)}", "red")

class BotManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade/FreqAI Manager")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(QSize(1000, 800))
        
        # Chemins importants
        self.base_dir = self.get_base_dir()
        self.db_path = os.path.join(self.base_dir, "bot_manager.db")
        self.config_dir = os.path.join(self.base_dir, "configs")
        self.log_dir = os.path.join(self.base_dir, "logs")
        
        # Variables d'état
        self.current_operation = None
        self.active_bots = {}  # {bot_id: worker}
        self.current_worker = None
        self.execution_history = []
        
        # Initialisation
        self.init_directories()
        self.init_db()
        self.check_system_dependencies()
        
        # Interface utilisateur
        self.init_ui()
        self.init_tray_icon()
        self.init_menu_bar()
        self.set_style()
        
        # Mise à jour initiale
        self.update_bots_list()
        self.update_ui_state()
        
        # Configuration du logging
        self.setup_logging()

    def setup_logging(self):
        """Configure le système de logging"""
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
    def log_message(self, message, level="INFO"):
        """Enregistre un message dans le fichier de log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to write to log file: {str(e)}")

    def get_base_dir(self):
        """Détermine le répertoire de base selon l'OS"""
        if platform.system() == "Windows":
            return os.path.join(os.environ.get("APPDATA", "C:\\"), "CryptoBotManager")
        else:
            return os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "crypto_bot_manager")

    def init_directories(self):
        """Crée les répertoires nécessaires"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Table des bots
            c.execute('''CREATE TABLE IF NOT EXISTS bots
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          type TEXT CHECK(type IN ('freqtrade', 'freqai')),
                          path TEXT,
                          version TEXT,
                          venv_path TEXT,
                          install_date TEXT,
                          status TEXT,
                          last_used TEXT)''')
            
            # Table des configurations
            c.execute('''CREATE TABLE IF NOT EXISTS configs
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          bot_id INTEGER,
                          name TEXT,
                          path TEXT,
                          last_used TEXT,
                          FOREIGN KEY(bot_id) REFERENCES bots(id) ON DELETE CASCADE,
                          UNIQUE(bot_id, name))''')
            
            # Table des dépendances
            c.execute('''CREATE TABLE IF NOT EXISTS dependencies
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          status TEXT,
                          install_date TEXT)''')
            
            # Table des exécutions
            c.execute('''CREATE TABLE IF NOT EXISTS executions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          bot_id INTEGER,
                          start_time TEXT,
                          end_time TEXT,
                          command TEXT,
                          config_id INTEGER,
                          status TEXT,
                          output TEXT,
                          FOREIGN KEY(bot_id) REFERENCES bots(id) ON DELETE CASCADE,
                          FOREIGN KEY(config_id) REFERENCES configs(id) ON DELETE SET NULL)''')
            
            # Table des paramètres
            c.execute('''CREATE TABLE IF NOT EXISTS settings
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          key TEXT UNIQUE,
                          value TEXT)''')
            
            # Insérer les paramètres par défaut
            c.execute('''INSERT OR IGNORE INTO settings (key, value) VALUES 
                         ('theme', 'dark'),
                         ('auto_update', '1'),
                         ('notifications', '1')''')
            
            conn.commit()
            conn.close()
            self.log_message("Database initialized successfully")
        except Exception as e:
            self.log_message(f"Failed to initialize database: {str(e)}", "ERROR")
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

    def get_setting(self, key, default=None):
        """Récupère un paramètre de la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT value FROM settings WHERE key=?", (key,))
            result = c.fetchone()
            conn.close()
            return result[0] if result else default
        except Exception as e:
            self.log_message(f"Failed to get setting {key}: {str(e)}", "ERROR")
            return default

    def set_setting(self, key, value):
        """Définit un paramètre dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO settings (key, value) 
                         VALUES (?, ?)''', (key, value))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            self.log_message(f"Failed to set setting {key}: {str(e)}", "ERROR")
            return False

    def check_system_dependencies(self):
        """Vérifie et enregistre les dépendances système"""
        dependencies = [
            ("git", ["git", "--version"]),
            ("python", ["python", "--version"]),
            ("docker", ["docker", "--version"]),
            ("pip", ["pip", "--version"]),
            ("freqtrade", ["freqtrade", "--version"])
        ]
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            for name, cmd in dependencies:
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    status = "installed"
                    self.log_message(f"Dependency {name} is installed")
                except:
                    status = "missing"
                    self.log_message(f"Dependency {name} is missing", "WARNING")
                
                # Mettre à jour ou insérer
                c.execute('''INSERT OR REPLACE INTO dependencies (name, status, install_date)
                             VALUES (?, ?, ?)''',
                         (name, status, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to check dependencies: {str(e)}", "ERROR")

    def log_execution(self, bot_id, command, status, config_id=None, output=""):
        """Journalise l'exécution dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            if status == "started":
                c.execute('''INSERT INTO executions 
                            (bot_id, start_time, command, config_id, status)
                            VALUES (?, ?, ?, ?, ?)''',
                         (bot_id, datetime.now().isoformat(), command, config_id, status))
                exec_id = c.lastrowid
            else:
                c.execute('''UPDATE executions 
                            SET end_time=?, status=?, output=?
                            WHERE id=(SELECT MAX(id) FROM executions WHERE bot_id=?)''',
                         (datetime.now().isoformat(), status, output, bot_id))
                exec_id = None
            
            conn.commit()
            conn.close()
            return exec_id
        except Exception as e:
            self.log_message(f"Failed to log execution: {str(e)}", "ERROR")
            return None

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Création des onglets
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Onglet Bots
        self.setup_bots_tab()
        
        # Onglet Installation
        self.setup_install_tab()
        
        # Onglet Configuration
        self.setup_config_tab()
        
        # Onglet Exécution
        self.setup_execution_tab()
        
        # Onglet Historique
        self.setup_history_tab()
        
        # Onglet Paramètres
        self.setup_settings_tab()
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")

    def setup_bots_tab(self):
        """Configure l'onglet de gestion des bots"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Gestion des Bots</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Splitter pour une meilleure organisation
        splitter = QSplitter(Qt.Vertical)
        
        # Liste des bots
        self.bots_tree = QTreeWidget()
        self.bots_tree.setHeaderLabels(["ID", "Nom", "Type", "Version", "Statut", "Dernière utilisation"])
        self.bots_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bots_tree.setSelectionMode(QTreeWidget.SingleSelection)
        self.bots_tree.itemSelectionChanged.connect(self.on_bot_selected)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Démarrer")
        self.start_btn.clicked.connect(self.start_selected_bot)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Arrêter")
        self.stop_btn.clicked.connect(self.stop_selected_bot)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("Redémarrer")
        self.restart_btn.clicked.connect(self.restart_selected_bot)
        self.restart_btn.setEnabled(False)
        btn_layout.addWidget(self.restart_btn)
        
        self.remove_btn = QPushButton("Supprimer")
        self.remove_btn.clicked.connect(self.remove_selected_bot)
        btn_layout.addWidget(self.remove_btn)
        
        self.update_btn = QPushButton("Mettre à jour")
        self.update_btn.clicked.connect(self.update_selected_bot)
        btn_layout.addWidget(self.update_btn)
        
        btn_container = QWidget()
        btn_container.setLayout(btn_layout)
        
        top_container = QWidget()
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.bots_tree)
        top_layout.addWidget(btn_container)
        top_container.setLayout(top_layout)
        
        # Détails du bot
        self.bot_details = QTextEdit()
        self.bot_details.setReadOnly(True)
        
        splitter.addWidget(top_container)
        splitter.addWidget(self.bot_details)
        splitter.setSizes([400, 200])
        
        layout.addWidget(splitter)
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Bots")

    def setup_install_tab(self):
        """Configure l'onglet d'installation"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Installation de Bot</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Type de bot
        type_group = QGroupBox("Type de bot")
        type_layout = QHBoxLayout()
        
        self.bot_type_combo = QComboBox()
        self.bot_type_combo.addItems(["Freqtrade", "FreqAI"])
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.bot_type_combo)
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Options d'installation
        options_group = QGroupBox("Options d'installation")
        options_layout = QVBoxLayout()
        
        # Nom du bot
        self.bot_name_input = QLineEdit()
        self.bot_name_input.setPlaceholderText("Nom du bot (unique)")
        options_layout.addWidget(self.bot_name_input)
        
        # Version
        version_layout = QHBoxLayout()
        self.version_combo = QComboBox()
        self.version_combo.addItems(["stable", "develop", "master"])
        version_layout.addWidget(QLabel("Version:"))
        version_layout.addWidget(self.version_combo)
        options_layout.addLayout(version_layout)
        
        # Chemin d'installation
        path_layout = QHBoxLayout()
        self.install_path_input = QLineEdit()
        self.install_path_input.setPlaceholderText("Chemin d'installation")
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_install_path)
        path_layout.addWidget(self.install_path_input)
        path_layout.addWidget(browse_btn)
        options_layout.addLayout(path_layout)
        
        # Options
        self.create_venv_check = QCheckBox("Créer un environnement virtuel")
        self.create_venv_check.setChecked(True)
        options_layout.addWidget(self.create_venv_check)
        
        self.install_deps_check = QCheckBox("Installer les dépendances supplémentaires")
        self.install_deps_check.setChecked(True)
        options_layout.addWidget(self.install_deps_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Bouton d'installation
        self.install_btn = QPushButton("Installer")
        self.install_btn.setStyleSheet("background-color: #27ae60; color: white;")
        self.install_btn.clicked.connect(self.start_bot_installation)
        layout.addWidget(self.install_btn)
        
        # Barre de progression
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Console de sortie
        self.install_output = QPlainTextEdit()
        self.install_output.setReadOnly(True)
        self.install_output.setFont(QFont("Consolas", 10))
        
        # Configurer les couleurs pour la sortie
        palette = self.install_output.palette()
        palette.setColor(palette.Base, QColor(53, 53, 53))
        palette.setColor(palette.Text, QColor(255, 255, 255))
        self.install_output.setPalette(palette)
        
        layout.addWidget(self.install_output)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Installation")

    def setup_config_tab(self):
        """Configure l'onglet de configuration"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Configuration des Bots</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Sélection du bot
        bot_layout = QHBoxLayout()
        self.config_bot_combo = QComboBox()
        self.config_bot_combo.currentIndexChanged.connect(self.update_config_list)
        bot_layout.addWidget(QLabel("Bot:"))
        bot_layout.addWidget(self.config_bot_combo)
        layout.addLayout(bot_layout)
        
        # Liste des configurations
        self.config_list = QTreeWidget()
        self.config_list.setHeaderLabels(["Nom", "Chemin", "Dernière utilisation"])
        self.config_list.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.config_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.config_list.customContextMenuRequested.connect(self.show_config_context_menu)
        layout.addWidget(self.config_list)
        
        # Boutons de configuration
        btn_layout = QHBoxLayout()
        
        self.add_config_btn = QPushButton("Ajouter")
        self.add_config_btn.clicked.connect(self.add_config)
        btn_layout.addWidget(self.add_config_btn)
        
        self.edit_config_btn = QPushButton("Éditer")
        self.edit_config_btn.clicked.connect(self.edit_config)
        btn_layout.addWidget(self.edit_config_btn)
        
        self.remove_config_btn = QPushButton("Supprimer")
        self.remove_config_btn.clicked.connect(self.remove_config)
        btn_layout.addWidget(self.remove_config_btn)
        
        self.duplicate_config_btn = QPushButton("Dupliquer")
        self.duplicate_config_btn.clicked.connect(self.duplicate_config)
        btn_layout.addWidget(self.duplicate_config_btn)
        
        layout.addLayout(btn_layout)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Configuration")

    def setup_execution_tab(self):
        """Configure l'onglet d'exécution"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Exécution du Bot</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Sélection du bot
        bot_layout = QHBoxLayout()
        self.exec_bot_combo = QComboBox()
        self.exec_bot_combo.currentIndexChanged.connect(self.update_exec_config_combo)
        bot_layout.addWidget(QLabel("Bot:"))
        bot_layout.addWidget(self.exec_bot_combo)
        layout.addLayout(bot_layout)
        
        # Sélection de la configuration
        config_layout = QHBoxLayout()
        self.exec_config_combo = QComboBox()
        config_layout.addWidget(QLabel("Configuration:"))
        config_layout.addWidget(self.exec_config_combo)
        layout.addLayout(config_layout)
        
        # Mode d'exécution
        mode_layout = QHBoxLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Trade", "Backtest", "Hyperopt", "Plot", "Edge", "Download Data", "Other"])
        self.mode_combo.currentIndexChanged.connect(self.update_execution_options)
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)
        
        # Options spécifiques
        self.options_stack = QStackedWidget()
        
        # Options pour le mode Trade
        trade_options = QWidget()
        trade_layout = QVBoxLayout()
        
        strategy_layout = QHBoxLayout()
        self.strategy_input = QLineEdit("SampleStrategy")
        strategy_layout.addWidget(QLabel("Stratégie:"))
        strategy_layout.addWidget(self.strategy_input)
        trade_layout.addLayout(strategy_layout)
        
        self.db_check = QCheckBox("Utiliser la base de données")
        self.db_check.setChecked(True)
        trade_layout.addWidget(self.db_check)
        
        self.dry_run_check = QCheckBox("Mode Dry Run")
        self.dry_run_check.setChecked(True)
        trade_layout.addWidget(self.dry_run_check)
        
        trade_options.setLayout(trade_layout)
        self.options_stack.addWidget(trade_options)
        
        # Options pour le mode Backtest
        backtest_options = QWidget()
        backtest_layout = QVBoxLayout()
        
        bt_strategy_layout = QHBoxLayout()
        self.bt_strategy_input = QLineEdit("SampleStrategy")
        bt_strategy_layout.addWidget(QLabel("Stratégie:"))
        bt_strategy_layout.addWidget(self.bt_strategy_input)
        backtest_layout.addLayout(bt_strategy_layout)
        
        timerange_layout = QHBoxLayout()
        self.timerange_input = QLineEdit()
        self.timerange_input.setPlaceholderText("YYYYMMDD-YYYYMMDD")
        timerange_layout.addWidget(QLabel("Plage de temps:"))
        timerange_layout.addWidget(self.timerange_input)
        backtest_layout.addLayout(timerange_layout)
        
        backtest_options.setLayout(backtest_layout)
        self.options_stack.addWidget(backtest_options)
        
        # Options pour le mode Other (commandes personnalisées)
        other_options = QWidget()
        other_layout = QVBoxLayout()
        
        self.custom_cmd_input = QLineEdit()
        self.custom_cmd_input.setPlaceholderText("Entrez votre commande Freqtrade/FreqAI personnalisée")
        other_layout.addWidget(self.custom_cmd_input)
        
        other_options.setLayout(other_layout)
        self.options_stack.addWidget(other_options)
        
        layout.addWidget(self.options_stack)
        
        # Boutons d'exécution
        btn_layout = QHBoxLayout()
        
        self.exec_start_btn = QPushButton("Démarrer")
        self.exec_start_btn.clicked.connect(self.start_execution)
        btn_layout.addWidget(self.exec_start_btn)
        
        self.exec_stop_btn = QPushButton("Arrêter")
        self.exec_stop_btn.clicked.connect(self.stop_execution)
        self.exec_stop_btn.setEnabled(False)
        btn_layout.addWidget(self.exec_stop_btn)
        
        self.exec_clear_btn = QPushButton("Effacer")
        self.exec_clear_btn.clicked.connect(self.clear_execution_output)
        btn_layout.addWidget(self.exec_clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Console de sortie
        self.exec_output = QPlainTextEdit()
        self.exec_output.setReadOnly(True)
        self.exec_output.setFont(QFont("Consolas", 10))
        
        # Configurer les couleurs pour la sortie
        palette = self.exec_output.palette()
        palette.setColor(palette.Base, QColor(53, 53, 53))
        palette.setColor(palette.Text, QColor(255, 255, 255))
        self.exec_output.setPalette(palette)
        
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
        
        self.history_filter_combo = QComboBox()
        self.history_filter_combo.addItems(["Toutes", "Freqtrade", "FreqAI"])
        self.history_filter_combo.currentIndexChanged.connect(self.update_history)
        filter_layout.addWidget(self.history_filter_combo)
        
        self.refresh_history_btn = QPushButton("Actualiser")
        self.refresh_history_btn.clicked.connect(self.update_history)
        filter_layout.addWidget(self.refresh_history_btn)
        
        self.clear_history_btn = QPushButton("Effacer")
        self.clear_history_btn.clicked.connect(self.clear_history)
        filter_layout.addWidget(self.clear_history_btn)
        
        layout.addLayout(filter_layout)
        
        # Tableau d'historique
        self.history_table = QTreeWidget()
        self.history_table.setHeaderLabels(["ID", "Bot", "Date", "Commande", "Statut"])
        self.history_table.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.history_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_history_context_menu)
        self.history_table.itemDoubleClicked.connect(self.view_history_details)
        layout.addWidget(self.history_table)
        
        self.update_history()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Historique")

    def setup_settings_tab(self):
        """Configure l'onglet des paramètres"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Paramètres</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Thème
        theme_group = QGroupBox("Apparence")
        theme_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre", "System"])
        current_theme = self.get_setting("theme", "dark")
        self.theme_combo.setCurrentText("Sombre" if current_theme == "dark" else "Clair" if current_theme == "light" else "System")
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(QLabel("Thème:"))
        theme_layout.addWidget(self.theme_combo)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Comportement
        behavior_group = QGroupBox("Comportement")
        behavior_layout = QVBoxLayout()
        
        self.auto_update_check = QCheckBox("Vérifier automatiquement les mises à jour")
        self.auto_update_check.setChecked(self.get_setting("auto_update", "1") == "1")
        self.auto_update_check.stateChanged.connect(lambda: self.set_setting("auto_update", "1" if self.auto_update_check.isChecked() else "0"))
        behavior_layout.addWidget(self.auto_update_check)
        
        self.notifications_check = QCheckBox("Activer les notifications")
        self.notifications_check.setChecked(self.get_setting("notifications", "1") == "1")
        self.notifications_check.stateChanged.connect(lambda: self.set_setting("notifications", "1" if self.notifications_check.isChecked() else "0"))
        behavior_layout.addWidget(self.notifications_check)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        self.reset_settings_btn = QPushButton("Réinitialiser")
        self.reset_settings_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(self.reset_settings_btn)
        
        self.check_updates_btn = QPushButton("Vérifier les mises à jour")
        self.check_updates_btn.clicked.connect(self.check_for_updates)
        btn_layout.addWidget(self.check_updates_btn)
        
        layout.addLayout(btn_layout)
        
        # Espacement
        layout.addStretch()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Paramètres")

    def init_menu_bar(self):
        """Initialise la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        new_action = QAction("Nouveau", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.show_install_tab)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Édition
        edit_menu = menubar.addMenu("Édition")
        
        settings_action = QAction("Paramètres", self)
        settings_action.setShortcut("Ctrl+P")
        settings_action.triggered.connect(lambda: self.tabs.setCurrentIndex(5))  # Onglet Paramètres
        edit_menu.addAction(settings_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("Outils")
        
        check_deps_action = QAction("Vérifier les dépendances", self)
        check_deps_action.triggered.connect(self.check_system_dependencies)
        tools_menu.addAction(check_deps_action)
        
        update_all_action = QAction("Mettre à jour tous les bots", self)
        update_all_action.triggered.connect(self.update_all_bots)
        tools_menu.addAction(update_all_action)
        
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
        
        tray_menu.addSeparator()
        
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Afficher une notification de bienvenue
        if self.get_setting("notifications", "1") == "1":
            self.tray_icon.showMessage("Freqtrade/FreqAI Manager", 
                                     "L'application fonctionne en arrière-plan",
                                     QSystemTrayIcon.Information, 3000)

    def tray_icon_activated(self, reason):
        """Gère les clics sur l'icône de la barre système"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
            self.raise_()

    def set_style(self):
        """Applique le style à l'application"""
        theme = self.get_setting("theme", "dark")
        
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2d2d2d;
                }
                QWidget {
                    color: #e0e0e0;
                }
                QGroupBox {
                    border: 1px solid #444;
                    border-radius: 4px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px;
                    color: #bbbbbb;
                }
                QPushButton {
                    padding: 5px;
                    border-radius: 4px;
                    min-height: 25px;
                    background-color: #3a3a3a;
                    border: 1px solid #444;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
                QTabWidget::pane {
                    border-top: 2px solid #444;
                }
                QTabBar::tab {
                    padding: 8px;
                    background: #3a3a3a;
                    border: 1px solid #444;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: #2d2d2d;
                    color: white;
                }
                QTreeWidget {
                    background-color: #252525;
                    alternate-background-color: #2a2a2a;
                }
                QHeaderView::section {
                    background-color: #3a3a3a;
                    padding: 5px;
                    border: 1px solid #444;
                }
                QLineEdit, QComboBox {
                    background-color: #3a3a3a;
                    border: 1px solid #444;
                    padding: 3px;
                }
                QProgressBar {
                    border: 1px solid #444;
                    border-radius: 3px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #27ae60;
                }
            """)
        elif theme == "light":
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
                QPushButton {
                    padding: 5px;
                    border-radius: 4px;
                    min-height: 25px;
                    background-color: #f8f9fa;
                    border: 1px solid #ddd;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                }
                QPushButton:pressed {
                    background-color: #dee2e6;
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
                QTreeWidget {
                    alternate-background-color: #f8f9fa;
                }
                QHeaderView::section {
                    background-color: #e9ecef;
                    padding: 5px;
                    border: 1px solid #ddd;
                }
                QLineEdit, QComboBox {
                    border: 1px solid #ddd;
                    padding: 3px;
                }
                QProgressBar {
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #27ae60;
                }
            """)
        else:
            # Style système par défaut
            self.setStyleSheet("")

    def change_theme(self, theme_name):
        """Change le thème de l'application"""
        theme_map = {
            "Clair": "light",
            "Sombre": "dark",
            "System": "system"
        }
        theme = theme_map.get(theme_name, "dark")
        self.set_setting("theme", theme)
        self.set_style()

    def reset_settings(self):
        """Réinitialise les paramètres par défaut"""
        reply = QMessageBox.question(self, "Confirmation", 
                                   "Voulez-vous vraiment réinitialiser tous les paramètres?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Supprimer tous les paramètres
                c.execute("DELETE FROM settings")
                
                # Réinsérer les valeurs par défaut
                c.execute('''INSERT INTO settings (key, value) VALUES 
                             ('theme', 'dark'),
                             ('auto_update', '1'),
                             ('notifications', '1')''')
                
                conn.commit()
                conn.close()
                
                # Mettre à jour l'interface
                self.theme_combo.setCurrentText("Sombre")
                self.auto_update_check.setChecked(True)
                self.notifications_check.setChecked(True)
                
                QMessageBox.information(self, "Succès", "Paramètres réinitialisés avec succès!")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la réinitialisation: {str(e)}")

    def check_for_updates(self):
        """Vérifie les mises à jour disponibles"""
        self.status_bar.showMessage("Vérification des mises à jour...")
        
        try:
            # Vérifier les mises à jour du manager
            # (Dans une vraie application, vous utiliseriez une API ou un dépôt)
            QMessageBox.information(self, "Mises à jour", 
                                  "Vérification des mises à jour non implémentée dans cette version.")
            
            # Vérifier les mises à jour des bots
            self.update_all_bots(check_only=True)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la vérification des mises à jour: {str(e)}")
        
        self.status_bar.showMessage("Prêt")

    def update_ui_state(self):
        """Met à jour l'état de l'interface"""
        # Mettre à jour les listes
        self.update_bots_list()
        self.update_config_bot_combo()
        self.update_exec_bot_combo()
        
        # Vérifier les dépendances
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT name, status FROM dependencies")
            deps = c.fetchall()
            
            missing_deps = [name for name, status in deps if status == "missing"]
            
            if missing_deps:
                msg = f"Les dépendances suivantes sont manquantes: {', '.join(missing_deps)}\nCertaines fonctionnalités peuvent ne pas être disponibles."
                self.status_bar.showMessage(msg, 5000)
                self.log_message(msg, "WARNING")
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to check dependencies: {str(e)}", "ERROR")

    def update_bots_list(self):
        """Met à jour la liste des bots dans l'onglet Bots"""
        self.bots_tree.clear()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name, type, version, status, last_used FROM bots ORDER BY last_used DESC")
            bots = c.fetchall()
            
            for bot in bots:
                item = QTreeWidgetItem([str(bot[0]), bot[1], bot[2], bot[3], bot[4], bot[5]])
                
                # Colorer les bots en cours d'exécution
                if bot[4] == "running":
                    item.setForeground(4, QColor(0, 200, 0))  # Vert
                elif bot[4] == "error":
                    item.setForeground(4, QColor(200, 0, 0))  # Rouge
                
                self.bots_tree.addTopLevelItem(item)
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update bots list: {str(e)}", "ERROR")

    def update_config_bot_combo(self):
        """Met à jour la liste des bots dans l'onglet Configuration"""
        self.config_bot_combo.clear()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name, type FROM bots ORDER BY name")
            bots = c.fetchall()
            
            for bot in bots:
                self.config_bot_combo.addItem(f"{bot[1]} ({bot[2]})", bot[0])
            
            if bots:
                self.update_config_list()
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update config bot combo: {str(e)}", "ERROR")

    def update_exec_bot_combo(self):
        """Met à jour la liste des bots dans l'onglet Exécution"""
        self.exec_bot_combo.clear()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name, type FROM bots ORDER BY name")
            bots = c.fetchall()
            
            for bot in bots:
                self.exec_bot_combo.addItem(f"{bot[1]} ({bot[2]})", bot[0])
            
            if bots:
                self.update_exec_config_combo()
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update exec bot combo: {str(e)}", "ERROR")

    def update_config_list(self):
        """Met à jour la liste des configurations pour le bot sélectionné"""
        self.config_list.clear()
        
        bot_id = self.config_bot_combo.currentData()
        if not bot_id:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name, path, last_used FROM configs WHERE bot_id=? ORDER BY last_used DESC", (bot_id,))
            configs = c.fetchall()
            
            for config in configs:
                item = QTreeWidgetItem([config[1], config[2], config[3]])
                item.setData(0, Qt.UserRole, config[0])
                self.config_list.addTopLevelItem(item)
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update config list: {str(e)}", "ERROR")

    def update_exec_config_combo(self):
        """Met à jour la liste des configurations pour l'exécution"""
        self.exec_config_combo.clear()
        
        bot_id = self.exec_bot_combo.currentData()
        if not bot_id:
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name FROM configs WHERE bot_id=? ORDER BY last_used DESC", (bot_id,))
            configs = c.fetchall()
            
            for config in configs:
                self.exec_config_combo.addItem(config[1], config[0])
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update exec config combo: {str(e)}", "ERROR")

    def update_execution_options(self):
        """Met à jour les options d'exécution en fonction du mode sélectionné"""
        mode = self.mode_combo.currentText().lower()
        
        if mode == "other":
            self.options_stack.setCurrentIndex(2)  # Options personnalisées
        elif mode == "backtest":
            self.options_stack.setCurrentIndex(1)  # Options backtest
        else:
            self.options_stack.setCurrentIndex(0)  # Options trade

    def update_history(self):
        """Met à jour l'historique des exécutions"""
        self.history_table.clear()
        
        filter_type = self.history_filter_combo.currentText()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            if filter_type == "Toutes":
                c.execute('''SELECT e.id, b.name, e.start_time, e.command, e.status 
                            FROM executions e JOIN bots b ON e.bot_id = b.id
                            ORDER BY e.start_time DESC LIMIT 100''')
            else:
                c.execute('''SELECT e.id, b.name, e.start_time, e.command, e.status 
                            FROM executions e JOIN bots b ON e.bot_id = b.id
                            WHERE b.type = ? ORDER BY e.start_time DESC LIMIT 100''',
                         (filter_type.lower(),))
            
            executions = c.fetchall()
            
            for exec_ in executions:
                item = QTreeWidgetItem([str(exec_[0]), exec_[1], exec_[2], exec_[3], exec_[4]])
                
                # Colorer selon le statut
                if exec_[4] == "running":
                    item.setForeground(4, QColor(0, 200, 0))  # Vert
                elif exec_[4] == "failed":
                    item.setForeground(4, QColor(200, 0, 0))  # Rouge
                elif exec_[4] == "completed":
                    item.setForeground(4, QColor(100, 100, 255))  # Bleu
                
                self.history_table.addTopLevelItem(item)
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update history: {str(e)}", "ERROR")

    def clear_history(self):
        """Efface l'historique des exécutions"""
        reply = QMessageBox.question(self, "Confirmation", 
                                   "Voulez-vous vraiment effacer tout l'historique?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                c.execute("DELETE FROM executions")
                conn.commit()
                conn.close()
                
                self.update_history()
                QMessageBox.information(self, "Succès", "Historique effacé avec succès!")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de l'effacement de l'historique: {str(e)}")

    def view_history_details(self, item, column):
        """Affiche les détails d'une entrée d'historique"""
        exec_id = int(item.text(0))
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''SELECT e.command, e.status, e.output, e.start_time, e.end_time, 
                                b.name, c.name
                         FROM executions e 
                         JOIN bots b ON e.bot_id = b.id
                         LEFT JOIN configs c ON e.config_id = c.id
                         WHERE e.id=?''', (exec_id,))
            
            result = c.fetchone()
            if result:
                command, status, output, start_time, end_time, bot_name, config_name = result
                
                details = f"""<h2>Détails de l'exécution #{exec_id}</h2>
                            <p><b>Bot:</b> {bot_name}</p>
                            <p><b>Configuration:</b> {config_name if config_name else 'N/A'}</p>
                            <p><b>Commande:</b> {command}</p>
                            <p><b>Statut:</b> {status}</p>
                            <p><b>Début:</b> {start_time}</p>
                            <p><b>Fin:</b> {end_time if end_time else 'En cours'}</p>
                            <h3>Sortie:</h3>
                            <pre>{output if output else 'Aucune sortie enregistrée'}</pre>"""
                
                msg_box = QMessageBox()
                msg_box.setWindowTitle(f"Détails de l'exécution #{exec_id}")
                msg_box.setTextFormat(Qt.RichText)
                msg_box.setText(details)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec_()
            
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'afficher les détails: {str(e)}")

    def show_config_context_menu(self, position):
        """Affiche le menu contextuel pour la liste des configurations"""
        item = self.config_list.itemAt(position)
        if not item:
            return
            
        menu = QMenu()
        
        edit_action = menu.addAction("Éditer")
        edit_action.triggered.connect(self.edit_config)
        
        remove_action = menu.addAction("Supprimer")
        remove_action.triggered.connect(self.remove_config)
        
        duplicate_action = menu.addAction("Dupliquer")
        duplicate_action.triggered.connect(self.duplicate_config)
        
        menu.addSeparator()
        
        show_in_explorer = menu.addAction("Ouvrir dans l'explorateur")
        show_in_explorer.triggered.connect(lambda: self.open_in_explorer(item.text(1)))
        
        menu.exec_(self.config_list.viewport().mapToGlobal(position))

    def show_history_context_menu(self, position):
        """Affiche le menu contextuel pour l'historique"""
        item = self.history_table.itemAt(position)
        if not item:
            return
            
        menu = QMenu()
        
        view_details = menu.addAction("Voir les détails")
        view_details.triggered.connect(lambda: self.view_history_details(item, 0))
        
        menu.addSeparator()
        
        copy_id = menu.addAction("Copier l'ID")
        copy_id.triggered.connect(lambda: QApplication.clipboard().setText(item.text(0)))
        
        copy_command = menu.addAction("Copier la commande")
        copy_command.triggered.connect(lambda: QApplication.clipboard().setText(item.text(3)))
        
        menu.exec_(self.history_table.viewport().mapToGlobal(position))

    def open_in_explorer(self, path):
        """Ouvre l'explorateur de fichiers à l'emplacement spécifié"""
        if platform.system() == "Windows":
            os.startfile(os.path.dirname(path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", "-R", path])
        else:
            subprocess.run(["xdg-open", os.path.dirname(path)])

    def on_bot_selected(self):
        """Affiche les détails du bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            return
            
        bot_id = int(selected[0].text(0))
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT * FROM bots WHERE id=?", (bot_id,))
            bot = c.fetchone()
            
            if bot:
                details = f"""<h2>{bot[1]} ({bot[2]})</h2>
                            <p><b>Version:</b> {bot[4]}</p>
                            <p><b>Statut:</b> {bot[7]}</p>
                            <p><b>Installé le:</b> {bot[6]}</p>
                            <p><b>Dernière utilisation:</b> {bot[8]}</p>
                            <p><b>Chemin:</b> {bot[3]}</p>
                            <p><b>Environnement virtuel:</b> {bot[5] if bot[5] else 'Non'}</p>
                            <h3>Dernières exécutions:</h3>"""
                
                # Ajouter les dernières exécutions
                c.execute('''SELECT start_time, command, status 
                            FROM executions WHERE bot_id=? 
                            ORDER BY start_time DESC LIMIT 5''', (bot_id,))
                executions = c.fetchall()
                
                if executions:
                    details += "<ul>"
                    for exec_ in executions:
                        details += f"<li>[{exec_[0]}] {exec_[1]} - <b>{exec_[2]}</b></li>"
                    details += "</ul>"
                else:
                    details += "<p>Aucune exécution enregistrée</p>"
                
                self.bot_details.setHtml(details)
            
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to get bot details: {str(e)}", "ERROR")

    def browse_install_path(self):
        """Ouvre un dialogue pour choisir le chemin d'installation"""
        path = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire d'installation")
        if path:
            self.install_path_input.setText(path)

    def start_bot_installation(self):
        """Démarre le processus d'installation d'un nouveau bot"""
        bot_name = self.bot_name_input.text().strip()
        bot_type = self.bot_type_combo.currentText().lower()
        version = self.version_combo.currentText()
        install_path = self.install_path_input.text().strip()
        create_venv = self.create_venv_check.isChecked()
        install_deps = self.install_deps_check.isChecked()
        
        # Validation
        if not bot_name:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nom pour le bot")
            return
            
        if not install_path:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un répertoire d'installation")
            return
            
        # Vérifier si le nom existe déjà
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT 1 FROM bots WHERE name=?", (bot_name,))
            if c.fetchone():
                QMessageBox.warning(self, "Erreur", "Un bot avec ce nom existe déjà")
                return
                
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to check bot name: {str(e)}", "ERROR")
            return
            
        # Préparer les commandes d'installation
        self.install_commands = []
        
        # 1. Créer le répertoire
        bot_path = os.path.join(install_path, bot_name)
        self.install_commands.append(f"@echo Création du répertoire {bot_path}")
        self.install_commands.append(f"mkdir \"{bot_path}\"")
        
        # 2. Cloner le dépôt
        repo_url = "https://github.com/freqtrade/freqtrade.git" if bot_type == "freqtrade" else "https://github.com/freqtrade/freqai.git"
        self.install_commands.append(f"@echo Clonage du dépôt {repo_url}")
        self.install_commands.append(f"git clone {repo_url} \"{bot_path}\"")
        
        # 3. Checkout la version
        self.install_commands.append(f"@echo Sélection de la version {version}")
        self.install_commands.append(f"cd \"{bot_path}\" && git checkout {version}")
        
        # 4. Créer l'environnement virtuel si demandé
        venv_path = ""
        if create_venv:
            venv_path = os.path.join(bot_path, "venv")
            self.install_commands.append(f"@echo Création de l'environnement virtuel")
            self.install_commands.append(f"python -m venv \"{venv_path}\"")
            
            # Activer l'environnement virtuel pour les commandes suivantes
            activate_cmd = os.path.join(venv_path, "Scripts", "activate") if platform.system() == "Windows" else f"source {os.path.join(venv_path, 'bin', 'activate')}"
            pip_cmd = os.path.join(venv_path, "Scripts", "pip") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "pip")
        
        # 5. Installer les dépendances
        self.install_commands.append(f"@echo Installation des dépendances principales")
        
        if create_venv:
            self.install_commands.append(f"cd \"{bot_path}\" && {pip_cmd} install --upgrade pip")
            self.install_commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -e .")
            self.install_commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-common.txt")
        else:
            self.install_commands.append(f"cd \"{bot_path}\" && python -m pip install --upgrade pip")
            self.install_commands.append(f"cd \"{bot_path}\" && python -m pip install -e .")
            self.install_commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-common.txt")
        
        # 6. Installer les dépendances supplémentaires si demandé
        if install_deps:
            self.install_commands.append(f"@echo Installation des dépendances supplémentaires")
            
            if create_venv:
                self.install_commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-ft.txt")
                self.install_commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-plot.txt")
            else:
                self.install_commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-ft.txt")
                self.install_commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-plot.txt")
        
        # Démarrer l'installation
        self.current_operation = "installation"
        self.install_output.clear()
        self.progress.setMaximum(len(self.install_commands))
        self.progress.setValue(0)
        self.install_btn.setEnabled(False)
        
        # Enregistrer les informations du bot avant l'installation
        self.installing_bot = {
            "name": bot_name,
            "type": bot_type,
            "path": bot_path,
            "version": version,
            "venv_path": venv_path if create_venv else None
        }
        
        # Exécuter les commandes une par une
        self.current_command = 0
        self.execute_next_install_command()

    def execute_next_install_command(self):
        """Exécute la prochaine commande d'installation"""
        if self.current_command >= len(self.install_commands):
            self.installation_completed()
            return
            
        cmd = self.install_commands[self.current_command]
        
        # Gestion spéciale des commandes echo
        if cmd.startswith("@echo "):
            self.append_install_output(f"<font color='blue'>{cmd[6:]}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_install_command)
            return
            
        self.append_install_output(f"> {cmd}")
        
        try:
            # Créer un worker pour exécuter la commande
            self.current_worker = CommandWorker(cmd)
            self.current_worker.output_signal.connect(self.handle_install_output)
            self.current_worker.finished_signal.connect(self.install_command_finished)
            self.current_worker.start()
        except Exception as e:
            self.append_install_output(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_install_command)

    def append_install_output(self, text):
        """Ajoute du texte à la sortie d'installation avec mise en forme"""
        cursor = self.install_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if "<font color=" in text:
            self.install_output.appendHtml(text)
        else:
            self.install_output.appendPlainText(text)
        
        # Faire défiler vers le bas
        self.install_output.ensureCursorVisible()

    def handle_install_output(self, text, color):
        """Affiche la sortie de l'installation"""
        if color == "red":
            self.append_install_output(f"<font color='{color}'>{text}</font>")
        else:
            self.append_install_output(text)

    def install_command_finished(self, success):
        """Appelé lorsqu'une commande d'installation est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if not success and self.current_command < len(self.install_commands):
            self.append_install_output("<font color='orange'>La commande a échoué mais nous continuons...</font>")
        
        if self.current_command < len(self.install_commands):
            QTimer.singleShot(100, self.execute_next_install_command)
        else:
            self.installation_completed()

    def installation_completed(self):
        """Finalise l'installation"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Enregistrer le bot dans la base de données
            c.execute('''INSERT INTO bots 
                        (name, type, path, version, venv_path, install_date, status, last_used)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (self.installing_bot["name"],
                      self.installing_bot["type"],
                      self.installing_bot["path"],
                      self.installing_bot["version"],
                      self.installing_bot["venv_path"],
                      datetime.now().isoformat(),
                      "installed",
                      datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            self.append_install_output("<font color='green'>Installation terminée avec succès!</font>")
            QMessageBox.information(self, "Succès", "Le bot a été installé avec succès!")
            
            # Mettre à jour l'interface
            self.update_ui_state()
            self.bot_name_input.clear()
            self.install_path_input.clear()
            
        except Exception as e:
            self.append_install_output(f"<font color='red'>ERREUR: Échec de l'enregistrement dans la base de données: {str(e)}</font>")
            QMessageBox.critical(self, "Erreur", "Le bot a été installé mais n'a pas pu être enregistré dans la base de données.")
        
        finally:
            self.current_operation = None
            self.install_btn.setEnabled(True)

    def add_config(self):
        """Ajoute une nouvelle configuration pour le bot sélectionné"""
        bot_id = self.config_bot_combo.currentData()
        if not bot_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        # Demander le nom de la configuration
        name, ok = QInputDialog.getText(self, "Nouvelle configuration", "Nom de la configuration:")
        if not ok or not name.strip():
            return
            
        # Vérifier si le nom existe déjà
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT 1 FROM configs WHERE bot_id=? AND name=?", (bot_id, name))
            if c.fetchone():
                QMessageBox.warning(self, "Erreur", "Une configuration avec ce nom existe déjà pour ce bot")
                return
                
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to check config name: {str(e)}", "ERROR")
            return
            
        # Sélectionner le fichier de configuration
        path, _ = QFileDialog.getOpenFileName(self, "Sélectionner le fichier de configuration", 
                                            "", "Fichiers JSON (*.json);;Tous les fichiers (*.*)")
        if not path:
            return
            
        # Copier le fichier dans le répertoire de configurations
        configs_dir = os.path.join(self.config_dir, str(bot_id))
        os.makedirs(configs_dir, exist_ok=True)
        
        dest_path = os.path.join(configs_dir, f"{name}.json")
        try:
            shutil.copy2(path, dest_path)
            
            # Enregistrer dans la base de données
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''INSERT INTO configs 
                        (bot_id, name, path, last_used)
                        VALUES (?, ?, ?, ?)''',
                     (bot_id, name, dest_path, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Succès", "Configuration ajoutée avec succès!")
            self.update_config_list()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'ajout de la configuration: {str(e)}")

    def edit_config(self):
        """Ouvre la configuration sélectionnée pour édition"""
        selected = self.config_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration")
            return
            
        config_id = selected[0].data(0, Qt.UserRole)
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT path FROM configs WHERE id=?", (config_id,))
            path = c.fetchone()[0]
            
            # Ouvrir avec l'éditeur par défaut
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
                
            # Mettre à jour la date d'utilisation
            c.execute("UPDATE configs SET last_used=? WHERE id=?", 
                     (datetime.now().isoformat(), config_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")

    def duplicate_config(self):
        """Duplique la configuration sélectionnée"""
        selected = self.config_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration")
            return
            
        config_id = selected[0].data(0, Qt.UserRole)
        old_name = selected[0].text(0)
        
        # Demander le nouveau nom
        new_name, ok = QInputDialog.getText(self, "Dupliquer la configuration", 
                                          "Nouveau nom:", text=f"{old_name}_copy")
        if not ok or not new_name.strip():
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Récupérer les infos de la config originale
            c.execute("SELECT bot_id, path FROM configs WHERE id=?", (config_id,))
            bot_id, old_path = c.fetchone()
            
            # Vérifier si le nom existe déjà
            c.execute("SELECT 1 FROM configs WHERE bot_id=? AND name=?", (bot_id, new_name))
            if c.fetchone():
                QMessageBox.warning(self, "Erreur", "Une configuration avec ce nom existe déjà pour ce bot")
                return
            
            # Créer le nouveau chemin
            configs_dir = os.path.join(self.config_dir, str(bot_id))
            new_path = os.path.join(configs_dir, f"{new_name}.json")
            
            # Copier le fichier
            shutil.copy2(old_path, new_path)
            
            # Enregistrer dans la base de données
            c.execute('''INSERT INTO configs 
                        (bot_id, name, path, last_used)
                        VALUES (?, ?, ?, ?)''',
                     (bot_id, new_name, new_path, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Succès", "Configuration dupliquée avec succès!")
            self.update_config_list()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la duplication: {str(e)}")

    def remove_config(self):
        """Supprime la configuration sélectionnée"""
        selected = self.config_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une configuration")
            return
            
        config_id = selected[0].data(0, Qt.UserRole)
        config_name = selected[0].text(0)
        
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment supprimer la configuration '{config_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Récupérer le chemin pour supprimer le fichier
                c.execute("SELECT path FROM configs WHERE id=?", (config_id,))
                path = c.fetchone()[0]
                
                # Supprimer de la base de données
                c.execute("DELETE FROM configs WHERE id=?", (config_id,))
                
                conn.commit()
                conn.close()
                
                # Supprimer le fichier
                try:
                    os.remove(path)
                except Exception as e:
                    self.log_message(f"Failed to remove config file: {str(e)}", "WARNING")
                
                QMessageBox.information(self, "Succès", "Configuration supprimée avec succès!")
                self.update_config_list()
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la suppression: {str(e)}")

    def start_selected_bot(self):
        """Démarre le bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        bot_id = int(selected[0].text(0))
        bot_name = selected[0].text(1)
        
        # Vérifier si le bot est déjà en cours d'exécution
        if bot_id in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Ce bot est déjà en cours d'exécution")
            return
            
        # Demander la configuration à utiliser
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name FROM configs WHERE bot_id=? ORDER BY last_used DESC LIMIT 5", (bot_id,))
            configs = c.fetchall()
            
            if not configs:
                QMessageBox.warning(self, "Erreur", "Aucune configuration disponible pour ce bot")
                return
                
            config_names = [f"{c[1]} (ID: {c[0]})" for c in configs]
            config_name, ok = QInputDialog.getItem(self, "Configuration", 
                                                  "Sélectionnez une configuration:", 
                                                  config_names, 0, False)
            
            if not ok:
                return
                
            config_id = configs[config_names.index(config_name)][0]
            
            # Récupérer les infos du bot
            c.execute("SELECT type, path, venv_path FROM bots WHERE id=?", (bot_id,))
            bot_type, bot_path, venv_path = c.fetchone()
            
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de démarrer le bot: {str(e)}")
            return
            
        # Construire la commande
        if bot_type == "freqtrade":
            cmd = self.build_freqtrade_command(bot_path, venv_path, config_id)
        else:  # freqai
            cmd = self.build_freqai_command(bot_path, venv_path, config_id)
        
        if not cmd:
            return
            
        # Démarrer le bot
        try:
            # Mettre à jour le statut dans la base de données
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("UPDATE bots SET status=?, last_used=? WHERE id=?", 
                     ("running", datetime.now().isoformat(), bot_id))
            
            conn.commit()
            conn.close()
            
            # Journaliser l'exécution
            exec_id = self.log_execution(bot_id, cmd, "started", config_id)
            
            # Créer le worker
            env = None
            if venv_path:
                env = os.environ.copy()
                if platform.system() == "Windows":
                    env["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + env["PATH"]
                else:
                    env["PATH"] = os.path.join(venv_path, "bin") + os.pathsep + env["PATH"]
            
            worker = CommandWorker(cmd, cwd=bot_path, env=env)
            worker.output_signal.connect(lambda text, color: self.handle_bot_output(bot_id, text, color))
            worker.finished_signal.connect(lambda success: self.bot_finished(bot_id, success))
            
            # Stocker le worker
            self.active_bots[bot_id] = {
                "worker": worker,
                "exec_id": exec_id,
                "name": bot_name
            }
            
            # Démarrer
            worker.start()
            
            # Mettre à jour l'interface
            self.update_bots_list()
            self.update_execution_buttons()
            
            QMessageBox.information(self, "Succès", f"Le bot {bot_name} a été démarré!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec du démarrage: {str(e)}")
            
            # Remettre le statut à "installed" en cas d'erreur
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                c.execute("UPDATE bots SET status=? WHERE id=?", 
                         ("installed", bot_id))
                
                conn.commit()
                conn.close()
            except Exception as e:
                self.log_message(f"Failed to reset bot status: {str(e)}", "ERROR")

    def build_freqtrade_command(self, bot_path, venv_path, config_id):
        """Construit la commande pour démarrer Freqtrade"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Récupérer le chemin de la configuration
            c.execute("SELECT path FROM configs WHERE id=?", (config_id,))
            config_path = c.fetchone()[0]
            
            # Demander le mode d'exécution
            mode, ok = QInputDialog.getItem(self, "Mode d'exécution", 
                                          "Sélectionnez un mode:", 
                                          ["trade", "backtest", "hyperopt", "plot", "edge", "download-data"], 
                                          0, False)
            if not ok:
                return None
                
            # Construire la commande de base
            cmd = f"freqtrade {mode} --config {config_path}"
            
            # Ajouter des options selon le mode
            if mode == "trade":
                strategy, ok = QInputDialog.getText(self, "Stratégie", 
                                                  "Nom de la stratégie:", 
                                                  text="SampleStrategy")
                if ok and strategy:
                    cmd += f" --strategy {strategy}"
                
                dry_run = QMessageBox.question(self, "Mode Dry Run", 
                                            "Voulez-vous exécuter en mode Dry Run?",
                                            QMessageBox.Yes | QMessageBox.No)
                if dry_run == QMessageBox.Yes:
                    cmd += " --dry-run"
            
            elif mode == "backtest":
                strategy, ok = QInputDialog.getText(self, "Stratégie", 
                                                  "Nom de la stratégie:", 
                                                  text="SampleStrategy")
                if ok and strategy:
                    cmd += f" --strategy {strategy}"
                
                timerange, ok = QInputDialog.getText(self, "Plage de temps", 
                                                   "Plage de temps (YYYYMMDD-YYYYMMDD):")
                if ok and timerange:
                    cmd += f" --timerange {timerange}"
            
            conn.close()
            return cmd
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de construire la commande: {str(e)}")
            return None

    def build_freqai_command(self, bot_path, venv_path, config_id):
        """Construit la commande pour démarrer FreqAI"""
        # Pour FreqAI, la commande est similaire à Freqtrade pour l'instant
        return self.build_freqtrade_command(bot_path, venv_path, config_id)

    def handle_bot_output(self, bot_id, text, color):
        """Affiche la sortie du bot"""
        cursor = self.exec_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if color == "red":
            self.exec_output.appendHtml(f"<font color='{color}'>[Bot {bot_id}] {text}</font>")
        else:
            self.exec_output.appendPlainText(f"[Bot {bot_id}] {text}")
        
        # Faire défiler vers le bas
        self.exec_output.ensureCursorVisible()

    def bot_finished(self, bot_id, success):
        """Appelé lorsqu'un bot s'arrête"""
        if bot_id not in self.active_bots:
            return
            
        # Journaliser la fin de l'exécution
        exec_id = self.active_bots[bot_id]["exec_id"]
        bot_name = self.active_bots[bot_id]["name"]
        
        status = "completed" if success else "failed"
        self.log_execution(bot_id, "", status, exec_id=exec_id)
        
        # Mettre à jour le statut dans la base de données
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("UPDATE bots SET status=? WHERE id=?", 
                     ("installed", bot_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update bot status: {str(e)}", "ERROR")
        
        # Supprimer le worker
        self.active_bots.pop(bot_id, None)
        
        # Mettre à jour l'interface
        self.update_bots_list()
        self.update_execution_buttons()
        
        # Afficher un message
        status_msg = "terminé avec succès" if success else "échoué"
        self.append_exec_output(f"<font color={'green' if success else 'red'}>[Bot {bot_id}] {bot_name} {status_msg}</font>")
        
        # Afficher une notification si activé
        if self.get_setting("notifications", "1") == "1":
            self.tray_icon.showMessage("Bot terminé", 
                                     f"Le bot {bot_name} a {status_msg}",
                                     QSystemTrayIcon.Information, 3000)

    def append_exec_output(self, text):
        """Ajoute du texte à la sortie d'exécution avec mise en forme"""
        cursor = self.exec_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if "<font color=" in text:
            self.exec_output.appendHtml(text)
        else:
            self.exec_output.appendPlainText(text)
        
        # Faire défiler vers le bas
        self.exec_output.ensureCursorVisible()

    def stop_selected_bot(self):
        """Arrête le bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        bot_id = int(selected[0].text(0))
        bot_name = selected[0].text(1)
        
        if bot_id not in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Ce bot n'est pas en cours d'exécution")
            return
            
        # Confirmation
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment arrêter le bot '{bot_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Arrêter le worker
                self.active_bots[bot_id]["worker"].stop()
                
                # Le reste sera géré par bot_finished
                self.append_exec_output(f"<font color='orange'>[Bot {bot_id}] Arrêt demandé...</font>")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de l'arrêt: {str(e)}")

    def restart_selected_bot(self):
        """Redémarre le bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        bot_id = int(selected[0].text(0))
        bot_name = selected[0].text(1)
        
        if bot_id not in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Ce bot n'est pas en cours d'exécution")
            return
            
        # Confirmation
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment redémarrer le bot '{bot_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Arrêter le worker
                self.active_bots[bot_id]["worker"].stop()
                
                # Redémarrer après un court délai
                QTimer.singleShot(2000, lambda: self.start_selected_bot())
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec du redémarrage: {str(e)}")

    def remove_selected_bot(self):
        """Supprime le bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        bot_id = int(selected[0].text(0))
        bot_name = selected[0].text(1)
        
        # Vérifier si le bot est en cours d'exécution
        if bot_id in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord arrêter le bot avant de le supprimer")
            return
            
        # Confirmation
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment supprimer le bot '{bot_name}'?\n"
                                   "Cette action supprimera également toutes ses configurations.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Récupérer le chemin pour supprimer le répertoire
                c.execute("SELECT path FROM bots WHERE id=?", (bot_id,))
                bot_path = c.fetchone()[0]
                
                # Supprimer les configurations associées
                c.execute("SELECT path FROM configs WHERE bot_id=?", (bot_id,))
                config_paths = [row[0] for row in c.fetchall()]
                
                # Supprimer de la base de données
                c.execute("DELETE FROM configs WHERE bot_id=?", (bot_id,))
                c.execute("DELETE FROM bots WHERE id=?", (bot_id,))
                
                conn.commit()
                conn.close()
                
                # Supprimer les fichiers
                try:
                    for path in config_paths:
                        os.remove(path)
                    
                    # Supprimer le répertoire du bot (s'il est vide)
                    try:
                        os.rmdir(bot_path)
                    except OSError:
                        # Le répertoire n'est pas vide, on ne le supprime pas
                        self.log_message(f"Le répertoire {bot_path} n'est pas vide, il n'a pas été supprimé", "INFO")
                except Exception as e:
                    self.log_message(f"Failed to remove files: {str(e)}", "WARNING")
                
                QMessageBox.information(self, "Succès", "Bot supprimé avec succès!")
                self.update_ui_state()
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la suppression: {str(e)}")

    def update_selected_bot(self):
        """Met à jour le bot sélectionné"""
        selected = self.bots_tree.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot")
            return
            
        bot_id = int(selected[0].text(0))
        bot_name = selected[0].text(1)
        
        # Vérifier si le bot est en cours d'exécution
        if bot_id in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord arrêter le bot avant de le mettre à jour")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Récupérer les infos du bot
            c.execute("SELECT path, venv_path, version FROM bots WHERE id=?", (bot_id,))
            bot_path, venv_path, current_version = c.fetchone()
            
            # Demander la version cible
            versions = ["stable", "develop", "master"]
            version, ok = QInputDialog.getItem(self, "Mise à jour", 
                                             "Version cible:", 
                                             versions, versions.index(current_version) if current_version in versions else 0, False)
            if not ok:
                return
            
            # Construire les commandes de mise à jour
            commands = []
            commands.append(f"@echo Mise à jour du bot {bot_name} vers {version}")
            commands.append(f"cd \"{bot_path}\" && git fetch --all")
            commands.append(f"cd \"{bot_path}\" && git checkout {version}")
            commands.append(f"cd \"{bot_path}\" && git pull")
            
            # Mise à jour des dépendances
            if venv_path:
                pip_cmd = os.path.join(venv_path, "Scripts", "pip") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "pip")
                commands.append(f"@echo Mise à jour des dépendances")
                commands.append(f"cd \"{bot_path}\" && {pip_cmd} install --upgrade pip")
                commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -e .")
                commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-common.txt")
                commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-ft.txt")
                commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-plot.txt")
            else:
                commands.append(f"@echo Mise à jour des dépendances")
                commands.append(f"cd \"{bot_path}\" && python -m pip install --upgrade pip")
                commands.append(f"cd \"{bot_path}\" && python -m pip install -e .")
                commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-common.txt")
                commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-ft.txt")
                commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-plot.txt")
            
            # Configurer l'interface pour l'affichage
            self.current_operation = "update"
            self.install_output.clear()
            self.progress.setMaximum(len(commands))
            self.progress.setValue(0)
            
            # Stocker les informations pour la mise à jour
            self.updating_bot = {
                "id": bot_id,
                "name": bot_name,
                "version": version,
                "commands": commands
            }
            
            # Exécuter les commandes
            self.current_command = 0
            self.execute_next_update_command()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de préparer la mise à jour: {str(e)}")

    def execute_next_update_command(self):
        """Exécute la prochaine commande de mise à jour"""
        if self.current_command >= len(self.updating_bot["commands"]):
            self.update_completed()
            return
            
        cmd = self.updating_bot["commands"][self.current_command]
        
        # Gestion spéciale des commandes echo
        if cmd.startswith("@echo "):
            self.append_install_output(f"<font color='blue'>{cmd[6:]}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_update_command)
            return
            
        self.append_install_output(f"> {cmd}")
        
        try:
            # Créer un worker pour exécuter la commande
            self.current_worker = CommandWorker(cmd)
            self.current_worker.output_signal.connect(self.handle_install_output)
            self.current_worker.finished_signal.connect(self.update_command_finished)
            self.current_worker.start()
        except Exception as e:
            self.append_install_output(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_update_command)

    def update_command_finished(self, success):
        """Appelé lorsqu'une commande de mise à jour est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if not success and self.current_command < len(self.updating_bot["commands"]):
            self.append_install_output("<font color='orange'>La commande a échoué mais nous continuons...</font>")
        
        if self.current_command < len(self.updating_bot["commands"]):
            QTimer.singleShot(100, self.execute_next_update_command)
        else:
            self.update_completed()

    def update_completed(self):
        """Finalise la mise à jour"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Mettre à jour la version dans la base de données
            c.execute("UPDATE bots SET version=?, last_used=? WHERE id=?", 
                     (self.updating_bot["version"], datetime.now().isoformat(), self.updating_bot["id"]))
            
            conn.commit()
            conn.close()
            
            self.append_install_output(f"<font color='green'>Mise à jour de {self.updating_bot['name']} terminée avec succès!</font>")
            QMessageBox.information(self, "Succès", f"Le bot {self.updating_bot['name']} a été mis à jour vers {self.updating_bot['version']}!")
            
            # Mettre à jour l'interface
            self.update_bots_list()
            
        except Exception as e:
            self.append_install_output(f"<font color='red'>ERREUR: Échec de l'enregistrement dans la base de données: {str(e)}</font>")
            QMessageBox.critical(self, "Erreur", "Le bot a été mis à jour mais la base de données n'a pas pu être mise à jour.")
        
        finally:
            self.current_operation = None
            self.updating_bot = None

    def update_all_bots(self, check_only=False):
        """Met à jour tous les bots"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT id, name, path, venv_path, version FROM bots")
            bots = c.fetchall()
            
            if not bots:
                QMessageBox.information(self, "Information", "Aucun bot à mettre à jour")
                return
                
            if check_only:
                update_available = False
                for bot in bots:
                    bot_id, bot_name, bot_path, venv_path, version = bot
                    
                    # Vérifier les mises à jour
                    try:
                        process = subprocess.Popen(["git", "fetch"], cwd=bot_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        process.wait()
                        
                        process = subprocess.Popen(["git", "status", "-uno"], cwd=bot_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        out, _ = process.communicate()
                        
                        if "Your branch is behind" in out:
                            update_available = True
                            self.log_message(f"Mise à jour disponible pour {bot_name}", "INFO")
                    except Exception as e:
                        self.log_message(f"Impossible de vérifier les mises à jour pour {bot_name}: {str(e)}", "ERROR")
                
                if update_available:
                    QMessageBox.information(self, "Mises à jour disponibles", 
                                          "Des mises à jour sont disponibles pour un ou plusieurs bots.")
                else:
                    QMessageBox.information(self, "À jour", 
                                          "Tous les bots sont à jour.")
                return
                
            # Demander confirmation
            reply = QMessageBox.question(self, "Confirmation", 
                                       f"Voulez-vous vraiment mettre à jour tous les bots ({len(bots)})?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply != QMessageBox.Yes:
                return
                
            # Configurer l'interface pour l'affichage
            self.current_operation = "update_all"
            self.install_output.clear()
            
            # Stocker les informations pour la mise à jour
            self.updating_bots = {
                "bots": bots,
                "current_bot": 0,
                "commands": []
            }
            
            # Commencer avec le premier bot
            self.prepare_next_bot_update()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de préparer la mise à jour: {str(e)}")

    def prepare_next_bot_update(self):
        """Prépare la mise à jour du bot suivant"""
        if self.updating_bots["current_bot"] >= len(self.updating_bots["bots"]):
            self.update_all_completed()
            return
            
        bot_id, bot_name, bot_path, venv_path, version = self.updating_bots["bots"][self.updating_bots["current_bot"]]
        
        # Construire les commandes de mise à jour
        commands = []
        commands.append(f"@echo Mise à jour du bot {bot_name}")
        commands.append(f"cd \"{bot_path}\" && git fetch --all")
        commands.append(f"cd \"{bot_path}\" && git pull")
        
        # Mise à jour des dépendances
        if venv_path:
            pip_cmd = os.path.join(venv_path, "Scripts", "pip") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "pip")
            commands.append(f"@echo Mise à jour des dépendances")
            commands.append(f"cd \"{bot_path}\" && {pip_cmd} install --upgrade pip")
            commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -e .")
            commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-common.txt")
            commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-ft.txt")
            commands.append(f"cd \"{bot_path}\" && {pip_cmd} install -r requirements-plot.txt")
        else:
            commands.append(f"@echo Mise à jour des dépendances")
            commands.append(f"cd \"{bot_path}\" && python -m pip install --upgrade pip")
            commands.append(f"cd \"{bot_path}\" && python -m pip install -e .")
            commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-common.txt")
            commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-ft.txt")
            commands.append(f"cd \"{bot_path}\" && python -m pip install -r requirements-plot.txt")
        
        self.updating_bots["commands"] = commands
        self.progress.setMaximum(len(commands))
        self.progress.setValue(0)
        
        # Exécuter les commandes
        self.current_command = 0
        self.execute_next_update_all_command()

    def execute_next_update_all_command(self):
        """Exécute la prochaine commande de mise à jour globale"""
        if self.current_command >= len(self.updating_bots["commands"]):
            # Passer au bot suivant
            self.updating_bots["current_bot"] += 1
            self.prepare_next_bot_update()
            return
            
        cmd = self.updating_bots["commands"][self.current_command]
        
        # Gestion spéciale des commandes echo
        if cmd.startswith("@echo "):
            self.append_install_output(f"<font color='blue'>{cmd[6:]}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_update_all_command)
            return
            
        self.append_install_output(f"> {cmd}")
        
        try:
            # Créer un worker pour exécuter la commande
            self.current_worker = CommandWorker(cmd)
            self.current_worker.output_signal.connect(self.handle_install_output)
            self.current_worker.finished_signal.connect(self.update_all_command_finished)
            self.current_worker.start()
        except Exception as e:
            self.append_install_output(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_update_all_command)

    def update_all_command_finished(self, success):
        """Appelé lorsqu'une commande de mise à jour globale est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if not success and self.current_command < len(self.updating_bots["commands"]):
            self.append_install_output("<font color='orange'>La commande a échoué mais nous continuons...</font>")
        
        if self.current_command < len(self.updating_bots["commands"]):
            QTimer.singleShot(100, self.execute_next_update_all_command)
        else:
            # Passer au bot suivant
            self.updating_bots["current_bot"] += 1
            self.prepare_next_bot_update()

    def update_all_completed(self):
        """Finalise la mise à jour de tous les bots"""
        self.append_install_output("<font color='green'>Mise à jour de tous les bots terminée!</font>")
        QMessageBox.information(self, "Succès", "Tous les bots ont été mis à jour!")
        
        # Mettre à jour l'interface
        self.update_bots_list()
        self.current_operation = None
        self.updating_bots = None

    def start_execution(self):
        """Démarre une exécution depuis l'onglet Exécution"""
        bot_id = self.exec_bot_combo.currentData()
        config_id = self.exec_config_combo.currentData()
        mode = self.mode_combo.currentText().lower()
        
        if not bot_id or not config_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un bot et une configuration")
            return
            
        # Vérifier si le bot est déjà en cours d'exécution
        if bot_id in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Ce bot est déjà en cours d'exécution")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Récupérer les infos du bot
            c.execute("SELECT name, type, path, venv_path FROM bots WHERE id=?", (bot_id,))
            bot_name, bot_type, bot_path, venv_path = c.fetchone()
            
            # Récupérer le chemin de la configuration
            c.execute("SELECT path FROM configs WHERE id=?", (config_id,))
            config_path = c.fetchone()[0]
            
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de démarrer l'exécution: {str(e)}")
            return
            
        # Construire la commande
        if bot_type == "freqtrade":
            cmd = self.build_freqtrade_exec_command(bot_path, config_path, mode)
        else:  # freqai
            cmd = self.build_freqai_exec_command(bot_path, config_path, mode)
        
        if not cmd:
            return
            
        # Démarrer l'exécution
        try:
            # Mettre à jour le statut dans la base de données
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("UPDATE bots SET status=?, last_used=? WHERE id=?", 
                     ("running", datetime.now().isoformat(), bot_id))
            
            # Mettre à jour la configuration
            c.execute("UPDATE configs SET last_used=? WHERE id=?", 
                     (datetime.now().isoformat(), config_id))
            
            conn.commit()
            conn.close()
            
            # Journaliser l'exécution
            exec_id = self.log_execution(bot_id, cmd, "started", config_id)
            
            # Créer le worker
            env = None
            if venv_path:
                env = os.environ.copy()
                if platform.system() == "Windows":
                    env["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + env["PATH"]
                else:
                    env["PATH"] = os.path.join(venv_path, "bin") + os.pathsep + env["PATH"]
            
            worker = CommandWorker(cmd, cwd=bot_path, env=env)
            worker.output_signal.connect(lambda text, color: self.handle_exec_output(text, color))
            worker.finished_signal.connect(lambda success: self.execution_finished(bot_id, success))
            
            # Stocker le worker
            self.active_bots[bot_id] = {
                "worker": worker,
                "exec_id": exec_id,
                "name": bot_name
            }
            
            # Démarrer
            worker.start()
            
            # Mettre à jour l'interface
            self.update_bots_list()
            self.update_execution_buttons()
            
            self.exec_output.clear()
            self.append_exec_output(f"<font color='green'>Démarrage de l'exécution pour {bot_name}...</font>")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec du démarrage: {str(e)}")
            
            # Remettre le statut à "installed" en cas d'erreur
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                c.execute("UPDATE bots SET status=? WHERE id=?", 
                         ("installed", bot_id))
                
                conn.commit()
                conn.close()
            except Exception as e:
                self.log_message(f"Failed to reset bot status: {str(e)}", "ERROR")

    def build_freqtrade_exec_command(self, bot_path, config_path, mode):
        """Construit la commande pour exécuter Freqtrade"""
        if mode == "other":
            cmd = self.custom_cmd_input.text().strip()
            if not cmd:
                QMessageBox.warning(self, "Erreur", "Veuillez entrer une commande valide")
                return None
            return cmd
        
        cmd = f"freqtrade {mode} --config {config_path}"
        
        # Ajouter des options selon le mode
        if mode == "trade":
            strategy = self.strategy_input.text()
            if strategy:
                cmd += f" --strategy {strategy}"
            
            if self.db_check.isChecked():
                cmd += " --db-url sqlite:///tradesv3.sqlite"
            
            if self.dry_run_check.isChecked():
                cmd += " --dry-run"
        
        elif mode == "backtest":
            strategy = self.bt_strategy_input.text()
            if strategy:
                cmd += f" --strategy {strategy}"
            
            timerange = self.timerange_input.text()
            if timerange:
                cmd += f" --timerange {timerange}"
        
        return cmd

    def build_freqai_exec_command(self, bot_path, config_path, mode):
        """Construit la commande pour exécuter FreqAI"""
        # Pour FreqAI, la commande est similaire à Freqtrade pour l'instant
        return self.build_freqtrade_exec_command(bot_path, config_path, mode)

    def handle_exec_output(self, text, color):
        """Affiche la sortie de l'exécution"""
        if color == "red":
            self.append_exec_output(f"<font color='{color}'>{text}</font>")
        else:
            self.append_exec_output(text)

    def execution_finished(self, bot_id, success):
        """Appelé lorsqu'une exécution se termine"""
        if bot_id not in self.active_bots:
            return
            
        # Journaliser la fin de l'exécution
        exec_id = self.active_bots[bot_id]["exec_id"]
        bot_name = self.active_bots[bot_id]["name"]
        
        status = "completed" if success else "failed"
        self.log_execution(bot_id, "", status, exec_id=exec_id)
        
        # Mettre à jour le statut dans la base de données
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("UPDATE bots SET status=? WHERE id=?", 
                     ("installed", bot_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_message(f"Failed to update bot status: {str(e)}", "ERROR")
        
        # Supprimer le worker
        self.active_bots.pop(bot_id, None)
        
        # Mettre à jour l'interface
        self.update_bots_list()
        self.update_execution_buttons()
        
        # Afficher un message
        status_msg = "terminée avec succès" if success else "échouée"
        self.append_exec_output(f"<font color={'green' if success else 'red'}>Exécution {status_msg}</font>")
        
        # Afficher une notification si activé
        if self.get_setting("notifications", "1") == "1":
            self.tray_icon.showMessage("Exécution terminée", 
                                     f"L'exécution pour {bot_name} a {status_msg}",
                                     QSystemTrayIcon.Information, 3000)

    def stop_execution(self):
        """Arrête l'exécution en cours depuis l'onglet Exécution"""
        bot_id = self.exec_bot_combo.currentData()
        
        if not bot_id or bot_id not in self.active_bots:
            QMessageBox.warning(self, "Erreur", "Aucune exécution en cours")
            return
            
        bot_name = self.active_bots[bot_id]["name"]
        
        # Confirmation
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment arrêter l'exécution de '{bot_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # Arrêter le worker
                self.active_bots[bot_id]["worker"].stop()
                
                # Le reste sera géré par execution_finished
                self.append_exec_output("<font color='orange'>Arrêt demandé...</font>")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de l'arrêt: {str(e)}")

    def clear_execution_output(self):
        """Efface la sortie de l'exécution"""
        self.exec_output.clear()

    def update_execution_buttons(self):
        """Met à jour l'état des boutons d'exécution"""
        bot_id = self.exec_bot_combo.currentData()
        is_running = bot_id and bot_id in self.active_bots
        
        self.exec_start_btn.setEnabled(not is_running)
        self.exec_stop_btn.setEnabled(is_running)

    def show_install_tab(self):
        """Affiche l'onglet d'installation"""
        self.tabs.setCurrentIndex(1)

    def open_documentation(self):
        """Ouvre la documentation"""
        url = "https://www.freqtrade.io/en/latest/" if self.bot_type_combo.currentText() == "Freqtrade" else "https://www.freqtrade.io/en/latest/freqai/"
        webbrowser.open(url)

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h1>Freqtrade/FreqAI Manager</h1>
        <p>Version 1.1.0</p>
        <p>Un gestionnaire graphique pour Freqtrade et FreqAI, les bots de trading algorithmique open-source.</p>
        <p>Développé avec Python et PyQt5</p>
        <p>© 2023 - Tous droits réservés</p>
        """
        QMessageBox.about(self, "À propos", about_text)

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.active_bots:
            reply = QMessageBox.question(
                self, "Bots en cours",
                "Un ou plusieurs bots sont toujours en cours d'exécution. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
            else:
                # Arrêter tous les bots
                for bot_id in list(self.active_bots.keys()):
                    try:
                        self.active_bots[bot_id]["worker"].stop()
                    except Exception as e:
                        self.log_message(f"Failed to stop bot {bot_id}: {str(e)}", "ERROR")
                
        if self.current_operation:
            reply = QMessageBox.question(
                self, "Opération en cours",
                "Une opération est en cours. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        # Fermer proprement
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
            
        event.accept()

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
    app.setStyle(QStyleFactory.create("Fusion"))
    
    # Vérifier la présence de git et python
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("Git et Python sont requis pour ce programme")
    
    # Créer et afficher la fenêtre principale
    window = BotManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())