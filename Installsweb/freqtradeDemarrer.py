import sys
import os
import json
import logging
import sqlite3
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QComboBox, QTextEdit, QLineEdit, QGroupBox,
                            QStatusBar, QSystemTrayIcon, QMenu, QAction, QMessageBox, QFileDialog,
                            QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QProgressBar)
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor
from PyQt5.QtCore import QTimer, Qt, QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('freqtrade_manager.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FreqTradeProcessThread(QThread):
    """Thread pour exécuter les commandes FreqTrade"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, command, parent=None):
        super().__init__(parent)
        self.command = command
        self.process = None

    def run(self):
        try:
            self.process = Popen(
                self.command,
                stdout=PIPE,
                stderr=STDOUT,
                shell=True,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )

            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip())

            return_code = self.process.poll()
            self.finished_signal.emit(return_code)

        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(-1)

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
            except Exception as e:
                logger.error(f"Error stopping process: {e}")


class DatabaseManager:
    """Gestion de la base de données SQLite pour la persistance"""
    def __init__(self, db_path='freqtrade_managfer.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Table des configurations
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configurations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    config_type TEXT NOT NULL,  
                    path TEXT NOT NULL,
                    config TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Table des commandes favorites
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorite_commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    command TEXT NOT NULL,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Table d'historique
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    exit_code INTEGER,
                    output TEXT,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def save_configuration(self, name, config_type, path, config):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO configurations 
                (name, config_type, path, config, updated_at)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', (name, config_type, path, json.dumps(config)))
            conn.commit()

    def get_configurations(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, config_type, path, config FROM configurations')
            return cursor.fetchall()

    def delete_configuration(self, config_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM configurations WHERE id = ?', (config_id,))
            conn.commit()

    def save_command_history(self, command, exit_code, output):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO command_history (command, exit_code, output)
                VALUES (?, ?, ?)
            ''', (command, exit_code, output))
            conn.commit()

    def get_command_history(self, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, command, exit_code, executed_at 
                FROM command_history 
                ORDER BY executed_at DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def save_favorite_command(self, name, command, category=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO favorite_commands 
                (name, command, category)
                VALUES (?, ?, ?)
            ''', (name, command, category))
            conn.commit()

    def get_favorite_commands(self, category=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute('''
                    SELECT id, name, command, category 
                    FROM favorite_commands 
                    WHERE category = ?
                    ORDER BY name
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT id, name, command, category 
                    FROM favorite_commands 
                    ORDER BY category, name
                ''')
            return cursor.fetchall()

    def delete_favorite_command(self, command_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM favorite_commands WHERE id = ?', (command_id,))
            conn.commit()

from PyQt5.QtWidgets import QDialogButtonBox

class FreqTradeManagerApp(QMainWindow):
    """Application principale FreqTrade Manager"""
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_process = None
        self.current_config = None
        self.setup_ui()
        self.setup_tray_icon()
        self.load_configurations()

    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.setWindowTitle("FreqTrade Manager")
        self.setGeometry(100, 100, 1200, 800)
        
        # Style de l'application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background: #353535;
            }
            QTabBar::tab {
                background: #444;
                color: #ddd;
                padding: 8px;
                border: 1px solid #444;
                border-bottom-color: #2d2d2d;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #505050;
                border-color: #555;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #505050;
                color: #ddd;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #606060;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QPushButton:disabled {
                background-color: #353535;
                color: #777;
            }
            QTextEdit, QLineEdit, QComboBox {
                background-color: #353535;
                color: #ddd;
                border: 1px solid #444;
                padding: 5px;
                selection-background-color: #505050;
            }
            QLabel {
                color: #ddd;
            }
            QTableWidget {
                background-color: #353535;
                color: #ddd;
                gridline-color: #444;
                border: 1px solid #444;
            }
            QHeaderView::section {
                background-color: #444;
                color: #ddd;
                padding: 5px;
                border: 1px solid #444;
            }
            QProgressBar {
                border: 1px solid #444;
                text-align: center;
                color: #ddd;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Barre d'onglets
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Onglets
        self.setup_dashboard_tab()
        self.setup_trade_tab()
        self.setup_backtest_tab()
        self.setup_hyperopt_tab()
        self.setup_utilities_tab()

        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

        # Timer pour les mises à jour périodiques
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(5000)  # Toutes les 5 secondes

    def setup_dashboard_tab(self):
        """Onglet Tableau de bord"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Groupe Configuration
        config_group = QGroupBox("Configuration FreqTrade")
        config_layout = QHBoxLayout(config_group)

        self.config_combo = QComboBox()
        self.config_combo.setMinimumWidth(300)
        self.config_combo.currentIndexChanged.connect(self.config_changed)
        config_layout.addWidget(QLabel("Configuration:"))
        config_layout.addWidget(self.config_combo)

        self.btn_add_config = QPushButton("Ajouter")
        self.btn_add_config.clicked.connect(self.add_configuration)
        config_layout.addWidget(self.btn_add_config)

        self.btn_edit_config = QPushButton("Modifier")
        self.btn_edit_config.clicked.connect(self.edit_configuration)
        config_layout.addWidget(self.btn_edit_config)

        self.btn_remove_config = QPushButton("Supprimer")
        self.btn_remove_config.clicked.connect(self.remove_configuration)
        config_layout.addWidget(self.btn_remove_config)

        layout.addWidget(config_group)

        # Groupe Commandes rapides
        quick_commands_group = QGroupBox("Commandes rapides")
        quick_commands_layout = QHBoxLayout(quick_commands_group)

        self.btn_start = QPushButton("Démarrer FreqTrade")
        self.btn_start.clicked.connect(self.start_freqtrade)
        quick_commands_layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Arrêter")
        self.btn_stop.clicked.connect(self.stop_freqtrade)
        self.btn_stop.setEnabled(False)
        quick_commands_layout.addWidget(self.btn_stop)

        self.btn_restart = QPushButton("Redémarrer")
        self.btn_restart.clicked.connect(self.restart_freqtrade)
        self.btn_restart.setEnabled(False)
        quick_commands_layout.addWidget(self.btn_restart)

        self.btn_status = QPushButton("Statut")
        self.btn_status.clicked.connect(self.check_status)
        quick_commands_layout.addWidget(self.btn_status)

        layout.addWidget(quick_commands_group)

        # Groupe Logs
        logs_group = QGroupBox("Logs")
        logs_layout = QVBoxLayout(logs_group)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier New", 10))
        logs_layout.addWidget(self.log_output)

        layout.addWidget(logs_group)

        self.tab_widget.addTab(tab, "Tableau de bord")

    def setup_trade_tab(self):
        """Onglet Trading"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Groupe Stratégie
        strategy_group = QGroupBox("Stratégie")
        strategy_layout = QVBoxLayout(strategy_group)

        # Sélection de stratégie
        strategy_select_layout = QHBoxLayout()
        strategy_select_layout.addWidget(QLabel("Stratégie:"))
        
        self.strategy_combo = QComboBox()
        self.strategy_combo.setMinimumWidth(200)
        strategy_select_layout.addWidget(self.strategy_combo)
        
        self.btn_refresh_strategies = QPushButton("Rafraîchir")
        self.btn_refresh_strategies.clicked.connect(self.refresh_strategies)
        strategy_select_layout.addWidget(self.btn_refresh_strategies)
        
        strategy_layout.addLayout(strategy_select_layout)

        # Commandes de stratégie
        strategy_commands_layout = QHBoxLayout()
        
        self.btn_start_strategy = QPushButton("Démarrer stratégie")
        self.btn_start_strategy.clicked.connect(self.start_strategy)
        self.btn_start_strategy.setEnabled(False)
        strategy_commands_layout.addWidget(self.btn_start_strategy)
        
        self.btn_stop_strategy = QPushButton("Arrêter stratégie")
        self.btn_stop_strategy.clicked.connect(self.stop_strategy)
        self.btn_stop_strategy.setEnabled(False)
        strategy_commands_layout.addWidget(self.btn_stop_strategy)
        
        strategy_layout.addLayout(strategy_commands_layout)

        layout.addWidget(strategy_group)

        # Groupe Paires de trading
        pairs_group = QGroupBox("Paires de trading")
        pairs_layout = QVBoxLayout(pairs_group)

        # Configuration des paires
        pairs_config_layout = QHBoxLayout()
        pairs_config_layout.addWidget(QLabel("Fichier de configuration:"))
        
        self.pairs_file_edit = QLineEdit()
        self.pairs_file_edit.setPlaceholderText("Chemin vers le fichier de configuration des paires")
        pairs_config_layout.addWidget(self.pairs_file_edit)
        
        self.btn_browse_pairs = QPushButton("Parcourir...")
        self.btn_browse_pairs.clicked.connect(self.browse_pairs_file)
        pairs_config_layout.addWidget(self.btn_browse_pairs)
        
        pairs_layout.addLayout(pairs_config_layout)

        # Commandes des paires
        pairs_commands_layout = QHBoxLayout()
        
        self.btn_load_pairs = QPushButton("Charger les paires")
        self.btn_load_pairs.clicked.connect(self.load_pairs)
        pairs_commands_layout.addWidget(self.btn_load_pairs)
        
        self.btn_update_pairs = QPushButton("Mettre à jour")
        self.btn_update_pairs.clicked.connect(self.update_pairs)
        self.btn_update_pairs.setEnabled(False)
        pairs_commands_layout.addWidget(self.btn_update_pairs)
        
        pairs_layout.addLayout(pairs_commands_layout)

        # Liste des paires
        self.pairs_table = QTableWidget()
        self.pairs_table.setColumnCount(3)
        self.pairs_table.setHorizontalHeaderLabels(["Paire", "Statut", "Actions"])
        self.pairs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        pairs_layout.addWidget(self.pairs_table)

        layout.addWidget(pairs_group)

        self.tab_widget.addTab(tab, "Trading")

    def setup_backtest_tab(self):
        """Onglet Backtest"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Groupe Configuration Backtest
        config_group = QGroupBox("Configuration Backtest")
        config_layout = QVBoxLayout(config_group)

        # Stratégie et intervalle
        strategy_layout = QHBoxLayout()
        strategy_layout.addWidget(QLabel("Stratégie:"))
        
        self.backtest_strategy_combo = QComboBox()
        strategy_layout.addWidget(self.backtest_strategy_combo)
        
        strategy_layout.addWidget(QLabel("Intervalle:"))
        
        self.backtest_interval_combo = QComboBox()
        self.backtest_interval_combo.addItems(["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
        strategy_layout.addWidget(self.backtest_interval_combo)
        
        config_layout.addLayout(strategy_layout)

        # Dates
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date de début:"))
        
        self.backtest_start_date = QLineEdit()
        self.backtest_start_date.setPlaceholderText("YYYY-MM-DD")
        date_layout.addWidget(self.backtest_start_date)
        
        date_layout.addWidget(QLabel("Date de fin:"))
        
        self.backtest_end_date = QLineEdit()
        self.backtest_end_date.setPlaceholderText("YYYY-MM-DD (vide pour maintenant)")
        date_layout.addWidget(self.backtest_end_date)
        
        config_layout.addLayout(date_layout)

        # Paires et export
        pairs_layout = QHBoxLayout()
        pairs_layout.addWidget(QLabel("Paires (séparées par des virgules):"))
        
        self.backtest_pairs = QLineEdit()
        self.backtest_pairs.setPlaceholderText("BTC/USDT,ETH/USDT")
        pairs_layout.addWidget(self.backtest_pairs)
        
        config_layout.addLayout(pairs_layout)

        # Options avancées
        advanced_layout = QHBoxLayout()
        advanced_layout.addWidget(QLabel("Options:"))
        
        self.backtest_live = QCheckBox("Live")
        advanced_layout.addWidget(self.backtest_live)
        
        self.backtest_enable_profit = QCheckBox("Profit")
        advanced_layout.addWidget(self.backtest_enable_profit)
        
        self.backtest_timeframe_detail = QCheckBox("Détail timeframe")
        advanced_layout.addWidget(self.backtest_timeframe_detail)
        
        config_layout.addLayout(advanced_layout)

        layout.addWidget(config_group)

        # Groupe Exécution
        execution_group = QGroupBox("Exécution")
        execution_layout = QVBoxLayout(execution_group)

        # Barre de progression
        self.backtest_progress = QProgressBar()
        execution_layout.addWidget(self.backtest_progress)

        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.btn_run_backtest = QPushButton("Lancer Backtest")
        self.btn_run_backtest.clicked.connect(self.run_backtest)
        buttons_layout.addWidget(self.btn_run_backtest)
        
        self.btn_stop_backtest = QPushButton("Arrêter")
        self.btn_stop_backtest.clicked.connect(self.stop_backtest)
        self.btn_stop_backtest.setEnabled(False)
        buttons_layout.addWidget(self.btn_stop_backtest)
        
        self.btn_export_backtest = QPushButton("Exporter résultats")
        self.btn_export_backtest.clicked.connect(self.export_backtest)
        self.btn_export_backtest.setEnabled(False)
        buttons_layout.addWidget(self.btn_export_backtest)
        
        execution_layout.addLayout(buttons_layout)

        # Résultats
        results_layout = QHBoxLayout()
        
        self.backtest_results = QTextEdit()
        self.backtest_results.setReadOnly(True)
        results_layout.addWidget(self.backtest_results)
        
        execution_layout.addLayout(results_layout)

        layout.addWidget(execution_group)

        self.tab_widget.addTab(tab, "Backtest")

    def setup_hyperopt_tab(self):
        """Onglet Hyperoptimisation"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Groupe Configuration Hyperopt
        config_group = QGroupBox("Configuration Hyperopt")
        config_layout = QVBoxLayout(config_group)

        # Stratégie et intervalle
        strategy_layout = QHBoxLayout()
        strategy_layout.addWidget(QLabel("Stratégie:"))
        
        self.hyperopt_strategy_combo = QComboBox()
        strategy_layout.addWidget(self.hyperopt_strategy_combo)
        
        strategy_layout.addWidget(QLabel("Intervalle:"))
        
        self.hyperopt_interval_combo = QComboBox()
        self.hyperopt_interval_combo.addItems(["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
        strategy_layout.addWidget(self.hyperopt_interval_combo)
        
        config_layout.addLayout(strategy_layout)

        # Dates
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date de début:"))
        
        self.hyperopt_start_date = QLineEdit()
        self.hyperopt_start_date.setPlaceholderText("YYYY-MM-DD")
        date_layout.addWidget(self.hyperopt_start_date)
        
        date_layout.addWidget(QLabel("Date de fin:"))
        
        self.hyperopt_end_date = QLineEdit()
        self.hyperopt_end_date.setPlaceholderText("YYYY-MM-DD (vide pour maintenant)")
        date_layout.addWidget(self.hyperopt_end_date)
        
        config_layout.addLayout(date_layout)

        # Paires
        pairs_layout = QHBoxLayout()
        pairs_layout.addWidget(QLabel("Paires (séparées par des virgules):"))
        
        self.hyperopt_pairs = QLineEdit()
        self.hyperopt_pairs.setPlaceholderText("BTC/USDT,ETH/USDT")
        pairs_layout.addWidget(self.hyperopt_pairs)
        
        config_layout.addLayout(pairs_layout)

        # Options
        options_layout = QHBoxLayout()
        options_layout.addWidget(QLabel("Epochs:"))
        
        self.hyperopt_epochs = QLineEdit()
        self.hyperopt_epochs.setPlaceholderText("100")
        options_layout.addWidget(self.hyperopt_epochs)
        
        options_layout.addWidget(QLabel("Jobs:"))
        
        self.hyperopt_jobs = QLineEdit()
        self.hyperopt_jobs.setPlaceholderText("-1 (tous les cores)")
        options_layout.addWidget(self.hyperopt_jobs)
        
        config_layout.addLayout(options_layout)

        # Espace de recherche
        search_space_layout = QHBoxLayout()
        search_space_layout.addWidget(QLabel("Espace de recherche:"))
        
        self.hyperopt_search_space = QComboBox()
        self.hyperopt_search_space.addItems(["default", "small", "all", "custom"])
        search_space_layout.addWidget(self.hyperopt_search_space)
        
        config_layout.addLayout(search_space_layout)

        layout.addWidget(config_group)

        # Groupe Exécution
        execution_group = QGroupBox("Exécution")
        execution_layout = QVBoxLayout(execution_group)

        # Barre de progression
        self.hyperopt_progress = QProgressBar()
        execution_layout.addWidget(self.hyperopt_progress)

        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.btn_run_hyperopt = QPushButton("Lancer Hyperopt")
        self.btn_run_hyperopt.clicked.connect(self.run_hyperopt)
        buttons_layout.addWidget(self.btn_run_hyperopt)
        
        self.btn_stop_hyperopt = QPushButton("Arrêter")
        self.btn_stop_hyperopt.clicked.connect(self.stop_hyperopt)
        self.btn_stop_hyperopt.setEnabled(False)
        buttons_layout.addWidget(self.btn_stop_hyperopt)
        
        self.btn_show_best = QPushButton("Afficher meilleurs")
        self.btn_show_best.clicked.connect(self.show_best_hyperopt)
        self.btn_show_best.setEnabled(False)
        buttons_layout.addWidget(self.btn_show_best)
        
        execution_layout.addLayout(buttons_layout)

        # Résultats
        results_layout = QHBoxLayout()
        
        self.hyperopt_results = QTextEdit()
        self.hyperopt_results.setReadOnly(True)
        results_layout.addWidget(self.hyperopt_results)
        
        execution_layout.addLayout(results_layout)

        layout.addWidget(execution_group)

        self.tab_widget.addTab(tab, "Hyperopt")

    def setup_utilities_tab(self):
        """Onglet Utilitaires"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Groupe Commandes personnalisées
        custom_cmd_group = QGroupBox("Commandes personnalisées")
        custom_cmd_layout = QVBoxLayout(custom_cmd_group)

        # Sélection de commande
        cmd_select_layout = QHBoxLayout()
        cmd_select_layout.addWidget(QLabel("Commande:"))
        
        self.custom_cmd_combo = QComboBox()
        self.custom_cmd_combo.setEditable(True)
        self.custom_cmd_combo.setMinimumWidth(400)
        cmd_select_layout.addWidget(self.custom_cmd_combo)
        
        self.btn_save_cmd = QPushButton("Enregistrer")
        self.btn_save_cmd.clicked.connect(self.save_custom_command)
        cmd_select_layout.addWidget(self.btn_save_cmd)
        
        custom_cmd_layout.addLayout(cmd_select_layout)

        # Boutons d'exécution
        cmd_exec_layout = QHBoxLayout()
        
        self.btn_exec_cmd = QPushButton("Exécuter")
        self.btn_exec_cmd.clicked.connect(self.execute_custom_command)
        cmd_exec_layout.addWidget(self.btn_exec_cmd)
        
        self.btn_stop_cmd = QPushButton("Arrêter")
        self.btn_stop_cmd.clicked.connect(self.stop_custom_command)
        self.btn_stop_cmd.setEnabled(False)
        cmd_exec_layout.addWidget(self.btn_stop_cmd)
        
        custom_cmd_layout.addLayout(cmd_exec_layout)

        # Liste des commandes favorites
        self.favorite_commands_table = QTableWidget()
        self.favorite_commands_table.setColumnCount(3)
        self.favorite_commands_table.setHorizontalHeaderLabels(["Nom", "Commande", "Actions"])
        self.favorite_commands_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.favorite_commands_table.setSelectionBehavior(QTableWidget.SelectRows)
        custom_cmd_layout.addWidget(self.favorite_commands_table)

        layout.addWidget(custom_cmd_group)

        # Groupe Historique
        history_group = QGroupBox("Historique des commandes")
        history_layout = QVBoxLayout(history_group)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Date", "Commande", "Statut", "Actions"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        history_layout.addWidget(self.history_table)

        layout.addWidget(history_group)

        self.tab_widget.addTab(tab, "Utilitaires")

    def setup_tray_icon(self):
        """Configuration de l'icône de la barre système"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("applications-internet"))

        tray_menu = QMenu()
        
        show_action = QAction("Afficher", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Masquer", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def load_configurations(self):
        """Charge les configurations depuis la base de données"""
        self.config_combo.clear()
        configurations = self.db.get_configurations()
        
        for config in configurations:
            self.config_combo.addItem(config[1], config[0])  # name as text, id as data
        
        if configurations:
            self.current_config = configurations[0]
            self.config_combo.setCurrentIndex(0)
            self.update_configuration_info()

    def update_configuration_info(self):
        """Met à jour les informations de configuration"""
        if not self.current_config:
            return
            
        # Active/désactive les boutons selon le type de configuration
        is_docker = self.current_config[2] == 'docker'
        
        # Met à jour l'interface en fonction de la configuration
        self.status_bar.showMessage(f"Configuration chargée: {self.current_config[1]}")

    def config_changed(self, index):
        """Appelé quand la configuration sélectionnée change"""
        if index >= 0:
            config_id = self.config_combo.itemData(index)
            configurations = self.db.get_configurations()
            self.current_config = next((c for c in configurations if c[0] == config_id), None)
            self.update_configuration_info()

    def add_configuration(self):
        """Ajoute une nouvelle configuration"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter une configuration")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        name_edit = QLineEdit()
        form_layout.addRow("Nom:", name_edit)
        
        type_combo = QComboBox()
        type_combo.addItems(["docker", "native"])
        form_layout.addRow("Type:", type_combo)
        
        path_edit = QLineEdit()
        form_layout.addRow("Chemin:", path_edit)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(lambda: self.browse_config_path(path_edit))
        form_layout.addRow(browse_btn)
        
        layout.addLayout(form_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text().strip()
            config_type = type_combo.currentText()
            path = path_edit.text().strip()
            
            if name and path:
                try:
                    # Lire le fichier de configuration
                    with open(path, 'r') as f:
                        config_content = json.load(f)
                    
                    self.db.save_configuration(name, config_type, path, config_content)
                    self.load_configurations()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier de configuration: {str(e)}")

    def browse_config_path(self, path_edit):
        """Ouvre un dialogue pour sélectionner le fichier de configuration"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner le fichier de configuration", 
            "", 
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if file_path:
            path_edit.setText(file_path)

    def edit_configuration(self):
        """Modifie la configuration sélectionnée"""
        if not self.current_config:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier la configuration")
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        name_edit = QLineEdit(self.current_config[1])
        form_layout.addRow("Nom:", name_edit)
        
        type_combo = QComboBox()
        type_combo.addItems(["docker", "native"])
        type_combo.setCurrentText(self.current_config[2])
        form_layout.addRow("Type:", type_combo)
        
        path_edit = QLineEdit(self.current_config[3])
        form_layout.addRow("Chemin:", path_edit)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(lambda: self.browse_config_path(path_edit))
        form_layout.addRow(browse_btn)
        
        layout.addLayout(form_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text().strip()
            config_type = type_combo.currentText()
            path = path_edit.text().strip()
            
            if name and path:
                try:
                    # Lire le fichier de configuration
                    with open(path, 'r') as f:
                        config_content = json.load(f)
                    
                    self.db.save_configuration(name, config_type, path, config_content)
                    self.load_configurations()
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier de configuration: {str(e)}")

    def remove_configuration(self):
        """Supprime la configuration sélectionnée"""
        if not self.current_config:
            return
            
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer la configuration '{self.current_config[1]}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_configuration(self.current_config[0])
            self.load_configurations()

    def start_freqtrade(self):
        """Démarre FreqTrade"""
        if not self.current_config:
            QMessageBox.warning(self, "Erreur", "Aucune configuration sélectionnée")
            return
            
        if self.current_process:
            QMessageBox.warning(self, "Erreur", "Une commande est déjà en cours d'exécution")
            return
            
        if self.current_config[2] == 'docker':
            command = f"docker-compose -f {self.current_config[3]} up"
        else:
            command = f"freqtrade trade --config {self.current_config[3]}"
        
        self.log_output.append(f">>> Démarrage de FreqTrade: {command}")
        
        self.current_process = FreqTradeProcessThread(command)
        self.current_process.output_signal.connect(self.handle_process_output)
        self.current_process.finished_signal.connect(self.handle_process_finished)
        self.current_process.start()
        
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_restart.setEnabled(False)
        
        self.db.save_command_history(command, -1, "En cours d'exécution")

    def stop_freqtrade(self):
        """Arrête FreqTrade"""
        if not self.current_process:
            return
            
        self.log_output.append(">>> Arrêt de FreqTrade en cours...")
        self.current_process.stop()
        self.btn_stop.setEnabled(False)

    def restart_freqtrade(self):
        """Redémarre FreqTrade"""
        self.stop_freqtrade()
        QTimer.singleShot(2000, self.start_freqtrade)

    def check_status(self):
        """Vérifie le statut de FreqTrade"""
        if not self.current_config:
            QMessageBox.warning(self, "Erreur", "Aucune configuration sélectionnée")
            return
            
        if self.current_config[2] == 'docker':
            command = f"docker-compose -f {self.current_config[3]} ps"
        else:
            command = "freqtrade list-workers"
        
        self.log_output.append(f">>> Vérification du statut: {command}")
        
        process = FreqTradeProcessThread(command)
        process.output_signal.connect(self.handle_process_output)
        process.finished_signal.connect(lambda x: self.log_output.append(">>> Vérification terminée"))
        process.start()

    def start_strategy(self):
        """Démarre une stratégie spécifique"""
        strategy = self.strategy_combo.currentText()
        if not strategy:
            return
            
        command = f"freqtrade trade --strategy {strategy}"
        self.execute_command(command)

    def stop_strategy(self):
        """Arrête la stratégie en cours"""
        self.execute_command("freqtrade stop")

    def refresh_strategies(self):
        """Rafraîchit la liste des stratégies disponibles"""
        if not self.current_config:
            return
            
        config_path = os.path.dirname(self.current_config[3])
        strategies_path = os.path.join(config_path, "strategies")
        
        if os.path.exists(strategies_path):
            strategies = []
            for file in os.listdir(strategies_path):
                if file.endswith(".py") and not file.startswith("_"):
                    strategies.append(file[:-3])
            
            self.strategy_combo.clear()
            self.strategy_combo.addItems(strategies)
            
            self.backtest_strategy_combo.clear()
            self.backtest_strategy_combo.addItems(strategies)
            
            self.hyperopt_strategy_combo.clear()
            self.hyperopt_strategy_combo.addItems(strategies)

    def browse_pairs_file(self):
        """Ouvre un dialogue pour sélectionner le fichier des paires"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner le fichier des paires", 
            "", 
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        if file_path:
            self.pairs_file_edit.setText(file_path)

    def load_pairs(self):
        """Charge les paires depuis le fichier"""
        file_path = self.pairs_file_edit.text()
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "Erreur", "Fichier de paires invalide")
            return
            
        try:
            with open(file_path, 'r') as f:
                pairs_data = json.load(f)
                
            if 'exchange' in pairs_data and 'pair_whitelist' in pairs_data['exchange']:
                pairs = pairs_data['exchange']['pair_whitelist']
                
                self.pairs_table.setRowCount(len(pairs))
                for i, pair in enumerate(pairs):
                    self.pairs_table.setItem(i, 0, QTableWidgetItem(pair))
                    self.pairs_table.setItem(i, 1, QTableWidgetItem("Non chargée"))
                    
                    btn = QPushButton("Activer")
                    btn.clicked.connect(lambda _, p=pair: self.toggle_pair(p))
                    self.pairs_table.setCellWidget(i, 2, btn)
                
                self.btn_update_pairs.setEnabled(True)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les paires: {str(e)}")

    def toggle_pair(self, pair):
        """Active/désactive une paire"""
        # Implémentez la logique pour activer/désactiver une paire
        pass

    def update_pairs(self):
        """Met à jour les paires dans la configuration"""
        # Implémentez la logique pour mettre à jour les paires
        pass

    def run_backtest(self):
        """Exécute un backtest"""
        strategy = self.backtest_strategy_combo.currentText()
        if not strategy:
            QMessageBox.warning(self, "Erreur", "Aucune stratégie sélectionnée")
            return
            
        interval = self.backtest_interval_combo.currentText()
        start_date = self.backtest_start_date.text()
        end_date = self.backtest_end_date.text()
        pairs = self.backtest_pairs.text()
        
        if not start_date:
            QMessageBox.warning(self, "Erreur", "Date de début requise")
            return
            
        command = f"freqtrade backtesting --strategy {strategy} --timerange {start_date}"
        
        if end_date:
            command += f"-{end_date}"
            
        command += f" --timeframe {interval}"
        
        if pairs:
            command += f" --pairs {pairs}"
            
        if self.backtest_live.isChecked():
            command += " --live"
            
        if self.backtest_enable_profit.isChecked():
            command += " --enable-protections"
            
        if self.backtest_timeframe_detail.isChecked():
            command += " --timeframe-detail"
            
        self.execute_command(command)

    def stop_backtest(self):
        """Arrête le backtest en cours"""
        if self.current_process:
            self.current_process.stop()

    def export_backtest(self):
        """Exporte les résultats du backtest"""
        # Implémentez la logique d'exportation
        pass

    def run_hyperopt(self):
        """Exécute une hyperoptimisation"""
        strategy = self.hyperopt_strategy_combo.currentText()
        if not strategy:
            QMessageBox.warning(self, "Erreur", "Aucune stratégie sélectionnée")
            return
            
        interval = self.hyperopt_interval_combo.currentText()
        start_date = self.hyperopt_start_date.text()
        end_date = self.hyperopt_end_date.text()
        pairs = self.hyperopt_pairs.text()
        epochs = self.hyperopt_epochs.text() or "100"
        jobs = self.hyperopt_jobs.text() or "-1"
        search_space = self.hyperopt_search_space.currentText()
        
        if not start_date:
            QMessageBox.warning(self, "Erreur", "Date de début requise")
            return
            
        command = f"freqtrade hyperopt --strategy {strategy} --timerange {start_date}"
        
        if end_date:
            command += f"-{end_date}"
            
        command += f" --timeframe {interval} --epochs {epochs} --job-workers {jobs}"
        
        if pairs:
            command += f" --pairs {pairs}"
            
        if search_space != "default":
            command += f" --spaces {search_space}"
            
        self.execute_command(command)

    def stop_hyperopt(self):
        """Arrête l'hyperoptimisation en cours"""
        if self.current_process:
            self.current_process.stop()

    def show_best_hyperopt(self):
        """Affiche les meilleurs résultats d'hyperoptimisation"""
        # Implémentez la logique pour afficher les meilleurs résultats
        pass

    def save_custom_command(self):
        """Enregistre une commande personnalisée"""
        name = self.custom_cmd_combo.currentText()
        command = self.custom_cmd_combo.currentText()
        
        if not name or not command:
            QMessageBox.warning(self, "Erreur", "Nom et commande requis")
            return
            
        self.db.save_favorite_command(name, command)
        self.update_favorite_commands()

    def execute_custom_command(self):
        """Exécute une commande personnalisée"""
        command = self.custom_cmd_combo.currentText()
        if not command:
            return
            
        self.execute_command(command)

    def stop_custom_command(self):
        """Arrête la commande personnalisée en cours"""
        if self.current_process:
            self.current_process.stop()

    def update_favorite_commands(self):
        """Met à jour la liste des commandes favorites"""
        favorites = self.db.get_favorite_commands()
        self.favorite_commands_table.setRowCount(len(favorites))
        
        for i, fav in enumerate(favorites):
            self.favorite_commands_table.setItem(i, 0, QTableWidgetItem(fav[1]))  # name
            self.favorite_commands_table.setItem(i, 1, QTableWidgetItem(fav[2]))  # command
            
            btn = QPushButton("Supprimer")
            btn.clicked.connect(lambda _, id=fav[0]: self.delete_favorite_command(id))
            self.favorite_commands_table.setCellWidget(i, 2, btn)

    def delete_favorite_command(self, command_id):
        """Supprime une commande favorite"""
        self.db.delete_favorite_command(command_id)
        self.update_favorite_commands()

    def update_command_history(self):
        """Met à jour l'historique des commandes"""
        history = self.db.get_command_history()
        self.history_table.setRowCount(len(history))
        
        for i, item in enumerate(history):
            self.history_table.setItem(i, 0, QTableWidgetItem(item[3].strftime("%Y-%m-%d %H:%M:%S")))  # date
            self.history_table.setItem(i, 1, QTableWidgetItem(item[1]))  # command
            self.history_table.setItem(i, 2, QTableWidgetItem(str(item[2]) if item[2] != -1 else "En cours"))  # status
            
            btn = QPushButton("Voir")
            btn.clicked.connect(lambda _, cmd=item[1]: self.show_command_details(cmd))
            self.history_table.setCellWidget(i, 3, btn)

    def show_command_details(self, command):
        """Affiche les détails d'une commande"""
        # Implémentez la logique pour afficher les détails
        pass

    def execute_command(self, command):
        """Exécute une commande FreqTrade générique"""
        if not self.current_config:
            QMessageBox.warning(self, "Erreur", "Aucune configuration sélectionnée")
            return
            
        if self.current_process:
            QMessageBox.warning(self, "Erreur", "Une commande est déjà en cours d'exécution")
            return
            
        self.log_output.append(f">>> Exécution: {command}")
        
        self.current_process = FreqTradeProcessThread(command)
        self.current_process.output_signal.connect(self.handle_process_output)
        self.current_process.finished_signal.connect(self.handle_process_finished)
        self.current_process.start()
        
        self.db.save_command_history(command, -1, "En cours d'exécution")

    def handle_process_output(self, output):
        """Gère la sortie du processus"""
        self.log_output.append(output)
        self.log_output.moveCursor(QTextCursor.End)

    def handle_process_finished(self, exit_code):
        """Gère la fin du processus"""
        self.log_output.append(f">>> Processus terminé avec le code: {exit_code}")
        self.current_process = None
        
        # Mettre à jour l'historique
        self.update_command_history()
        
        # Réactiver les boutons appropriés
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_restart.setEnabled(True)

    def update_status(self):
        """Met à jour le statut périodiquement"""
        if self.current_config:
            self.check_status()

    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.current_process:
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                "Un processus est en cours d'exécution. Voulez-vous vraiment quitter?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
            self.current_process.stop()
        
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Définir une palette sombre pour un look moderne
    palette = app.palette()
    palette.setColor(palette.Window, QColor(53, 53, 53))
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, QColor(25, 25, 25))
    palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, QColor(53, 53, 53))
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Link, QColor(42, 130, 218))
    palette.setColor(palette.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    window = FreqTradeManagerApp()
    window.show()
    
    sys.exit(app.exec_())