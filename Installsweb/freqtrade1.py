


import sys
import os
import subprocess
import platform
import sqlite3
import shutil
import webbrowser
import json
import winreg
import psutil
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QWidget, QLabel, QTextEdit,
                           QMessageBox, QProgressBar, QCheckBox, 
                           QGroupBox, QHBoxLayout, QComboBox, QTabWidget,
                           QFileDialog, QLineEdit, QSystemTrayIcon, QMenu,
                           QAction, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal, QSettings
from PyQt5.QtGui import QIcon, QFont, QTextCursor, QColor
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread
import json
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDateEdit, QDialog
import zipfile
import tempfile
from urllib.request import urlopen
from packaging import version
class OutputReader(QThread):
    """Thread pour lire la sortie d'un processus en temps réel"""
    output_signal = pyqtSignal(str, bool)  # text, is_error
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        
    def run(self):
        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip(), False)
            
            err = self.process.stderr.readline()
            if err:
                self.output_signal.emit(err.strip(), True)
class FreqtradeManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade Manager Pro++")
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(QSize(900, 700))
        
        # Chemins importants
        self.base_dir = self.get_app_data_dir()
        self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
        self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
        self.config_dir = os.path.join(self.base_dir, "user_data")
        self.venv_dir = os.path.join(self.base_dir, "venv")
        self.log_dir = os.path.join(self.base_dir, "logs")
        
        # Variables d'état
        self.installation_in_progress = False
        self.freqtrade_running = False
        self.current_worker = None
        self.current_process = None
        self.telegram_bot_enabled = False
        
        # Configuration des chemins système
        self.add_to_path()
        
        # Initialisation des composants
        self.init_db()
        self.check_dependencies()
        self.init_ui()
        self.init_tray_icon()
        self.init_menu_bar()
        self.set_style()
        self.update_ui_state()
        
        # Charger les paramètres
        self.load_settings()

    def get_app_data_dir(self):
        """Retourne le répertoire de données de l'application"""
        appdata = os.getenv('APPDATA')
        base_dir = os.path.join(appdata, "FreqtradeManagerPro")
        
        if not os.path.exists(base_dir):
            try:
                os.makedirs(base_dir)
                # Ajouter des permissions pour éviter les problèmes
                os.chmod(base_dir, 0o755)
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible de créer le répertoire: {str(e)}")
                return os.path.expanduser("~")
        
        return base_dir

    def add_to_path(self):
        """Ajoute les répertoires importants au PATH si nécessaire"""
        paths_to_add = [
            self.venv_dir,
            os.path.join(self.venv_dir, "Scripts"),
            self.freqtrade_dir
        ]
        
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
                path_value, _ = winreg.QueryValueEx(key, 'Path')
                
                for path in paths_to_add:
                    if path not in path_value:
                        path_value = f"{path};{path_value}"
                
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, path_value)
                
            # Prévenir Windows du changement
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            import ctypes
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment')
            
        except Exception as e:
            print(f"Impossible de mettre à jour le PATH: {str(e)}")

    def init_db(self):
        """Initialise la base de données avec des tables étendues"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Table des installations
            c.execute('''CREATE TABLE IF NOT EXISTS installations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          version TEXT,
                          python_version TEXT,
                          path TEXT,
                          install_date TEXT,
                          status TEXT,
                          details TEXT,
                          execution_time REAL)''')
            
            # Table des exécutions
            c.execute('''CREATE TABLE IF NOT EXISTS executions
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          start_time TEXT,
                          end_time TEXT,
                          command TEXT,
                          mode TEXT,
                          strategy TEXT,
                          status TEXT,
                          output TEXT,
                          profit REAL,
                          duration REAL)''')
            
            # Table des configurations
            c.execute('''CREATE TABLE IF NOT EXISTS configurations
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          path TEXT,
                          last_used TEXT,
                          strategy TEXT,
                          exchange TEXT,
                          pairlist TEXT)''')
            
            # Table des stratégies
            c.execute('''CREATE TABLE IF NOT EXISTS strategies
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE,
                          path TEXT,
                          last_modified TEXT,
                          performance REAL)''')
            
            # Table des paramètres
            c.execute('''CREATE TABLE IF NOT EXISTS settings
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          key TEXT UNIQUE,
                          value TEXT)''')
            
            conn.commit()
            conn.close()
            
            # Créer le répertoire user_data s'il n'existe pas
            os.makedirs(os.path.join(self.config_dir, "configs"), exist_ok=True)
            os.makedirs(os.path.join(self.config_dir, "strategies"), exist_ok=True)
            
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

    def check_dependencies(self):
        """Vérifie les dépendances requises avec des vérifications plus robustes"""
        self.git_installed = self.check_command_available(["git", "--version"])
        self.python_installed = self.check_python_installation()
        self.docker_installed = False  # On désactive Docker par défaut pour Windows
        self.freqtrade_installed = self.check_freqtrade_installation()
        self.venv_created = os.path.exists(self.venv_dir)
        
    def check_python_installation(self):
        """Vérifie l'installation de Python et sa version"""
        try:
            result = subprocess.run(["python", "--version"], 
                                   capture_output=True, 
                                   text=True,
                                   check=True)
            version = result.stdout.strip()
            self.python_version = version.split()[1]
            
            # Vérifier que c'est Python 3.8+
            major, minor = map(int, self.python_version.split('.')[:2])
            return major == 3 and minor >= 8
            
        except:
            try:
                result = subprocess.run(["python3", "--version"], 
                                      capture_output=True, 
                                      text=True,
                                      check=True)
                version = result.stdout.strip()
                self.python_version = version.split()[1]
                
                major, minor = map(int, self.python_version.split('.')[:2])
                return major == 3 and minor >= 8
                
            except:
                return False

    def check_command_available(self, command):
        """Vérifie si une commande système est disponible"""
        try:
            subprocess.run(command, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         timeout=10,
                         check=True)
            return True
        except:
            return False
            
    def check_freqtrade_installation(self):
        """Vérifie si Freqtrade est installé et fonctionnel"""
        if not os.path.exists(self.freqtrade_dir):
            return False
            
        try:
            # Activer l'environnement virtuel si nécessaire
            python_exec = os.path.join(self.venv_dir, "Scripts", "python.exe") if self.venv_created else "python"
            
            result = subprocess.run([python_exec, "-m", "freqtrade", "--version"], 
                                  cwd=self.freqtrade_dir,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=30)
            return result.returncode == 0
        except:
            return False

    def init_ui(self):
        """Initialise l'interface utilisateur avec des onglets supplémentaires"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Création des onglets
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Onglets
        self.setup_install_tab()
        self.setup_config_tab()
        self.setup_strategy_tab()
        self.setup_execution_tab()
        self.setup_telegram_tab()
        self.setup_performance_tab()
        self.setup_history_tab()
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")

    def setup_install_tab(self):
        """Configure l'onglet d'installation avec plus d'options"""
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
        self.python_status = QLabel(f"Python: {'Installé' if self.python_installed else 'Manquant'} ({getattr(self, 'python_version', 'N/A')})")
        self.freqtrade_status = QLabel(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        self.venv_status = QLabel(f"Environnement virtuel: {'Créé' if self.venv_created else 'Manquant'}")
        
        deps_layout.addWidget(self.git_status)
        deps_layout.addWidget(self.python_status)
        deps_layout.addWidget(self.freqtrade_status)
        deps_layout.addWidget(self.venv_status)
        
        deps_group.setLayout(deps_layout)
        layout.addWidget(deps_group)
        
        # Options d'installation
        options_group = QGroupBox("Options d'installation avancées")
        options_layout = QVBoxLayout()
        
        # Version à installer
        version_layout = QHBoxLayout()
        version_label = QLabel("Version Freqtrade:")
        self.version_combo = QComboBox()
        self.version_combo.addItems(["stable", "develop", "feat/short", "custom"])
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_combo)
        options_layout.addLayout(version_layout)
        
        # Version Python
        python_version_layout = QHBoxLayout()
        python_label = QLabel("Version Python:")
        self.python_combo = QComboBox()
        self.python_combo.addItems(["3.8", "3.9", "3.10", "3.11"])
        self.python_combo.setCurrentText(self.python_version.split('.')[1] if hasattr(self, 'python_version') else "3.10")
        python_version_layout.addWidget(python_label)
        python_version_layout.addWidget(self.python_combo)
        options_layout.addLayout(python_version_layout)
        
        # Options
        self.venv_check = QCheckBox("Créer un environnement virtuel Python")
        self.venv_check.setChecked(True)
        options_layout.addWidget(self.venv_check)
        
        self.plot_check = QCheckBox("Installer les dépendances de visualisation")
        self.plot_check.setChecked(True)
        options_layout.addWidget(self.plot_check)
        
        self.ta_check = QCheckBox("Installer les dépendances d'analyse technique")
        self.ta_check.setChecked(True)
        options_layout.addWidget(self.ta_check)
        
        self.optimize_check = QCheckBox("Optimiser l'installation pour Windows")
        self.optimize_check.setChecked(True)
        options_layout.addWidget(self.optimize_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        self.install_btn = QPushButton("Installer Freqtrade" if not self.freqtrade_installed else "Mettre à jour Freqtrade")
        self.install_btn.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.install_btn.clicked.connect(self.start_installation)
        btn_layout.addWidget(self.install_btn)
        
        self.repair_btn = QPushButton("Réparer")
        self.repair_btn.setStyleSheet("background-color: #f39c12; color: white;")
        self.repair_btn.clicked.connect(self.repair_installation)
        btn_layout.addWidget(self.repair_btn)
        
        self.clean_btn = QPushButton("Nettoyer")
        self.clean_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        self.clean_btn.clicked.connect(self.clean_installation)
        btn_layout.addWidget(self.clean_btn)
        
        layout.addLayout(btn_layout)
        
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
        """Configure l'onglet de configuration avec plus de fonctionnalités"""
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
        self.use_config_btn = QPushButton("Utiliser")
        self.use_config_btn.clicked.connect(self.use_selected_config)
        btn_layout.addWidget(self.use_config_btn)
        
        self.edit_config_btn = QPushButton("Éditer")
        self.edit_config_btn.clicked.connect(self.edit_selected_config)
        btn_layout.addWidget(self.edit_config_btn)
        
        self.delete_config_btn = QPushButton("Supprimer")
        self.delete_config_btn.clicked.connect(self.delete_selected_config)
        btn_layout.addWidget(self.delete_config_btn)
        
        config_layout.addLayout(btn_layout)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Nouvelle configuration
        new_config_group = QGroupBox("Nouvelle configuration")
        new_config_layout = QVBoxLayout()
        
        # Nom de la configuration
        name_layout = QHBoxLayout()
        name_label = QLabel("Nom:")
        self.new_config_name = QLineEdit()
        self.new_config_name.setPlaceholderText("Nom unique pour cette configuration")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.new_config_name)
        new_config_layout.addLayout(name_layout)
        
        # Fichier de configuration
        file_layout = QHBoxLayout()
        self.config_path_input = QLineEdit()
        self.config_path_input.setPlaceholderText("Chemin du fichier de configuration")
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_config_file)
        file_layout.addWidget(self.config_path_input)
        file_layout.addWidget(browse_btn)
        new_config_layout.addLayout(file_layout)
        
        # Options rapides
        quick_settings = QGroupBox("Options rapides")
        quick_layout = QHBoxLayout()
        
        # Exchange
        exchange_label = QLabel("Exchange:")
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(["binance", "kraken", "ftx", "coinbasepro"])
        quick_layout.addWidget(exchange_label)
        quick_layout.addWidget(self.exchange_combo)
        
        # Paires
        pair_label = QLabel("Paires:")
        self.pair_input = QLineEdit()
        self.pair_input.setPlaceholderText("BTC/USDT,ETH/USDT")
        quick_layout.addWidget(pair_label)
        quick_layout.addWidget(self.pair_input)
        
        quick_settings.setLayout(quick_layout)
        new_config_layout.addWidget(quick_settings)
        
        # Bouton de création
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

    def setup_strategy_tab(self):
        """Configure l'onglet de gestion des stratégies"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Gestion des Stratégies</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Stratégies existantes
        strategy_group = QGroupBox("Stratégies disponibles")
        strategy_layout = QVBoxLayout()
        
        self.strategy_combo = QComboBox()
        self.load_strategies()
        strategy_layout.addWidget(self.strategy_combo)
        
        btn_layout = QHBoxLayout()
        self.edit_strategy_btn = QPushButton("Éditer")
        self.edit_strategy_btn.clicked.connect(self.edit_selected_strategy)
        btn_layout.addWidget(self.edit_strategy_btn)
        
        self.test_strategy_btn = QPushButton("Tester")
        self.test_strategy_btn.clicked.connect(self.test_selected_strategy)
        btn_layout.addWidget(self.test_strategy_btn)
        
        self.delete_strategy_btn = QPushButton("Supprimer")
        self.delete_strategy_btn.clicked.connect(self.delete_selected_strategy)
        btn_layout.addWidget(self.delete_strategy_btn)
        
        strategy_layout.addLayout(btn_layout)
        strategy_group.setLayout(strategy_layout)
        layout.addWidget(strategy_group)
        
        # Nouvelle stratégie
        new_strategy_group = QGroupBox("Nouvelle stratégie")
        new_strategy_layout = QVBoxLayout()
        
        # Nom de la stratégie
        name_layout = QHBoxLayout()
        name_label = QLabel("Nom:")
        self.new_strategy_name = QLineEdit()
        self.new_strategy_name.setPlaceholderText("Nom de la stratégie (sans espaces)")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.new_strategy_name)
        new_strategy_layout.addLayout(name_layout)
        
        # Basée sur
        base_layout = QHBoxLayout()
        base_label = QLabel("Basée sur:")
        self.base_strategy_combo = QComboBox()
        self.base_strategy_combo.addItems(["SampleStrategy", "EMACross", "RSIStrategy", "Blank"])
        base_layout.addWidget(base_label)
        base_layout.addWidget(self.base_strategy_combo)
        new_strategy_layout.addLayout(base_layout)
        
        # Bouton de création
        self.create_strategy_btn = QPushButton("Créer stratégie")
        self.create_strategy_btn.clicked.connect(self.create_new_strategy)
        new_strategy_layout.addWidget(self.create_strategy_btn)
        
        new_strategy_group.setLayout(new_strategy_layout)
        layout.addWidget(new_strategy_group)
        
        # Documentation
        doc_btn = QPushButton("Ouvrir la documentation des stratégies")
        doc_btn.clicked.connect(lambda: webbrowser.open("https://www.freqtrade.io/en/latest/strategy-customization/"))
        layout.addWidget(doc_btn)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Stratégies")

    def setup_execution_tab(self):
        """Configure l'onglet d'exécution avec plus d'options"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Exécution Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Boutons d'exécution
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Démarrer")
        self.start_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.start_btn.clicked.connect(self.start_freqtrade)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Arrêter")
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
        
        # Mode
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
        self.strategy_input = QComboBox()
        self.load_strategies_to_combo(self.strategy_input)
        strategy_layout.addWidget(strategy_label)
        strategy_layout.addWidget(self.strategy_input)
        trade_options_layout.addLayout(strategy_layout)
        
        config_layout = QHBoxLayout()
        config_label = QLabel("Configuration:")
        self.config_input = QComboBox()
        self.load_configurations_to_combo(self.config_input)
        config_layout.addWidget(config_label)
        config_layout.addWidget(self.config_input)
        trade_options_layout.addLayout(config_layout)
        
        self.db_check = QCheckBox("Utiliser la base de données")
        self.db_check.setChecked(True)
        trade_options_layout.addWidget(self.db_check)
        
        self.dry_run_check = QCheckBox("Mode Dry Run")
        self.dry_run_check.setChecked(True)
        trade_options_layout.addWidget(self.dry_run_check)
        
        self.trade_options.setLayout(trade_options_layout)
        self.mode_options_layout.addWidget(self.trade_options)
        
        # Options pour le mode Backtest
        self.backtest_options = QWidget()
        backtest_options_layout = QVBoxLayout(self.backtest_options)
        
        bt_strategy_layout = QHBoxLayout()
        bt_strategy_label = QLabel("Stratégie:")
        self.bt_strategy_input = QComboBox()
        self.load_strategies_to_combo(self.bt_strategy_input)
        bt_strategy_layout.addWidget(bt_strategy_label)
        bt_strategy_layout.addWidget(self.bt_strategy_input)
        backtest_options_layout.addLayout(bt_strategy_layout)
        
        bt_config_layout = QHBoxLayout()
        bt_config_label = QLabel("Configuration:")
        self.bt_config_input = QComboBox()
        self.load_configurations_to_combo(self.bt_config_input)
        bt_config_layout.addWidget(bt_config_label)
        bt_config_layout.addWidget(self.bt_config_input)
        backtest_options_layout.addLayout(bt_config_layout)
        
        timerange_layout = QHBoxLayout()
        timerange_label = QLabel("Plage de temps:")
        self.timerange_input = QLineEdit()
        self.timerange_input.setPlaceholderText("YYYYMMDD-YYYYMMDD")
        timerange_layout.addWidget(timerange_label)
        timerange_layout.addWidget(self.timerange_input)
        backtest_options_layout.addLayout(timerange_layout)
        
        self.bt_download_check = QCheckBox("Télécharger les données si manquantes")
        self.bt_download_check.setChecked(True)
        backtest_options_layout.addWidget(self.bt_download_check)
        
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

    def setup_telegram_tab(self):
        """Configure l'onglet de gestion du bot Telegram"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Configuration Telegram</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Activation
        self.telegram_group = QGroupBox("Bot Telegram")
        telegram_layout = QVBoxLayout()
        
        self.telegram_enable = QCheckBox("Activer le bot Telegram")
        self.telegram_enable.setChecked(False)
        self.telegram_enable.stateChanged.connect(self.toggle_telegram_settings)
        telegram_layout.addWidget(self.telegram_enable)
        
        # Paramètres
        form_layout = QVBoxLayout()
        
        token_layout = QHBoxLayout()
        token_label = QLabel("Token:")
        self.telegram_token = QLineEdit()
        self.telegram_token.setPlaceholderText("123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.telegram_token)
        form_layout.addLayout(token_layout)
        
        chat_id_layout = QHBoxLayout()
        chat_id_label = QLabel("Chat ID:")
        self.telegram_chat_id = QLineEdit()
        self.telegram_chat_id.setPlaceholderText("123456789")
        chat_id_layout.addWidget(chat_id_label)
        chat_id_layout.addWidget(self.telegram_chat_id)
        form_layout.addLayout(chat_id_layout)
        
        telegram_layout.addLayout(form_layout)
        
        # Boutons
        btn_layout = QHBoxLayout()
        self.telegram_test_btn = QPushButton("Tester")
        self.telegram_test_btn.clicked.connect(self.test_telegram)
        btn_layout.addWidget(self.telegram_test_btn)
        
        self.telegram_save_btn = QPushButton("Enregistrer")
        self.telegram_save_btn.clicked.connect(self.save_telegram_settings)
        btn_layout.addWidget(self.telegram_save_btn)
        
        telegram_layout.addLayout(btn_layout)
        
        self.telegram_group.setLayout(telegram_layout)
        layout.addWidget(self.telegram_group)
        
        # Documentation
        doc_btn = QPushButton("Comment obtenir un token Telegram")
        doc_btn.clicked.connect(lambda: webbrowser.open("https://core.telegram.org/bots#6-botfather"))
        layout.addWidget(doc_btn)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Telegram")

    def setup_performance_tab(self):
        """Configure l'onglet de performance et optimisation"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Performance et Optimisation</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Statistiques système
        sys_group = QGroupBox("Ressources système")
        sys_layout = QVBoxLayout()
        
        self.cpu_label = QLabel("CPU: N/A")
        self.mem_label = QLabel("Mémoire: N/A")
        self.disk_label = QLabel("Disque: N/A")
        self.net_label = QLabel("Réseau: N/A")
        
        sys_layout.addWidget(self.cpu_label)
        sys_layout.addWidget(self.mem_label)
        sys_layout.addWidget(self.disk_label)
        sys_layout.addWidget(self.net_label)
        
        self.sys_monitor_btn = QPushButton("Démarrer le monitoring")
        self.sys_monitor_btn.clicked.connect(self.toggle_system_monitor)
        sys_layout.addWidget(self.sys_monitor_btn)
        
        sys_group.setLayout(sys_layout)
        layout.addWidget(sys_group)
        
        # Optimisation
        opti_group = QGroupBox("Optimisation")
        opti_layout = QVBoxLayout()
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Normal", "Haut", "Temps réel"])
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(QLabel("Priorité:"))
        priority_layout.addWidget(self.priority_combo)
        opti_layout.addLayout(priority_layout)
        
        self.set_priority_btn = QPushButton("Appliquer")
        self.set_priority_btn.clicked.connect(self.set_process_priority)
        opti_layout.addWidget(self.set_priority_btn)
        
        opti_group.setLayout(opti_layout)
        layout.addWidget(opti_group)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Performance")

    def setup_history_tab(self):
        """Configure l'onglet d'historique avec plus de détails"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Historique des Exécutions</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Filtres
        filter_layout = QHBoxLayout()
        
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(["Tous", "Installations", "Exécutions", "Stratégies"])
        self.filter_type_combo.currentIndexChanged.connect(self.update_history)
        filter_layout.addWidget(self.filter_type_combo)
        
        date_layout = QHBoxLayout()
        date_label = QLabel("De:")
        self.history_date_from = QDateEdit()
        self.history_date_from.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.history_date_from)
        
        to_label = QLabel("À:")
        self.history_date_to = QDateEdit()
        self.history_date_to.setCalendarPopup(True)
        date_layout.addWidget(to_label)
        date_layout.addWidget(self.history_date_to)
        filter_layout.addLayout(date_layout)
        
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
        """Initialise la barre de menu avec plus d'options"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        settings_action = QAction("Paramètres", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Exporter la configuration", self)
        export_action.triggered.connect(self.export_settings)
        file_menu.addAction(export_action)
        
        import_action = QAction("Importer la configuration", self)
        import_action.triggered.connect(self.import_settings)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Quitter", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Outils
        tools_menu = menubar.addMenu("Outils")
        
        update_action = QAction("Vérifier les mises à jour", self)
        update_action.triggered.connect(self.check_for_updates)
        tools_menu.addAction(update_action)
        
        backup_action = QAction("Sauvegarder", self)
        backup_action.triggered.connect(self.create_backup)
        tools_menu.addAction(backup_action)
        
        restore_action = QAction("Restaurer", self)
        restore_action.triggered.connect(self.restore_backup)
        tools_menu.addAction(restore_action)
        
        tools_menu.addSeparator()
        
        log_action = QAction("Ouvrir les logs", self)
        log_action.triggered.connect(self.open_logs)
        tools_menu.addAction(log_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        
        docs_action = QAction("Documentation", self)
        docs_action.triggered.connect(self.open_documentation)
        help_menu.addAction(docs_action)
        
        forum_action = QAction("Forum Freqtrade", self)
        forum_action.triggered.connect(lambda: webbrowser.open("https://github.com/freqtrade/freqtrade/discussions"))
        help_menu.addAction(forum_action)
        
        help_menu.addSeparator()
        
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


    def tray_icon_activated(self, reason):
        """Gère les interactions avec l'icône de la barre système"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
        elif reason == QSystemTrayIcon.Trigger:
            self.show_tray_notification()

    def show_tray_notification(self):
        """Affiche une notification dans la barre système"""
        status = "En cours d'exécution" if self.freqtrade_running else "Arrêté"
        self.tray_icon.showMessage(
            "Freqtrade Manager",
            f"Statut: {status}\nCliquez pour plus d'options",
            QSystemTrayIcon.Information,
            2000
        )

    def export_settings(self):
        """Exporte les paramètres et configurations dans un fichier zip"""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exporter les paramètres",
                "",
                "Fichiers ZIP (*.zip);;Tous les fichiers (*)",
                options=options
            )
            
            if file_path:
                if not file_path.endswith('.zip'):
                    file_path += '.zip'
                
                with zipfile.ZipFile(file_path, 'w') as zipf:
                    # Exporter la base de données
                    zipf.write(self.db_path, os.path.basename(self.db_path))
                    
                    # Exporter les configurations
                    config_dir = os.path.join(self.config_dir, 'configs')
                    if os.path.exists(config_dir):
                        for file in os.listdir(config_dir):
                            zipf.write(
                                os.path.join(config_dir, file),
                                os.path.join('configs', file)
                            )
                    
                    # Exporter les stratégies
                    strategy_dir = os.path.join(self.config_dir, 'strategies')
                    if os.path.exists(strategy_dir):
                        for file in os.listdir(strategy_dir):
                            zipf.write(
                                os.path.join(strategy_dir, file),
                                os.path.join('strategies', file)
                            )
                
                QMessageBox.information(self, "Succès", "Paramètres exportés avec succès!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'exportation: {str(e)}")
    def open_logs(self):
        """Ouvre le répertoire des logs ou le fichier log actuel"""
        try:
            # Vérifier si le répertoire de logs existe
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
                
            # Créer un nom de fichier de log basé sur la date
            log_file = os.path.join(self.log_dir, f"freqtrade_{datetime.now().strftime('%Y-%m-%d')}.log")
            
            # Si Freqtrade est en cours d'exécution, utiliser le log actuel
            if self.freqtrade_running and hasattr(self, 'current_process'):
                # Essayer de trouver le fichier log le plus récent
                log_files = sorted(
                    [f for f in os.listdir(self.log_dir) if f.startswith('freqtrade_') and f.endswith('.log')],
                    key=lambda x: os.path.getmtime(os.path.join(self.log_dir, x)),
                    reverse=True
                )
                if log_files:
                    log_file = os.path.join(self.log_dir, log_files[0])
            
            # Si le fichier log n'existe pas encore, créer un fichier vide
            if not os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    f.write("Fichier log initialisé le {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            # Ouvrir le fichier log avec l'éditeur par défaut
            if platform.system() == "Windows":
                os.startfile(log_file)
            elif platform.system() == "Darwin":
                subprocess.run(["open", log_file])
            else:
                subprocess.run(["xdg-open", log_file])
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir les logs: {str(e)}")


    def setup_logging(self):
        """Configure le système de logging pour l'application"""
        # Créer le répertoire de logs s'il n'existe pas
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # Configurer le logging
        log_file = os.path.join(self.log_dir, f"manager_{datetime.now().strftime('%Y-%m-%d')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("FreqtradeManager")


    def log_message(self, message, level="info"):
        """Journalise un message avec différents niveaux de sévérité"""
        if not hasattr(self, 'logger'):
            self.setup_logging()
        
        if level.lower() == "debug":
            self.logger.debug(message)
        elif level.lower() == "info":
            self.logger.info(message)
        elif level.lower() == "warning":
            self.logger.warning(message)
        elif level.lower() == "error":
            self.logger.error(message)
        elif level.lower() == "critical":
            self.logger.critical(message)
        
        # Ajouter aussi au output si l'interface est initialisée
        if hasattr(self, 'output'):
            color = {
                "debug": "gray",
                "info": "black",
                "warning": "orange",
                "error": "red",
                "critical": "darkred"
            }.get(level.lower(), "black")
            
            self.output.append(f'<font color="{color}">{message}</font>')
            
    def import_settings(self):
        """Importe les paramètres et configurations depuis un fichier zip"""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Importer les paramètres",
                "",
                "Fichiers ZIP (*.zip);;Tous les fichiers (*)",
                options=options
            )
            
            if file_path:
                # Créer un dossier temporaire pour l'extraction
                temp_dir = tempfile.mkdtemp()
                
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Vérifier la structure des fichiers
                db_file = os.path.join(temp_dir, os.path.basename(self.db_path))
                config_dir = os.path.join(temp_dir, 'configs')
                strategy_dir = os.path.join(temp_dir, 'strategies')
                
                if not os.path.exists(db_file):
                    raise FileNotFoundError("Fichier de base de données introuvable dans l'archive")
                
                # Sauvegarder les fichiers existants
                backup_path = os.path.join(self.base_dir, 'backup_before_import.zip')
                self.create_backup(backup_path)
                
                # Remplacer les fichiers
                shutil.copy(db_file, self.db_path)
                
                if os.path.exists(config_dir):
                    dest_config_dir = os.path.join(self.config_dir, 'configs')
                    os.makedirs(dest_config_dir, exist_ok=True)
                    for file in os.listdir(config_dir):
                        shutil.copy(
                            os.path.join(config_dir, file),
                            os.path.join(dest_config_dir, file)
                        )
                
                if os.path.exists(strategy_dir):
                    dest_strategy_dir = os.path.join(self.config_dir, 'strategies')
                    os.makedirs(dest_strategy_dir, exist_ok=True)
                    for file in os.listdir(strategy_dir):
                        shutil.copy(
                            os.path.join(strategy_dir, file),
                            os.path.join(dest_strategy_dir, file)
                        )
                
                QMessageBox.information(
                    self, 
                    "Succès", 
                    "Paramètres importés avec succès!\n"
                    f"Une sauvegarde a été créée à: {backup_path}"
                )
                
                # Recharger les données
                self.load_settings()
                self.load_configurations()
                self.load_strategies()
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'importation: {str(e)}")

    def check_for_updates(self):
        """Vérifie les mises à jour disponibles"""
        try:
            self.status_bar.showMessage("Vérification des mises à jour...")
            
            # Récupérer la version actuelle
            current_version = "2.0.0"  # À remplacer par votre système de version
            
            # Récupérer la dernière version depuis GitHub
            with urlopen("https://api.github.com/repos/freqtrade/freqtrade/releases/latest") as response:
                data = json.loads(response.read().decode())
                latest_version = data['tag_name'].strip('v')
            
            if version.parse(latest_version) > version.parse(current_version):
                reply = QMessageBox.question(
                    self,
                    "Mise à jour disponible",
                    f"Une nouvelle version {latest_version} est disponible (vous avez {current_version}).\n"
                    "Voulez-vous visiter la page de téléchargement?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    webbrowser.open("https://github.com/freqtrade/freqtrade/releases")
            else:
                QMessageBox.information(
                    self,
                    "À jour",
                    f"Vous utilisez la dernière version ({current_version})."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible de vérifier les mises à jour: {str(e)}"
            )
        finally:
            self.status_bar.clearMessage()

    def create_backup(self, backup_path=None):
        """Crée une sauvegarde des paramètres"""
        try:
            if not backup_path:
                options = QFileDialog.Options()
                backup_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Créer une sauvegarde",
                    "",
                    "Fichiers ZIP (*.zip);;Tous les fichiers (*)",
                    options=options
                )
                
                if not backup_path:
                    return
                
                if not backup_path.endswith('.zip'):
                    backup_path += '.zip'
            
            with zipfile.ZipFile(backup_path, 'w') as zipf:
                # Sauvegarder la base de données
                zipf.write(self.db_path, os.path.basename(self.db_path))
                
                # Sauvegarder les configurations
                config_dir = os.path.join(self.config_dir, 'configs')
                if os.path.exists(config_dir):
                    for file in os.listdir(config_dir):
                        zipf.write(
                            os.path.join(config_dir, file),
                            os.path.join('configs', file)
                        )
                
                # Sauvegarder les stratégies
                strategy_dir = os.path.join(self.config_dir, 'strategies')
                if os.path.exists(strategy_dir):
                    for file in os.listdir(strategy_dir):
                        zipf.write(
                            os.path.join(strategy_dir, file),
                            os.path.join('strategies', file)
                        )
            
            if backup_path:
                QMessageBox.information(
                    self, 
                    "Succès", 
                    f"Sauvegarde créée avec succès à:\n{backup_path}"
                )
            
            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la sauvegarde: {str(e)}")
            return False

    def restore_backup(self):
        """Restaure une sauvegarde des paramètres"""
        try:
            options = QFileDialog.Options()
            backup_path, _ = QFileDialog.getOpenFileName(
                self,
                "Restaurer une sauvegarde",
                "",
                "Fichiers ZIP (*.zip);;Tous les fichiers (*)",
                options=options
            )
            
            if backup_path:
                reply = QMessageBox.question(
                    self,
                    "Confirmation",
                    "Cette action va remplacer tous vos paramètres actuels.\n"
                    "Voulez-vous continuer?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # Créer une sauvegarde avant la restauration
                    temp_backup = os.path.join(self.base_dir, 'pre_restore_backup.zip')
                    self.create_backup(temp_backup)
                    
                    # Créer un dossier temporaire pour l'extraction
                    temp_dir = tempfile.mkdtemp()
                    
                    with zipfile.ZipFile(backup_path, 'r') as zipf:
                        zipf.extractall(temp_dir)
                    
                    # Vérifier la structure des fichiers
                    db_file = os.path.join(temp_dir, os.path.basename(self.db_path))
                    config_dir = os.path.join(temp_dir, 'configs')
                    strategy_dir = os.path.join(temp_dir, 'strategies')
                    
                    if not os.path.exists(db_file):
                        raise FileNotFoundError("Fichier de base de données introuvable dans la sauvegarde")
                    
                    # Remplacer les fichiers
                    shutil.copy(db_file, self.db_path)
                    
                    if os.path.exists(config_dir):
                        dest_config_dir = os.path.join(self.config_dir, 'configs')
                        os.makedirs(dest_config_dir, exist_ok=True)
                        shutil.rmtree(dest_config_dir)
                        shutil.copytree(config_dir, dest_config_dir)
                    
                    if os.path.exists(strategy_dir):
                        dest_strategy_dir = os.path.join(self.config_dir, 'strategies')
                        os.makedirs(dest_strategy_dir, exist_ok=True)
                        shutil.rmtree(dest_strategy_dir)
                        shutil.copytree(strategy_dir, dest_strategy_dir)
                    
                    QMessageBox.information(
                        self, 
                        "Succès", 
                        "Sauvegarde restaurée avec succès!\n"
                        f"Une sauvegarde de vos anciens paramètres a été créée à: {temp_backup}"
                    )
                    
                    # Recharger les données
                    self.load_settings()
                    self.load_configurations()
                    self.load_strategies()
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de la restauration: {str(e)}")



    def init_tray_icon(self):
        """Initialise l'icône de la barre système avec plus d'options"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("system-run"))
        
        tray_menu = QMenu()
        
        open_action = tray_menu.addAction("Ouvrir")
        open_action.triggered.connect(self.show)
        
        start_action = tray_menu.addAction("Démarrer Freqtrade")
        start_action.triggered.connect(self.start_freqtrade)
        
        stop_action = tray_menu.addAction("Arrêter Freqtrade")
        stop_action.triggered.connect(self.stop_freqtrade)
        
        tray_menu.addSeparator()
        
        stats_action = tray_menu.addAction("Statistiques")


    def init_tray_icon(self):
        """Initialise l'icône de la barre système avec plus d'options"""
        # Créer l'icône
        self.tray_icon = QSystemTrayIcon(self)
        
        # Charger une icône personnalisée ou utiliser l'icône système par défaut
        icon_path = os.path.join(os.path.dirname(__file__), "freqtrade_icon.png")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(QIcon.fromTheme("system-run"))
        
        # Créer le menu contextuel
        tray_menu = QMenu()
        
        # Action pour ouvrir la fenêtre principale
        open_action = tray_menu.addAction("Ouvrir Freqtrade Manager")
        open_action.triggered.connect(self.show)
        open_action.setIcon(QIcon.fromTheme("window"))
        
        # Actions pour contrôler Freqtrade
        tray_menu.addSeparator()
        
        self.tray_start_action = tray_menu.addAction("Démarrer Freqtrade")
        self.tray_start_action.triggered.connect(self.start_freqtrade)
        self.tray_start_action.setIcon(QIcon.fromTheme("media-playback-start"))
        self.tray_start_action.setEnabled(self.freqtrade_installed)
        
        self.tray_stop_action = tray_menu.addAction("Arrêter Freqtrade")
        self.tray_stop_action.triggered.connect(self.stop_freqtrade)
        self.tray_stop_action.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.tray_stop_action.setEnabled(False)
        
        self.tray_restart_action = tray_menu.addAction("Redémarrer Freqtrade")
        self.tray_restart_action.triggered.connect(self.restart_freqtrade)
        self.tray_restart_action.setIcon(QIcon.fromTheme("view-refresh"))
        self.tray_restart_action.setEnabled(False)
        
        # Sous-menu pour les modes rapides
        mode_menu = tray_menu.addMenu("Mode rapide")
        mode_menu.setIcon(QIcon.fromTheme("system-run"))
        
        trade_action = mode_menu.addAction("Mode Trading")
        trade_action.triggered.connect(lambda: self.set_quick_mode("trade"))
        
        backtest_action = mode_menu.addAction("Mode Backtest")
        backtest_action.triggered.connect(lambda: self.set_quick_mode("backtest"))
        
        hyperopt_action = mode_menu.addAction("Mode Hyperopt")
        hyperopt_action.triggered.connect(lambda: self.set_quick_mode("hyperopt"))
        
        # Action pour afficher les stats
        tray_menu.addSeparator()
        stats_action = tray_menu.addAction("Statistiques")
        stats_action.triggered.connect(self.show_tray_stats)
        stats_action.setIcon(QIcon.fromTheme("dialog-information"))
        
        # Action pour les notifications Telegram
        self.telegram_toggle_action = tray_menu.addAction("Notifications Telegram")
        self.telegram_toggle_action.setCheckable(True)
        self.telegram_toggle_action.setChecked(False)
        self.telegram_toggle_action.triggered.connect(self.toggle_telegram_notifications)
        self.telegram_toggle_action.setIcon(QIcon.fromTheme("mail-send"))
        
        # Quitter
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        
        # Assigner le menu à l'icône
        self.tray_icon.setContextMenu(tray_menu)
        
        # Configurer les signaux
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.messageClicked.connect(self.show)
        
        # Afficher l'icône
        self.tray_icon.show()
        
        # Mettre à jour l'état initial
        self.update_tray_icon_state()
        
        # Charger l'état Telegram
        self.load_telegram_tray_state()

    def on_tray_icon_activated(self, reason):
        """Gère les clics sur l'icône de la barre système"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
        elif reason == QSystemTrayIcon.Trigger:
            # Afficher un message d'état rapide
            status = "En cours d'exécution" if self.freqtrade_running else "Arrêté"
            self.tray_icon.showMessage(
                "Freqtrade Manager", 
                f"Statut: {status}\nCliquez pour plus d'options",
                QSystemTrayIcon.Information, 
                2000
            )

    def update_tray_icon_state(self):
        """Met à jour l'état des actions du menu tray"""
        self.tray_start_action.setEnabled(not self.freqtrade_running and self.freqtrade_installed)
        self.tray_stop_action.setEnabled(self.freqtrade_running)
        self.tray_restart_action.setEnabled(self.freqtrade_running)
        
        # Mettre à jour l'icône en fonction de l'état
        if self.freqtrade_running:
            self.tray_icon.setIcon(QIcon.fromTheme("media-playback-start"))
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "freqtrade_icon.png")
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            else:
                self.tray_icon.setIcon(QIcon.fromTheme("system-run"))

    def set_quick_mode(self, mode):
        """Configure un mode rapide depuis le menu tray"""
        self.mode_combo.setCurrentText(mode.capitalize())
        
        if not self.isVisible():
            self.show()
            QTimer.singleShot(100, lambda: self.start_freqtrade())
        else:
            self.start_freqtrade()

    def show_tray_stats(self):
        """Affiche les statistiques dans un message tray"""
        if self.freqtrade_running:
            stats = self.get_current_stats()
            self.tray_icon.showMessage(
                "Statistiques Freqtrade",
                f"Mode: {stats['mode']}\n"
                f"Stratégie: {stats['strategy']}\n"
                f"Durée: {stats['duration']}\n"
                f"Profit: {stats['profit']}",
                QSystemTrayIcon.Information,
                3000
            )
        else:
            self.tray_icon.showMessage(
                "Statistiques Freqtrade",
                "Freqtrade n'est pas en cours d'exécution",
                QSystemTrayIcon.Warning,
                2000
            )

    def toggle_telegram_notifications(self, checked):
        """Active/désactive les notifications Telegram"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                     ("telegram_enabled", str(checked)))
            conn.commit()
            conn.close()
            
            if checked:
                self.tray_icon.showMessage(
                    "Notifications Telegram",
                    "Les notifications Telegram sont maintenant activées",
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'état Telegram: {str(e)}")

    def load_telegram_tray_state(self):
        """Charge l'état des notifications Telegram"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT value FROM settings WHERE key='telegram_enabled'")
            result = c.fetchone()
            if result:
                self.telegram_toggle_action.setChecked(result[0] == "True")
            conn.close()
        except Exception as e:
            print(f"Erreur lors du chargement de l'état Telegram: {str(e)}")

    def get_current_stats(self):
        """Retourne les statistiques actuelles de trading"""
        # Cette fonction devrait être implémentée pour récupérer les vraies stats
        return {
            "mode": self.mode_combo.currentText(),
            "strategy": self.strategy_input.currentText(),
            "duration": "2h 15m",
            "profit": "+3.2%"
        }





    def set_style(self):
        """Applique un style moderne et professionnel à l'application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                font-weight: bold;
            }
            QTextEdit, QLineEdit, QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background: white;
            }
            QTextEdit {
                font-family: Consolas, Courier New, monospace;
            }
            QPushButton {
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid #3498db;
                min-height: 25px;
                background-color: #3498db;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                border-color: #7f8c8d;
            }
            QTabWidget::pane {
                border-top: 2px solid #bdc3c7;
                background: white;
            }
            QTabBar::tab {
                padding: 8px 12px;
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                border-color: #2980b9;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                width: 10px;
            }
            QLabel[status="error"] {
                color: #e74c3c;
                font-weight: bold;
            }
            QLabel[status="success"] {
                color: #27ae60;
                font-weight: bold;
            }
            QLabel[status="warning"] {
                color: #f39c12;
                font-weight: bold;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)

        # Appliquer une police plus moderne
        font = QFont()
        font.setFamily("Segoe UI" if platform.system() == "Windows" else "Arial")
        font.setPointSize(9)
        QApplication.setFont(font)

    def update_ui_state(self):
        """Met à jour l'état de l'interface utilisateur"""
        # Mettre à jour les états des dépendances
        self.git_status.setText(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
        self.python_status.setText(f"Python: {'Installé' if self.python_installed else 'Manquant'} ({getattr(self, 'python_version', 'N/A')})")
        self.freqtrade_status.setText(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        self.venv_status.setText(f"Environnement virtuel: {'Créé' if self.venv_created else 'Manquant'}")

        # Mettre à jour les styles en fonction de l'état
        for label, condition in [
            (self.git_status, self.git_installed),
            (self.python_status, self.python_installed),
            (self.freqtrade_status, self.freqtrade_installed),
            (self.venv_status, self.venv_created)
        ]:
            status = "success" if condition else "error"
            label.setProperty("status", status)
            label.style().unpolish(label)
            label.style().polish(label)

        # Activer/désactiver les boutons en fonction des dépendances
        self.install_btn.setEnabled(self.git_installed and self.python_installed)
        self.install_btn.setText("Installer Freqtrade" if not self.freqtrade_installed else "Mettre à jour Freqtrade")
        self.start_btn.setEnabled(self.freqtrade_installed)
        self.repair_btn.setEnabled(self.freqtrade_installed)
        self.clean_btn.setEnabled(self.freqtrade_installed)

    def get_install_commands(self, version):
        """Retourne les commandes d'installation optimisées pour Windows"""
        commands = []
        python_exec = "python"
        pip_exec = "pip"

        # Si on utilise un environnement virtuel
        if self.venv_check.isChecked():
            if not os.path.exists(self.venv_dir):
                commands.append(f"@echo Création de l'environnement virtuel Python {self.python_combo.currentText()}")
                commands.append(f"python -m venv \"{self.venv_dir}\"")
            
            python_exec = os.path.join(self.venv_dir, "Scripts", "python.exe")
            pip_exec = os.path.join(self.venv_dir, "Scripts", "pip.exe")

        commands.append("@echo Installation des outils de compilation...")
        commands.append(f"{python_exec} -m pip install --upgrade pip setuptools wheel")

        # Clonage ou mise à jour du dépôt
        if not os.path.exists(os.path.join(self.freqtrade_dir, ".git")):
            commands.append("@echo Clonage du dépôt Freqtrade...")
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{self.freqtrade_dir}\"")
        else:
            commands.append("@echo Mise à jour du dépôt Freqtrade...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && git fetch --all")

        commands.append(f"@echo Sélection de la version {version}")
        commands.append(f"cd \"{self.freqtrade_dir}\" && git checkout {version}")
        commands.append(f"cd \"{self.freqtrade_dir}\" && git pull")

        # Installation optimisée pour Windows
        commands.append("@echo Installation des dépendances principales...")
        commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install --upgrade pip")
        commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install numpy --only-binary=:all:")

        if self.optimize_check.isChecked():
            commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install . --use-pep517 --no-cache-dir")
        else:
            commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install .")

        commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-common.txt")

        # Dépendances optionnelles
        if self.plot_check.isChecked():
            commands.append("@echo Installation des dépendances de visualisation...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-plot.txt")

        if self.ta_check.isChecked():
            commands.append("@echo Installation des dépendances d'analyse technique...")
            commands.append(f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-ft.txt")

        # Installation des outils supplémentaires recommandés
        commands.append("@echo Installation des outils supplémentaires...")
        commands.append(f"{pip_exec} install TA-Lib") if self.ta_check.isChecked() else ""
        commands.append(f"{pip_exec} install pandas")

        return [cmd for cmd in commands if cmd]  # Retirer les chaînes vides

    def start_installation(self):
        """Lance le processus d'installation avec gestion des erreurs améliorée"""
        if self.installation_in_progress:
            QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
            return

        # Vérifier les prérequis
        if not self.git_installed:
            reply = QMessageBox.question(self, "Git manquant", 
                                       "Git n'est pas installé. Voulez-vous l'installer maintenant?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.install_git()
            return

        if not self.python_installed:
            reply = QMessageBox.question(self, "Python manquant", 
                                       "Python 3.8+ n'est pas installé. Voulez-vous l'installer maintenant?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.install_python()
            return

        self.installation_in_progress = True
        self.install_btn.setEnabled(False)
        self.output.clear()

        # Créer les répertoires nécessaires
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

        # Préparer les commandes d'installation
        version = self.version_combo.currentText()
        commands = self.get_install_commands(version)

        # Exécuter les commandes
        self.current_command = 0
        self.commands = commands
        self.progress.setMaximum(len(commands))
        self.execute_next_command()

    def install_git(self):
        """Installe Git automatiquement sur Windows"""
        try:
            self.output.append("@echo Installation de Git...")
            subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], check=True)
            self.git_installed = True
            self.update_ui_state()
            QMessageBox.information(self, "Succès", "Git a été installé avec succès!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'installation de Git: {str(e)}")

    def install_python(self):
        """Installe Python automatiquement sur Windows"""
        try:
            self.output.append("@echo Installation de Python...")
            version = self.python_combo.currentText()
            url = f"https://www.python.org/ftp/python/3.{version}/python-3.{version}-amd64.exe"
            installer_path = os.path.join(self.base_dir, "python_installer.exe")

            # Télécharger l'installateur
            subprocess.run([
                "curl", "-o", installer_path, "-L", url
            ], check=True)

            # Exécuter l'installateur en mode silencieux
            subprocess.run([
                installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"
            ], check=True)

            # Supprimer l'installateur
            os.remove(installer_path)

            self.python_installed = True
            self.update_ui_state()
            QMessageBox.information(self, "Succès", f"Python 3.{version} a été installé avec succès!")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'installation de Python: {str(e)}")

    def execute_next_command(self):
        """Exécute la prochaine commande dans la séquence"""
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

    def handle_command_output(self, text, color):
        """Affiche la sortie de la commande dans la console"""
        if color == "red":
            self.output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.output.append(text)

        # Faire défiler vers le bas automatiquement
        self.output.moveCursor(QTextCursor.End)

    def command_finished(self):
        """Appelé lorsqu'une commande est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)

        if self.current_command < len(self.commands):
            # Passer à la commande suivante
            QTimer.singleShot(100, self.execute_next_command)
        else:
            # Installation terminée
            self.installation_completed()

    def installation_completed(self):
        """Appelé lorsque l'installation est terminée"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)

        # Vérifier si l'installation a réussi
        self.check_dependencies()
        self.update_ui_state()

        version = self.version_combo.currentText()
        if self.freqtrade_installed:
            self.log_installation(version, "Succès", "Installation terminée avec succès")
            QMessageBox.information(self, "Succès", 
                                  "Freqtrade a été installé avec succès!\n\n"
                                  f"Répertoire : {self.freqtrade_dir}")
        else:
            self.log_installation(version, "Échec", "Installation incomplète")
            QMessageBox.warning(self, "Avertissement",
                              "L'installation semble incomplète.\n"
                              "Veuillez vérifier la sortie pour les erreurs.")

    def repair_installation(self):
        """Tente de réparer une installation existante"""
        reply = QMessageBox.question(self, "Réparer", 
                                   "Voulez-vous réparer l'installation Freqtrade?\n"
                                   "Cela réinstallera toutes les dépendances.",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.installation_in_progress = True
            self.output.clear()

            # Commandes de réparation
            python_exec = os.path.join(self.venv_dir, "Scripts", "python.exe") if self.venv_created else "python"
            pip_exec = os.path.join(self.venv_dir, "Scripts", "pip.exe") if self.venv_created else "pip"

            commands = [
                f"@echo Réparation de l'installation Freqtrade",
                f"cd \"{self.freqtrade_dir}\" && {pip_exec} install --upgrade pip",
                f"cd \"{self.freqtrade_dir}\" && {pip_exec} install --force-reinstall .",
                f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-common.txt",
                f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-plot.txt",
                f"cd \"{self.freqtrade_dir}\" && {pip_exec} install -r requirements-ft.txt"
            ]

            self.current_command = 0
            self.commands = commands
            self.progress.setMaximum(len(commands))
            self.execute_next_command()

    def clean_installation(self):
        """Nettoie l'installation et supprime les fichiers temporaires"""
        reply = QMessageBox.question(self, "Nettoyer", 
                                   "Voulez-vous nettoyer l'installation?\n"
                                   "Cela supprimera les fichiers temporaires et les caches.",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.output.append("@echo Nettoyage de l'installation...")

                # Supprimer les caches pip
                subprocess.run(["python", "-m", "pip", "cache", "purge"], check=True)

                # Supprimer les fichiers temporaires
                temp_dirs = [
                    os.path.join(self.freqtrade_dir, "build"),
                    os.path.join(self.freqtrade_dir, "dist"),
                    os.path.join(self.freqtrade_dir, "freqtrade.egg-info"),
                    os.path.join(self.freqtrade_dir, "__pycache__")
                ]

                for temp_dir in temp_dirs:
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                        self.output.append(f"Supprimé: {temp_dir}")

                self.output.append("<font color='green'>Nettoyage terminé avec succès!</font>")
            except Exception as e:
                self.output.append(f"<font color='red'>Erreur lors du nettoyage: {str(e)}</font>")

    def start_freqtrade(self):
        """Démarre Freqtrade avec les paramètres sélectionnés"""
        if self.freqtrade_running:
            QMessageBox.warning(self, "Déjà en cours", "Freqtrade est déjà en cours d'exécution")
            return

        mode = self.mode_combo.currentText().lower()
        python_exec = os.path.join(self.venv_dir, "Scripts", "python.exe") if self.venv_created else "python"

        # Construire la commande de base
        cmd = f"{python_exec} -m freqtrade {mode}"

        # Ajouter des options spécifiques au mode
        if mode == "trade":
            strategy = self.strategy_input.currentText()
            config = self.config_input.currentText()
            cmd += f" --strategy {strategy} --config {os.path.join(self.config_dir, 'configs', 'config.json')}"

            if self.dry_run_check.isChecked():
                cmd += " --dry-run"

            if not self.db_check.isChecked():
                cmd += " --db-url sqlite:///"

        elif mode == "backtest":
            strategy = self.bt_strategy_input.currentText()
            config = self.bt_config_input.currentText()
            timerange = self.timerange_input.text()
            
            cmd += f" --strategy {strategy} --config {os.path.join(self.config_dir, 'configs', 'config.json')}"
            
            if timerange:
                cmd += f" --timerange {timerange}"
                
            if self.bt_download_check.isChecked():
                cmd += " --download-data"

        # Démarrer le processus
        try:
            self.exec_output.clear()
            self.freqtrade_running = True
            self.update_execution_buttons()

            # Journaliser l'exécution
            self.log_execution(cmd, mode, "Démarré")

            # Démarrer dans un nouveau processus
            self.current_process = subprocess.Popen(
                cmd,
                cwd=self.freqtrade_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                bufsize=1
            )

            # Démarrer un thread pour lire la sortie
            self.output_thread = OutputReader(self.current_process)
            self.output_thread.output_signal.connect(self.handle_execution_output)
            self.output_thread.finished.connect(self.execution_finished)
            self.output_thread.start()

        except Exception as e:
            self.exec_output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.freqtrade_running = False
            self.update_execution_buttons()

    def stop_freqtrade(self):
        """Arrête Freqtrade proprement"""
        if not self.freqtrade_running:
            return

        try:
            if self.current_process:
                # Envoyer CTRL+C pour un arrêt propre
                self.current_process.send_signal(subprocess.signal.CTRL_C_EVENT)
                
                # Attendre un peu avant de forcer l'arrêt
                try:
                    self.current_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.current_process.kill()

            self.freqtrade_running = False
            self.update_execution_buttons()
            self.log_execution("", "", "Arrêté")

        except Exception as e:
            self.exec_output.append(f"<font color='red'>ERREUR lors de l'arrêt: {str(e)}</font>")

    def restart_freqtrade(self):
        """Redémarre Freqtrade"""
        self.stop_freqtrade()
        QTimer.singleShot(2000, self.start_freqtrade)

    def handle_execution_output(self, text, is_error):
        """Affiche la sortie de l'exécution de Freqtrade"""
        color = "red" if is_error else "white"
        
        if is_error:
            self.exec_output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.exec_output.append(text)

        # Faire défiler vers le bas automatiquement
        self.exec_output.moveCursor(QTextCursor.End)

        # Analyser la sortie pour détecter les erreurs critiques
        if "ERROR" in text or "Exception" in text:
            self.status_bar.showMessage(f"Erreur détectée: {text[:100]}...", 5000)

    def execution_finished(self):
        """Appelé lorsque l'exécution de Freqtrade est terminée"""
        self.freqtrade_running = False
        self.update_execution_buttons()

        # Capturer la sortie finale
        output = self.exec_output.toPlainText()
        self.log_execution("", "", "Terminé", output)

        # Vérifier le code de sortie
        if self.current_process and self.current_process.returncode != 0:
            self.exec_output.append(f"<font color='red'>Freqtrade s'est arrêté avec le code d'erreur: {self.current_process.returncode}</font>")

    def update_execution_buttons(self):
        """Met à jour l'état des boutons d'exécution"""
        self.start_btn.setEnabled(not self.freqtrade_running and self.freqtrade_installed)
        self.stop_btn.setEnabled(self.freqtrade_running)
        self.restart_btn.setEnabled(self.freqtrade_running)

    def update_mode_options(self):
        """Met à jour les options affichées en fonction du mode sélectionné"""
        mode = self.mode_combo.currentText().lower()

        # Masquer toutes les options
        for i in range(self.mode_options_layout.count()):
            widget = self.mode_options_layout.itemAt(i).widget()
            if widget:
                widget.hide()

        # Afficher les options appropriées
        if mode == "trade":
            self.trade_options.show()
        elif mode == "backtest":
            self.backtest_options.show()
        # Ajouter d'autres conditions pour les autres modes...

    def load_configurations(self):
        """Charge les configurations depuis la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT name FROM configurations ORDER BY last_used DESC")
            configs = [row[0] for row in c.fetchall()]
            
            self.config_combo.clear()
            self.config_combo.addItems(configs)
            
            conn.close()
        except Exception as e:
            print(f"Failed to load configurations: {str(e)}")

    def load_configurations_to_combo(self, combo):
        """Charge les configurations dans un QComboBox spécifique"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT name FROM configurations ORDER BY last_used DESC")
            configs = [row[0] for row in c.fetchall()]
            
            combo.clear()
            combo.addItems(configs)
            
            conn.close()
        except Exception as e:
            print(f"Failed to load configurations: {str(e)}")

    def load_strategies(self):
        """Charge les stratégies disponibles depuis le répertoire des stratégies"""
        strategy_dir = os.path.join(self.config_dir, "strategies")
        os.makedirs(strategy_dir, exist_ok=True)
        
        try:
            strategies = []
            for file in os.listdir(strategy_dir):
                if file.endswith(".py") and not file.startswith("_"):
                    strategies.append(file[:-3])  # Retirer l'extension .py
            
            self.strategy_combo.clear()
            self.strategy_combo.addItems(strategies)
        except Exception as e:
            print(f"Failed to load strategies: {str(e)}")

    def load_strategies_to_combo(self, combo):
        """Charge les stratégies dans un QComboBox spécifique"""
        strategy_dir = os.path.join(self.config_dir, "strategies")
        os.makedirs(strategy_dir, exist_ok=True)
        
        try:
            strategies = []
            for file in os.listdir(strategy_dir):
                if file.endswith(".py") and not file.startswith("_"):
                    strategies.append(file[:-3])  # Retirer l'extension .py
            
            combo.clear()
            combo.addItems(strategies)
        except Exception as e:
            print(f"Failed to load strategies: {str(e)}")

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
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")

    def delete_selected_config(self):
        """Supprime la configuration sélectionnée"""
        config_name = self.config_combo.currentText()
        if not config_name:
            return
            
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment supprimer la configuration '{config_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("DELETE FROM configurations WHERE name=?", (config_name,))
                conn.commit()
                conn.close()
                
                self.load_configurations()
                QMessageBox.information(self, "Succès", "Configuration supprimée avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer la configuration: {str(e)}")

    def browse_config_file(self):
        """Ouvre un dialogue pour sélectionner un fichier de configuration"""
        path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier de configuration", 
                                            "", "Fichiers JSON (*.json);;Tous les fichiers (*)")
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
                
            # Lire et mettre à jour la configuration avec les options rapides
            with open(path, 'r') as f:
                config = json.load(f)
                
            # Mettre à jour les options rapides
            exchange = self.exchange_combo.currentText()
            pairs = [p.strip() for p in self.pair_input.text().split(",") if p.strip()]
            
            if exchange and pairs:
                config['exchange']['name'] = exchange
                config['exchange']['pair_whitelist'] = pairs
                
                # Sauvegarder les modifications
                with open(path, 'w') as f:
                    json.dump(config, f, indent=4)
            
            # Insérer la nouvelle configuration
            c.execute("INSERT INTO configurations (name, path, last_used, exchange, pairlist) VALUES (?, ?, ?, ?, ?)",
                     (name, path, datetime.now().isoformat(), exchange, ",".join(pairs)))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Succès", "Configuration créée avec succès!")
            self.load_configurations()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer la configuration: {str(e)}")

    def edit_selected_strategy(self):
        """Ouvre la stratégie sélectionnée pour édition"""
        strategy_name = self.strategy_combo.currentText()
        if not strategy_name:
            return
            
        try:
            path = os.path.join(self.config_dir, "strategies", f"{strategy_name}.py")
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir la stratégie: {str(e)}")

    def test_selected_strategy(self):
        """Teste la stratégie sélectionnée avec un backtest rapide"""
        strategy_name = self.strategy_combo.currentText()
        if not strategy_name:
            return
            
        try:
            # Utiliser la première configuration disponible
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT name FROM configurations ORDER BY last_used DESC LIMIT 1")
            config_name = c.fetchone()[0]
            conn.close()
            
            # Configurer automatiquement l'onglet d'exécution
            self.tabs.setCurrentIndex(3)  # Onglet Exécution
            self.mode_combo.setCurrentText("Backtest")
            self.bt_strategy_input.setCurrentText(strategy_name)
            self.bt_config_input.setCurrentText(config_name)
            self.timerange_input.setText("20230101-")
            
            QMessageBox.information(self, "Prêt", 
                                  f"La stratégie '{strategy_name}' a été configurée pour un backtest.\n"
                                  "Cliquez sur 'Démarrer' pour lancer le test.")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de tester la stratégie: {str(e)}")

    def delete_selected_strategy(self):
        """Supprime la stratégie sélectionnée"""
        strategy_name = self.strategy_combo.currentText()
        if not strategy_name:
            return
            
        reply = QMessageBox.question(self, "Confirmation", 
                                   f"Voulez-vous vraiment supprimer la stratégie '{strategy_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                path = os.path.join(self.config_dir, "strategies", f"{strategy_name}.py")
                os.remove(path)
                
                self.load_strategies()
                QMessageBox.information(self, "Succès", "Stratégie supprimée avec succès!")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer la stratégie: {str(e)}")

    def create_new_strategy(self):
        """Crée une nouvelle stratégie basée sur un modèle"""
        strategy_name = self.new_strategy_name.text().strip()
        base_strategy = self.base_strategy_combo.currentText()
        
        if not strategy_name:
            QMessageBox.warning(self, "Nom manquant", "Veuillez entrer un nom pour la stratégie")
            return
            
        # Vérifier les caractères valides
        if not strategy_name.isidentifier():
            QMessageBox.warning(self, "Nom invalide", 
                              "Le nom de la stratégie ne doit contenir que des lettres, chiffres et underscores")
            return
            
        try:
            strategy_dir = os.path.join(self.config_dir, "strategies")
            os.makedirs(strategy_dir, exist_ok=True)
            
            path = os.path.join(strategy_dir, f"{strategy_name}.py")
            
            if os.path.exists(path):
                QMessageBox.warning(self, "Existe déjà", "Une stratégie avec ce nom existe déjà")
                return
                
            # Créer la stratégie basée sur le modèle sélectionné
            if base_strategy == "Blank":
                content = """from freqtrade.strategy import IStrategy

class {class_name}(IStrategy):
    # Configuration de la stratégie
    INTERFACE_VERSION = 3
    
    # Paramètres temporels
    timeframe = '5m'
    
    # Paramètres de trading
    stoploss = -0.10
    trailing_stop = False
    
    # ROI (Return on Investment)
    minimal_roi = {{
        "0": 0.10
    }}
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Ajouter des indicateurs ici
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Logique d'entrée
        dataframe.loc[
            (
                # Condition d'entrée
            ),
            'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Logique de sortie
        dataframe.loc[
            (
                # Condition de sortie
            ),
            'exit_long'] = 1
        
        return dataframe
""".format(class_name=strategy_name)
            else:
                # Copier la stratégie de base
                base_path = os.path.join(self.freqtrade_dir, "freqtrade", "strategy", "strategies", f"{base_strategy}.py")
                
                if not os.path.exists(base_path):
                    QMessageBox.critical(self, "Erreur", f"Le modèle de stratégie '{base_strategy}' est introuvable")
                    return
                    
                with open(base_path, 'r') as f:
                    content = f.read()
                
                # Remplacer le nom de la classe
                content = content.replace(f"class {base_strategy}", f"class {strategy_name}")

            # Écrire le nouveau fichier
            with open(path, 'w') as f:
                f.write(content)
                
            QMessageBox.information(self, "Succès", 
                                  f"La stratégie '{strategy_name}' a été créée avec succès!\n"
                                  f"Fichier: {path}")
            
            # Recharger la liste des stratégies
            self.load_strategies()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer la stratégie: {str(e)}")

    def toggle_telegram_settings(self, state):
        """Active ou désactive les paramètres Telegram"""
        enabled = state == Qt.Checked
        self.telegram_token.setEnabled(enabled)
        self.telegram_chat_id.setEnabled(enabled)
        self.telegram_test_btn.setEnabled(enabled)
        self.telegram_save_btn.setEnabled(enabled)

    def test_telegram(self):
        """Teste la connexion Telegram"""
        token = self.telegram_token.text().strip()
        chat_id = self.telegram_chat_id.text().strip()
        
        if not token or not chat_id:
            QMessageBox.warning(self, "Champs manquants", "Veuillez entrer le token et le chat ID")
            return
            
        try:
            import requests
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            params = {
                "chat_id": chat_id,
                "text": "Test de notification depuis Freqtrade Manager",
                "disable_notification": False
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                QMessageBox.information(self, "Succès", "Message Telegram envoyé avec succès!")
            else:
                QMessageBox.critical(self, "Erreur", 
                                    f"Échec de l'envoi du message. Code: {response.status_code}\n"
                                    f"Réponse: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de tester Telegram: {str(e)}")

    def save_telegram_settings(self):
        """Enregistre les paramètres Telegram"""
        token = self.telegram_token.text().strip()
        chat_id = self.telegram_chat_id.text().strip()
        enabled = self.telegram_enable.isChecked()
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Sauvegarder les paramètres
            c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                     ("telegram_enabled", str(enabled)))
            c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                     ("telegram_token", token))
            c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                     ("telegram_chat_id", chat_id))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Succès", "Paramètres Telegram enregistrés!")
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer les paramètres: {str(e)}")

    def toggle_system_monitor(self):
        """Active ou désactive le monitoring système"""
        if hasattr(self, 'monitor_timer') and self.monitor_timer.isActive():
            self.monitor_timer.stop()
            self.sys_monitor_btn.setText("Démarrer le monitoring")
            self.cpu_label.setText("CPU: N/A")
            self.mem_label.setText("Mémoire: N/A")
            self.disk_label.setText("Disque: N/A")
            self.net_label.setText("Réseau: N/A")
        else:
            self.monitor_timer = QTimer()
            self.monitor_timer.timeout.connect(self.update_system_stats)
            self.monitor_timer.start(1000)  # Mettre à jour toutes les secondes
            self.sys_monitor_btn.setText("Arrêter le monitoring")

    def update_system_stats(self):
        """Met à jour les statistiques système"""
        # CPU
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.setText(f"CPU: {cpu_percent}%")
        
        # Mémoire
        mem = psutil.virtual_memory()
        self.mem_label.setText(f"Mémoire: {mem.percent}% utilisé ({mem.used/1024/1024:.1f}MB / {mem.total/1024/1024:.1f}MB)")
        
        # Disque
        disk = psutil.disk_usage(self.base_dir)
        self.disk_label.setText(f"Disque: {disk.percent}% utilisé ({disk.used/1024/1024:.1f}MB / {disk.total/1024/1024:.1f}MB)")
        
        # Réseau
        net_io = psutil.net_io_counters()
        self.net_label.setText(f"Réseau: Envoi {net_io.bytes_sent/1024:.1f}KB / Reçu {net_io.bytes_recv/1024:.1f}KB")

    def set_process_priority(self):
        """Définit la priorité du processus Freqtrade"""
        if not self.freqtrade_running or not self.current_process:
            QMessageBox.warning(self, "Erreur", "Freqtrade n'est pas en cours d'exécution")
            return
            
        priority = self.priority_combo.currentText()
        
        try:
            import win32api
            import win32process
            import win32con
            
            priority_map = {
                "Normal": win32process.NORMAL_PRIORITY_CLASS,
                "Haut": win32process.HIGH_PRIORITY_CLASS,
                "Temps réel": win32process.REALTIME_PRIORITY_CLASS
            }
            
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self.current_process.pid)
            win32process.SetPriorityClass(handle, priority_map[priority])
            win32api.CloseHandle(handle)
            
            QMessageBox.information(self, "Succès", f"Priorité définie à '{priority}'")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de définir la priorité: {str(e)}")

    def update_history(self):
        """Met à jour l'historique avec des filtres"""
        filter_type = self.filter_type_combo.currentText()
        date_from = self.history_date_from.date().toString("yyyy-MM-dd")
        date_to = self.history_date_to.date().toString("yyyy-MM-dd")
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            history_text = ""
            
            if filter_type in ["Tous", "Installations"]:
                c.execute("""
                    SELECT * FROM installations 
                    WHERE install_date BETWEEN ? AND ?
                    ORDER BY install_date DESC LIMIT 10
                """, (date_from, date_to))
                
                installations = c.fetchall()
                
                history_text += "<h2>Dernières Installations</h2>"
                history_text += "<table border='1'><tr><th>Date</th><th>Version</th><th>Python</th><th>Statut</th></tr>"
                
                for install in installations:
                    history_text += f"""
                        <tr>
                            <td>{install[3][:19]}</td>
                            <td>{install[1]}</td>
                            <td>{install[2]}</td>
                            <td>{install[4]}</td>
                        </tr>
                    """
                
                history_text += "</table><br>"
            
            if filter_type in ["Tous", "Exécutions"]:
                c.execute("""
                    SELECT * FROM executions 
                    WHERE start_time BETWEEN ? AND ?
                    ORDER BY start_time DESC LIMIT 20
                """, (date_from, date_to))
                
                executions = c.fetchall()
                
                history_text += "<h2>Dernières Exécutions</h2>"
                history_text += "<table border='1'><tr><th>Date</th><th>Mode</th><th>Stratégie</th><th>Statut</th></tr>"
                
                for exec_ in executions:
                    history_text += f"""
                        <tr>
                            <td>{exec_[1][:19]}</td>
                            <td>{exec_[3]}</td>
                            <td>{exec_[4]}</td>
                            <td>{exec_[5]}</td>
                        </tr>
                    """
                
                history_text += "</table>"
            
            self.history_table.setHtml(history_text)
            conn.close()
            
        except Exception as e:
            self.history_table.setPlainText(f"Erreur lors du chargement de l'historique: {str(e)}")

    def log_installation(self, version, status, details=""):
        """Journalise l'installation dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("""
                INSERT INTO installations 
                (version, python_version, path, install_date, status, details) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                version,
                self.python_version,
                self.freqtrade_dir,
                datetime.now().isoformat(),
                status,
                details
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log installation: {str(e)}")

    def log_execution(self, command, mode, status, output=""):
        """Journalise l'exécution dans la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            if status == "Démarré":
                strategy = self.strategy_input.currentText() if mode == "trade" else self.bt_strategy_input.currentText()
                c.execute("""
                    INSERT INTO executions 
                    (start_time, command, mode, strategy, status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    command,
                    mode,
                    strategy,
                    status
                ))
            else:
                # Mettre à jour la dernière exécution
                c.execute("""
                    UPDATE executions SET 
                    end_time=?, 
                    status=?, 
                    output=? 
                    WHERE id=(SELECT MAX(id) FROM executions)
                """, (
                    datetime.now().isoformat(),
                    status,
                    output
                ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to log execution: {str(e)}")

    def load_settings(self):
        """Charge les paramètres depuis la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Paramètres Telegram
            c.execute("SELECT value FROM settings WHERE key='telegram_enabled'")
            result = c.fetchone()
            if result:
                self.telegram_enable.setChecked(result[0] == "True")
            
            c.execute("SELECT value FROM settings WHERE key='telegram_token'")
            result = c.fetchone()
            if result:
                self.telegram_token.setText(result[0])
            
            c.execute("SELECT value FROM settings WHERE key='telegram_chat_id'")
            result = c.fetchone()
            if result:
                self.telegram_chat_id.setText(result[0])
            
            conn.close()
        except Exception as e:
            print(f"Failed to load settings: {str(e)}")

    def show_settings(self):
        """Affiche la boîte de dialogue des paramètres"""
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Paramètres")
        settings_dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Option pour l'environnement virtuel
        venv_group = QGroupBox("Environnement virtuel")
        venv_layout = QVBoxLayout()
        
        self.venv_path_edit = QLineEdit(self.venv_dir)
        venv_layout.addWidget(QLabel("Chemin:"))
        venv_layout.addWidget(self.venv_path_edit)
        
        venv_browse_btn = QPushButton("Parcourir...")
        venv_browse_btn.clicked.connect(self.browse_venv_path)
        venv_layout.addWidget(venv_browse_btn)
        
        venv_group.setLayout(venv_layout)
        layout.addWidget(venv_group)
        
        # Boutons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(lambda: self.save_settings(settings_dialog))
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(settings_dialog.close)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def browse_venv_path(self):
        """Ouvre un dialogue pour sélectionner le chemin de l'environnement virtuel"""
        path = QFileDialog.getExistingDirectory(self, "Sélectionner le répertoire de l'environnement virtuel", 
                                              self.venv_dir)
        if path:
            self.venv_path_edit.setText(path)

    def save_settings(self, dialog):
        """Enregistre les paramètres"""
        new_venv_path = self.venv_path_edit.text()
        
        if new_venv_path != self.venv_dir:
            reply = QMessageBox.question(self, "Confirmation", 
                                       "Changer le chemin de l'environnement virtuel nécessite un redémarrage. Continuer?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    conn = sqlite3.connect(self.db_path)
                    c = conn.cursor()
                    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                             ("venv_path", new_venv_path))
                    conn.commit()
                    conn.close()
                    
                    self.venv_dir = new_venv_path
                    QMessageBox.information(self, "Succès", 
                                          "Les paramètres ont été enregistrés. Veuillez redémarrer l'application.")
                    dialog.close()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer les paramètres: {str(e)}")
        else:
            dialog.close()

    def open_documentation(self):
        """Ouvre la documentation Freqtrade dans le navigateur"""
        webbrowser.open("https://www.freqtrade.io/en/latest/")

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h1>Freqtrade Manager Pro++</h1>
        <p>Version 2.0.0</p>
        <p>Un gestionnaire graphique complet pour Freqtrade, le bot de trading algorithmique open-source.</p>
        <p>Fonctionnalités:</p>
        <ul>
            <li>Installation et mise à jour automatique</li>
            <li>Gestion des configurations et stratégies</li>
            <li>Exécution et monitoring</li>
            <li>Intégration Telegram</li>
            <li>Optimisation pour Windows</li>
        </ul>
        <p>Développé avec Python et PyQt5</p>
        <p>© 2023 - Tous droits réservés</p>
        """
        QMessageBox.about(self, "À propos", about_text)

    def closeEvent(self, event):
        """Gère la fermeture propre de l'application"""
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
                
        # Sauvegarder les paramètres
        self.save_telegram_settings()
        
        # Fermer proprement
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
            
        event.accept()



    def __init__(self):
        super().__init__()
        self.setup_directories()
        self.init_ui()
        self.init_system()
        self.load_settings()
        
    def setup_directories(self):
        """Configure les répertoires de l'application avec vérification des permissions"""
        try:
            # Chemin de base dans AppData/Roaming
            self.base_dir = os.path.join(os.getenv('APPDATA'), "FreqtradeManagerPro")
            
            # Créer les répertoires nécessaires avec vérification
            required_dirs = {
                'base': self.base_dir,
                'freqtrade': os.path.join(self.base_dir, "freqtrade"),
                'config': os.path.join(self.base_dir, "user_data"),
                'venv': os.path.join(self.base_dir, "venv"),
                'logs': os.path.join(self.base_dir, "logs"),
                'strategies': os.path.join(self.base_dir, "user_data", "strategies"),
                'configs': os.path.join(self.base_dir, "user_data", "configs")
            }
            
            for name, path in required_dirs.items():
                if not os.path.exists(path):
                    os.makedirs(path)
                    # Définir des permissions appropriées
                    os.chmod(path, 0o755)
            
            # Chemin de la base de données
            self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur d'initialisation", 
                                f"Impossible de configurer les répertoires: {str(e)}")
            sys.exit(1)
    
    def init_system(self):
        """Initialise les vérifications système et dépendances"""
        self.check_dependencies()
        self.check_python_installation()
        self.check_freqtrade_installation()
        self.setup_path_environment()
        
    def check_dependencies(self):
        """Vérifie les dépendances système avec gestion d'erreur améliorée"""
        try:
            # Vérification de Git
            self.git_installed = self._check_command_available(["git", "--version"])
            
            # Vérification de Docker (désactivé par défaut sur Windows)
            self.docker_installed = False
            
            # Vérification des outils de compilation
            self.compiler_tools = self._check_compiler_tools()
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur de dépendances", 
                              f"Erreur lors de la vérification des dépendances: {str(e)}")
    
    def _check_command_available(self, command):
        """Vérifie si une commande système est disponible"""
        try:
            result = subprocess.run(command, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 timeout=10,
                                 check=True,
                                 creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            return True
        except:
            return False
            
    def _check_compiler_tools(self):
        """Vérifie la présence des outils de compilation sur Windows"""
        if platform.system() != "Windows":
            return True
            
        try:
            # Vérifier Visual C++ Build Tools
            result = subprocess.run(["where", "cl.exe"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  timeout=10,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            return result.returncode == 0
        except:
            return False
    
    def check_python_installation(self):
        """Vérifie l'installation de Python avec gestion de version"""
        try:
            # Essayer python puis python3
            for cmd in ["python", "python3"]:
                try:
                    result = subprocess.run([cmd, "--version"], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          text=True,
                                          timeout=10,
                                          creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
                    
                    if result.returncode == 0:
                        version_str = result.stdout.strip()
                        if "Python" in version_str:
                            self.python_version = version_str.split()[1]
                            major, minor = map(int, self.python_version.split('.')[:2])
                            self.python_installed = major == 3 and minor >= 8
                            return
                except:
                    continue
                    
            self.python_installed = False
            self.python_version = "N/A"
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur Python", 
                              f"Erreur lors de la vérification de Python: {str(e)}")
            self.python_installed = False
            self.python_version = "N/A"
    
    def check_freqtrade_installation(self):
        """Vérifie si Freqtrade est installé et fonctionnel"""
        try:
            python_exec = self.get_python_executable()
            
            result = subprocess.run([python_exec, "-m", "freqtrade", "--version"], 
                                  cwd=self.freqtrade_dir,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=30,
                                  creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            
            self.freqtrade_installed = result.returncode == 0
            return self.freqtrade_installed
            
        except Exception as e:
            print(f"Erreur de vérification Freqtrade: {str(e)}")
            self.freqtrade_installed = False
            return False
    
    def get_python_executable(self):
        """Retourne le chemin de l'exécutable Python approprié"""
        if hasattr(self, 'venv_dir') and os.path.exists(self.venv_dir):
            if platform.system() == "Windows":
                return os.path.join(self.venv_dir, "Scripts", "python.exe")
            else:
                return os.path.join(self.venv_dir, "bin", "python")
        return "python"
    
    def setup_path_environment(self):
        """Configure les variables d'environnement PATH"""
        try:
            paths_to_add = [
                self.venv_dir,
                os.path.join(self.venv_dir, "Scripts") if platform.system() == "Windows" else os.path.join(self.venv_dir, "bin"),
                self.freqtrade_dir
            ]
            
            # Mettre à jour le PATH de l'utilisateur
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
                path_value, _ = winreg.QueryValueEx(key, 'Path')
                
                for path in paths_to_add:
                    if path not in path_value:
                        path_value = f"{path};{path_value}"
                
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, path_value)
            
            # Mettre à jour le PATH pour la session en cours
            os.environ['PATH'] = f"{';'.join(paths_to_add)};{os.environ['PATH']}"
            
            # Prévenir Windows du changement
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            import ctypes
            ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment')
            
        except Exception as e:
            print(f"Impossible de mettre à jour le PATH: {str(e)}")
    
    def init_ui(self):
        """Initialise l'interface utilisateur avec onglets et styles"""
        self.setWindowTitle("Freqtrade Manager Pro++")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(QSize(1000, 800))
        
        # Configuration du style
        self.set_style()
        
        # Widget central et layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Barre d'onglets
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Création des onglets
        self.setup_install_tab()
        self.setup_config_tab()
        self.setup_strategy_tab()
        self.setup_execution_tab()
        self.setup_telegram_tab()
        self.setup_performance_tab()
        self.setup_history_tab()
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")
        
        # Icône système
        self.init_tray_icon()
        
        # Menu
        self.init_menu_bar()
        
        # Mettre à jour l'état de l'UI
        self.update_ui_state()
    
    def set_style(self):
        """Applique un style moderne à l'application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                border: 1px solid #dcdde1;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                font-weight: bold;
                color: #2f3640;
            }
            QTextEdit, QLineEdit, QComboBox {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 5px;
                background: white;
                min-height: 25px;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 4px;
                border: 1px solid #3498db;
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                border-color: #95a5a6;
            }
            QTabWidget::pane {
                border-top: 2px solid #bdc3c7;
                background: white;
            }
            QTabBar::tab {
                padding: 8px 15px;
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
                border-color: #2980b9;
            }
            QProgressBar {
                border: 1px solid #dcdde1;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                width: 10px;
            }
        """)
        
        # Police moderne
        font = QFont()
        font.setFamily("Segoe UI" if platform.system() == "Windows" else "Arial")
        font.setPointSize(10)
        QApplication.setFont(font)
    
    def setup_install_tab(self):
        """Configure l'onglet d'installation avec options avancées"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Header
        header = QLabel("<h1>Installation Freqtrade</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Vérification des dépendances
        deps_group = QGroupBox("Vérification des dépendances")
        deps_layout = QVBoxLayout(deps_group)
        
        self.git_status = QLabel(f"Git: {'Installé' if self.git_installed else 'Manquant'}")
        self.python_status = QLabel(f"Python: {'Installé' if self.python_installed else 'Manquant'} ({self.python_version})")
        self.freqtrade_status = QLabel(f"Freqtrade: {'Installé' if self.freqtrade_installed else 'Manquant'}")
        self.compiler_status = QLabel(f"Outils de compilation: {'Disponibles' if self.compiler_tools else 'Manquants'}")
        
        deps_layout.addWidget(self.git_status)
        deps_layout.addWidget(self.python_status)
        deps_layout.addWidget(self.freqtrade_status)
        deps_layout.addWidget(self.compiler_status)
        
        # Boutons d'installation des dépendances
        dep_btn_layout = QHBoxLayout()
        self.install_git_btn = QPushButton("Installer Git")
        self.install_git_btn.clicked.connect(self.install_git)
        dep_btn_layout.addWidget(self.install_git_btn)
        
        self.install_python_btn = QPushButton("Installer Python")
        self.install_python_btn.clicked.connect(self.install_python)
        dep_btn_layout.addWidget(self.install_python_btn)
        
        self.install_compiler_btn = QPushButton("Installer les outils de compilation")
        self.install_compiler_btn.clicked.connect(self.install_compiler_tools)
        dep_btn_layout.addWidget(self.install_compiler_btn)
        
        deps_layout.addLayout(dep_btn_layout)
        layout.addWidget(deps_group)
        
        # Options d'installation
        options_group = QGroupBox("Options d'installation avancées")
        options_layout = QVBoxLayout(options_group)
        
        # Version à installer
        version_layout = QHBoxLayout()
        version_label = QLabel("Version Freqtrade:")
        self.version_combo = QComboBox()
        self.version_combo.addItems(["stable", "develop", "feat/short"])
        self.version_combo.setCurrentText("stable")
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_combo)
        options_layout.addLayout(version_layout)
        
        # Options d'installation
        self.venv_check = QCheckBox("Créer un environnement virtuel Python")
        self.venv_check.setChecked(True)
        options_layout.addWidget(self.venv_check)
        
        self.plot_check = QCheckBox("Installer les dépendances de visualisation")
        self.plot_check.setChecked(True)
        options_layout.addWidget(self.plot_check)
        
        self.ta_check = QCheckBox("Installer les dépendances d'analyse technique")
        self.ta_check.setChecked(True)
        options_layout.addWidget(self.ta_check)
        
        self.optimize_check = QCheckBox("Optimiser l'installation pour Windows")
        self.optimize_check.setChecked(True)
        options_layout.addWidget(self.optimize_check)
        
        layout.addWidget(options_group)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        
        self.install_btn = QPushButton("Installer Freqtrade" if not self.freqtrade_installed else "Mettre à jour Freqtrade")
        self.install_btn.setStyleSheet("background-color: #27ae60;")
        self.install_btn.clicked.connect(self.start_installation)
        btn_layout.addWidget(self.install_btn)
        
        self.repair_btn = QPushButton("Réparer")
        self.repair_btn.setStyleSheet("background-color: #f39c12;")
        self.repair_btn.clicked.connect(self.repair_installation)
        btn_layout.addWidget(self.repair_btn)
        
        self.clean_btn = QPushButton("Nettoyer")
        self.clean_btn.setStyleSheet("background-color: #e74c3c;")
        self.clean_btn.clicked.connect(self.clean_installation)
        btn_layout.addWidget(self.clean_btn)
        
        layout.addLayout(btn_layout)
        
        # Barre de progression
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Console de sortie
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.output)
        
        self.tabs.addTab(tab, "Installation")
    
    def install_git(self):
        """Installe Git automatiquement sur Windows"""
        try:
            self.output.append("Installation de Git...")
            
            # Utiliser winget si disponible, sinon télécharger l'installateur
            if self._check_command_available(["winget", "--version"]):
                subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], 
                             check=True, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Télécharger l'installateur Git
                url = "https://github.com/git-for-windows/git/releases/download/v2.40.1.windows.1/Git-2.40.1-64-bit.exe"
                installer_path = os.path.join(self.base_dir, "Git-Installer.exe")
                
                self.download_file(url, installer_path)
                
                # Exécuter l'installateur en mode silencieux
                subprocess.run([installer_path, "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"], 
                             check=True, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Supprimer l'installateur
                os.remove(installer_path)
            
            self.git_installed = True
            self.update_ui_state()
            self.output.append("Git installé avec succès!")
            
        except Exception as e:
            self.output.append(f"<font color='red'>Échec de l'installation de Git: {str(e)}</font>")
    
    def install_python(self):
        """Installe Python automatiquement sur Windows"""
        try:
            version = "3.10"  # Version recommandée pour Freqtrade
            self.output.append(f"Installation de Python {version}...")
            
            url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
            installer_path = os.path.join(self.base_dir, "Python-Installer.exe")
            
            self.download_file(url, installer_path)
            
            # Exécuter l'installateur avec les options appropriées
            subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_launcher=0"], 
                         check=True, 
                         creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Supprimer l'installateur
            os.remove(installer_path)
            
            # Vérifier l'installation
            self.check_python_installation()
            self.update_ui_state()
            self.output.append(f"Python {version} installé avec succès!")
            
        except Exception as e:
            self.output.append(f"<font color='red'>Échec de l'installation de Python: {str(e)}</font>")
    
    def install_compiler_tools(self):
        """Installe les outils de compilation Visual C++ sur Windows"""
        try:
            self.output.append("Installation des outils de compilation...")
            
            # Utiliser winget si disponible
            if self._check_command_available(["winget", "--version"]):
                subprocess.run(["winget", "install", "--id", "Microsoft.VisualStudio.2022.BuildTools", "-e", "--source", "winget"], 
                             check=True, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Télécharger le bootstrapper de Visual Studio Build Tools
                url = "https://aka.ms/vs/17/release/vs_BuildTools.exe"
                installer_path = os.path.join(self.base_dir, "VS_BuildTools.exe")
                
                self.download_file(url, installer_path)
                
                # Installer les composants nécessaires
                args = [
                    installer_path,
                    "--quiet", "--wait", "--norestart", "--nocache",
                    "--add", "Microsoft.VisualStudio.Workload.VCTools",
                    "--add", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
                ]
                
                subprocess.run(args, 
                             check=True, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
                
                # Supprimer l'installateur
                os.remove(installer_path)
            
            self.compiler_tools = True
            self.update_ui_state()
            self.output.append("Outils de compilation installés avec succès!")
            
        except Exception as e:
            self.output.append(f"<font color='red'>Échec de l'installation des outils de compilation: {str(e)}</font>")
    
    def download_file(self, url, dest_path):
        """Télécharge un fichier avec affichage de la progression"""
        try:
            from urllib.request import urlretrieve
            import urllib
            
            def report_progress(block_num, block_size, total_size):
                percent = min(100, (block_num * block_size * 100) / total_size)
                self.progress.setValue(int(percent))
                QApplication.processEvents()
            
            self.output.append(f"Téléchargement de {url}...")
            self.progress.setValue(0)
            
            urlretrieve(url, dest_path, report_progress)
            self.progress.setValue(100)
            
        except urllib.error.URLError as e:
            raise Exception(f"Échec du téléchargement: {str(e)}")
    
    def start_installation(self):
        """Lance le processus d'installation avec gestion des erreurs"""
        if hasattr(self, 'installation_in_progress') and self.installation_in_progress:
            QMessageBox.warning(self, "Installation", "Une installation est déjà en cours")
            return
        
        # Vérifier les prérequis
        if not self.git_installed:
            QMessageBox.warning(self, "Git manquant", "Git doit être installé pour continuer")
            return
            
        if not self.python_installed:
            QMessageBox.warning(self, "Python manquant", "Python 3.8+ doit être installé pour continuer")
            return
        
        self.installation_in_progress = True
        self.install_btn.setEnabled(False)
        self.output.clear()
        
        # Créer les répertoires nécessaires
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Préparer les commandes d'installation
        version = self.version_combo.currentText()
        commands = self.get_install_commands(version)
        
        # Exécuter les commandes
        self.current_command = 0
        self.commands = commands
        self.progress.setMaximum(len(commands))
        self.execute_next_command()
    
    def get_install_commands(self, version):
        """Génère les commandes d'installation appropriées"""
        commands = []
        python_exec = "python"
        pip_exec = "pip"
        
        # Si on utilise un environnement virtuel
        if self.venv_check.isChecked():
            venv_path = os.path.join(self.base_dir, "venv")
            if not os.path.exists(venv_path):
                commands.append(f"@echo Création de l'environnement virtuel Python")
                commands.append(f"python -m venv \"{venv_path}\"")
            
            if platform.system() == "Windows":
                python_exec = os.path.join(venv_path, "Scripts", "python.exe")
                pip_exec = os.path.join(venv_path, "Scripts", "pip.exe")
            else:
                python_exec = os.path.join(venv_path, "bin", "python")
                pip_exec = os.path.join(venv_path, "bin", "pip")
        
        commands.append(f"@echo Installation des outils de base")
        commands.append(f"{python_exec} -m pip install --upgrade pip setuptools wheel")
        
        # Clonage ou mise à jour du dépôt
        freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
        if not os.path.exists(os.path.join(freqtrade_dir, ".git")):
            commands.append(f"@echo Clonage du dépôt Freqtrade")
            commands.append(f"git clone https://github.com/freqtrade/freqtrade.git \"{freqtrade_dir}\"")
        else:
            commands.append(f"@echo Mise à jour du dépôt Freqtrade")
            commands.append(f"cd \"{freqtrade_dir}\" && git fetch --all")
        
        commands.append(f"@echo Sélection de la version {version}")
        commands.append(f"cd \"{freqtrade_dir}\" && git checkout {version}")
        commands.append(f"cd \"{freqtrade_dir}\" && git pull")
        
        # Installation optimisée
        commands.append(f"@echo Installation des dépendances principales")
        commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install --upgrade pip")
        
        if platform.system() == "Windows" and self.compiler_tools and self.optimize_check.isChecked():
            commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install numpy --only-binary=:all:")
            commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install . --use-pep517 --no-cache-dir")
        else:
            commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install .")
        
        commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install -r requirements-common.txt")
        
        # Dépendances optionnelles
        if self.plot_check.isChecked():
            commands.append(f"@echo Installation des dépendances de visualisation")
            commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install -r requirements-plot.txt")
        
        if self.ta_check.isChecked():
            commands.append(f"@echo Installation des dépendances d'analyse technique")
            commands.append(f"cd \"{freqtrade_dir}\" && {pip_exec} install -r requirements-ft.txt")
        
        # Outils supplémentaires
        commands.append(f"@echo Installation des outils supplémentaires")
        if self.ta_check.isChecked():
            commands.append(f"{pip_exec} install TA-Lib")
        commands.append(f"{pip_exec} install pandas")
        
        return [cmd for cmd in commands if cmd]
    
    def execute_next_command(self):
        """Exécute la prochaine commande dans la séquence"""
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
    
    def handle_command_output(self, text, color):
        """Affiche la sortie de la commande"""
        if color == "red":
            self.output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.output.append(text)
        
        # Faire défiler vers le bas automatiquement
        self.output.moveCursor(QTextCursor.End)
    
    def command_finished(self):
        """Appelé lorsqu'une commande est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if self.current_command < len(self.commands):
            # Passer à la commande suivante
            QTimer.singleShot(100, self.execute_next_command)
        else:
            # Installation terminée
            self.installation_completed()
    
    def installation_completed(self):
        """Appelé lorsque l'installation est terminée"""
        self.installation_in_progress = False
        self.install_btn.setEnabled(True)
        
        # Vérifier si l'installation a réussi
        self.check_freqtrade_installation()
        self.update_ui_state()
        
        version = self.version_combo.currentText()
        if self.freqtrade_installed:
            self.log_installation(version, "Succès", "Installation terminée avec succès")
            QMessageBox.information(self, "Succès", 
                                  "Freqtrade a été installé avec succès!\n\n"
                                  f"Répertoire : {self.freqtrade_dir}")
        else:
            self.log_installation(version, "Échec", "Installation incomplète")
            QMessageBox.warning(self, "Avertissement",
                              "L'installation semble incomplète.\n"
                              "Veuillez vérifier la sortie pour les erreurs.")
    
    # ... [Le reste des méthodes reste inchangé mais devrait être inclus dans la classe]


    def __init__(self):
        super().__init__()
        
        # Initialisation des attributs avant toute autre opération
        self.git_installed = False
        self.python_installed = False
        self.python_version = "N/A"
        self.compiler_tools = False
        self.freqtrade_installed = False
        self.venv_created = False
        self.installation_in_progress = False
        self.freqtrade_running = False
        
        # Configuration des chemins
        self.setup_directories()
        
        # Initialisation de l'interface
        self.init_ui()
        
        # Vérification du système
        self.init_system()
        
        # Chargement des paramètres
        self.load_settings()
        
        # Mise à jour de l'interface
        self.update_ui_state()

    def setup_directories(self):
        """Configure les répertoires de base avec gestion des erreurs"""
        try:
            # Chemin de base dans AppData/Roaming
            self.base_dir = os.path.join(os.getenv('APPDATA'), "FreqtradeManagerPro")
            
            # Création des répertoires nécessaires
            self.freqtrade_dir = os.path.join(self.base_dir, "freqtrade")
            self.db_path = os.path.join(self.base_dir, "freqtrade_manager.db")
            self.config_dir = os.path.join(self.base_dir, "user_data")
            self.venv_dir = os.path.join(self.base_dir, "venv")
            self.log_dir = os.path.join(self.base_dir, "logs")
            
            # Création des répertoires s'ils n'existent pas
            os.makedirs(self.base_dir, exist_ok=True)
            os.makedirs(self.freqtrade_dir, exist_ok=True)
            os.makedirs(self.config_dir, exist_ok=True)
            os.makedirs(self.venv_dir, exist_ok=True)
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Sous-répertoires pour les configurations et stratégies
            os.makedirs(os.path.join(self.config_dir, "configs"), exist_ok=True)
            os.makedirs(os.path.join(self.config_dir, "strategies"), exist_ok=True)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur d'initialisation", 
                               f"Impossible de configurer les répertoires: {str(e)}")
            sys.exit(1)

    def init_system(self):
        """Initialise les vérifications système"""
        self.check_dependencies()
        self.check_python_installation()
        self.check_freqtrade_installation()
        self.setup_path_environment()

    def check_dependencies(self):
        """Vérifie les dépendances système"""
        try:
            # Vérification de Git
            self.git_installed = self._check_command_available(["git", "--version"])
            
            # Vérification des outils de compilation (Windows seulement)
            self.compiler_tools = self._check_compiler_tools() if platform.system() == "Windows" else True
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur de dépendances", 
                              f"Erreur lors de la vérification des dépendances: {str(e)}")

    def _check_command_available(self, command):
        """Vérifie si une commande système est disponible"""
        try:
            result = subprocess.run(command, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  timeout=10,
                                  check=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            return True
        except:
            return False

    def _check_compiler_tools(self):
        """Vérifie les outils de compilation sur Windows"""
        try:
            # Vérifie si cl.exe (compilateur Visual C++) est disponible
            result = subprocess.run(["where", "cl.exe"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  timeout=10,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            return result.returncode == 0
        except:
            return False

    def check_python_installation(self):
        """Vérifie l'installation de Python avec gestion de version"""
        try:
            # Essayer python puis python3
            for cmd in ["python", "python3"]:
                try:
                    result = subprocess.run([cmd, "--version"], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          text=True,
                                          timeout=10,
                                          creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
                    
                    if result.returncode == 0:
                        version_str = result.stdout.strip()
                        if "Python" in version_str:
                            self.python_version = version_str.split()[1]
                            major, minor = map(int, self.python_version.split('.')[:2])
                            self.python_installed = major == 3 and minor >= 8
                            return
                except:
                    continue
                    
            self.python_installed = False
            self.python_version = "N/A"
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur Python", 
                              f"Erreur lors de la vérification de Python: {str(e)}")
            self.python_installed = False
            self.python_version = "N/A"

    def check_freqtrade_installation(self):
        """Vérifie si Freqtrade est installé et fonctionnel"""
        try:
            python_exec = self.get_python_executable()
            
            result = subprocess.run([python_exec, "-m", "freqtrade", "--version"], 
                                  cwd=self.freqtrade_dir,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True,
                                  timeout=30,
                                  creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            
            self.freqtrade_installed = result.returncode == 0
            self.venv_created = os.path.exists(self.venv_dir)
            
        except Exception as e:
            print(f"Erreur de vérification Freqtrade: {str(e)}")
            self.freqtrade_installed = False
            self.venv_created = False

    def get_python_executable(self):
        """Retourne le chemin de l'exécutable Python approprié"""
        if os.path.exists(self.venv_dir):
            if platform.system() == "Windows":
                return os.path.join(self.venv_dir, "Scripts", "python.exe")
            else:
                return os.path.join(self.venv_dir, "bin", "python")
        return "python"

    def setup_path_environment(self):
        """Configure les variables d'environnement PATH"""
        try:
            paths_to_add = []
            
            if os.path.exists(self.venv_dir):
                paths_to_add.append(self.venv_dir)
                if platform.system() == "Windows":
                    paths_to_add.append(os.path.join(self.venv_dir, "Scripts"))
                else:
                    paths_to_add.append(os.path.join(self.venv_dir, "bin"))
            
            paths_to_add.append(self.freqtrade_dir)
            
            # Mettre à jour le PATH pour la session en cours
            os.environ['PATH'] = f"{';'.join(paths_to_add)};{os.environ['PATH']}"
            
            # Mettre à jour le PATH de l'utilisateur (Windows seulement)
            if platform.system() == "Windows":
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  'Environment', 0, winreg.KEY_ALL_ACCESS) as key:
                    path_value, _ = winreg.QueryValueEx(key, 'Path')
                    
                    for path in paths_to_add:
                        if path and path not in path_value:
                            path_value = f"{path};{path_value}"
                    
                    winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, path_value)
                
                # Notifier Windows du changement
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                import ctypes
                ctypes.windll.user32.SendMessageW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment')
            
        except Exception as e:
            print(f"Impossible de mettre à jour le PATH: {str(e)}")

    # ... [Le reste des méthodes reste inchangé mais doit être inclus]

if __name__ == "__main__":
    # Vérifier et installer les dépendances si nécessaire
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
        from PyQt5.QtWidgets import QApplication
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Vérifier les autres dépendances
    try:
        import psutil
        import requests
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "requests"])
        import psutil
        import requests
    
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
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
        from PyQt5.QtWidgets import QApplication
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Vérifier les autres dépendances
    try:
        import psutil
        import requests
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "requests"])
        import psutil
        import requests
    
    # Créer et afficher la fenêtre principale
    window = FreqtradeManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())

