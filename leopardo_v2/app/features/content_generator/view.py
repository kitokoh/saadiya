import sys
import os
import sqlite3
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QListWidget, QTreeView, QLabel, QLineEdit,
                            QTextEdit, QFileSystemModel, QTabWidget, QSplitter, QToolBar,
                            QStatusBar, QDialog, QFormLayout, QComboBox, QCheckBox,
                            QMessageBox, QInputDialog, QFileDialog, QMenu, QAction,
                            QStackedWidget, QGroupBox, QScrollArea, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QMimeData, QUrl, QDateTime
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QPixmap, QDrag, QColor
import webbrowser
import subprocess
from pathlib import Path
import mimetypes

class ContentGeneratorWidget(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Ultimate Content Creation Hub Pro")

        self.current_project = None
        self.current_content_type = None
        self.quick_access_tools = []
        self.project_folder = str(Path.home() / "ContentHub")

        self.init_db()
        self.init_ui()

        self.check_default_folders()
        self.initial_load()

    def init_db(self):
        """Initialise la base de données avec des tables étendues"""
        self.db = self.db_manager.db
        cursor = self.db.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        content_type TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'draft',
                        cover_image TEXT,
                        color_code TEXT,
                        tags TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS resources (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        url TEXT,
                        path TEXT,
                        type TEXT NOT NULL,
                        category TEXT,
                        description TEXT,
                        is_favorite BOOLEAN DEFAULT 0,
                        last_used DATETIME,
                        icon_path TEXT,
                        launch_command TEXT,
                        metadata TEXT,
                        api_key TEXT DEFAULT '')''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS content_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_id INTEGER,
                        title TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        content_type TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        modified_at DATETIME,
                        size INTEGER,
                        tags TEXT,
                        metadata TEXT,
                        folder_path TEXT,
                        FOREIGN KEY(project_id) REFERENCES projects(id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS folder_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        structure TEXT NOT NULL,
                        content_type TEXT,
                        is_default BOOLEAN DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS workflows (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        steps TEXT NOT NULL,
                        content_type TEXT,
                        last_run DATETIME)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS content_hub_settings (
                        key TEXT PRIMARY KEY,
                        value TEXT)''')

        self.insert_default_data(cursor)
        self.db.commit()

    def insert_default_data(self, cursor):
        """Insère les données par défaut (templates, ressources communes)"""
        cursor.execute("SELECT COUNT(*) FROM folder_templates")
        if cursor.fetchone()[0] == 0:
            default_templates = [
                ('Vidéo YouTube', '{"root": "Projet", "folders": ["1. Assets", "2. Séquences", "3. Exports", "4. Scripts"]}', 'video', 1),
                ('Article Blog', '{"root": "Projet", "folders": ["1. Recherche", "2. Brouillons", "3. Images", "4. Final"]}', 'text', 1),
            ]
            cursor.executemany("INSERT INTO folder_templates (name, structure, content_type, is_default) VALUES (?, ?, ?, ?)", default_templates)
            common_resources = [
                ('ChatGPT', 'https://chat.openai.com', '', 'ai', 'text-generation', 'Outil de génération de texte IA', 1, None, '', '{"command": "web", "url": "https://chat.openai.com"}', '{}', ''),
                ('Canva', 'https://www.canva.com', '', 'online-tool', 'graphic-design', 'Outil de design graphique', 1, None, '', '{"command": "web", "url": "https://www.canva.com"}', '{}', ''),
            ]
            cursor.executemany('''INSERT INTO resources
                              (name, url, path, type, category, description, is_favorite, last_used, icon_path, launch_command, metadata, api_key)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', common_resources)
            default_settings = [('default_project_folder', str(Path.home() / "ContentHub")), ('dark_mode', '1')]
            cursor.executemany("INSERT INTO content_hub_settings (key, value) VALUES (?, ?)", default_settings)

    def check_default_folders(self):
        """Vérifie et crée les dossiers par défaut si nécessaire"""
        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)

    def initial_load(self):
        """Charge les données initiales après le démarrage de l'UI"""
        self.load_projects()
        self.load_resources()
        self.load_content_items()
        self.load_workflows()
        self.apply_settings()

    def apply_settings(self):
        """Applique les paramètres stockés"""
        cursor = self.db.cursor()
        cursor.execute("SELECT value FROM content_hub_settings WHERE key='dark_mode'")
        dark_mode = cursor.fetchone()
        if dark_mode and dark_mode[0] == '1':
            self.set_dark_theme()

    def set_dark_theme(self):
        """Applique un thème sombre au widget"""
        dark_palette = self.palette()
        dark_palette.setColor(dark_palette.Window, QColor(53, 53, 53))
        dark_palette.setColor(dark_palette.WindowText, Qt.white)
        dark_palette.setColor(dark_palette.Base, QColor(25, 25, 25))
        dark_palette.setColor(dark_palette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(dark_palette.ToolTipBase, Qt.white)
        dark_palette.setColor(dark_palette.ToolTipText, Qt.white)
        dark_palette.setColor(dark_palette.Text, Qt.white)
        dark_palette.setColor(dark_palette.Button, QColor(53, 53, 53))
        dark_palette.setColor(dark_palette.ButtonText, Qt.white)
        dark_palette.setColor(dark_palette.BrightText, Qt.red)
        dark_palette.setColor(dark_palette.Link, QColor(42, 130, 218))
        dark_palette.setColor(dark_palette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(dark_palette.HighlightedText, Qt.black)
        self.setPalette(dark_palette)
        self.setAutoFillBackground(True)

    def init_ui(self):
        """Initialise l'interface utilisateur complète"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        self.side_panel = self.create_side_panel()
        main_layout.addWidget(self.side_panel, stretch=1)

        self.main_tabs = QTabWidget()
        self.main_tabs.setDocumentMode(True)
        self.main_tabs.setTabsClosable(True)
        self.main_tabs.tabCloseRequested.connect(self.close_tab)

        self.setup_dashboard_tab()
        self.setup_projects_tab()
        self.setup_resources_tab()
        self.setup_organizer_tab()
        self.setup_workflows_tab()

        main_layout.addWidget(self.main_tabs, stretch=4)
        self.connect_signals()

    def create_side_panel(self):
        """Crée le panneau latéral avec projets et vue des dossiers"""
        side_panel = QWidget()
        layout = QVBoxLayout(side_panel)
        layout.setContentsMargins(0,0,0,0)
        side_tabs = QTabWidget()
        side_tabs.setTabPosition(QTabWidget.West)

        projects_tab = QWidget()
        projects_layout = QVBoxLayout(projects_tab)
        self.projects_list = QListWidget()
        projects_filter = QLineEdit()
        projects_filter.setPlaceholderText("Filtrer...")
        projects_filter.textChanged.connect(self.filter_projects)
        projects_layout.addWidget(projects_filter)
        projects_layout.addWidget(self.projects_list)
        projects_tab.setLayout(projects_layout)

        folders_tab = QWidget()
        folders_layout = QVBoxLayout(folders_tab)
        self.folder_tree = QTreeView()
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath(self.project_folder)
        self.folder_tree.setModel(self.folder_model)
        self.folder_tree.setRootIndex(self.folder_model.index(self.project_folder))
        folders_layout.addWidget(self.folder_tree)
        folders_tab.setLayout(folders_layout)

        side_tabs.addTab(projects_tab, "Projets")
        side_tabs.addTab(folders_tab, "Dossiers")
        layout.addWidget(side_tabs)
        return side_panel

    def setup_dashboard_tab(self):
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)
        layout.addWidget(QLabel("<h1>Dashboard</h1>"))
        dashboard_tab.setLayout(layout)
        self.main_tabs.addTab(dashboard_tab, "Dashboard")

    def setup_projects_tab(self):
        projects_tab = QWidget()
        layout = QVBoxLayout(projects_tab)
        self.projects_table = QTreeView()
        self.projects_model = QStandardItemModel()
        self.projects_model.setHorizontalHeaderLabels(["Nom", "Type", "Statut", "Dernière modification"])
        self.projects_table.setModel(self.projects_model)
        layout.addWidget(self.projects_table)
        projects_tab.setLayout(layout)
        self.main_tabs.addTab(projects_tab, "Projets")

    def setup_resources_tab(self):
        resources_tab = QWidget()
        layout = QVBoxLayout(resources_tab)
        self.resources_list = QListWidget()
        self.resources_list.setViewMode(QListWidget.IconMode)
        layout.addWidget(self.resources_list)
        resources_tab.setLayout(layout)
        self.main_tabs.addTab(resources_tab, "Ressources")

    def setup_organizer_tab(self):
        organizer_tab = QWidget()
        layout = QVBoxLayout(organizer_tab)
        self.content_table = QTreeView()
        self.content_model = QStandardItemModel()
        self.content_model.setHorizontalHeaderLabels(["Nom", "Type", "Projet", "Date"])
        self.content_table.setModel(self.content_model)
        layout.addWidget(self.content_table)
        organizer_tab.setLayout(layout)
        self.main_tabs.addTab(organizer_tab, "Organisation")

    def setup_workflows_tab(self):
        workflows_tab = QWidget()
        layout = QVBoxLayout(workflows_tab)
        self.workflows_list = QListWidget()
        layout.addWidget(self.workflows_list)
        workflows_tab.setLayout(layout)
        self.main_tabs.addTab(workflows_tab, "Workflows")

    def connect_signals(self):
        self.projects_list.itemDoubleClicked.connect(self.open_project_from_list)

    def close_tab(self, index):
        if index > 0: # Don't close dashboard
            self.main_tabs.removeTab(index)

    def load_projects(self):
        self.projects_list.clear()
        self.projects_model.clear()
        self.projects_model.setHorizontalHeaderLabels(["Nom", "Type", "Statut", "Dernière modification"])
        cursor = self.db.cursor()
        cursor.execute("SELECT name, content_type, status, updated_at FROM projects ORDER BY updated_at DESC")
        for row in cursor.fetchall():
            self.projects_list.addItem(row[0])
            self.projects_model.appendRow([QStandardItem(str(i)) for i in row])

    def load_resources(self):
        self.resources_list.clear()
        cursor = self.db.cursor()
        cursor.execute("SELECT name, description, icon_path FROM resources ORDER BY name")
        for row in cursor.fetchall():
            item = QListWidgetItem(QIcon(row[2] if row[2] else ''), row[0])
            item.setToolTip(row[1])
            self.resources_list.addItem(item)

    def load_content_items(self):
        self.content_model.clear()
        self.content_model.setHorizontalHeaderLabels(["Nom", "Type", "Projet", "Date"])
        cursor = self.db.cursor()
        cursor.execute("""SELECT c.title, c.content_type, p.name, c.created_at
                          FROM content_items c LEFT JOIN projects p ON c.project_id = p.id
                          ORDER BY c.created_at DESC""")
        for row in cursor.fetchall():
            self.content_model.appendRow([QStandardItem(str(i)) for i in row])

    def load_workflows(self):
        self.workflows_list.clear()
        cursor = self.db.cursor()
        cursor.execute("SELECT name FROM workflows")
        for row in cursor.fetchall():
            self.workflows_list.addItem(row[0])

    def filter_projects(self, text):
        for i in range(self.projects_list.count()):
            item = self.projects_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def open_project_from_list(self, item):
        project_name = item.text()
        # Check if tab is already open
        for i in range(self.main_tabs.count()):
            if self.main_tabs.tabText(i) == project_name:
                self.main_tabs.setCurrentIndex(i)
                return

        # Create a new tab for the project
        project_widget = QLabel(f"Project Details for {project_name}") # Placeholder
        self.main_tabs.addTab(project_widget, project_name)
        self.main_tabs.setCurrentWidget(project_widget)
