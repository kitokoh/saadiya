import sys
import os
import sqlite3
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
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

class ContentCreationHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate Content Creation Hub Pro")
        self.setGeometry(100, 50, 1600, 950)

        # Configuration initiale
        self.current_project = None
        self.current_content_type = None
        self.quick_access_tools = []
        self.project_folder = str(Path.home() / "ContentHub")

        # Initialisation des composants
        self.init_db()
        self.init_ui()
        self.load_state()

        # Vérification des dossiers par défaut
        self.check_default_folders()

        # Charger les données initiales
        QTimer.singleShot(100, self.initial_load)

    def init_db(self):
        """Initialise la base de données avec des tables étendues"""
        self.db = sqlite3.connect(str(Path(self.project_folder) / 'content_hub_ultimate.db'))
        cursor = self.db.cursor()

        # Table des projets
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

        # Table des ressources
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

        # Table des éléments de contenu
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

        # Table des templates d'organisation
        cursor.execute('''CREATE TABLE IF NOT EXISTS folder_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        structure TEXT NOT NULL,
                        content_type TEXT,
                        is_default BOOLEAN DEFAULT 0)''')

        # Table des workflows
        cursor.execute('''CREATE TABLE IF NOT EXISTS workflows (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        steps TEXT NOT NULL,
                        content_type TEXT,
                        last_run DATETIME)''')

        # Table des paramètres
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT)''')

        # Insertion des données par défaut si nécessaire
        self.insert_default_data(cursor)
        self.db.commit()

    def insert_default_data(self, cursor):
        """Insère les données par défaut (templates, ressources communes)"""
        # Vérifier si les données existent déjà
        cursor.execute("SELECT COUNT(*) FROM folder_templates")
        if cursor.fetchone()[0] == 0:
            # Templates d'organisation par défaut
            default_templates = [
                ('Vidéo YouTube', '{"root": "Projet", "folders": ["1. Assets", "2. Séquences", "3. Exports", "4. Scripts"]}', 'video', 1),
                ('Article Blog', '{"root": "Projet", "folders": ["1. Recherche", "2. Brouillons", "3. Images", "4. Final"]}', 'text', 1),
                ('Podcast', '{"root": "Projet", "folders": ["1. Enregistrements", "2. Montage", "3. Musique", "4. Export"]}', 'audio', 1),
                ('Réseaux Sociaux', '{"root": "Projet", "folders": ["1. Contenu", "2. Visuels", "3. Captions", "4. Planification"]}', 'social', 1)
            ]
            cursor.executemany("INSERT INTO folder_templates (name, structure, content_type, is_default) VALUES (?, ?, ?, ?)", default_templates)

            # Ressources communes
            common_resources = [
                ('ChatGPT', 'https://chat.openai.com', '', 'ai', 'text-generation', 'Outil de génération de texte IA', 1, None, '', '{"command": "web", "url": "https://chat.openai.com"}', '{}', ''),
                ('Midjourney', 'https://www.midjourney.com', '', 'ai', 'image-generation', 'Générateur d\'images IA', 1, None, '', '{"command": "web", "url": "https://www.midjourney.com"}', '{}', ''),
                ('Adobe Premiere', '', 'C:\\Program Files\\Adobe\\Premiere Pro\\', 'software', 'video-editing', 'Logiciel de montage vidéo', 1, None, '', '{"command": "exe", "path": "C:\\\\Program Files\\\\Adobe\\\\Premiere Pro\\\\Adobe Premiere Pro.exe"}', '{}', ''),
                ('Canva', 'https://www.canva.com', '', 'online-tool', 'graphic-design', 'Outil de design graphique', 1, None, '', '{"command": "web", "url": "https://www.canva.com"}', '{}', ''),
                ('OBS Studio', '', 'C:\\Program Files\\obs-studio\\', 'software', 'video-recording', 'Logiciel d\'enregistrement vidéo', 1, None, '', '{"command": "exe", "path": "C:\\\\Program Files\\\\obs-studio\\\\bin\\\\64bit\\\\obs64.exe"}', '{}', '')
            ]
            cursor.executemany('''INSERT INTO resources
                              (name, url, path, type, category, description, is_favorite, last_used, icon_path, launch_command, metadata, api_key)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', common_resources)

            # Paramètres par défaut
            default_settings = [
                ('default_project_folder', str(Path.home() / "ContentHub")),
                ('dark_mode', '1'),
                ('auto_organize', '1'),
                ('backup_enabled', '1')
            ]
            cursor.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", default_settings)

    def check_default_folders(self):
        """Vérifie et crée les dossiers par défaut si nécessaire"""
        default_folders = [
            'Projects',
            'Resources',
            'Templates',
            'Exports',
            'Backups'
        ]

        if not os.path.exists(self.project_folder):
            os.makedirs(self.project_folder)

        for folder in default_folders:
            path = os.path.join(self.project_folder, folder)
            if not os.path.exists(path):
                os.makedirs(path)

    def initial_load(self):
        """Charge les données initiales après le démarrage de l'UI"""
        self.load_projects()
        self.load_resources()
        self.load_content_items()
        self.load_workflows()
        self.load_recent_activity()

        # Appliquer les paramètres
        self.apply_settings()

    def apply_settings(self):
        """Applique les paramètres stockés"""
        cursor = self.db.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='dark_mode'")
        dark_mode = cursor.fetchone()
        if dark_mode and dark_mode[0] == '1':
            self.set_dark_theme()

    def set_dark_theme(self):
        """Applique un thème sombre à l'application"""
        dark_palette = QApplication.palette()
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
        QApplication.setPalette(dark_palette)

        self.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
            QMenuBar::item:selected {
                background: #2a82da;
            }
        """)

    def init_ui(self):
        """Initialise l'interface utilisateur complète"""
        # Style global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0e0e0, stop:1 #c0c0c0);
                border-bottom: 1px solid #aaa;
                spacing: 5px;
                padding: 3px;
            }
            QToolButton {
                padding: 5px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background: rgba(0,0,0,0.1);
            }
            QStatusBar {
                background: #e0e0e0;
                border-top: 1px solid #aaa;
            }
            QListWidget, QTreeView {
                background: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: white;
            }
            QTabBar::tab {
                padding: 8px;
                background: #e0e0e0;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                margin-bottom: -1px;
            }
        """)

        # Barre d'outils principale
        self.init_toolbars()

        # Zone centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Panneau latéral gauche
        self.side_panel = self.create_side_panel()
        main_layout.addWidget(self.side_panel, stretch=1)

        # Zone de contenu principale (avec onglets)
        self.main_tabs = QTabWidget()
        self.main_tabs.setDocumentMode(True)
        self.main_tabs.setTabsClosable(True)
        self.main_tabs.tabCloseRequested.connect(self.close_tab)

        # Onglets principaux
        self.setup_dashboard_tab()
        self.setup_projects_tab()
        self.setup_resources_tab()
        self.setup_organizer_tab()
        self.setup_workflows_tab()

        main_layout.addWidget(self.main_tabs, stretch=4)

        # Barre d'état
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt", 3000)

        # Menu contextuel
        self.setup_context_menus()

        # Connecter les signaux
        self.connect_signals()

    def init_toolbars(self):
        """Initialise les barres d'outils"""
        # Barre d'outils principale
        main_toolbar = QToolBar("Main Toolbar")
        main_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, main_toolbar)

        # Actions principales
        new_project_action = QAction(QIcon.fromTheme("document-new"), "Nouveau Projet", self)
        new_project_action.triggered.connect(self.create_new_project)
        main_toolbar.addAction(new_project_action)

        quick_access_menu = QMenu(self)
        quick_access_menu.addAction("IA Textuelle")
        quick_access_menu.addAction("IA Visuelle")
        quick_access_menu.addAction("Montage Vidéo")
        quick_access_menu.addSeparator()
        quick_access_menu.addAction("Configurer Accès Rapide...")

        quick_access_action = QAction(QIcon.fromTheme("starred"), "Accès Rapide", self)
        quick_access_action.setMenu(quick_access_menu)
        main_toolbar.addAction(quick_access_action)

        main_toolbar.addSeparator()

        import_action = QAction(QIcon.fromTheme("document-import"), "Importer", self)
        import_action.triggered.connect(self.import_content)
        main_toolbar.addAction(import_action)

        export_action = QAction(QIcon.fromTheme("document-export"), "Exporter", self)
        export_action.triggered.connect(self.export_content)
        main_toolbar.addAction(export_action)

        # Barre d'outils secondaire (formatting)
        format_toolbar = QToolBar("Formatting Toolbar")
        self.addToolBar(Qt.TopToolBarArea, format_toolbar)

        # Barre d'outils latérale (outils)
        tools_toolbar = QToolBar("Tools", self)
        tools_toolbar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.LeftToolBarArea, tools_toolbar)

        # Ajouter des boutons pour les outils fréquents
        ai_tools_button = QPushButton("Outils IA")
        ai_tools_button.setMenu(self.create_ai_tools_menu())
        tools_toolbar.addWidget(ai_tools_button)

        editing_tools_button = QPushButton("Édition")
        editing_tools_button.setMenu(self.create_editing_tools_menu())
        tools_toolbar.addWidget(editing_tools_button)

    def create_side_panel(self):
        """Crée le panneau latéral avec projets et vue des dossiers"""
        side_panel = QWidget()
        layout = QVBoxLayout(side_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Onglets du panneau latéral
        side_tabs = QTabWidget()
        side_tabs.setTabPosition(QTabWidget.West)

        # Onglet Projets
        projects_tab = QWidget()
        projects_layout = QVBoxLayout(projects_tab)

        self.projects_list = QListWidget()
        self.projects_list.setSelectionMode(QListWidget.SingleSelection)
        self.projects_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.projects_list.customContextMenuRequested.connect(self.show_project_context_menu)

        projects_filter = QLineEdit()
        projects_filter.setPlaceholderText("Filtrer les projets...")
        projects_filter.textChanged.connect(self.filter_projects)

        projects_layout.addWidget(projects_filter)
        projects_layout.addWidget(self.projects_list)

        # Onglet Dossiers
        folders_tab = QWidget()
        folders_layout = QVBoxLayout(folders_tab)

        self.folder_tree = QTreeView()
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath("")
        self.folder_tree.setModel(self.folder_model)
        self.folder_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.folder_tree.customContextMenuRequested.connect(self.show_folder_context_menu)

        folders_layout.addWidget(self.folder_tree)

        # Ajout des onglets
        side_tabs.addTab(projects_tab, "Projets")
        side_tabs.addTab(folders_tab, "Dossiers")

        layout.addWidget(side_tabs)

        return side_panel

    def setup_dashboard_tab(self):
        """Configure l'onglet Dashboard"""
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)

        # Section de bienvenue
        welcome_group = QGroupBox("Bienvenue dans votre Content Hub")
        welcome_layout = QVBoxLayout()

        welcome_label = QLabel("""
            <h1>Content Creation Hub</h1>
            <p>Votre plateforme centralisée pour la création et l'organisation de contenu</p>
        """)
        welcome_label.setAlignment(Qt.AlignCenter)

        welcome_layout.addWidget(welcome_label)
        welcome_group.setLayout(welcome_layout)

        # Section d'activité récente
        recent_group = QGroupBox("Activité Récente")
        recent_layout = QVBoxLayout()

        self.recent_list = QListWidget()
        self.load_recent_activity()

        recent_layout.addWidget(self.recent_list)
        recent_group.setLayout(recent_layout)

        # Section de statistiques
        stats_group = QGroupBox("Statistiques")
        stats_layout = QHBoxLayout()

        # Widgets de statistiques (simplifiés pour l'exemple)
        projects_stats = QLabel("<h3>Projets: 12</h3><p>5 en cours</p>")
        content_stats = QLabel("<h3>Contenus: 87</h3><p>Vidéos: 23</p>")
        resources_stats = QLabel("<h3>Ressources: 45</h3><p>Favoris: 8</p>")

        stats_layout.addWidget(projects_stats)
        stats_layout.addWidget(content_stats)
        stats_layout.addWidget(resources_stats)
        stats_group.setLayout(stats_layout)

        # Ajout au layout principal
        layout.addWidget(welcome_group)
        layout.addWidget(recent_group)
        layout.addWidget(stats_group)

        self.main_tabs.addTab(dashboard_tab, QIcon.fromTheme("go-home"), "Dashboard")

    def setup_projects_tab(self):
        """Configure l'onglet de gestion des projets"""
        self.projects_tab = QWidget()
        layout = QVBoxLayout(self.projects_tab)

        # Barre d'outils des projets
        project_toolbar = QToolBar()
        project_toolbar.setIconSize(QSize(20, 20))

        new_project_btn = QPushButton("Nouveau Projet")
        new_project_btn.clicked.connect(self.create_new_project)
        project_toolbar.addWidget(new_project_btn)

        delete_project_btn = QPushButton("Supprimer")
        delete_project_btn.clicked.connect(self.delete_project)
        project_toolbar.addWidget(delete_project_btn)

        layout.addWidget(project_toolbar)

        # Liste des projets avec détails
        self.projects_table = QTreeView()
        self.projects_model = QStandardItemModel()
        self.projects_model.setHorizontalHeaderLabels(["Nom", "Type", "Statut", "Dernière modification"])
        self.projects_table.setModel(self.projects_model)
        self.projects_table.setSelectionMode(QTreeView.SingleSelection)
        self.projects_table.setEditTriggers(QTreeView.NoEditTriggers)
        self.projects_table.doubleClicked.connect(self.open_project_details)

        layout.addWidget(self.projects_table)

        self.main_tabs.addTab(self.projects_tab, QIcon.fromTheme("folder"), "Projets")
        self.load_projects()

    def setup_resources_tab(self):
        """Configure l'onglet de gestion des ressources"""
        self.resources_tab = QWidget()
        layout = QVBoxLayout(self.resources_tab)

        # Barre d'outils des ressources
        resource_toolbar = QToolBar()

        filter_combo = QComboBox()
        filter_combo.addItems(["Toutes", "IA", "Logiciels", "Assets", "Templates"])
        filter_combo.currentTextChanged.connect(self.filter_resources)
        resource_toolbar.addWidget(QLabel("Filtrer:"))
        resource_toolbar.addWidget(filter_combo)

        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Rechercher...")
        search_edit.textChanged.connect(self.search_resources)
        resource_toolbar.addWidget(search_edit)

        layout.addWidget(resource_toolbar)

        # Liste des ressources
        self.resources_list = QListWidget()
        self.resources_list.setViewMode(QListWidget.IconMode)
        self.resources_list.setIconSize(QSize(48, 48))
        self.resources_list.setResizeMode(QListWidget.Adjust)
        self.resources_list.setMovement(QListWidget.Static)
        self.resources_list.setSpacing(10)
        self.resources_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resources_list.customContextMenuRequested.connect(self.show_resource_context_menu)
        self.resources_list.itemDoubleClicked.connect(self.launch_resource)

        layout.addWidget(self.resources_list)

        self.main_tabs.addTab(self.resources_tab, QIcon.fromTheme("applications-other"), "Ressources")
        self.load_resources()

    def setup_organizer_tab(self):
        """Configure l'onglet d'organisation du contenu"""
        self.organizer_tab = QWidget()
        layout = QVBoxLayout(self.organizer_tab)

        # Barre d'outils
        organizer_toolbar = QToolBar()

        content_type_combo = QComboBox()
        content_type_combo.addItems(["Tous", "Vidéo", "Image", "Audio", "Texte"])
        content_type_combo.currentTextChanged.connect(self.filter_content_items)
        organizer_toolbar.addWidget(QLabel("Type:"))
        organizer_toolbar.addWidget(content_type_combo)

        layout.addWidget(organizer_toolbar)

        # Splitter horizontal
        splitter = QSplitter(Qt.Horizontal)

        # Panel de contenu
        content_panel = QWidget()
        content_layout = QVBoxLayout(content_panel)

        self.content_table = QTreeView()
        self.content_model = QStandardItemModel()
        self.content_model.setHorizontalHeaderLabels(["Nom", "Type", "Projet", "Date"])
        self.content_table.setModel(self.content_model)
        self.content_table.setSelectionMode(QTreeView.ExtendedSelection)

        content_layout.addWidget(self.content_table)

        # Panel d'organisation
        org_panel = QWidget()
        org_layout = QVBoxLayout(org_panel)

        self.suggestions_list = QListWidget()
        self.suggestions_list.addItems([
            "Créer une structure YouTube",
            "Organiser par date",
            "Organiser par projet",
            "Suggestion personnalisée..."
        ])
        self.suggestions_list.itemClicked.connect(self.apply_organization_suggestion)

        org_layout.addWidget(QLabel("Suggestions d'Organisation"))
        org_layout.addWidget(self.suggestions_list)

        # Ajout des panels au splitter
        splitter.addWidget(content_panel)
        splitter.addWidget(org_panel)
        splitter.setSizes([600, 200])

        layout.addWidget(splitter)

        self.main_tabs.addTab(self.organizer_tab, QIcon.fromTheme("folder-organize"), "Organisation")
        self.load_content_items()

    def setup_workflows_tab(self):
        """Configure l'onglet de gestion des workflows"""
        self.workflows_tab = QWidget()
        layout = QVBoxLayout(self.workflows_tab)

        # Barre d'outils
        workflow_toolbar = QToolBar()

        new_workflow_btn = QPushButton("Nouveau Workflow")
        new_workflow_btn.clicked.connect(self.create_new_workflow)
        workflow_toolbar.addWidget(new_workflow_btn)

        run_workflow_btn = QPushButton("Exécuter")
        run_workflow_btn.clicked.connect(self.run_workflow)
        workflow_toolbar.addWidget(run_workflow_btn)

        layout.addWidget(workflow_toolbar)

        # Liste des workflows
        self.workflows_list = QListWidget()
        self.workflows_list.setViewMode(QListWidget.IconMode)
        self.workflows_list.setIconSize(QSize(64, 64))
        self.load_workflows()

        layout.addWidget(self.workflows_list)

        self.main_tabs.addTab(self.workflows_tab, QIcon.fromTheme("system-run"), "Workflows")

    def setup_context_menus(self):
        """Configure les menus contextuels"""
        # Menu contextuel pour les projets
        self.project_context_menu = QMenu()

        open_action = QAction("Ouvrir", self)
        open_action.triggered.connect(self.open_selected_project)
        self.project_context_menu.addAction(open_action)

        delete_action = QAction("Supprimer", self)
        delete_action.triggered.connect(self.delete_project)
        self.project_context_menu.addAction(delete_action)

        # Menu contextuel pour les ressources
        self.resource_context_menu = QMenu()

        launch_action = QAction("Lancer", self)
        launch_action.triggered.connect(self.launch_selected_resource)
        self.resource_context_menu.addAction(launch_action)

        edit_action = QAction("Modifier", self)
        edit_action.triggered.connect(self.edit_resource)
        self.resource_context_menu.addAction(edit_action)

        favorite_action = QAction("Favoris", self)
        favorite_action.triggered.connect(self.toggle_favorite)
        self.resource_context_menu.addAction(favorite_action)

        # Menu contextuel pour les dossiers
        self.folder_context_menu = QMenu()

        new_folder_action = QAction("Nouveau dossier", self)
        new_folder_action.triggered.connect(self.create_new_folder)
        self.folder_context_menu.addAction(new_folder_action)

        organize_action = QAction("Organiser automatiquement", self)
        organize_action.triggered.connect(self.auto_organize_folder)
        self.folder_context_menu.addAction(organize_action)

    def connect_signals(self):
        """Connecte les signaux et slots"""
        self.projects_list.itemSelectionChanged.connect(self.project_selected)
        self.folder_tree.doubleClicked.connect(self.folder_double_clicked)

    def create_ai_tools_menu(self):
        """Crée le menu des outils IA"""
        menu = QMenu(self)

        # Textuel
        text_submenu = menu.addMenu("Génération Textuelle")
        text_submenu.addAction("ChatGPT")
        text_submenu.addAction("Claude AI")
        text_submenu.addAction("Modèles Locaux")

        # Visuel
        image_submenu = menu.addMenu("Génération d'Images")
        image_submenu.addAction("Midjourney")
        image_submenu.addAction("Stable Diffusion")
        image_submenu.addAction("DALL-E")

        # Audio
        audio_submenu = menu.addMenu("Génération Audio")
        audio_submenu.addAction("ElevenLabs")
        audio_submenu.addAction("Murf AI")

        return menu

    def create_editing_tools_menu(self):
        """Crée le menu des outils d'édition"""
        menu = QMenu(self)

        # Vidéo
        video_submenu = menu.addMenu("Vidéo")
        video_submenu.addAction("Adobe Premiere")
        video_submenu.addAction("Final Cut Pro")
        video_submenu.addAction("DaVinci Resolve")

        # Image
        image_submenu = menu.addMenu("Image")
        image_submenu.addAction("Photoshop")
        image_submenu.addAction("GIMP")
        image_submenu.addAction("Canva")

        # Audio
        audio_submenu = menu.addMenu("Audio")
        audio_submenu.addAction("Audacity")
        audio_submenu.addAction("Adobe Audition")

        return menu

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Style d'application moderne
    app.setStyle("Fusion")

    # Création et affichage de la fenêtre principale
    hub = ContentCreationHub()
    hub.show()

    sys.exit(app.exec_())