class OutputReader(QThread):
    """Thread pour lire la sortie d'un processus en temps réel"""
    output_signal = pyqtSignal(str, bool)  # text, is_error
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        
    def run(self):
        while True:
            output = self.process.stdout.readline()
            if output == '' and self.process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip(), False)
            
            err = self.process.stderr.readline()
            if err:
                self.output_signal.emit(err.strip(), True)



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
from PyQt5.QtCore import QThread

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
    # Vérifier et installer les dépendances si nécessaire
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
        from PyQt5.QtWidgets import QApplication
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Vérifier les dépendances système
    try:
        import psutil
        import requests
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "requests"])
        import psutil
        import requests
    
    # Créer et afficher la fenêtre principale
    window = FreqtradeManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())




class CommandWorker(QThread):
    """Thread pour exécuter des commandes système avec gestion robuste des erreurs"""
    output_signal = pyqtSignal(str, str)  # text, color
    
    def __init__(self, command, cwd=None):
        super().__init__()
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.process = None
        
    def run(self):
        try:
            # Créer un environnement propre pour les variables d'environnement
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            # Configurer le processus avec gestion améliorée des erreurs
            creationflags = 0
            if platform.system() == "Windows":
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            
            self.process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True,
                bufsize=1,
                env=env,
                creationflags=creationflags
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
            self.output_signal.emit(f"Erreur d'exécution: {str(e)}", "red")
            
    def stop(self):
        """Arrête le processus proprement"""
        if self.process and self.process.poll() is None:
            try:
                if platform.system() == "Windows":
                    self.process.send_signal(subprocess.signal.CTRL_C_EVENT)
                    try:
                        self.process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                else:
                    self.process.terminate()
                    self.process.wait()
            except Exception as e:
                self.output_signal.emit(f"Erreur lors de l'arrêt: {str(e)}", "red")

