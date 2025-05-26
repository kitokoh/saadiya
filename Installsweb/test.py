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
                           QAction, QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QTextCursor
from PyQt5.QtWidgets import QStackedWidget

class CommandWorker(QThread):
    output_signal = pyqtSignal(str, str)  # text, color
    finished_signal = pyqtSignal(bool)  # success
    
    def __init__(self, command, cwd=None, env=None):
        super().__init__()
        self.command = command
        self.cwd = cwd or os.getcwd()
        self.env = env or os.environ.copy()
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
                bufsize=1,
                env=self.env
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
            
            return_code = self.process.poll()
            self.finished_signal.emit(return_code == 0)
                    
        except Exception as e:
            self.output_signal.emit(f"Error executing command: {str(e)}", "red")
            self.finished_signal.emit(False)
            
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

class BotManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuration de base
        self.setWindowTitle("Freqtrade/FreqAI Manager")
        self.setGeometry(100, 100, 1000, 800)
        self.setMinimumSize(QSize(900, 700))
        
        # Chemins importants
        self.base_dir = self.get_base_dir()
        self.db_path = os.path.join(self.base_dir, "bot_manager.db")
        self.config_dir = os.path.join(self.base_dir, "configs")
        
        # Variables d'état
        self.current_operation = None
        self.active_bots = {}  # {bot_id: worker}
        self.current_worker = None
        
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

    def get_base_dir(self):
        """Détermine le répertoire de base selon l'OS"""
        if platform.system() == "Windows":
            return os.path.join(os.environ.get("APPDATA", "C:\\"), "CryptoBotManager")
        else:
            return os.path.join(os.path.expanduser("~"), ".crypto_bot_manager")

    def init_directories(self):
        """Crée les répertoires nécessaires"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)

    def init_db(self):
        """Initialise la base de données SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Table des bots
            c.execute('''CREATE TABLE IF NOT EXISTS bots
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT,
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
                          FOREIGN KEY(bot_id) REFERENCES bots(id))''')
            
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
                          FOREIGN KEY(bot_id) REFERENCES bots(id),
                          FOREIGN KEY(config_id) REFERENCES configs(id))''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {str(e)}")

    def check_system_dependencies(self):
        """Vérifie et enregistre les dépendances système"""
        dependencies = [
            ("git", ["git", "--version"]),
            ("python", ["python", "--version"]),
            ("docker", ["docker", "--version"]),
            ("pip", ["pip", "--version"])
        ]
        
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            for name, cmd in dependencies:
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    status = "installed"
                except:
                    status = "missing"
                
                # Mettre à jour ou insérer
                c.execute('''INSERT OR REPLACE INTO dependencies (name, status, install_date)
                             VALUES (?, ?, ?)''',
                         (name, status, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to check dependencies: {str(e)}")

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
            print(f"Failed to log execution: {str(e)}")
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

    def setup_bots_tab(self):
        """Configure l'onglet de gestion des bots"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("<h1>Gestion des Bots</h1>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Liste des bots
        self.bots_tree = QTreeWidget()
        self.bots_tree.setHeaderLabels(["ID", "Nom", "Type", "Version", "Statut", "Dernière utilisation"])
        self.bots_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.bots_tree.setSelectionMode(QTreeWidget.SingleSelection)
        self.bots_tree.itemSelectionChanged.connect(self.on_bot_selected)
        layout.addWidget(self.bots_tree)
        
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
        
        layout.addLayout(btn_layout)
        
        # Détails du bot
        self.bot_details = QTextEdit()
        self.bot_details.setReadOnly(True)
        layout.addWidget(self.bot_details)
        
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
        self.install_output = QTextEdit()
        self.install_output.setReadOnly(True)
        self.install_output.setFont(QFont("Consolas", 10))
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
        self.mode_combo.addItems(["Trade", "Backtest", "Hyperopt", "Plot", "Edge", "Download Data"])
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
        
        layout.addWidget(self.options_stack)
        self.mode_combo.currentIndexChanged.connect(lambda: self.options_stack.setCurrentIndex(self.mode_combo.currentIndex()))
        
        # Boutons d'exécution
        btn_layout = QHBoxLayout()
        
        self.exec_start_btn = QPushButton("Démarrer")
        self.exec_start_btn.clicked.connect(self.start_execution)
        btn_layout.addWidget(self.exec_start_btn)
        
        self.exec_stop_btn = QPushButton("Arrêter")
        self.exec_stop_btn.clicked.connect(self.stop_execution)
        self.exec_stop_btn.setEnabled(False)
        btn_layout.addWidget(self.exec_stop_btn)
        
        layout.addLayout(btn_layout)
        
        # Console de sortie
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
        
        self.history_filter_combo = QComboBox()
        self.history_filter_combo.addItems(["Toutes", "Freqtrade", "FreqAI"])
        self.history_filter_combo.currentIndexChanged.connect(self.update_history)
        filter_layout.addWidget(self.history_filter_combo)
        
        self.refresh_history_btn = QPushButton("Actualiser")
        self.refresh_history_btn.clicked.connect(self.update_history)
        filter_layout.addWidget(self.refresh_history_btn)
        
        layout.addLayout(filter_layout)
        
        # Tableau d'historique
        self.history_table = QTreeWidget()
        self.history_table.setHeaderLabels(["ID", "Bot", "Date", "Commande", "Statut"])
        self.history_table.header().setSectionResizeMode(QHeaderView.ResizeToContents)
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
        
        # Menu Outils
        tools_menu = menubar.addMenu("Outils")
        
        check_deps_action = QAction("Vérifier les dépendances", self)
        check_deps_action.triggered.connect(self.check_system_dependencies)
        tools_menu.addAction(check_deps_action)
        
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
                QMessageBox.warning(self, "Dépendances manquantes", 
                                  f"Les dépendances suivantes sont manquantes: {', '.join(missing_deps)}\n"
                                  "Certaines fonctionnalités peuvent ne pas être disponibles.")
            
            conn.close()
        except Exception as e:
            print(f"Failed to check dependencies: {str(e)}")

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
                    item.setForeground(4, Qt.green)
                
                self.bots_tree.addTopLevelItem(item)
            
            conn.close()
        except Exception as e:
            print(f"Failed to update bots list: {str(e)}")

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
            print(f"Failed to update config bot combo: {str(e)}")

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
            print(f"Failed to update exec bot combo: {str(e)}")

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
            print(f"Failed to update config list: {str(e)}")

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
            print(f"Failed to update exec config combo: {str(e)}")

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
                            ORDER BY e.start_time DESC LIMIT 50''')
            else:
                c.execute('''SELECT e.id, b.name, e.start_time, e.command, e.status 
                            FROM executions e JOIN bots b ON e.bot_id = b.id
                            WHERE b.type = ? ORDER BY e.start_time DESC LIMIT 50''',
                         (filter_type.lower(),))
            
            executions = c.fetchall()
            
            for exec_ in executions:
                item = QTreeWidgetItem([str(exec_[0]), exec_[1], exec_[2], exec_[3], exec_[4]])
                
                # Colorer selon le statut
                if exec_[4] == "running":
                    item.setForeground(4, Qt.green)
                elif exec_[4] == "failed":
                    item.setForeground(4, Qt.red)
                
                self.history_table.addTopLevelItem(item)
            
            conn.close()
        except Exception as e:
            print(f"Failed to update history: {str(e)}")

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
                            <p><b>Environnement virtuel:</b> {bot[5]}</p>"""
                
                self.bot_details.setHtml(details)
            
            conn.close()
        except Exception as e:
            print(f"Failed to get bot details: {str(e)}")

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
            print(f"Failed to check bot name: {str(e)}")
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
            self.install_output.append(f"<font color='blue'>{cmd[6:]}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_install_command)
            return
            
        self.install_output.append(f"> {cmd}")
        
        try:
            # Créer un worker pour exécuter la commande
            self.current_worker = CommandWorker(cmd)
            self.current_worker.output_signal.connect(self.handle_install_output)
            self.current_worker.finished_signal.connect(self.install_command_finished)
            self.current_worker.start()
        except Exception as e:
            self.install_output.append(f"<font color='red'>ERREUR: {str(e)}</font>")
            self.current_command += 1
            self.progress.setValue(self.current_command)
            QTimer.singleShot(100, self.execute_next_install_command)

    def handle_install_output(self, text, color):
        """Affiche la sortie de l'installation"""
        if color == "red":
            self.install_output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.install_output.append(text)
        
        # Faire défiler vers le bas
        self.install_output.moveCursor(QTextCursor.End)

    def install_command_finished(self, success):
        """Appelé lorsqu'une commande d'installation est terminée"""
        self.current_command += 1
        self.progress.setValue(self.current_command)
        
        if not success and self.current_command < len(self.install_commands):
            self.install_output.append("<font color='orange'>La commande a échoué mais nous continuons...</font>")
        
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
            
            self.install_output.append("<font color='green'>Installation terminée avec succès!</font>")
            QMessageBox.information(self, "Succès", "Le bot a été installé avec succès!")
            
            # Mettre à jour l'interface
            self.update_ui_state()
            
        except Exception as e:
            self.install_output.append(f"<font color='red'>ERREUR: Échec de l'enregistrement dans la base de données: {str(e)}</font>")
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
            print(f"Failed to check config name: {str(e)}")
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
                    print(f"Failed to remove config file: {str(e)}")
                
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
            except:
                pass

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
        # Pour l'instant, nous affichons simplement dans la console d'exécution
        if color == "red":
            self.exec_output.append(f"<font color='{color}'>[Bot {bot_id}] {text}</font>")
        else:
            self.exec_output.append(f"[Bot {bot_id}] {text}")
        
        # Faire défiler vers le bas
        self.exec_output.moveCursor(QTextCursor.End)

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
            print(f"Failed to update bot status: {str(e)}")
        
        # Supprimer le worker
        self.active_bots.pop(bot_id, None)
        
        # Mettre à jour l'interface
        self.update_bots_list()
        self.update_execution_buttons()
        
        # Afficher un message
        status_msg = "terminé avec succès" if success else "échoué"
        self.exec_output.append(f"<font color={'green' if success else 'red'}>[Bot {bot_id}] {bot_name} {status_msg}</font>")

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
                QMessageBox.information(self, "Succès", f"Le bot {bot_name} est en cours d'arrêt...")
                
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
                        pass
                except Exception as e:
                    print(f"Failed to remove files: {str(e)}")
                
                QMessageBox.information(self, "Succès", "Bot supprimé avec succès!")
                self.update_ui_state()
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de la suppression: {str(e)}")

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
            self.exec_output.append(f"<font color='green'>Démarrage de l'exécution pour {bot_name}...</font>")
            
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
            except:
                pass

    def build_freqtrade_exec_command(self, bot_path, config_path, mode):
        """Construit la commande pour exécuter Freqtrade"""
        cmd = f"freqtrade {mode} --config {config_path}"
        
        # Ajouter des options selon le mode
        if mode == "trade":
            strategy = self.strategy_input.text()
            if strategy:
                cmd += f" --strategy {strategy}"
            
            if self.db_check.isChecked():
                cmd += " --db-url sqlite:///tradesv3.sqlite"
        
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
            self.exec_output.append(f"<font color='{color}'>{text}</font>")
        else:
            self.exec_output.append(text)
        
        # Faire défiler vers le bas
        self.exec_output.moveCursor(QTextCursor.End)

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
            print(f"Failed to update bot status: {str(e)}")
        
        # Supprimer le worker
        self.active_bots.pop(bot_id, None)
        
        # Mettre à jour l'interface
        self.update_bots_list()
        self.update_execution_buttons()
        
        # Afficher un message
        status_msg = "terminée avec succès" if success else "échouée"
        self.exec_output.append(f"<font color={'green' if success else 'red'}>Exécution {status_msg}</font>")

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
                self.exec_output.append("<font color='orange'>Arrêt demandé...</font>")
                
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Échec de l'arrêt: {str(e)}")

    def update_execution_buttons(self):
        """Met à jour l'état des boutons d'exécution"""
        bot_id = self.exec_bot_combo.currentData()
        is_running = bot_id and bot_id in self.active_bots
        
        self.exec_start_btn.setEnabled(not is_running)
        self.exec_stop_btn.setEnabled(is_running)

    def open_documentation(self):
        """Ouvre la documentation"""
        url = "https://www.freqtrade.io/en/latest/" if self.bot_type_combo.currentText() == "Freqtrade" else "https://www.freqtrade.io/en/latest/freqai/"
        webbrowser.open(url)

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h1>Freqtrade/FreqAI Manager</h1>
        <p>Version 1.0.0</p>
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
                    except:
                        pass
                
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
        from PyQt5.QtWidgets import QApplication, QInputDialog
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
            from PyQt5.QtWidgets import QApplication, QInputDialog
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
    window = BotManager()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec_())