import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QStackedWidget, QFrame, QSizePolicy,
                            QTableWidget, QTableWidgetItem, QComboBox, QDateEdit, QLineEdit,
                            QProgressBar, QTabWidget, QCheckBox, QMessageBox, QFileDialog,
                            QInputDialog, QFormLayout, QSpacerItem, QGroupBox)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
import pyqtgraph as pg
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import hashlib
import os
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QDoubleSpinBox

class DatabaseManager:
    def __init__(self, db_name='management.db'):
        self.db_name = db_name
        self.init_db()
        
    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des membres d'équipe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS team_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    department TEXT NOT NULL,
                    hire_date TEXT NOT NULL,
                    performance INTEGER DEFAULT 0,
                    skills TEXT,
                    notes TEXT,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # Table des projets
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    budget REAL NOT NULL,
                    status TEXT DEFAULT 'planning',
                    progress INTEGER DEFAULT 0,
                    manager_id INTEGER,
                    priority TEXT DEFAULT 'medium',
                    FOREIGN KEY (manager_id) REFERENCES team_members(id)
                )
            ''')
            
            # Table des tâches
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    assignee_id INTEGER,
                    status TEXT DEFAULT 'todo',
                    priority TEXT DEFAULT 'medium',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    deadline TEXT,
                    completed_at TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id),
                    FOREIGN KEY (assignee_id) REFERENCES team_members(id)
                )
            ''')
            
            # Table des KPI
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kpis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    target REAL NOT NULL,
                    trend TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des activités
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Insérer l'admin par défaut si nécessaire
            cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
            if cursor.fetchone()[0] == 0:
                hashed_pwd = hashlib.sha256('admin123'.encode()).hexdigest()
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', hashed_pwd, 'Administrateur', 'admin@company.com', 'admin'))
            
            conn.commit()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)

