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
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QSize

class DatabaseManager:
    def __init__(self, db_name='leopardo_v2_management.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
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
            conn.commit()

class ManagementDashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.current_user = None

        self.setWindowTitle("Management Dashboard Pro")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setup_topbar()
        main_layout.addWidget(self.topbar)

        self.main_content = QStackedWidget()
        self.main_content.setStyleSheet("background-color: #ffffff;")

        self.setup_dashboard_page()
        self.setup_team_page()
        self.setup_projects_page()
        self.setup_tasks_page()
        self.setup_reports_page()
        self.setup_settings_page()

        main_layout.addWidget(self.main_content)

    def setup_topbar(self):
        self.topbar = QFrame()
        self.topbar.setFixedHeight(70)
        self.topbar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
                border-bottom: 1px solid #3498db;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                padding: 10px 15px;
                border: none;
                font-size: 14px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        topbar_layout = QHBoxLayout(self.topbar)
        topbar_layout.setContentsMargins(15, 10, 15, 10)
        topbar_layout.setSpacing(20)

        logo_text = QLabel("Management Pro")
        logo_text.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db;")
        topbar_layout.addWidget(logo_text)
        topbar_layout.addStretch(1)

        self.nav_buttons = []
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.clicked.connect(lambda: self.change_page(0))
        self.nav_buttons.append(dashboard_btn)
        topbar_layout.addWidget(dashboard_btn)

        management_btn = QPushButton("Management")
        management_menu = QMenu()
        management_menu.addAction("Team", lambda: self.change_page(1))
        management_menu.addAction("Settings", lambda: self.change_page(5))
        management_btn.setMenu(management_menu)
        self.nav_buttons.append(management_btn)
        topbar_layout.addWidget(management_btn)

        topbar_layout.addStretch(1)

    def setup_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        title = QLabel("Management Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.date_picker = QDateEdit(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        refresh_btn = QPushButton("Refresh")
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.date_picker)
        header_layout.addWidget(refresh_btn)

        self.kpi_widget = QWidget()
        self.kpi_layout = QHBoxLayout(self.kpi_widget)
        self.kpi_layout.setSpacing(15)

        graph_widget = QWidget()
        graph_layout = QHBoxLayout(graph_widget)
        graph_layout.setSpacing(15)

        self.performance_graph = pg.PlotWidget()
        self.project_progress_graph = pg.PlotWidget()
        graph_layout.addWidget(self.performance_graph, 1)
        graph_layout.addWidget(self.project_progress_graph, 1)

        activities_widget = QGroupBox("Recent Activities")
        activities_layout = QVBoxLayout(activities_widget)
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(4)
        self.activities_table.setHorizontalHeaderLabels(["Date", "Member", "Action", "Details"])
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

        header = QWidget()
        header_layout = QHBoxLayout(header)

        title = QLabel("Team Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        self.add_member_btn = QPushButton("Add Member")
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

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_member_btn)

        filters = QWidget()
        filters_layout = QHBoxLayout(filters)

        self.team_search = QLineEdit()
        self.team_search.setPlaceholderText("Search a member...")
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "Project Manager", "Developer", "Designer", "HR", "Marketing", "Finance"])
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Statuses", "Active", "Inactive", "On Leave"])

        filters_layout.addWidget(self.team_search)
        filters_layout.addWidget(self.role_filter)
        filters_layout.addWidget(self.status_filter)

        self.team_table = QTableWidget()
        self.team_table.setColumnCount(8)
        self.team_table.setHorizontalHeaderLabels(["Name", "Role", "Department", "Performance", "Hire Date", "Status", "Tasks", "Actions"])
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

        header = QWidget()
        header_layout = QHBoxLayout(header)

        title = QLabel("Project Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        self.add_project_btn = QPushButton("New Project")
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

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_project_btn)

        filters = QWidget()
        filters_layout = QHBoxLayout(filters)

        self.project_search = QLineEdit()
        self.project_search.setPlaceholderText("Search a project...")
        self.status_filter_proj = QComboBox()
        self.status_filter_proj.addItems(["All Statuses", "Planning", "In Progress", "Late", "Completed"])
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All Priorities", "High", "Medium", "Low"])

        filters_layout.addWidget(self.project_search)
        filters_layout.addWidget(self.status_filter_proj)
        filters_layout.addWidget(self.priority_filter)

        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(8)
        self.projects_table.setHorizontalHeaderLabels(["Name", "Status", "Progress", "Priority", "Deadline", "Budget", "Manager", "Actions"])
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

        header = QWidget()
        header_layout = QHBoxLayout(header)

        title = QLabel("Task Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        self.add_task_btn = QPushButton("New Task")
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

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_task_btn)

        filters = QWidget()
        filters_layout = QHBoxLayout(filters)

        self.task_search = QLineEdit()
        self.task_search.setPlaceholderText("Search a task...")
        self.task_status_filter = QComboBox()
        self.task_status_filter.addItems(["All Statuses", "To Do", "In Progress", "In Review", "Completed"])
        self.task_priority_filter = QComboBox()
        self.task_priority_filter.addItems(["All Priorities", "High", "Medium", "Low"])
        self.task_project_filter = QComboBox()
        self.task_project_filter.addItem("All Projects")

        filters_layout.addWidget(self.task_search)
        filters_layout.addWidget(self.task_status_filter)
        filters_layout.addWidget(self.task_priority_filter)
        filters_layout.addWidget(self.task_project_filter)

        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["Name", "Project", "Status", "Priority", "Assigned To", "Deadline", "Actions"])
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

        title = QLabel("Reports and Analytics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        report_options = QWidget()
        options_layout = QHBoxLayout(report_options)

        self.report_type = QComboBox()
        self.report_type.addItems(["Team Performance", "Project Progress", "Workload", "Key Indicators", "Budget Analysis"])
        self.report_period = QComboBox()
        self.report_period.addItems(["Last 7 Days", "Last 30 Days", "Current Quarter", "Current Year", "Custom..."])
        generate_btn = QPushButton("Generate Report")
        export_btn = QPushButton("Export PDF")

        options_layout.addWidget(QLabel("Type:"))
        options_layout.addWidget(self.report_type)
        options_layout.addWidget(QLabel("Period:"))
        options_layout.addWidget(self.report_period)
        options_layout.addWidget(generate_btn)
        options_layout.addWidget(export_btn)

        self.report_view = QTabWidget()
        self.graph_tab = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_tab)
        self.data_tab = QWidget()
        self.data_layout = QVBoxLayout(self.data_tab)
        self.report_data_table = QTableWidget()
        self.data_layout.addWidget(self.report_data_table)
        self.report_view.addTab(self.graph_tab, "Visualization")
        self.report_view.addTab(self.data_tab, "Data")

        layout.addWidget(title)
        layout.addWidget(report_options)
        layout.addWidget(self.report_view)

        self.main_content.addWidget(page)

    def setup_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        tabs = QTabWidget()

        account_tab = QWidget()
        account_layout = QFormLayout(account_tab)
        account_layout.addRow(QLabel("<b>Personal Information</b>"))
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        account_layout.addRow("Full Name:", self.name_edit)
        account_layout.addRow("Email:", self.email_edit)
        account_layout.addRow("Phone:", self.phone_edit)
        account_layout.addRow(QLabel("<b>Security</b>"))
        self.current_pwd_edit = QLineEdit()
        self.current_pwd_edit.setEchoMode(QLineEdit.Password)
        self.new_pwd_edit = QLineEdit()
        self.new_pwd_edit.setEchoMode(QLineEdit.Password)
        self.confirm_pwd_edit = QLineEdit()
        self.confirm_pwd_edit.setEchoMode(QLineEdit.Password)
        account_layout.addRow("Current Password:", self.current_pwd_edit)
        account_layout.addRow("New Password:", self.new_pwd_edit)
        account_layout.addRow("Confirm:", self.confirm_pwd_edit)
        save_btn = QPushButton("Save Changes")
        account_layout.addRow(save_btn)

        pref_tab = QWidget()
        pref_layout = QFormLayout(pref_tab)
        pref_layout.addRow(QLabel("<b>Display</b>"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Blue", "Automatic"])
        self.density_combo = QComboBox()
        self.density_combo.addItems(["Compact", "Normal", "Large"])
        self.language_combo = QComboBox()
        self.language_combo.addItems(["French", "English", "Spanish"])
        pref_layout.addRow("Theme:", self.theme_combo)
        pref_layout.addRow("Density:", self.density_combo)
        pref_layout.addRow("Language:", self.language_combo)
        pref_layout.addRow(QLabel("<b>Notifications</b>"))
        self.email_notif = QCheckBox("Email")
        self.app_notif = QCheckBox("Application")
        self.sms_notif = QCheckBox("SMS")
        pref_layout.addRow(self.email_notif)
        pref_layout.addRow(self.app_notif)
        pref_layout.addRow(self.sms_notif)
        save_pref_btn = QPushButton("Save Preferences")
        pref_layout.addRow(save_pref_btn)

        team_tab = QWidget()
        team_layout = QVBoxLayout(team_tab)
        self.access_table = QTableWidget()
        self.access_table.setColumnCount(4)
        self.access_table.setHorizontalHeaderLabels(["Name", "Role", "Access", "Actions"])
        team_layout.addWidget(self.access_table)

        tabs.addTab(account_tab, "Account")
        tabs.addTab(pref_tab, "Preferences")
        tabs.addTab(team_tab, "Access Management")

        layout.addWidget(title)
        layout.addWidget(tabs)

        self.main_content.addWidget(page)

    def change_page(self, index):
        self.main_content.setCurrentIndex(index)
