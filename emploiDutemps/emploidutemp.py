import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QTextEdit, QDateEdit, QTimeEdit, 
                            QListWidget, QCalendarWidget, QSystemTrayIcon, QMenu, QMessageBox,
                            QStyledItemDelegate, QStyle, QComboBox, QGroupBox, QSplitter, 
                            QTabWidget, QListView, QAbstractItemView, QProgressBar)
from PyQt5.QtCore import Qt, QDateTime, QTimer, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt5 import QtGui
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QListWidgetItem

class TaskDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            gradient = QLinearGradient(option.rect.topLeft(), option.rect.bottomLeft())
            gradient.setColorAt(0, QColor(240, 248, 255))
            gradient.setColorAt(1, QColor(230, 240, 250))
            painter.fillRect(option.rect, QBrush(gradient))
        
        super().paint(painter, option, index)

class TaskWidget(QWidget):
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        self.setMinimumHeight(80)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Header avec titre et boutons
        header = QHBoxLayout()
        
        self.completed_check = QPushButton()
        self.completed_check.setCheckable(True)
        self.completed_check.setChecked(bool(self.task_data[7]))
        self.completed_check.setStyleSheet("""
            QPushButton {
                border: 2px solid #ccc;
                border-radius: 10px;
                background: white;
            }
            QPushButton:checked {
                background: #4CAF50;
                border-color: #45a049;
            }
        """)
        self.completed_check.setFixedSize(20, 20)
        self.completed_check.clicked.connect(self.toggle_completed)
        header.addWidget(self.completed_check)
        
        title = QLabel(self.task_data[1])
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setBold(True)
        title.setFont(title_font)
        
        if self.task_data[7]:  # Si tâche complétée
            title.setStyleSheet("color: #888; text-decoration: line-through;")
        
        header.addWidget(title, 1)
        
        # Boutons d'action
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon.fromTheme("document-edit"))
        edit_btn.setFixedSize(24, 24)
        edit_btn.setToolTip("Modifier")
        edit_btn.clicked.connect(lambda: self.parent.edit_task(self.task_data[0]))
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon.fromTheme("edit-delete"))
        delete_btn.setFixedSize(24, 24)
        delete_btn.setToolTip("Supprimer")
        delete_btn.clicked.connect(lambda: self.parent.delete_task(self.task_data[0]))
        btn_layout.addWidget(delete_btn)
        
        header.addLayout(btn_layout)
        layout.addLayout(header)
        
        # Description
        if self.task_data[2]:
            desc = QLabel(self.task_data[2])
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #555;")
            layout.addWidget(desc)
        
        # Dates et catégorie
        footer = QHBoxLayout()
        
        start = datetime.strptime(self.task_data[3], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(self.task_data[4], '%Y-%m-%d %H:%M:%S')
        
        time_label = QLabel(f"⏱ {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
        time_label.setStyleSheet("color: #666; font-size: 10pt;")
        footer.addWidget(time_label)
        
        if self.task_data[6]:  # Catégorie
            category_label = QLabel(f"📁 {self.task_data[6]}")
            category_label.setStyleSheet(f"color: {self.get_category_color(self.task_data[6])}; font-size: 10pt;")
            footer.addWidget(category_label)
        
        footer.addStretch()
        
        # Indicateur de priorité
        priority_colors = {1: "#ff5252", 2: "#ffab40", 3: "#66bb6a"}
        priority_label = QLabel(["❗ Haute", "🔸 Moyenne", "🔹 Basse"][self.task_data[5]-1])
        priority_label.setStyleSheet(f"color: {priority_colors[self.task_data[5]]}; font-size: 10pt;")
        footer.addWidget(priority_label)
        
        layout.addLayout(footer)
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
            }
        """)
    
    def get_category_color(self, category_name):
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("SELECT color FROM categories_1 WHERE name=?", (category_name,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else "#777"
    
    def toggle_completed(self):
        completed = 1 if self.completed_check.isChecked() else 0
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("UPDATE tasks_1 SET completed=? WHERE id=?", (completed, self.task_data[0]))
        conn.commit()
        conn.close()
        self.parent.load_tasks()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WorkPlanner Pro+")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialisation de la base de données
        self.init_db()
        
        # Configuration de l'interface
        self.setup_ui()
        self.setup_tray_icon()
        self.load_tasks()
        self.setup_notification_timer()
        
        # Style moderne avec thème
        self.apply_styles()
        self.load_settings()
    
    def init_db(self):
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        # Table des tâches (avec suffixe _1)
        c.execute('''CREATE TABLE IF NOT EXISTS tasks_1
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     description TEXT,
                     start_datetime TEXT NOT NULL,
                     end_datetime TEXT NOT NULL,
                     priority INTEGER DEFAULT 2,
                     category TEXT,
                     completed INTEGER DEFAULT 0,
                     reminder_sent INTEGER DEFAULT 0)''')
        
        # Table des paramètres (avec suffixe _1)
        c.execute('''CREATE TABLE IF NOT EXISTS settings_1
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     notify_before INTEGER DEFAULT 15,
                     theme TEXT DEFAULT 'light',
                     default_view TEXT DEFAULT 'day')''')
        
        # Table des catégories (avec suffixe _1)
        c.execute('''CREATE TABLE IF NOT EXISTS categories_1
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     color TEXT NOT NULL)''')
        
        # Insertion des catégories par défaut si nécessaire
        c.execute("SELECT COUNT(*) FROM categories_1")
        if c.fetchone()[0] == 0:
            default_categories = [
                ('Réunion', '#FF5252'),
                ('Travail', '#4CAF50'),
                ('Personnel', '#2196F3'),
                ('Urgent', '#FF9800'),
                ('Projet', '#9C27B0')
            ]
            c.executemany("INSERT INTO categories_1 (name, color) VALUES (?, ?)", default_categories)
        
        conn.commit()
        conn.close()
    
    def setup_ui(self):
        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo et titre
        logo = QLabel("WorkPlanner Pro+")
        logo.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                border-bottom: 1px solid #34495e;
            }
        """)
        logo.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(logo)
        
        # Menu de navigation
        nav_buttons = [
            ("📅 Aujourd'hui", "today"),
            ("📝 Tâches", "tasks"),
            ("📊 Statistiques", "stats"),
            ("⚙ Paramètres", "settings")
        ]
        
        self.nav_btns = []
        for text, action in nav_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    text-align: left;
                    padding: 12px 20px;
                    border: none;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)
            self.nav_btns.append(btn)
        
        sidebar_layout.addStretch()
        
        # Bouton d'ajout rapide
        add_btn = QPushButton("➕ Nouvelle Tâche")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                margin: 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_btn.clicked.connect(self.show_add_task_dialog)
        sidebar_layout.addWidget(add_btn)
        
        # Contenu principal
        self.main_content = QStackedWidget()
        
        # Page "Aujourd'hui"
        self.setup_today_page()
        
        # Page "Tâches"
        self.setup_tasks_page()
        
        # Page "Statistiques"
        self.setup_stats_page()
        
        # Page "Paramètres"
        self.setup_settings_page()
        
        # Ajout des pages au stacked widget
        self.main_content.addWidget(self.today_page)
        self.main_content.addWidget(self.tasks_page)
        self.main_content.addWidget(self.stats_page)
        self.main_content.addWidget(self.settings_page)
        
        # Connecter les boutons de navigation
        for i, btn in enumerate(self.nav_btns):
            btn.clicked.connect(lambda _, x=i: self.main_content.setCurrentIndex(x))
        
        # Ajout des widgets au layout principal
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.main_content)
    
    def setup_today_page(self):
        self.today_page = QWidget()
        layout = QVBoxLayout(self.today_page)
        
        # En-tête
        header = QLabel("Aujourd'hui")
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(header)
        
        # Date actuelle
        today = QLabel(datetime.now().strftime("%A %d %B %Y"))
        today.setStyleSheet("font-size: 16px; color: #7f8c8d; padding: 0 20px;")
        layout.addWidget(today)
        
        # Liste des tâches du jour
        self.today_tasks = QListWidget()
        self.today_tasks.setItemDelegate(TaskDelegate())
        self.today_tasks.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
        """)
        self.today_tasks.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        layout.addWidget(self.today_tasks)
        
        # Charger les tâches du jour
        self.load_today_tasks()
    
    def load_today_tasks(self):
        self.today_tasks.clear()
        
        today = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, title, description, start_datetime, end_datetime, 
                     priority, category, completed FROM tasks_1 
                     WHERE date(start_datetime) = ? 
                     ORDER BY datetime(start_datetime)''', (today,))
        
        tasks = c.fetchall()
        
        for task in tasks:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, task[0])
            
            task_widget = TaskWidget(task, self)
            item.setSizeHint(task_widget.sizeHint())
            
            self.today_tasks.addItem(item)
            self.today_tasks.setItemWidget(item, task_widget)
        
        conn.close()
        
        # Afficher un message si aucune tâche
        if not tasks:
            empty_label = QLabel("Aucune tâche prévue pour aujourd'hui")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #95a5a6; font-size: 14px;")
            item = QListWidgetItem()
            item.setSizeHint(empty_label.sizeHint())
            self.today_tasks.addItem(item)
            self.today_tasks.setItemWidget(item, empty_label)
    
    def setup_tasks_page(self):
        self.tasks_page = QWidget()
        layout = QVBoxLayout(self.tasks_page)
        
        # En-tête avec filtre
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Toutes les tâches")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Filtres
        filter_layout = QHBoxLayout()
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes les catégories", None)
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("SELECT name FROM categories_1 ORDER BY name")
        for cat in c.fetchall():
            self.category_filter.addItem(cat[0], cat[0])
        conn.close()
        self.category_filter.currentIndexChanged.connect(self.load_all_tasks)
        filter_layout.addWidget(self.category_filter)
        
        self.status_filter = QComboBox()
        self.status_filter.addItem("Toutes", -1)
        self.status_filter.addItem("À faire", 0)
        self.status_filter.addItem("Terminées", 1)
        self.status_filter.currentIndexChanged.connect(self.load_all_tasks)
        filter_layout.addWidget(self.status_filter)
        
        header_layout.addLayout(filter_layout)
        layout.addWidget(header)
        
        # Liste des tâches
        self.all_tasks_list = QListWidget()
        self.all_tasks_list.setItemDelegate(TaskDelegate())
        self.all_tasks_list.setStyleSheet("QListWidget { border: none; }")
        self.all_tasks_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        layout.addWidget(self.all_tasks_list)
        
        # Charger toutes les tâches
        self.load_all_tasks()
    
    def load_all_tasks(self):
        self.all_tasks_list.clear()
        
        category = self.category_filter.currentData()
        status = self.status_filter.currentData()
        
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        query = '''SELECT id, title, description, start_datetime, end_datetime, 
                   priority, category, completed FROM tasks_1'''
        
        conditions = []
        params = []
        
        if category is not None:
            conditions.append("category=?")
            params.append(category)
        
        if status != -1:
            conditions.append("completed=?")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY datetime(start_datetime) DESC"
        
        c.execute(query, tuple(params))
        tasks = c.fetchall()
        
        for task in tasks:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, task[0])
            
            task_widget = TaskWidget(task, self)
            item.setSizeHint(task_widget.sizeHint())
            
            self.all_tasks_list.addItem(item)
            self.all_tasks_list.setItemWidget(item, task_widget)
        
        conn.close()
        
        # Afficher un message si aucune tâche
        if not tasks:
            empty_label = QLabel("Aucune tâche correspondant aux filtres")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #95a5a6; font-size: 14px;")
            item = QListWidgetItem()
            item.setSizeHint(empty_label.sizeHint())
            self.all_tasks_list.addItem(item)
            self.all_tasks_list.setItemWidget(item, empty_label)
    
    def setup_stats_page(self):
        self.stats_page = QWidget()
        layout = QVBoxLayout(self.stats_page)
        
        # En-tête
        header = QLabel("Statistiques")
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(header)
        
        # Statistiques principales
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        # Statistique 1 - Tâches complétées
        stat1 = QWidget()
        stat1_layout = QVBoxLayout(stat1)
        
        stat1_title = QLabel("Tâches complétées")
        stat1_title.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        stat1_layout.addWidget(stat1_title)
        
        self.completed_count = QLabel("0")
        self.completed_count.setStyleSheet("font-size: 36px; font-weight: bold; color: #2ecc71;")
        stat1_layout.addWidget(self.completed_count)
        
        stats_layout.addWidget(stat1)
        
        # Statistique 2 - Tâches en retard
        stat2 = QWidget()
        stat2_layout = QVBoxLayout(stat2)
        
        stat2_title = QLabel("Tâches en retard")
        stat2_title.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        stat2_layout.addWidget(stat2_title)
        
        self.overdue_count = QLabel("0")
        self.overdue_count.setStyleSheet("font-size: 36px; font-weight: bold; color: #e74c3c;")
        stat2_layout.addWidget(self.overdue_count)
        
        stats_layout.addWidget(stat2)
        
        # Statistique 3 - Productivité
        stat3 = QWidget()
        stat3_layout = QVBoxLayout(stat3)
        
        stat3_title = QLabel("Taux de complétion")
        stat3_title.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        stat3_layout.addWidget(stat3_title)
        
        self.completion_rate = QProgressBar()
        self.completion_rate.setRange(0, 100)
        self.completion_rate.setStyleSheet("""
            QProgressBar {
                height: 30px;
                text-align: center;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        stat3_layout.addWidget(self.completion_rate)
        
        stats_layout.addWidget(stat3)
        
        layout.addWidget(stats_widget)
        
        # Charger les statistiques
        self.load_stats()
    
    def load_stats(self):
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        # Tâches complétées
        c.execute("SELECT COUNT(*) FROM tasks_1 WHERE completed=1")
        completed = c.fetchone()[0]
        self.completed_count.setText(str(completed))
        
        # Tâches en retard
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("SELECT COUNT(*) FROM tasks_1 WHERE completed=0 AND datetime(end_datetime) < datetime(?)", (now,))
        overdue = c.fetchone()[0]
        self.overdue_count.setText(str(overdue))
        
        # Taux de complétion
        c.execute("SELECT COUNT(*) FROM tasks_1")
        total = c.fetchone()[0]
        if total > 0:
            rate = int((completed / total) * 100)
        else:
            rate = 0
        self.completion_rate.setValue(rate)
        self.completion_rate.setFormat(f"{rate}%")
        
        conn.close()
    
    def setup_settings_page(self):
        self.settings_page = QWidget()
        layout = QVBoxLayout(self.settings_page)
        
        # En-tête
        header = QLabel("Paramètres")
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                color: #2c3e50;
            }
        """)
        layout.addWidget(header)
        
        # Groupe notifications
        notif_group = QGroupBox("Notifications")
        notif_layout = QVBoxLayout(notif_group)
        
        notif_label = QLabel("Prévenir avant une tâche (minutes):")
        notif_layout.addWidget(notif_label)
        
        self.notify_before = QComboBox()
        self.notify_before.addItems(["5", "10", "15", "30", "60"])
        notif_layout.addWidget(self.notify_before)
        
        layout.addWidget(notif_group)
        
        # Groupe apparence
        appearance_group = QGroupBox("Apparence")
        appearance_layout = QVBoxLayout(appearance_group)
        
        theme_label = QLabel("Thème:")
        appearance_layout.addWidget(theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Clair", "Sombre"])
        appearance_layout.addWidget(self.theme_selector)
        
        layout.addWidget(appearance_group)
        
        # Bouton de sauvegarde
        save_btn = QPushButton("Enregistrer les paramètres")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def load_settings(self):
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        c.execute("SELECT notify_before, theme FROM settings_1 LIMIT 1")
        settings = c.fetchone()
        
        if settings:
            notify_before, theme = settings
            index = self.notify_before.findText(str(notify_before))
            if index >= 0:
                self.notify_before.setCurrentIndex(index)
            
            index = self.theme_selector.findText("Sombre" if theme == "dark" else "Clair")
            if index >= 0:
                self.theme_selector.setCurrentIndex(index)
        
        conn.close()
    
    def save_settings(self):
        notify_before = int(self.notify_before.currentText())
        theme = "dark" if self.theme_selector.currentText() == "Sombre" else "light"
        
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        # Vérifier s'il existe déjà des paramètres
        c.execute("SELECT COUNT(*) FROM settings_1")
        if c.fetchone()[0] > 0:
            c.execute("UPDATE settings_1 SET notify_before=?, theme=?", (notify_before, theme))
        else:
            c.execute("INSERT INTO settings_1 (notify_before, theme) VALUES (?, ?)", (notify_before, theme))
        
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Paramètres", "Les paramètres ont été enregistrés avec succès.")
        self.apply_styles()
    
    def apply_styles(self):
        # Déterminer le thème
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("SELECT theme FROM settings_1 LIMIT 1")
        result = c.fetchone()
        theme = result[0] if result else "light"
        conn.close()
        
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #34495e;
                }
                QWidget {
                    color: #ecf0f1;
                }
                QGroupBox {
                    border: 1px solid #2c3e50;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f7fa;
                }
                QWidget {
                    color: #2c3e50;
                }
                QGroupBox {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 15px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                }
            """)
    
    def setup_tray_icon(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("Ouvrir WorkPlanner")
        show_action.triggered.connect(self.showNormal)
        
        add_task_action = tray_menu.addAction("Ajouter une tâche")
        add_task_action.triggered.connect(self.show_add_task_dialog)
        
        tray_menu.addSeparator()
        
        exit_action = tray_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
    
    def setup_notification_timer(self):
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_upcoming_tasks)
        self.notification_timer.start(60000)  # Vérifie toutes les minutes
    
    def check_upcoming_tasks(self):
        now = datetime.now()
        notify_before = 15  # Valeur par défaut
        
        # Récupérer le délai de notification depuis les paramètres
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("SELECT notify_before FROM settings_1 LIMIT 1")
        result = c.fetchone()
        if result:
            notify_before = result[0]
        
        # Récupérer les tâches à venir
        c.execute('''SELECT id, title, start_datetime FROM tasks_1 
                     WHERE completed = 0 AND reminder_sent = 0 
                     AND datetime(start_datetime) > datetime(?)
                     AND datetime(start_datetime) <= datetime(?, ?) 
                     ORDER BY datetime(start_datetime)''', 
                     (now.strftime('%Y-%m-%d %H:%M:%S'), 
                      now.strftime('%Y-%m-%d %H:%M:%S'), 
                      f"+{notify_before} minutes"))
        
        tasks = c.fetchall()
        
        for task in tasks:
            task_time = datetime.strptime(task[2], '%Y-%m-%d %H:%M:%S')
            self.show_notification(f"Tâche à venir: {task[1]}", 
                                 f"Commence à {task_time.strftime('%H:%M')}")
            
            # Marquer comme notifié
            c.execute("UPDATE tasks_1 SET reminder_sent=1 WHERE id=?", (task[0],))
        
        conn.commit()
        conn.close()
    
    def show_notification(self, title, message):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 10000)
    
    def show_add_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter une tâche")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Titre
        title_label = QLabel("Titre:")
        self.task_title = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(self.task_title)
        
        # Description
        desc_label = QLabel("Description:")
        self.task_desc = QTextEdit()
        self.task_desc.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(self.task_desc)
        
        # Dates
        date_layout = QHBoxLayout()
        
        start_layout = QVBoxLayout()
        start_label = QLabel("Début:")
        self.task_start = QDateTimeEdit()
        self.task_start.setDateTime(QDateTime.currentDateTime())
        self.task_start.setCalendarPopup(True)
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.task_start)
        date_layout.addLayout(start_layout)
        
        end_layout = QVBoxLayout()
        end_label = QLabel("Fin:")
        self.task_end = QDateTimeEdit()
        self.task_end.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.task_end.setCalendarPopup(True)
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.task_end)
        date_layout.addLayout(end_layout)
        
        layout.addLayout(date_layout)
        
        # Catégorie
        cat_label = QLabel("Catégorie:")
        self.task_category = QComboBox()
        self.task_category.addItem("Aucune", None)
        
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        c.execute("SELECT name FROM categories_1 ORDER BY name")
        for cat in c.fetchall():
            self.task_category.addItem(cat[0], cat[0])
        conn.close()
        
        layout.addWidget(cat_label)
        layout.addWidget(self.task_category)
        
        # Priorité
        prio_label = QLabel("Priorité:")
        self.task_priority = QComboBox()
        self.task_priority.addItem("Haute", 1)
        self.task_priority.addItem("Moyenne", 2)
        self.task_priority.addItem("Basse", 3)
        self.task_priority.setCurrentIndex(1)
        layout.addWidget(prio_label)
        layout.addWidget(self.task_priority)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setDefault(True)
        save_btn.clicked.connect(lambda: self.save_task_and_close(dialog))
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec_()
    
    def save_task_and_close(self, dialog):
        title = self.task_title.text()
        description = self.task_desc.toPlainText()
        start = self.task_start.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end = self.task_end.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        category = self.task_category.currentData()
        priority = self.task_priority.currentData()
        
        if not title:
            QMessageBox.warning(self, "Erreur", "Le titre de la tâche est requis")
            return
        
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        c.execute('''INSERT INTO tasks_1 
                     (title, description, start_datetime, end_datetime, priority, category)
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                     (title, description, start, end, priority, category))
        
        conn.commit()
        conn.close()
        
        self.load_today_tasks()
        self.load_all_tasks()
        self.load_stats()
        
        dialog.accept()
    
    def edit_task(self, task_id):
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        c.execute('''SELECT id, title, description, start_datetime, end_datetime, 
                     priority, category, completed FROM tasks_1 WHERE id=?''', (task_id,))
        task = c.fetchone()
        
        if not task:
            conn.close()
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier la tâche")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Titre
        title_label = QLabel("Titre:")
        self.edit_title = QLineEdit(task[1])
        layout.addWidget(title_label)
        layout.addWidget(self.edit_title)
        
        # Description
        desc_label = QLabel("Description:")
        self.edit_desc = QTextEdit(task[2])
        self.edit_desc.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(self.edit_desc)
        
        # Dates
        date_layout = QHBoxLayout()
        
        start_layout = QVBoxLayout()
        start_label = QLabel("Début:")
        self.edit_start = QDateTimeEdit()
        self.edit_start.setDateTime(QDateTime.fromString(task[3], 'yyyy-MM-dd HH:mm:ss'))
        self.edit_start.setCalendarPopup(True)
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.edit_start)
        date_layout.addLayout(start_layout)
        
        end_layout = QVBoxLayout()
        end_label = QLabel("Fin:")
        self.edit_end = QDateTimeEdit()
        self.edit_end.setDateTime(QDateTime.fromString(task[4], 'yyyy-MM-dd HH:mm:ss'))
        self.edit_end.setCalendarPopup(True)
        end_layout.addWidget(end_label)
        end_layout.addWidget(self.edit_end)
        date_layout.addLayout(end_layout)
        
        layout.addLayout(date_layout)
        
        # Catégorie
        cat_label = QLabel("Catégorie:")
        self.edit_category = QComboBox()
        self.edit_category.addItem("Aucune", None)
        
        c.execute("SELECT name FROM categories_1 ORDER BY name")
        for cat in c.fetchall():
            self.edit_category.addItem(cat[0], cat[0])
            if task[6] and cat[0] == task[6]:
                self.edit_category.setCurrentIndex(self.edit_category.count() - 1)
        
        layout.addWidget(cat_label)
        layout.addWidget(self.edit_category)
        
        # Priorité
        prio_label = QLabel("Priorité:")
        self.edit_priority = QComboBox()
        self.edit_priority.addItem("Haute", 1)
        self.edit_priority.addItem("Moyenne", 2)
        self.edit_priority.addItem("Basse", 3)
        self.edit_priority.setCurrentIndex(task[5] - 1)
        layout.addWidget(prio_label)
        layout.addWidget(self.edit_priority)
        
        # Statut
        status_layout = QHBoxLayout()
        self.edit_completed = QCheckBox("Tâche complétée")
        self.edit_completed.setChecked(bool(task[7]))
        status_layout.addWidget(self.edit_completed)
        layout.addLayout(status_layout)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Supprimer")
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_btn.clicked.connect(lambda: self.confirm_delete_task(dialog, task_id))
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.setDefault(True)
        save_btn.clicked.connect(lambda: self.update_task_and_close(dialog, task_id))
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        conn.close()
        dialog.exec_()
    
    def update_task_and_close(self, dialog, task_id):
        title = self.edit_title.text()
        description = self.edit_desc.toPlainText()
        start = self.edit_start.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end = self.edit_end.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        category = self.edit_category.currentData()
        priority = self.edit_priority.currentData()
        completed = 1 if self.edit_completed.isChecked() else 0
        
        if not title:
            QMessageBox.warning(self, "Erreur", "Le titre de la tâche est requis")
            return
        
        conn = sqlite3.connect('workplanner.db')
        c = conn.cursor()
        
        c.execute('''UPDATE tasks_1 SET 
                     title=?, description=?, start_datetime=?, end_datetime=?,
                     priority=?, category=?, completed=?, reminder_sent=0
                     WHERE id=?''', 
                     (title, description, start, end, priority, category, completed, task_id))
        
        conn.commit()
        conn.close()
        
        self.load_today_tasks()
        self.load_all_tasks()
        self.load_stats()
        
        dialog.accept()
    
    def confirm_delete_task(self, dialog, task_id):
        reply = QMessageBox.question(
            self, 'Confirmation',
            'Êtes-vous sûr de vouloir supprimer cette tâche ?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect('workplanner.db')
            c = conn.cursor()
            c.execute("DELETE FROM tasks_1 WHERE id=?", (task_id,))
            conn.commit()
            conn.close()
            
            self.load_today_tasks()
            self.load_all_tasks()
            self.load_stats()
            
            dialog.accept()
    
    def delete_task(self, task_id):
        self.confirm_delete_task(None, task_id)
    
    def closeEvent(self, event):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Définir une police moderne
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())