class MainDashboard(QMainWindow):



    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent=parent
        self.db = DatabaseManager()
        self.current_user = None
        
        self.setWindowTitle("Management Dashboard Pro")
        self.setWindowIcon(QIcon(self.resource_path('icons/app_icon.png')))
        self.setGeometry(100, 100, 1400, 900)
        
        # Style global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        self.init_ui()
        self.load_initial_data()
    def module_closed(self, module_id):
        """Nettoyer après la fermeture d'un module"""
        self.parent.modules[module_id] = None        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
            
        return os.path.join(base_path, relative_path)
        
    def init_ui(self):
        # Création du widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # On utilise un layout vertical maintenant (topbar au-dessus du contenu principal)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Topbar (remplace la sidebar)
        self.setup_topbar()  # Remplace setup_sidebar()
        main_layout.addWidget(self.topbar)

        # Contenu principal
        self.main_content = QStackedWidget()
        self.main_content.setStyleSheet("""
            QStackedWidget {
                background-color: #ffffff;
            }
        """)

        # Pages
        self.setup_dashboard_page()
        self.setup_team_page()
        self.setup_projects_page()
        self.setup_tasks_page()
        self.setup_reports_page()
        self.setup_settings_page()

        # On ajoute le contenu principal en dessous de la topbar
        main_layout.addWidget(self.main_content)

        # Barre de statut
        self.statusBar().showMessage("Prêt")

        # Vérifier si l'utilisateur est connecté
        if not self.current_user:
            self.show_login_dialog()


    def setup_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 12px 20px;
                border: none;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton#selected {
                background-color: #3498db;
                font-weight: bold;
            }
            QLabel {
                color: white;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(5, 20, 5, 20)
        sidebar_layout.setSpacing(10)
        
        # Logo et titre
        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        logo_icon.setPixmap(QIcon(self.resource_path('icons/logo.png')).pixmap(40, 40))
        logo_text = QLabel("Management Pro")
        logo_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        sidebar_layout.addLayout(logo_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #34495e;")
        sidebar_layout.addWidget(separator)
        
        # Boutons de navigation
        nav_buttons = [
            ("Tableau de bord", "dashboard.png", 0),
            ("Gestion d'équipe", "team.png", 1),
            ("Projets", "projects.png", 2),
            ("Tâches", "tasks.png", 3),
            ("Rapports", "reports.png", 4),
            ("Paramètres", "settings.png", 5)
        ]
        
        self.nav_buttons = []
        for text, icon, idx in nav_buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(self.resource_path(f'icons/{icon}')))
            btn.clicked.connect(lambda _, i=idx: self.change_page(i))
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)
        
        # Sélectionner le premier bouton par défaut
        self.nav_buttons[0].setObjectName("selected")
        
        sidebar_layout.addStretch()
        
        # User info
        self.user_widget = QWidget()
        self.user_widget.setStyleSheet("""
            QWidget {
                background-color: #34495e; 
                border-radius: 5px;
                padding: 10px;
            }
            QLabel#user_name {
                font-weight: bold;
                font-size: 14px;
            }
            QLabel#user_role {
                font-size: 12px;
                color: #bdc3c7;
            }
        """)
        
        user_layout = QHBoxLayout(self.user_widget)
        
        self.user_icon = QLabel()
        self.user_icon.setPixmap(QIcon(self.resource_path('icons/user.png')).pixmap(40, 40))
        
        user_info = QVBoxLayout()
        self.user_name = QLabel("Invité")
        self.user_name.setObjectName("user_name")
        self.user_role = QLabel("Non connecté")
        self.user_role.setObjectName("user_role")
        
        user_info.addWidget(self.user_name)
        user_info.addWidget(self.user_role)
        
        user_layout.addWidget(self.user_icon)
        user_layout.addLayout(user_info)
        
        logout_btn = QPushButton()
        logout_btn.setIcon(QIcon(self.resource_path('icons/logout.png')))
        logout_btn.setToolTip("Déconnexion")
        logout_btn.setFixedSize(30, 30)
        logout_btn.setStyleSheet("background-color: transparent;")
        logout_btn.clicked.connect(self.logout)
        
        user_layout.addWidget(logout_btn)
        
        sidebar_layout.addWidget(self.user_widget)
    def setup_topbar(self):
        self.topbar = QFrame()
        self.topbar.setFixedHeight(60)  # Hauteur au lieu de largeur
        self.topbar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                padding: 10px 20px;
                border: none;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton#selected {
                background-color: #3498db;
                font-weight: bold;
            }
            QLabel {
                color: white;
            }
        """)

        topbar_layout = QHBoxLayout(self.topbar)
        topbar_layout.setContentsMargins(10, 10, 10, 10)
        topbar_layout.setSpacing(20)

        # Logo et titre à gauche
        logo_icon = QLabel()
        logo_icon.setPixmap(QIcon(self.resource_path('icons/logo.png')).pixmap(40, 40))
        logo_text = QLabel("Management Pro")
        logo_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #3498db;")

        topbar_layout.addWidget(logo_icon)
        topbar_layout.addWidget(logo_text)

        # Espace entre logo et boutons
        topbar_layout.addSpacing(30)

        # Boutons de navigation (au milieu)
        nav_buttons = [
            ("Tableau de bord", "dashboard.png", 0),
            ("Équipe", "team.png", 1),
            ("Projets", "projects.png", 2),
            ("Tâches", "tasks.png", 3),
            ("Rapports", "reports.png", 4),
            ("Paramètres", "settings.png", 5)
        ]

        self.nav_buttons = []
        for text, icon, idx in nav_buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(self.resource_path(f'icons/{icon}')))
            btn.clicked.connect(lambda _, i=idx: self.change_page(i))
            self.nav_buttons.append(btn)
            topbar_layout.addWidget(btn)

        self.nav_buttons[0].setObjectName("selected")

        topbar_layout.addStretch()

        # Infos utilisateur à droite
        user_icon = QLabel()
        user_icon.setPixmap(QIcon(self.resource_path('icons/user.png')).pixmap(30, 30))

        self.user_name = QLabel("Invité")
        self.user_name.setStyleSheet("font-weight: bold;")

        self.user_role = QLabel("Non connecté")
        self.user_role.setStyleSheet("font-size: 10px; color: #bdc3c7;")

        user_info = QVBoxLayout()
        user_info.addWidget(self.user_name)
        user_info.addWidget(self.user_role)

        user_widget = QHBoxLayout()
        user_widget.addWidget(user_icon)
        user_widget.addLayout(user_info)

        logout_btn = QPushButton()
        logout_btn.setIcon(QIcon(self.resource_path('icons/logout.png')))
        logout_btn.setToolTip("Déconnexion")
        logout_btn.setFixedSize(30, 30)
        logout_btn.setStyleSheet("background-color: transparent;")
        logout_btn.clicked.connect(self.logout)

        user_widget_container = QWidget()
        user_widget_container.setLayout(user_widget)
        user_widget_container.setStyleSheet("background-color: transparent;")

        topbar_layout.addWidget(user_widget_container)
        topbar_layout.addWidget(logout_btn)








    def setup_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Tableau de Bord Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.date_picker.dateChanged.connect(self.update_dashboard)
        
        refresh_btn = QPushButton("Actualiser")
        refresh_btn.setIcon(QIcon(self.resource_path('icons/refresh.png')))
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_btn.clicked.connect(self.update_dashboard)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.date_picker)
        header_layout.addWidget(refresh_btn)
        
        # KPIs
        self.kpi_widget = QWidget()
        self.kpi_layout = QHBoxLayout(self.kpi_widget)
        self.kpi_layout.setSpacing(15)
        
        # Graphiques
        graph_widget = QWidget()
        graph_layout = QHBoxLayout(graph_widget)
        graph_layout.setSpacing(15)
        
        # Graphique de performance
        self.performance_graph = pg.PlotWidget()
        self.performance_graph.setBackground('w')
        self.performance_graph.setTitle("Performance de l'équipe", color='#333333', size='12pt')
        self.performance_graph.showGrid(x=True, y=True)
        self.performance_graph.setMinimumHeight(300)
        
        # Graphique d'avancement des projets
        self.project_progress_graph = pg.PlotWidget()
        self.project_progress_graph.setBackground('w')
        self.project_progress_graph.setTitle("Avancement des projets", color='#333333', size='12pt')
        self.project_progress_graph.showGrid(x=True, y=True)
        self.project_progress_graph.setMinimumHeight(300)
        
        graph_layout.addWidget(self.performance_graph, 1)
        graph_layout.addWidget(self.project_progress_graph, 1)
        
        # Dernières activités
        activities_widget = QGroupBox("Dernières Activités")
        activities_widget.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        
        activities_layout = QVBoxLayout(activities_widget)
        
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(4)
        self.activities_table.setHorizontalHeaderLabels(["Date", "Membre", "Action", "Détails"])
        self.activities_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.activities_table.verticalHeader().setVisible(False)
        self.activities_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.activities_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.activities_table.setSortingEnabled(True)
        
        activities_layout.addWidget(self.activities_table)
        
        layout.addWidget(header)
        layout.addWidget(self.kpi_widget)
        layout.addWidget(graph_widget)
        layout.addWidget(activities_widget)
        
        self.main_content.addWidget(page)
    
    def setup_team_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Gestion d'Équipe")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        self.add_member_btn = QPushButton("Ajouter Membre")
        self.add_member_btn.setIcon(QIcon(self.resource_path('icons/add_user.png')))
        self.add_member_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.add_member_btn.clicked.connect(self.show_add_member_dialog)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_member_btn)
        
        # Filtres
        filters = QWidget()
        filters_layout = QHBoxLayout(filters)
        
        self.team_search = QLineEdit()
        self.team_search.setPlaceholderText("Rechercher un membre...")
        self.team_search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.team_search.textChanged.connect(self.filter_team_members)
        
        self.role_filter = QComboBox()
        self.role_filter.addItems(["Tous les rôles", "Chef de projet", "Développeur", "Designer", "RH", "Marketing", "Finance"])
        self.role_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.role_filter.currentIndexChanged.connect(self.filter_team_members)
        
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Tous statuts", "Actif", "Inactif", "En congé"])
        self.status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.status_filter.currentIndexChanged.connect(self.filter_team_members)
        
        filters_layout.addWidget(self.team_search)
        filters_layout.addWidget(self.role_filter)
        filters_layout.addWidget(self.status_filter)
        
        # Tableau des membres
        self.team_table = QTableWidget()
        self.team_table.setColumnCount(8)
        self.team_table.setHorizontalHeaderLabels(["Nom", "Rôle", "Département", "Performance", "Date embauche", "Statut", "Tâches", "Actions"])
        self.team_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.team_table.verticalHeader().setVisible(False)
        self.team_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.team_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.team_table.setSortingEnabled(True)
        self.team_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addWidget(filters)
        layout.addWidget(self.team_table)
        
        self.main_content.addWidget(page)
    
    def setup_projects_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Gestion des Projets")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        self.add_project_btn = QPushButton("Nouveau Projet")
        self.add_project_btn.setIcon(QIcon(self.resource_path('icons/add_project.png')))
        self.add_project_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.add_project_btn.clicked.connect(self.show_add_project_dialog)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_project_btn)
        
        # Filtres
        filters = QWidget()
        filters_layout = QHBoxLayout(filters)
        
        self.project_search = QLineEdit()
        self.project_search.setPlaceholderText("Rechercher un projet...")
        self.project_search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.project_search.textChanged.connect(self.filter_projects)
        
        self.status_filter_proj = QComboBox()
        self.status_filter_proj.addItems(["Tous statuts", "Planification", "En cours", "En retard", "Terminé"])
        self.status_filter_proj.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.status_filter_proj.currentIndexChanged.connect(self.filter_projects)
        
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["Toutes priorités", "Haute", "Moyenne", "Basse"])
        self.priority_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.priority_filter.currentIndexChanged.connect(self.filter_projects)
        
        filters_layout.addWidget(self.project_search)
        filters_layout.addWidget(self.status_filter_proj)
        filters_layout.addWidget(self.priority_filter)
        
        # Tableau des projets
        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(8)
        self.projects_table.setHorizontalHeaderLabels(["Nom", "Statut", "Avancement", "Priorité", "Échéance", "Budget", "Responsable", "Actions"])
        self.projects_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.projects_table.verticalHeader().setVisible(False)
        self.projects_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.projects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.projects_table.setSortingEnabled(True)
        self.projects_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addWidget(filters)
        layout.addWidget(self.projects_table)
        
        self.main_content.addWidget(page)
    
    def setup_tasks_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Gestion des Tâches")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        self.add_task_btn = QPushButton("Nouvelle Tâche")
        self.add_task_btn.setIcon(QIcon(self.resource_path('icons/add_task.png')))
        self.add_task_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.add_task_btn.clicked.connect(self.show_add_task_dialog)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_task_btn)
        
        # Filtres
        filters = QWidget()
        filters_layout = QHBoxLayout(filters)
        
        self.task_search = QLineEdit()
        self.task_search.setPlaceholderText("Rechercher une tâche...")
        self.task_search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.task_search.textChanged.connect(self.filter_tasks)
        
        self.task_status_filter = QComboBox()
        self.task_status_filter.addItems(["Tous statuts", "À faire", "En cours", "En revue", "Terminé"])
        self.task_status_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.task_status_filter.currentIndexChanged.connect(self.filter_tasks)
        
        self.task_priority_filter = QComboBox()
        self.task_priority_filter.addItems(["Toutes priorités", "Haute", "Moyenne", "Basse"])
        self.task_priority_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.task_priority_filter.currentIndexChanged.connect(self.filter_tasks)
        
        self.task_project_filter = QComboBox()
        self.task_project_filter.addItem("Tous les projets")
        self.task_project_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        self.task_project_filter.currentIndexChanged.connect(self.filter_tasks)
        
        filters_layout.addWidget(self.task_search)
        filters_layout.addWidget(self.task_status_filter)
        filters_layout.addWidget(self.task_priority_filter)
        filters_layout.addWidget(self.task_project_filter)
        
        # Tableau des tâches
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["Nom", "Projet", "Statut", "Priorité", "Assigné à", "Échéance", "Actions"])
        self.tasks_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.tasks_table.verticalHeader().setVisible(False)
        self.tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tasks_table.setSortingEnabled(True)
        self.tasks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addWidget(filters)
        layout.addWidget(self.tasks_table)
        
        self.main_content.addWidget(page)
    
    def setup_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Rapports et Analyses")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        # Options de rapport
        report_options = QWidget()
        options_layout = QHBoxLayout(report_options)
        
        self.report_type = QComboBox()
        self.report_type.addItems(["Performance d'équipe", "Avancement projets", "Charge de travail", "Indicateurs clés", "Analyse budgétaire"])
        self.report_type.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        self.report_period = QComboBox()
        self.report_period.addItems(["7 derniers jours", "30 derniers jours", "Trimestre en cours", "Année en cours", "Personnalisé..."])
        self.report_period.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        
        generate_btn = QPushButton("Générer Rapport")
        generate_btn.setIcon(QIcon(self.resource_path('icons/generate_report.png')))
        generate_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        generate_btn.clicked.connect(self.generate_report)
        
        export_btn = QPushButton("Exporter PDF")
        export_btn.setIcon(QIcon(self.resource_path('icons/export_pdf.png')))
        export_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #e74c3c;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        export_btn.clicked.connect(self.export_report)
        
        options_layout.addWidget(QLabel("Type:"))
        options_layout.addWidget(self.report_type)
        options_layout.addWidget(QLabel("Période:"))
        options_layout.addWidget(self.report_period)
        options_layout.addWidget(generate_btn)
        options_layout.addWidget(export_btn)
        
        # Zone de rapport
        self.report_view = QTabWidget()
        self.report_view.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 8px 15px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # Onglet Graphique
        self.graph_tab = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_tab)
        
        # Onglet Données
        self.data_tab = QWidget()
        self.data_layout = QVBoxLayout(self.data_tab)
        
        self.report_data_table = QTableWidget()
        self.report_data_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.report_data_table.verticalHeader().setVisible(False)
        self.report_data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.data_layout.addWidget(self.report_data_table)
        
        self.report_view.addTab(self.graph_tab, "Visualisation")
        self.report_view.addTab(self.data_tab, "Données")
        
        layout.addWidget(title)
        layout.addWidget(report_options)
        layout.addWidget(self.report_view)
        
        self.main_content.addWidget(page)
    
    def setup_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Paramètres")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        
        # Onglets
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 8px 15px;
                background: #f1f1f1;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # Onglet Compte
        account_tab = QWidget()
        account_layout = QFormLayout(account_tab)
        account_layout.setSpacing(15)
        
        account_layout.addRow(QLabel("<b>Informations Personnelles</b>"))
        
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        
        account_layout.addRow("Nom complet:", self.name_edit)
        account_layout.addRow("Email:", self.email_edit)
        account_layout.addRow("Téléphone:", self.phone_edit)
        
        account_layout.addItem(QSpacerItem(20, 20))
        account_layout.addRow(QLabel("<b>Sécurité</b>"))
        
        self.current_pwd_edit = QLineEdit()
        self.current_pwd_edit.setEchoMode(QLineEdit.Password)
        self.new_pwd_edit = QLineEdit()
        self.new_pwd_edit.setEchoMode(QLineEdit.Password)
        self.confirm_pwd_edit = QLineEdit()
        self.confirm_pwd_edit.setEchoMode(QLineEdit.Password)
        
        account_layout.addRow("Mot de passe actuel:", self.current_pwd_edit)
        account_layout.addRow("Nouveau mot de passe:", self.new_pwd_edit)
        account_layout.addRow("Confirmer:", self.confirm_pwd_edit)
        
        save_btn = QPushButton("Enregistrer les modifications")
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        save_btn.clicked.connect(self.save_account_settings)
        account_layout.addRow(save_btn)
        
        # Onglet Préférences
        pref_tab = QWidget()
        pref_layout = QFormLayout(pref_tab)
        pref_layout.setSpacing(15)
        
        pref_layout.addRow(QLabel("<b>Affichage</b>"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Clair", "Sombre", "Bleu", "Automatique"])
        
        self.density_combo = QComboBox()
        self.density_combo.addItems(["Compact", "Normal", "Large"])
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Français", "Anglais", "Espagnol"])
        
        pref_layout.addRow("Thème:", self.theme_combo)
        pref_layout.addRow("Densité:", self.density_combo)
        pref_layout.addRow("Langue:", self.language_combo)
        
        pref_layout.addItem(QSpacerItem(20, 20))
        pref_layout.addRow(QLabel("<b>Notifications</b>"))
        
        self.email_notif = QCheckBox("Email")
        self.app_notif = QCheckBox("Application")
        self.sms_notif = QCheckBox("SMS")
        
        pref_layout.addRow(self.email_notif)
        pref_layout.addRow(self.app_notif)
        pref_layout.addRow(self.sms_notif)
        
        save_pref_btn = QPushButton("Enregistrer les préférences")
        save_pref_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        save_pref_btn.clicked.connect(self.save_preferences)
        pref_layout.addRow(save_pref_btn)
        
        # Onglet Équipe
        team_tab = QWidget()
        team_layout = QVBoxLayout(team_tab)
        
        self.access_table = QTableWidget()
        self.access_table.setColumnCount(4)
        self.access_table.setHorizontalHeaderLabels(["Nom", "Rôle", "Accès", "Actions"])
        self.access_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.access_table.verticalHeader().setVisible(False)
        self.access_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.access_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        
        team_layout.addWidget(self.access_table)
        
        tabs.addTab(account_tab, "Compte")
        tabs.addTab(pref_tab, "Préférences")
        tabs.addTab(team_tab, "Gestion d'accès")
        
        layout.addWidget(title)
        layout.addWidget(tabs)
        
        self.main_content.addWidget(page)
    
    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Connexion")
        dialog.setFixedSize(350, 250)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton#login_btn {
                background-color: #3498db;
                color: white;
            }
            QPushButton#login_btn:hover {
                background-color: #2980b9;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        logo = QLabel()
        logo.setPixmap(QIcon(self.resource_path('icons/logo.png')).pixmap(80, 80))
        logo.setAlignment(Qt.AlignCenter)
        
        username_edit = QLineEdit()
        username_edit.setPlaceholderText("Nom d'utilisateur")
        
        password_edit = QLineEdit()
        password_edit.setPlaceholderText("Mot de passe")
        password_edit.setEchoMode(QLineEdit.Password)
        
        login_btn = QPushButton("Se connecter")
        login_btn.setObjectName("login_btn")
        login_btn.clicked.connect(lambda: self.handle_login(username_edit.text(), password_edit.text(), dialog))
        
        layout.addWidget(logo)
        layout.addWidget(QLabel("Nom d'utilisateur:"))
        layout.addWidget(username_edit)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(password_edit)
        layout.addItem(QSpacerItem(20, 20))
        layout.addWidget(login_btn)
        
        dialog.exec_()
    
    def handle_login(self, username, password, dialog):
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pwd))
            user = cursor.fetchone()
            
            if user:
                self.current_user = {
                    'id': user[0],
                    'username': user[1],
                    'full_name': user[3],
                    'email': user[4],
                    'role': user[5]
                }
                
                # Mettre à jour l'interface utilisateur
                self.user_name.setText(self.current_user['full_name'])
                self.user_role.setText(self.current_user['role'].capitalize())
                
                # Enregistrer l'activité
                self.log_activity(f"Connexion de {self.current_user['full_name']}")
                
                # Charger les données
                self.load_initial_data()
                
                dialog.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")
    
    def logout(self):
        if self.current_user:
            self.log_activity(f"Déconnexion de {self.current_user['full_name']}")
            
        self.current_user = None
        self.user_name.setText("Invité")
        self.user_role.setText("Non connecté")
        self.show_login_dialog()
    
    def log_activity(self, action, details=None):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            user_id = self.current_user['id'] if self.current_user else None
            cursor.execute('''
                INSERT INTO activities (user_id, action, details)
                VALUES (?, ?, ?)
            ''', (user_id, action, details))
            conn.commit()
    
    def load_initial_data(self):
        self.load_kpis()
        self.load_team_members()
        self.load_projects()
        self.load_tasks()
        self.load_activities()
        self.load_access_table()
        self.update_project_filter()
        
        # Configurer les préférences utilisateur si connecté
        if self.current_user:
            self.load_user_preferences()
    
    def load_kpis(self):
        # Effacer les anciens KPIs
        for i in reversed(range(self.kpi_layout.count())):
            widget = self.kpi_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Charger les KPIs depuis la base de données
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, value, target, trend, unit FROM kpis")
            kpis = cursor.fetchall()
            
            for name, value, target, trend, unit in kpis:
                frame = QFrame()
                frame.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border-radius: 5px;
                        padding: 15px;
                        border: 1px solid #e0e0e0;
                    }
                    QLabel {
                        font-size: 14px;
                        color: #555555;
                    }
                    QLabel#kpi_title {
                        font-size: 16px;
                        font-weight: bold;
                        color: #2c3e50;
                    }
                    QLabel#kpi_value {
                        font-size: 28px;
                        font-weight: bold;
                        color: #3498db;
                    }
                """)
                frame.setFixedWidth(220)
                
                frame_layout = QVBoxLayout(frame)
                frame_layout.setSpacing(5)
                
                title = QLabel(name.capitalize())
                title.setObjectName("kpi_title")
                
                value_label = QLabel(f"{value}{unit}")
                value_label.setObjectName("kpi_value")
                
                target_label = QLabel(f"Cible: {target}{unit}")
                
                trend_icon = QLabel()
                if trend == "up":
                    trend_icon.setPixmap(QIcon(self.resource_path('icons/trend_up.png')).pixmap(16, 16))
                elif trend == "down":
                    trend_icon.setPixmap(QIcon(self.resource_path('icons/trend_down.png')).pixmap(16, 16))
                else:
                    trend_icon.setPixmap(QIcon(self.resource_path('icons/trend_flat.png')).pixmap(16, 16))
                
                trend_layout = QHBoxLayout()
                trend_layout.addWidget(QLabel("Tendance:"))
                trend_layout.addWidget(trend_icon)
                trend_layout.addStretch()
                
                frame_layout.addWidget(title)
                frame_layout.addWidget(value_label)
                frame_layout.addWidget(target_label)
                frame_layout.addLayout(trend_layout)
                
                self.kpi_layout.addWidget(frame)
            
            # Si pas de KPIs, en créer des exemples
            if not kpis:
                example_kpis = [
                    ("Productivité", 78, 85, "up", "%"),
                    ("Qualité", 92, 90, "stable", "%"),
                    ("Efficacité", 81, 80, "up", "%"),
                    ("Satisfaction", 88, 85, "down", "%")
                ]
                
                for name, value, target, trend, unit in example_kpis:
                    cursor.execute('''
                        INSERT INTO kpis (name, value, target, trend, unit)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, value, target, trend, unit))
                
                conn.commit()
                # Recharger les KPIs
                self.load_kpis()
    
    def load_team_members(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, role, department, performance, hire_date, status FROM team_members WHERE status != 'deleted'")
            members = cursor.fetchall()
            
            self.team_table.setRowCount(len(members))
            
            for row, (id, name, role, department, performance, hire_date, status) in enumerate(members):
                self.team_table.setItem(row, 0, QTableWidgetItem(name))
                self.team_table.setItem(row, 1, QTableWidgetItem(role))
                self.team_table.setItem(row, 2, QTableWidgetItem(department))
                
                # Performance avec couleur
                perf_item = QTableWidgetItem(f"{performance}%")
                if performance >= 90:
                    perf_item.setForeground(QColor('#27ae60'))
                elif performance >= 80:
                    perf_item.setForeground(QColor('#f39c12'))
                else:
                    perf_item.setForeground(QColor('#e74c3c'))
                self.team_table.setItem(row, 3, perf_item)
                
                self.team_table.setItem(row, 4, QTableWidgetItem(hire_date))
                
                # Statut avec icône
                status_item = QTableWidgetItem()
                if status == "active":
                    status_item.setIcon(QIcon(self.resource_path('icons/active.png')))
                    status_item.setText("Actif")
                elif status == "inactive":
                    status_item.setIcon(QIcon(self.resource_path('icons/inactive.png')))
                    status_item.setText("Inactif")
                else:
                    status_item.setIcon(QIcon(self.resource_path('icons/leave.png')))
                    status_item.setText("En congé")
                self.team_table.setItem(row, 5, status_item)
                
                # Nombre de tâches
                cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id=?", (id,))
                task_count = cursor.fetchone()[0]
                self.team_table.setItem(row, 6, QTableWidgetItem(str(task_count)))
                
                # Boutons d'action
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)
                
                edit_btn = QPushButton()
                edit_btn.setIcon(QIcon(self.resource_path('icons/edit.png')))
                edit_btn.setToolTip("Modifier")
                edit_btn.setFixedSize(30, 30)
                edit_btn.setStyleSheet("background-color: transparent;")
                edit_btn.clicked.connect(lambda _, member_id=id: self.edit_member(member_id))
                
                delete_btn = QPushButton()
                delete_btn.setIcon(QIcon(self.resource_path('icons/delete.png')))
                delete_btn.setToolTip("Supprimer")
                delete_btn.setFixedSize(30, 30)
                delete_btn.setStyleSheet("background-color: transparent;")
                delete_btn.clicked.connect(lambda _, member_id=id: self.delete_member(member_id))
                
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.team_table.setCellWidget(row, 7, action_widget)
            
            self.team_table.resizeColumnsToContents()
    
    def load_projects(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.name, p.status, p.progress, p.priority, p.deadline, p.budget, t.name 
                FROM projects p
                LEFT JOIN team_members t ON p.manager_id = t.id
                WHERE p.status != 'deleted'
            ''')
            projects = cursor.fetchall()
            
            self.projects_table.setRowCount(len(projects))
            
            for row, (id, name, status, progress, priority, deadline, budget, manager) in enumerate(projects):
                self.projects_table.setItem(row, 0, QTableWidgetItem(name))
                
                # Statut avec couleur
                status_item = QTableWidgetItem(status.capitalize())
                if status == "completed":
                    status_item.setForeground(QColor('#27ae60'))
                elif status == "late":
                    status_item.setForeground(QColor('#e74c3c'))
                elif status == "in_progress":
                    status_item.setForeground(QColor('#3498db'))
                self.projects_table.setItem(row, 1, status_item)
                
                # Barre de progression
                progress_widget = QWidget()
                progress_layout = QHBoxLayout(progress_widget)
                progress_layout.setContentsMargins(5, 5, 5, 5)
                
                progress_bar = QProgressBar()
                progress_bar.setValue(progress)
                progress_bar.setAlignment(Qt.AlignCenter)
                progress_bar.setFormat(f"{progress}%")
                progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #bdc3c7;
                        border-radius: 5px;
                        text-align: center;
                        height: 20px;
                    }
                    QProgressBar::chunk {
                        background-color: #3498db;
                        border-radius: 4px;
                    }
                """)
                
                progress_layout.addWidget(progress_bar)
                self.projects_table.setCellWidget(row, 2, progress_widget)
                
                # Priorité avec icône
                priority_item = QTableWidgetItem()
                if priority == "high":
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_high.png')))
                    priority_item.setText("Haute")
                elif priority == "medium":
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_medium.png')))
                    priority_item.setText("Moyenne")
                else:
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_low.png')))
                    priority_item.setText("Basse")
                self.projects_table.setItem(row, 3, priority_item)
                
                self.projects_table.setItem(row, 4, QTableWidgetItem(deadline))
                self.projects_table.setItem(row, 5, QTableWidgetItem(f"€{budget:,.2f}"))
                self.projects_table.setItem(row, 6, QTableWidgetItem(manager if manager else "Non assigné"))
                
                # Boutons d'action
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)
                
                details_btn = QPushButton()
                details_btn.setIcon(QIcon(self.resource_path('icons/details.png')))
                details_btn.setToolTip("Détails")
                details_btn.setFixedSize(30, 30)
                details_btn.setStyleSheet("background-color: transparent;")
                details_btn.clicked.connect(lambda _, project_id=id: self.show_project_details(project_id))
                
                edit_btn = QPushButton()
                edit_btn.setIcon(QIcon(self.resource_path('icons/edit.png')))
                edit_btn.setToolTip("Modifier")
                edit_btn.setFixedSize(30, 30)
                edit_btn.setStyleSheet("background-color: transparent;")
                edit_btn.clicked.connect(lambda _, project_id=id: self.edit_project(project_id))
                
                delete_btn = QPushButton()
                delete_btn.setIcon(QIcon(self.resource_path('icons/delete.png')))
                delete_btn.setToolTip("Supprimer")
                delete_btn.setFixedSize(30, 30)
                delete_btn.setStyleSheet("background-color: transparent;")
                delete_btn.clicked.connect(lambda _, project_id=id: self.delete_project(project_id))
                
                action_layout.addWidget(details_btn)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.projects_table.setCellWidget(row, 7, action_widget)
            
            self.projects_table.resizeColumnsToContents()
    
    def load_tasks(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.name, p.name, t.status, t.priority, m.name, t.deadline
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN team_members m ON t.assignee_id = m.id
                WHERE t.status != 'deleted'
            ''')
            tasks = cursor.fetchall()
            
            self.tasks_table.setRowCount(len(tasks))
            
            for row, (id, name, project, status, priority, assignee, deadline) in enumerate(tasks):
                self.tasks_table.setItem(row, 0, QTableWidgetItem(name))
                self.tasks_table.setItem(row, 1, QTableWidgetItem(project))
                
                # Statut
                status_item = QTableWidgetItem()
                if status == "completed":
                    status_item.setText("Terminé")
                    status_item.setForeground(QColor('#27ae60'))
                elif status == "in_progress":
                    status_item.setText("En cours")
                    status_item.setForeground(QColor('#3498db'))
                elif status == "in_review":
                    status_item.setText("En revue")
                    status_item.setForeground(QColor('#f39c12'))
                else:
                    status_item.setText("À faire")
                self.tasks_table.setItem(row, 2, status_item)
                
                # Priorité
                priority_item = QTableWidgetItem()
                if priority == "high":
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_high.png')))
                    priority_item.setText("Haute")
                elif priority == "medium":
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_medium.png')))
                    priority_item.setText("Moyenne")
                else:
                    priority_item.setIcon(QIcon(self.resource_path('icons/priority_low.png')))
                    priority_item.setText("Basse")
                self.tasks_table.setItem(row, 3, priority_item)
                
                self.tasks_table.setItem(row, 4, QTableWidgetItem(assignee if assignee else "Non assigné"))
                self.tasks_table.setItem(row, 5, QTableWidgetItem(deadline if deadline else "-"))
                
                # Boutons d'action
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)
                
                complete_btn = QPushButton()
                complete_btn.setIcon(QIcon(self.resource_path('icons/complete.png')))
                complete_btn.setToolTip("Marquer comme terminé")
                complete_btn.setFixedSize(30, 30)
                complete_btn.setStyleSheet("background-color: transparent;")
                complete_btn.clicked.connect(lambda _, task_id=id: self.complete_task(task_id))
                
                edit_btn = QPushButton()
                edit_btn.setIcon(QIcon(self.resource_path('icons/edit.png')))
                edit_btn.setToolTip("Modifier")
                edit_btn.setFixedSize(30, 30)
                edit_btn.setStyleSheet("background-color: transparent;")
                edit_btn.clicked.connect(lambda _, task_id=id: self.edit_task(task_id))
                
                delete_btn = QPushButton()
                delete_btn.setIcon(QIcon(self.resource_path('icons/delete.png')))
                delete_btn.setToolTip("Supprimer")
                delete_btn.setFixedSize(30, 30)
                delete_btn.setStyleSheet("background-color: transparent;")
                delete_btn.clicked.connect(lambda _, task_id=id: self.delete_task(task_id))
                
                action_layout.addWidget(complete_btn)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.tasks_table.setCellWidget(row, 6, action_widget)
            
            self.tasks_table.resizeColumnsToContents()
    
    def load_activities(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.timestamp, u.full_name, a.action, a.details
                FROM activities a
                LEFT JOIN users u ON a.user_id = u.id
                ORDER BY a.timestamp DESC
                LIMIT 50
            ''')
            activities = cursor.fetchall()
            
            self.activities_table.setRowCount(len(activities))
            
            for row, (timestamp, user, action, details) in enumerate(activities):
                self.activities_table.setItem(row, 0, QTableWidgetItem(timestamp))
                self.activities_table.setItem(row, 1, QTableWidgetItem(user if user else "Système"))
                self.activities_table.setItem(row, 2, QTableWidgetItem(action))
                self.activities_table.setItem(row, 3, QTableWidgetItem(details if details else ""))
            
            self.activities_table.resizeColumnsToContents()
    
    def load_access_table(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, full_name, role FROM users")
            users = cursor.fetchall()
            
            self.access_table.setRowCount(len(users))
            
            for row, (id, username, full_name, role) in enumerate(users):
                self.access_table.setItem(row, 0, QTableWidgetItem(full_name))
                self.access_table.setItem(row, 1, QTableWidgetItem(role.capitalize()))
                
                # Niveau d'accès
                access_item = QTableWidgetItem()
                if role == "admin":
                    access_item.setText("Administrateur")
                    access_item.setForeground(QColor('#e74c3c'))
                elif role == "manager":
                    access_item.setText("Gestionnaire")
                    access_item.setForeground(QColor('#3498db'))
                else:
                    access_item.setText("Utilisateur")
                self.access_table.setItem(row, 2, access_item)
                
                # Boutons d'action
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(5)
                
                edit_btn = QPushButton()
                edit_btn.setIcon(QIcon(self.resource_path('icons/edit.png')))
                edit_btn.setToolTip("Modifier")
                edit_btn.setFixedSize(30, 30)
                edit_btn.setStyleSheet("background-color: transparent;")
                edit_btn.clicked.connect(lambda _, user_id=id: self.edit_user_access(user_id))
                
                action_layout.addWidget(edit_btn)
                self.access_table.setCellWidget(row, 3, action_widget)
            
            self.access_table.resizeColumnsToContents()
    
    def load_user_preferences(self):
        # Charger les préférences utilisateur depuis la base de données
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, email, phone FROM users WHERE id=?", (self.current_user['id'],))
            user_data = cursor.fetchone()
            
            if user_data:
                self.name_edit.setText(user_data[0])
                self.email_edit.setText(user_data[1])
                self.phone_edit.setText(user_data[2] if user_data[2] else "")
    
    def update_project_filter(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM projects WHERE status != 'deleted'")
            projects = cursor.fetchall()
            
            self.task_project_filter.clear()
            self.task_project_filter.addItem("Tous les projets")
            
            for id, name in projects:
                self.task_project_filter.addItem(name, id)
    
    def filter_team_members(self):
        search_text = self.team_search.text().lower()
        role_filter = self.role_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        for row in range(self.team_table.rowCount()):
            name = self.team_table.item(row, 0).text().lower()
            role = self.team_table.item(row, 1).text()
            status = self.team_table.item(row, 5).text()
            
            name_match = search_text in name
            role_match = role_filter == "Tous les rôles" or role == role_filter
            status_match = status_filter == "Tous statuts" or status == status_filter
            
            self.team_table.setRowHidden(row, not (name_match and role_match and status_match))
    
    def filter_projects(self):
        search_text = self.project_search.text().lower()
        status_filter = self.status_filter_proj.currentText()
        priority_filter = self.priority_filter.currentText()
        
        for row in range(self.projects_table.rowCount()):
            name = self.projects_table.item(row, 0).text().lower()
            status = self.projects_table.item(row, 1).text()
            priority = self.projects_table.item(row, 3).text()
            
            name_match = search_text in name
            status_match = status_filter == "Tous statuts" or status == status_filter
            priority_match = priority_filter == "Toutes priorités" or priority == priority_filter
            
            self.projects_table.setRowHidden(row, not (name_match and status_match and priority_match))
    
    def filter_tasks(self):
        search_text = self.task_search.text().lower()
        status_filter = self.task_status_filter.currentText()
        priority_filter = self.task_priority_filter.currentText()
        project_filter = self.task_project_filter.currentText()
        
        for row in range(self.tasks_table.rowCount()):
            name = self.tasks_table.item(row, 0).text().lower()
            project = self.tasks_table.item(row, 1).text()
            status = self.tasks_table.item(row, 2).text()
            priority = self.tasks_table.item(row, 3).text()
            
            name_match = search_text in name
            project_match = project_filter == "Tous les projets" or project == project_filter
            status_match = status_filter == "Tous statuts" or status == status_filter
            priority_match = priority_filter == "Toutes priorités" or priority == priority_filter
            
            self.tasks_table.setRowHidden(row, not (name_match and project_match and status_match and priority_match))
    
    def update_dashboard(self):
        self.load_kpis()
        self.load_activities()
        self.update_charts()
        self.statusBar().showMessage("Tableau de bord actualisé", 3000)
    
    def update_charts(self):
        # Performance de l'équipe
        self.performance_graph.clear()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, performance FROM team_members WHERE status='active' ORDER BY performance DESC")
            members = cursor.fetchall()
            
            names = [m[0] for m in members]
            performance = [m[1] for m in members]
            
            bg = pg.BarGraphItem(x=range(len(names)), height=performance, width=0.6, brush='#3498db')
            self.performance_graph.addItem(bg)
            
            self.performance_graph.getAxis('bottom').setTicks([[(i, name) for i, name in enumerate(names)]])
            self.performance_graph.setYRange(0, 100)
            self.performance_graph.setLabel('left', 'Performance (%)')
            self.performance_graph.setTitle("Performance de l'équipe")
        
        # Avancement des projets
        self.project_progress_graph.clear()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, progress FROM projects WHERE status != 'completed' AND status != 'deleted' ORDER BY progress DESC")
            projects = cursor.fetchall()
            
            names = [p[0] for p in projects]
            progress = [p[1] for p in projects]
            
            bg = pg.BarGraphItem(x=range(len(names)), height=progress, width=0.6, brush='#2ecc71')
            self.project_progress_graph.addItem(bg)
            
            self.project_progress_graph.getAxis('bottom').setTicks([[(i, name) for i, name in enumerate(names)]])
            self.project_progress_graph.setYRange(0, 100)
            self.project_progress_graph.setLabel('left', 'Progression (%)')
            self.project_progress_graph.setTitle("Avancement des projets")
    
    def generate_report(self):
        report_type = self.report_type.currentText()
        period = self.report_period.currentText()
        
        # Effacer les onglets précédents
        for i in reversed(range(self.graph_layout.count())):
            self.graph_layout.itemAt(i).widget().deleteLater()
        
        # Effacer le tableau de données
        self.report_data_table.clear()
        
        if report_type == "Performance d'équipe":
            self.generate_team_performance_report(period)
        elif report_type == "Avancement projets":
            self.generate_project_progress_report(period)
        elif report_type == "Charge de travail":
            self.generate_workload_report(period)
        elif report_type == "Indicateurs clés":
            self.generate_kpi_report(period)
        elif report_type == "Analyse budgétaire":
            self.generate_budget_report(period)
        
        self.statusBar().showMessage(f"Rapport '{report_type}' généré pour la période '{period}'", 3000)
    
    def generate_team_performance_report(self, period):
        # Graphique
        fig = plt.figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, performance FROM team_members WHERE status='active' ORDER BY performance DESC")
            data = cursor.fetchall()
            
            names = [d[0] for d in data]
            performance = [d[1] for d in data]
            
            bars = ax.bar(names, performance, color='#3498db')
            ax.set_title("Performance de l'équipe")
            ax.set_ylabel("Performance (%)")
            ax.set_ylim(0, 100)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}%', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            self.graph_layout.addWidget(canvas)
            
            # Données
            self.report_data_table.setColumnCount(2)
            self.report_data_table.setHorizontalHeaderLabels(["Membre", "Performance (%)"])
            self.report_data_table.setRowCount(len(data))
            
            for row, (name, perf) in enumerate(data):
                self.report_data_table.setItem(row, 0, QTableWidgetItem(name))
                self.report_data_table.setItem(row, 1, QTableWidgetItem(str(perf)))
            
            self.report_data_table.resizeColumnsToContents()
    
    def generate_project_progress_report(self, period):
        # Graphique
        fig = plt.figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, progress, status FROM projects WHERE status != 'deleted' ORDER BY progress DESC")
            data = cursor.fetchall()
            
            names = [d[0] for d in data]
            progress = [d[1] for d in data]
            statuses = [d[2] for d in data]
            
            colors = []
            for status in statuses:
                if status == "completed":
                    colors.append('#2ecc71')
                elif status == "late":
                    colors.append('#e74c3c')
                else:
                    colors.append('#3498db')
            
            bars = ax.bar(names, progress, color=colors)
            ax.set_title("Avancement des projets")
            ax.set_ylabel("Progression (%)")
            ax.set_ylim(0, 100)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}%', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            self.graph_layout.addWidget(canvas)
            
            # Données
            self.report_data_table.setColumnCount(4)
            self.report_data_table.setHorizontalHeaderLabels(["Projet", "Progression (%)", "Statut", "Budget"])
            self.report_data_table.setRowCount(len(data))
            
            for row, (name, progress, status, _) in enumerate(data):
                self.report_data_table.setItem(row, 0, QTableWidgetItem(name))
                self.report_data_table.setItem(row, 1, QTableWidgetItem(str(progress)))
                
                status_item = QTableWidgetItem()
                if status == "completed":
                    status_item.setText("Terminé")
                elif status == "late":
                    status_item.setText("En retard")
                elif status == "in_progress":
                    status_item.setText("En cours")
                else:
                    status_item.setText("Planification")
                self.report_data_table.setItem(row, 2, status_item)
                
                # Ajouter le budget (requête supplémentaire)
                cursor.execute("SELECT budget FROM projects WHERE name=?", (name,))
                budget = cursor.fetchone()[0]
                self.report_data_table.setItem(row, 3, QTableWidgetItem(f"€{budget:,.2f}"))
            
            self.report_data_table.resizeColumnsToContents()
    
    def generate_workload_report(self, period):
        # Graphique
        fig = plt.figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.name, COUNT(t.id) 
                FROM team_members m
                LEFT JOIN tasks t ON m.id = t.assignee_id AND t.status != 'completed' AND t.status != 'deleted'
                WHERE m.status = 'active'
                GROUP BY m.id
                ORDER BY COUNT(t.id) DESC
            ''')
            data = cursor.fetchall()
            
            names = [d[0] for d in data]
            task_counts = [d[1] for d in data]
            
            bars = ax.bar(names, task_counts, color='#9b59b6')
            ax.set_title("Charge de travail par membre")
            ax.set_ylabel("Nombre de tâches")
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            self.graph_layout.addWidget(canvas)
            
            # Données
            self.report_data_table.setColumnCount(3)
            self.report_data_table.setHorizontalHeaderLabels(["Membre", "Tâches en cours", "Performance"])
            self.report_data_table.setRowCount(len(data))
            
            for row, (name, task_count) in enumerate(data):
                self.report_data_table.setItem(row, 0, QTableWidgetItem(name))
                self.report_data_table.setItem(row, 1, QTableWidgetItem(str(task_count)))
                
                # Ajouter la performance
                cursor.execute("SELECT performance FROM team_members WHERE name=?", (name,))
                perf = cursor.fetchone()[0]
                perf_item = QTableWidgetItem(f"{perf}%")
                
                if perf >= 90:
                    perf_item.setForeground(QColor('#27ae60'))
                elif perf >= 80:
                    perf_item.setForeground(QColor('#f39c12'))
                else:
                    perf_item.setForeground(QColor('#e74c3c'))
                
                self.report_data_table.setItem(row, 2, perf_item)
            
            self.report_data_table.resizeColumnsToContents()
    
    def generate_kpi_report(self, period):
        # Graphique
        fig = plt.figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, value, target FROM kpis")
            data = cursor.fetchall()
            
            names = [d[0] for d in data]
            values = [d[1] for d in data]
            targets = [d[2] for d in data]
            
            x = range(len(names))
            width = 0.35
            
            bars1 = ax.bar(x, values, width, label='Valeur actuelle', color='#3498db')
            bars2 = ax.bar([p + width for p in x], targets, width, label='Cible', color='#e74c3c')
            
            ax.set_title("Indicateurs clés de performance")
            ax.set_ylabel("Valeur")
            ax.set_xticks([p + width/2 for p in x])
            ax.set_xticklabels(names)
            ax.legend()
            
            for bar in bars1:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}', ha='center', va='bottom')
            
            for bar in bars2:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            self.graph_layout.addWidget(canvas)
            
            # Données
            self.report_data_table.setColumnCount(4)
            self.report_data_table.setHorizontalHeaderLabels(["KPI", "Valeur", "Cible", "Écart"])
            self.report_data_table.setRowCount(len(data))
            
            for row, (name, value, target) in enumerate(data):
                self.report_data_table.setItem(row, 0, QTableWidgetItem(name.capitalize()))
                self.report_data_table.setItem(row, 1, QTableWidgetItem(str(value)))
                self.report_data_table.setItem(row, 2, QTableWidgetItem(str(target)))
                
                diff = value - target
                diff_item = QTableWidgetItem(f"{diff:+}")
                
                if diff >= 0:
                    diff_item.setForeground(QColor('#27ae60'))
                else:
                    diff_item.setForeground(QColor('#e74c3c'))
                
                self.report_data_table.setItem(row, 3, diff_item)
            
            self.report_data_table.resizeColumnsToContents()
    
    def generate_budget_report(self, period):
        # Graphique
        fig = plt.figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, budget FROM projects WHERE status != 'deleted' ORDER BY budget DESC")
            data = cursor.fetchall()
            
            names = [d[0] for d in data]
            budgets = [d[1] for d in data]
            
            bars = ax.bar(names, budgets, color='#f39c12')
            ax.set_title("Répartition budgétaire par projet")
            ax.set_ylabel("Budget (€)")
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'€{height:,.2f}', ha='center', va='bottom')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            self.graph_layout.addWidget(canvas)
            
            # Données
            self.report_data_table.setColumnCount(3)
            self.report_data_table.setHorizontalHeaderLabels(["Projet", "Budget", "Statut"])
            self.report_data_table.setRowCount(len(data))
            
            for row, (name, budget) in enumerate(data):
                self.report_data_table.setItem(row, 0, QTableWidgetItem(name))
                self.report_data_table.setItem(row, 1, QTableWidgetItem(f"€{budget:,.2f}"))
                
                # Ajouter le statut
                cursor.execute("SELECT status FROM projects WHERE name=?", (name,))
                status = cursor.fetchone()[0]
                
                status_item = QTableWidgetItem()
                if status == "completed":
                    status_item.setText("Terminé")
                elif status == "late":
                    status_item.setText("En retard")
                elif status == "in_progress":
                    status_item.setText("En cours")
                else:
                    status_item.setText("Planification")
                
                self.report_data_table.setItem(row, 2, status_item)
            
            self.report_data_table.resizeColumnsToContents()
    
    def export_report(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Exporter le rapport", "", "PDF Files (*.pdf);;Excel Files (*.xlsx)", options=options)
        
        if file_name:
            try:
                if file_name.endswith('.pdf'):
                    # Exporter en PDF (implémentation simplifiée)
                    QMessageBox.information(self, "Export PDF", "Fonctionnalité PDF en cours de développement")
                elif file_name.endswith('.xlsx'):
                    # Exporter en Excel
                    data = []
                    headers = []
                    
                    for col in range(self.report_data_table.columnCount()):
                        headers.append(self.report_data_table.horizontalHeaderItem(col).text())
                    
                    for row in range(self.report_data_table.rowCount()):
                        row_data = []
                        for col in range(self.report_data_table.columnCount()):
                            item = self.report_data_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        data.append(row_data)
                    
                    df = pd.DataFrame(data, columns=headers)
                    df.to_excel(file_name, index=False)
                    
                    self.statusBar().showMessage(f"Rapport exporté vers {file_name}", 3000)
                    QMessageBox.information(self, "Export réussi", f"Le rapport a été exporté avec succès vers {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de l'export: {str(e)}")
    
    def show_add_member_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un membre d'équipe")
        dialog.setFixedSize(400, 500)
        
        layout = QFormLayout(dialog)
        
        name_edit = QLineEdit()
        role_combo = QComboBox()
        role_combo.addItems(["Chef de projet", "Développeur", "Designer", "RH", "Marketing", "Finance"])
        
        department_combo = QComboBox()
        department_combo.addItems(["IT", "RH", "Marketing", "Finance", "Direction"])
        
        performance_spin = QSpinBox()
        performance_spin.setRange(0, 100)
        performance_spin.setValue(80)
        
        hire_date = QDateEdit(QDate.currentDate())
        hire_date.setCalendarPopup(True)
        
        status_combo = QComboBox()
        status_combo.addItems(["Actif", "Inactif", "En congé"])
        
        skills_edit = QLineEdit()
        skills_edit.setPlaceholderText("Compétences séparées par des virgules")
        
        notes_edit = QTextEdit()
        notes_edit.setPlaceholderText("Notes supplémentaires...")
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addRow("Nom complet:", name_edit)
        layout.addRow("Rôle:", role_combo)
        layout.addRow("Département:", department_combo)
        layout.addRow("Performance initiale (%):", performance_spin)
        layout.addRow("Date d'embauche:", hire_date)
        layout.addRow("Statut:", status_combo)
        layout.addRow("Compétences:", skills_edit)
        layout.addRow("Notes:", notes_edit)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text()
            role = role_combo.currentText()
            department = department_combo.currentText()
            performance = performance_spin.value()
            hire_date_str = hire_date.date().toString("yyyy-MM-dd")
            status = status_combo.currentText().lower().replace(" ", "_")
            skills = skills_edit.text()
            notes = notes_edit.toPlainText()
            
            if name:
                with self.db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO team_members (name, role, department, performance, hire_date, status, skills, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, role, department, performance, hire_date_str, status, skills, notes))
                    conn.commit()
                
                self.load_team_members()
                self.log_activity(f"Ajout du membre d'équipe: {name}")
                self.statusBar().showMessage(f"Membre d'équipe {name} ajouté avec succès", 3000)
            else:
                QMessageBox.warning(self, "Erreur", "Le nom du membre est obligatoire")
    
    def edit_member(self, member_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, role, department, performance, hire_date, status, skills, notes FROM team_members WHERE id=?", (member_id,))
            member = cursor.fetchone()
            
            if member:
                dialog = QDialog(self)
                dialog.setWindowTitle("Modifier un membre d'équipe")
                dialog.setFixedSize(400, 500)
                
                layout = QFormLayout(dialog)
                
                name_edit = QLineEdit(member[0])
                role_combo = QComboBox()
                role_combo.addItems(["Chef de projet", "Développeur", "Designer", "RH", "Marketing", "Finance"])
                role_combo.setCurrentText(member[1])
                
                department_combo = QComboBox()
                department_combo.addItems(["IT", "RH", "Marketing", "Finance", "Direction"])
                department_combo.setCurrentText(member[2])
                
                performance_spin = QSpinBox()
                performance_spin.setRange(0, 100)
                performance_spin.setValue(member[3])
                
                hire_date = QDateEdit(QDate.fromString(member[4], "yyyy-MM-dd"))
                hire_date.setCalendarPopup(True)
                
                status_combo = QComboBox()
                status_combo.addItems(["Actif", "Inactif", "En congé"])
                status_map = {"active": "Actif", "inactive": "Inactif", "on_leave": "En congé"}
                status_combo.setCurrentText(status_map.get(member[5], "Actif"))
                
                skills_edit = QLineEdit(member[6] if member[6] else "")
                skills_edit.setPlaceholderText("Compétences séparées par des virgules")
                
                notes_edit = QTextEdit(member[7] if member[7] else "")
                notes_edit.setPlaceholderText("Notes supplémentaires...")
                
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                
                layout.addRow("Nom complet:", name_edit)
                layout.addRow("Rôle:", role_combo)
                layout.addRow("Département:", department_combo)
                layout.addRow("Performance (%):", performance_spin)
                layout.addRow("Date d'embauche:", hire_date)
                layout.addRow("Statut:", status_combo)
                layout.addRow("Compétences:", skills_edit)
                layout.addRow("Notes:", notes_edit)
                layout.addRow(button_box)
                
                if dialog.exec_() == QDialog.Accepted:
                    name = name_edit.text()
                    role = role_combo.currentText()
                    department = department_combo.currentText()
                    performance = performance_spin.value()
                    hire_date_str = hire_date.date().toString("yyyy-MM-dd")
                    status = status_combo.currentText().lower().replace(" ", "_")
                    skills = skills_edit.text()
                    notes = notes_edit.toPlainText()
                    
                    if name:
                        cursor.execute('''
                            UPDATE team_members 
                            SET name=?, role=?, department=?, performance=?, hire_date=?, status=?, skills=?, notes=?
                            WHERE id=?
                        ''', (name, role, department, performance, hire_date_str, status, skills, notes, member_id))
                        conn.commit()
                        
                        self.load_team_members()
                        self.log_activity(f"Mise à jour du membre d'équipe: {name}")
                        self.statusBar().showMessage(f"Membre d'équipe {name} mis à jour avec succès", 3000)
                    else:
                        QMessageBox.warning(self, "Erreur", "Le nom du membre est obligatoire")
    
    def delete_member(self, member_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM team_members WHERE id=?", (member_id,))
            member_name = cursor.fetchone()[0]
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer le membre {member_name}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Marquer comme supprimé plutôt que de supprimer réellement
                cursor.execute("UPDATE team_members SET status='deleted' WHERE id=?", (member_id,))
                conn.commit()
                
                self.load_team_members()
                self.log_activity(f"Suppression du membre d'équipe: {member_name}")
                self.statusBar().showMessage(f"Membre d'équipe {member_name} supprimé", 3000)
    
    def show_add_project_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouveau projet")
        dialog.setFixedSize(500, 500)
        
        layout = QFormLayout(dialog)
        
        name_edit = QLineEdit()
        desc_edit = QTextEdit()
        desc_edit.setPlaceholderText("Description du projet...")
        
        start_date = QDateEdit(QDate.currentDate())
        start_date.setCalendarPopup(True)
        
        deadline = QDateEdit(QDate.currentDate().addMonths(1))
        deadline.setCalendarPopup(True)
        
        budget_spin = QDoubleSpinBox()
        budget_spin.setRange(0, 1000000)
        budget_spin.setPrefix("€ ")
        budget_spin.setValue(10000)
        
        status_combo = QComboBox()
        status_combo.addItems(["Planification", "En cours", "En retard", "Terminé"])
        
        priority_combo = QComboBox()
        priority_combo.addItems(["Haute", "Moyenne", "Basse"])
        
        manager_combo = QComboBox()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM team_members WHERE status='active'")
            managers = cursor.fetchall()
            
            for id, name in managers:
                manager_combo.addItem(name, id)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addRow("Nom du projet:", name_edit)
        layout.addRow("Description:", desc_edit)
        layout.addRow("Date de début:", start_date)
        layout.addRow("Échéance:", deadline)
        layout.addRow("Budget:", budget_spin)
        layout.addRow("Statut:", status_combo)
        layout.addRow("Priorité:", priority_combo)
        layout.addRow("Responsable:", manager_combo)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text()
            description = desc_edit.toPlainText()
            start_date_str = start_date.date().toString("yyyy-MM-dd")
            deadline_str = deadline.date().toString("yyyy-MM-dd")
            budget = budget_spin.value()
            status = status_combo.currentText().lower().replace(" ", "_")
            priority = priority_combo.currentText().lower()
            manager_id = manager_combo.currentData()
            
            if name:
                with self.db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO projects (name, description, start_date, deadline, budget, status, priority, manager_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, description, start_date_str, deadline_str, budget, status, priority, manager_id))
                    conn.commit()
                
                self.load_projects()
                self.update_project_filter()
                self.log_activity(f"Ajout du projet: {name}")
                self.statusBar().showMessage(f"Projet {name} ajouté avec succès", 3000)
            else:
                QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire")
    
    def edit_project(self, project_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.name, p.description, p.start_date, p.deadline, p.budget, p.status, p.priority, p.manager_id, t.name
                FROM projects p
                LEFT JOIN team_members t ON p.manager_id = t.id
                WHERE p.id=?
            ''', (project_id,))
            project = cursor.fetchone()
            
            if project:
                dialog = QDialog(self)
                dialog.setWindowTitle("Modifier un projet")
                dialog.setFixedSize(500, 500)
                
                layout = QFormLayout(dialog)
                
                name_edit = QLineEdit(project[0])
                desc_edit = QTextEdit(project[1] if project[1] else "")
                desc_edit.setPlaceholderText("Description du projet...")
                
                start_date = QDateEdit(QDate.fromString(project[2], "yyyy-MM-dd"))
                start_date.setCalendarPopup(True)
                
                deadline = QDateEdit(QDate.fromString(project[3], "yyyy-MM-dd"))
                deadline.setCalendarPopup(True)
                
                budget_spin = QDoubleSpinBox()
                budget_spin.setRange(0, 1000000)
                budget_spin.setPrefix("€ ")
                budget_spin.setValue(project[4])
                
                status_combo = QComboBox()
                status_combo.addItems(["Planification", "En cours", "En retard", "Terminé"])
                status_map = {
                    "planning": "Planification",
                    "in_progress": "En cours",
                    "late": "En retard",
                    "completed": "Terminé"
                }
                status_combo.setCurrentText(status_map.get(project[5], "Planification"))
                
                priority_combo = QComboBox()
                priority_combo.addItems(["Haute", "Moyenne", "Basse"])
                priority_map = {
                    "high": "Haute",
                    "medium": "Moyenne",
                    "low": "Basse"
                }
                priority_combo.setCurrentText(priority_map.get(project[6], "Moyenne"))
                
                manager_combo = QComboBox()
                cursor.execute("SELECT id, name FROM team_members WHERE status='active'")
                managers = cursor.fetchall()
                
                current_manager_index = 0
                for idx, (id, name) in enumerate(managers):
                    manager_combo.addItem(name, id)
                    if id == project[7]:
                        current_manager_index = idx
                
                manager_combo.setCurrentIndex(current_manager_index)
                
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                
                layout.addRow("Nom du projet:", name_edit)
                layout.addRow("Description:", desc_edit)
                layout.addRow("Date de début:", start_date)
                layout.addRow("Échéance:", deadline)
                layout.addRow("Budget:", budget_spin)
                layout.addRow("Statut:", status_combo)
                layout.addRow("Priorité:", priority_combo)
                layout.addRow("Responsable:", manager_combo)
                layout.addRow(button_box)
                
                if dialog.exec_() == QDialog.Accepted:
                    name = name_edit.text()
                    description = desc_edit.toPlainText()
                    start_date_str = start_date.date().toString("yyyy-MM-dd")
                    deadline_str = deadline.date().toString("yyyy-MM-dd")
                    budget = budget_spin.value()
                    status = status_combo.currentText().lower().replace(" ", "_")
                    priority = priority_combo.currentText().lower()
                    manager_id = manager_combo.currentData()
                    
                    if name:
                        cursor.execute('''
                            UPDATE projects 
                            SET name=?, description=?, start_date=?, deadline=?, budget=?, status=?, priority=?, manager_id=?
                            WHERE id=?
                        ''', (name, description, start_date_str, deadline_str, budget, status, priority, manager_id, project_id))
                        conn.commit()
                        
                        self.load_projects()
                        self.update_project_filter()
                        self.log_activity(f"Mise à jour du projet: {name}")
                        self.statusBar().showMessage(f"Projet {name} mis à jour avec succès", 3000)
                    else:
                        QMessageBox.warning(self, "Erreur", "Le nom du projet est obligatoire")
    
    def show_project_details(self, project_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.name, p.description, p.start_date, p.deadline, p.budget, p.status, p.priority, p.progress, 
                       t.name, p.manager_id
                FROM projects p
                LEFT JOIN team_members t ON p.manager_id = t.id
                WHERE p.id=?
            ''', (project_id,))
            project = cursor.fetchone()
            
            if project:
                dialog = QDialog(self)
                dialog.setWindowTitle(f"Détails du projet: {project[0]}")
                dialog.setFixedSize(600, 500)
                
                layout = QVBoxLayout(dialog)
                
                # Informations de base
                info_group = QGroupBox("Informations du projet")
                info_layout = QFormLayout(info_group)
                
                name_label = QLabel(project[0])
                name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
                
                desc_label = QLabel(project[1] if project[1] else "Aucune description")
                desc_label.setWordWrap(True)
                
                start_date = QLabel(project[2])
                deadline = QLabel(project[3])
                budget = QLabel(f"€{project[4]:,.2f}")
                
                status = QLabel()
                status_map = {
                    "planning": ("Planification", "#3498db"),
                    "in_progress": ("En cours", "#2ecc71"),
                    "late": ("En retard", "#e74c3c"),
                    "completed": ("Terminé", "#9b59b6")
                }
                status_text, status_color = status_map.get(project[5], ("Inconnu", "#000000"))
                status.setText(status_text)
                status.setStyleSheet(f"color: {status_color}; font-weight: bold;")
                
                priority = QLabel()
                priority_map = {
                    "high": ("Haute", "#e74c3c"),
                    "medium": ("Moyenne", "#f39c12"),
                    "low": ("Basse", "#2ecc71")
                }
                priority_text, priority_color = priority_map.get(project[6], ("Inconnue", "#000000"))
                priority.setText(priority_text)
                priority.setStyleSheet(f"color: {priority_color}; font-weight: bold;")
                
                progress = QLabel(f"{project[7]}%")
                
                manager = QLabel(project[8] if project[8] else "Non assigné")
                
                info_layout.addRow("Nom:", name_label)
                info_layout.addRow("Description:", desc_label)
                info_layout.addRow("Date de début:", start_date)
                info_layout.addRow("Échéance:", deadline)
                info_layout.addRow("Budget:", budget)
                info_layout.addRow("Statut:", status)
                info_layout.addRow("Priorité:", priority)
                info_layout.addRow("Progression:", progress)
                info_layout.addRow("Responsable:", manager)
                
                # Tâches du projet
                tasks_group = QGroupBox("Tâches associées")
                tasks_layout = QVBoxLayout(tasks_group)
                
                tasks_table = QTableWidget()
                tasks_table.setColumnCount(5)
                tasks_table.setHorizontalHeaderLabels(["Nom", "Statut", "Priorité", "Assigné à", "Échéance"])
                tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
                tasks_table.verticalHeader().setVisible(False)
                
                cursor.execute('''
                    SELECT t.name, t.status, t.priority, m.name, t.deadline
                    FROM tasks t
                    LEFT JOIN team_members m ON t.assignee_id = m.id
                    WHERE t.project_id=? AND t.status != 'deleted'
                ''', (project_id,))
                tasks = cursor.fetchall()
                
                tasks_table.setRowCount(len(tasks))
                
                for row, (name, status, priority, assignee, deadline) in enumerate(tasks):
                    tasks_table.setItem(row, 0, QTableWidgetItem(name))
                    
                    # Statut
                    status_item = QTableWidgetItem()
                    if status == "completed":
                        status_item.setText("Terminé")
                        status_item.setForeground(QColor('#2ecc71'))
                    elif status == "in_progress":
                        status_item.setText("En cours")
                        status_item.setForeground(QColor('#3498db'))
                    elif status == "in_review":
                        status_item.setText("En revue")
                        status_item.setForeground(QColor('#f39c12'))
                    else:
                        status_item.setText("À faire")
                    tasks_table.setItem(row, 1, status_item)
                    
                    # Priorité
                    priority_item = QTableWidgetItem()
                    if priority == "high":
                        priority_item.setText("Haute")
                        priority_item.setForeground(QColor('#e74c3c'))
                    elif priority == "medium":
                        priority_item.setText("Moyenne")
                        priority_item.setForeground(QColor('#f39c12'))
                    else:
                        priority_item.setText("Basse")
                        priority_item.setForeground(QColor('#2ecc71'))
                    tasks_table.setItem(row, 2, priority_item)
                    
                    tasks_table.setItem(row, 3, QTableWidgetItem(assignee if assignee else "Non assigné"))
                    tasks_table.setItem(row, 4, QTableWidgetItem(deadline if deadline else "-"))
                
                tasks_table.resizeColumnsToContents()
                tasks_layout.addWidget(tasks_table)
                
                # Boutons
                button_box = QDialogButtonBox(QDialogButtonBox.Close)
                button_box.rejected.connect(dialog.reject)
                
                layout.addWidget(info_group)
                layout.addWidget(tasks_group)
                layout.addWidget(button_box)
                
                dialog.exec_()
    
    def delete_project(self, project_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM projects WHERE id=?", (project_id,))
            project_name = cursor.fetchone()[0]
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer le projet {project_name}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Marquer comme supprimé plutôt que de supprimer réellement
                cursor.execute("UPDATE projects SET status='deleted' WHERE id=?", (project_id,))
                conn.commit()
                
                self.load_projects()
                self.update_project_filter()
                self.log_activity(f"Suppression du projet: {project_name}")
                self.statusBar().showMessage(f"Projet {project_name} supprimé", 3000)
    
    def show_add_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle tâche")
        dialog.setFixedSize(400, 400)
        
        layout = QFormLayout(dialog)
        
        name_edit = QLineEdit()
        
        project_combo = QComboBox()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM projects WHERE status != 'completed' AND status != 'deleted'")
            projects = cursor.fetchall()
            
            for id, name in projects:
                project_combo.addItem(name, id)
        
        desc_edit = QTextEdit()
        desc_edit.setPlaceholderText("Description de la tâche...")
        
        status_combo = QComboBox()
        status_combo.addItems(["À faire", "En cours", "En revue"])
        
        priority_combo = QComboBox()
        priority_combo.addItems(["Haute", "Moyenne", "Basse"])
        
        assignee_combo = QComboBox()
        assignee_combo.addItem("Non assigné", None)
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM team_members WHERE status='active'")
            members = cursor.fetchall()
            
            for id, name in members:
                assignee_combo.addItem(name, id)
        
        deadline_edit = QDateEdit(QDate.currentDate().addDays(7))
        deadline_edit.setCalendarPopup(True)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        layout.addRow("Nom de la tâche:", name_edit)
        layout.addRow("Projet:", project_combo)
        layout.addRow("Description:", desc_edit)
        layout.addRow("Statut:", status_combo)
        layout.addRow("Priorité:", priority_combo)
        layout.addRow("Assigné à:", assignee_combo)
        layout.addRow("Échéance:", deadline_edit)
        layout.addRow(button_box)
        
        if dialog.exec_() == QDialog.Accepted:
            name = name_edit.text()
            project_id = project_combo.currentData()
            description = desc_edit.toPlainText()
            status = status_combo.currentText().lower().replace(" ", "_")
            priority = priority_combo.currentText().lower()
            assignee_id = assignee_combo.currentData()
            deadline = deadline_edit.date().toString("yyyy-MM-dd")
            
            if name and project_id:
                with self.db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO tasks (project_id, name, description, status, priority, assignee_id, deadline)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (project_id, name, description, status, priority, assignee_id, deadline))
                    conn.commit()
                
                self.load_tasks()
                self.log_activity(f"Ajout de la tâche: {name}")
                self.statusBar().showMessage(f"Tâche {name} ajoutée avec succès", 3000)
            else:
                QMessageBox.warning(self, "Erreur", "Le nom de la tâche et le projet sont obligatoires")
    
    def edit_task(self, task_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.name, t.project_id, p.name, t.description, t.status, t.priority, 
                       t.assignee_id, m.name, t.deadline
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN team_members m ON t.assignee_id = m.id
                WHERE t.id=?
            ''', (task_id,))
            task = cursor.fetchone()
            
            if task:
                dialog = QDialog(self)
                dialog.setWindowTitle("Modifier une tâche")
                dialog.setFixedSize(400, 400)
                
                layout = QFormLayout(dialog)
                
                name_edit = QLineEdit(task[0])
                
                project_combo = QComboBox()
                cursor.execute("SELECT id, name FROM projects WHERE status != 'completed' AND status != 'deleted'")
                projects = cursor.fetchall()
                
                current_project_index = 0
                for idx, (id, name) in enumerate(projects):
                    project_combo.addItem(name, id)
                    if id == task[1]:
                        current_project_index = idx
                
                project_combo.setCurrentIndex(current_project_index)
                
                desc_edit = QTextEdit(task[3] if task[3] else "")
                desc_edit.setPlaceholderText("Description de la tâche...")
                
                status_combo = QComboBox()
                status_combo.addItems(["À faire", "En cours", "En revue", "Terminé"])
                status_map = {
                    "todo": "À faire",
                    "in_progress": "En cours",
                    "in_review": "En revue",
                    "completed": "Terminé"
                }
                status_combo.setCurrentText(status_map.get(task[4], "À faire"))
                
                priority_combo = QComboBox()
                priority_combo.addItems(["Haute", "Moyenne", "Basse"])
                priority_map = {
                    "high": "Haute",
                    "medium": "Moyenne",
                    "low": "Basse"
                }
                priority_combo.setCurrentText(priority_map.get(task[5], "Moyenne"))
                
                assignee_combo = QComboBox()
                assignee_combo.addItem("Non assigné", None)
                cursor.execute("SELECT id, name FROM team_members WHERE status='active'")
                members = cursor.fetchall()
                
                current_assignee_index = 0
                for idx, (id, name) in enumerate(members):
                    assignee_combo.addItem(name, id)
                    if id == task[6]:
                        current_assignee_index = idx + 1  # +1 pour "Non assigné"
                
                assignee_combo.setCurrentIndex(current_assignee_index)
                
                deadline_edit = QDateEdit(QDate.fromString(task[8], "yyyy-MM-dd") if task[8] else QDate.currentDate())
                deadline_edit.setCalendarPopup(True)
                
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                
                layout.addRow("Nom de la tâche:", name_edit)
                layout.addRow("Projet:", project_combo)
                layout.addRow("Description:", desc_edit)
                layout.addRow("Statut:", status_combo)
                layout.addRow("Priorité:", priority_combo)
                layout.addRow("Assigné à:", assignee_combo)
                layout.addRow("Échéance:", deadline_edit)
                layout.addRow(button_box)
                
                if dialog.exec_() == QDialog.Accepted:
                    name = name_edit.text()
                    project_id = project_combo.currentData()
                    description = desc_edit.toPlainText()
                    status = status_combo.currentText().lower().replace(" ", "_")
                    priority = priority_combo.currentText().lower()
                    assignee_id = assignee_combo.currentData()
                    deadline = deadline_edit.date().toString("yyyy-MM-dd")
                    
                    if name and project_id:
                        cursor.execute('''
                            UPDATE tasks 
                            SET name=?, project_id=?, description=?, status=?, priority=?, assignee_id=?, deadline=?
                            WHERE id=?
                        ''', (name, project_id, description, status, priority, assignee_id, deadline, task_id))
                        conn.commit()
                        
                        self.load_tasks()
                        self.log_activity(f"Mise à jour de la tâche: {name}")
                        self.statusBar().showMessage(f"Tâche {name} mise à jour avec succès", 3000)
                    else:
                        QMessageBox.warning(self, "Erreur", "Le nom de la tâche et le projet sont obligatoires")
    
    def complete_task(self, task_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM tasks WHERE id=?", (task_id,))
            task_name = cursor.fetchone()[0]
            
            cursor.execute('''
                UPDATE tasks 
                SET status='completed', completed_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (task_id,))
            conn.commit()
            
            self.load_tasks()
            self.log_activity(f"Tâche marquée comme terminée: {task_name}")
            self.statusBar().showMessage(f"Tâche {task_name} marquée comme terminée", 3000)
    
    def delete_task(self, task_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM tasks WHERE id=?", (task_id,))
            task_name = cursor.fetchone()[0]
            
            reply = QMessageBox.question(
                self, 
                "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer la tâche {task_name}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Marquer comme supprimé plutôt que de supprimer réellement
                cursor.execute("UPDATE tasks SET status='deleted' WHERE id=?", (task_id,))
                conn.commit()
                
                self.load_tasks()
                self.log_activity(f"Suppression de la tâche: {task_name}")
                self.statusBar().showMessage(f"Tâche {task_name} supprimée", 3000)
    
    def edit_user_access(self, user_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, full_name, role FROM users WHERE id=?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                dialog = QDialog(self)
                dialog.setWindowTitle(f"Modifier les accès de {user[1]}")
                dialog.setFixedSize(300, 200)
                
                layout = QFormLayout(dialog)
                
                username_label = QLabel(user[0])
                name_label = QLabel(user[1])
                
                role_combo = QComboBox()
                role_combo.addItems(["Administrateur", "Gestionnaire", "Utilisateur"])
                role_map = {
                    "admin": "Administrateur",
                    "manager": "Gestionnaire",
                    "user": "Utilisateur"
                }
                role_combo.setCurrentText(role_map.get(user[2], "Utilisateur"))
                
                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                
                layout.addRow("Nom d'utilisateur:", username_label)
                layout.addRow("Nom complet:", name_label)
                layout.addRow("Rôle:", role_combo)
                layout.addRow(button_box)
                
                if dialog.exec_() == QDialog.Accepted:
                    role = role_combo.currentText().lower()
                    
                    cursor.execute('''
                        UPDATE users 
                        SET role=?
                        WHERE id=?
                    ''', (role, user_id))
                    conn.commit()
                    
                    self.load_access_table()
                    self.log_activity(f"Modification du rôle de {user[1]} en {role}")
                    self.statusBar().showMessage(f"Rôle de {user[1]} mis à jour", 3000)
    
    def save_account_settings(self):
        if not self.current_user:
            QMessageBox.warning(self, "Erreur", "Vous devez être connecté pour modifier vos paramètres")
            return
        
        full_name = self.name_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        current_pwd = self.current_pwd_edit.text()
        new_pwd = self.new_pwd_edit.text()
        confirm_pwd = self.confirm_pwd_edit.text()
        
        if not full_name or not email:
            QMessageBox.warning(self, "Erreur", "Le nom complet et l'email sont obligatoires")
            return
        
        if new_pwd and (new_pwd != confirm_pwd):
            QMessageBox.warning(self, "Erreur", "Les nouveaux mots de passe ne correspondent pas")
            return
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier le mot de passe actuel si un nouveau est fourni
            if new_pwd:
                cursor.execute("SELECT password FROM users WHERE id=?", (self.current_user['id'],))
                db_pwd = cursor.fetchone()[0]
                hashed_current = hashlib.sha256(current_pwd.encode()).hexdigest()
                
                if hashed_current != db_pwd:
                    QMessageBox.warning(self, "Erreur", "Le mot de passe actuel est incorrect")
                    return
            
            # Mettre à jour les informations
            update_fields = []
            update_values = []
            
            update_fields.append("full_name=?")
            update_values.append(full_name)
            
            update_fields.append("email=?")
            update_values.append(email)
            
            if phone:
                update_fields.append("phone=?")
                update_values.append(phone)
            else:
                update_fields.append("phone=NULL")
            
            if new_pwd:
                hashed_new = hashlib.sha256(new_pwd.encode()).hexdigest()
                update_fields.append("password=?")
                update_values.append(hashed_new)
            
            update_values.append(self.current_user['id'])
            
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id=?"
            cursor.execute(query, update_values)
            conn.commit()
            
            # Mettre à jour l'utilisateur courant
            self.current_user['full_name'] = full_name
            self.current_user['email'] = email
            self.user_name.setText(full_name)
            
            self.log_activity("Mise à jour des informations du compte")
            QMessageBox.information(self, "Succès", "Les modifications ont été enregistrées")
            
            # Effacer les champs de mot de passe
            self.current_pwd_edit.clear()
            self.new_pwd_edit.clear()
            self.confirm_pwd_edit.clear()
    
    def save_preferences(self):
        if not self.current_user:
            QMessageBox.warning(self, "Erreur", "Vous devez être connecté pour modifier vos préférences")
            return
        
        theme = self.theme_combo.currentText()
        density = self.density_combo.currentText()
        language = self.language_combo.currentText()
        email_notif = self.email_notif.isChecked()
        app_notif = self.app_notif.isChecked()
        sms_notif = self.sms_notif.isChecked()
        
        # Ici, vous pourriez enregistrer ces préférences dans la base de données
        # Pour cet exemple, nous allons juste afficher un message
        
        QMessageBox.information(
            self, 
            "Préférences enregistrées", 
            f"Vos préférences ont été enregistrées:\n"
            f"Thème: {theme}\n"
            f"Densité: {density}\n"
            f"Langue: {language}\n"
            f"Notifications: Email {'activées' if email_notif else 'désactivées'}, "
            f"App {'activées' if app_notif else 'désactivées'}, "
            f"SMS {'activées' if sms_notif else 'désactivées'}"
        )
        
        self.log_activity("Mise à jour des préférences utilisateur")
    
    def change_page(self, index):
        self.main_content.setCurrentIndex(index)
        
        # Mise à jour du style des boutons de navigation
        for btn in self.nav_buttons:
            btn.setObjectName("")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        self.nav_buttons[index].setObjectName("selected")
        self.nav_buttons[index].style().unpolish(self.nav_buttons[index])
        self.nav_buttons[index].style().polish(self.nav_buttons[index])
        
        # Mettre à jour les données si nécessaire
        if index == 0:  # Dashboard
            self.update_dashboard()
        elif index == 1:  # Équipe
            self.load_team_members()
        elif index == 2:  # Projets
            self.load_projects()
        elif index == 3:  # Tâches
            self.load_tasks()
        elif index == 4:  # Rapports
            pass  # Les rapports sont générés à la demande
        elif index == 5:  # Paramètres
            self.load_access_table()
    
    def closeEvent(self, event):
        if self.current_user:
            self.log_activity(f"Fermeture de l'application par {self.current_user['full_name']}")
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Style global
    app.setStyle("Fusion")
    
    # Police par défaut
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainDashboard()
    window.show()
    sys.exit(app.exec_())