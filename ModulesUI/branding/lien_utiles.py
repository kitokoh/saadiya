import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel,
    QHBoxLayout, QMessageBox, QTimeEdit, QListWidget, QListWidgetItem, QInputDialog,
    QAction, QMenuBar, QFileDialog, QStyleFactory
)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView


# Style CSS pour l'interface
STYLE_SHEET = """
    QMainWindow {
        background-color: #2E3440;
    }
    QPushButton {
        background-color: #4C566A;
        color: #ECEFF4;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #5E81AC;
    }
    QLineEdit {
        background-color: #3B4252;
        color: #ECEFF4;
        border-radius: 5px;
        padding: 5px;
        font-size: 14px;
    }
    QListWidget {
        background-color: #3B4252;
        color: #ECEFF4;
        border-radius: 5px;
        padding: 5px;
        font-size: 14px;
    }
    QLabel {
        color: #ECEFF4;
        font-size: 16px;
    }
    QMenuBar {
        background-color: #4C566A;
        color: #ECEFF4;
    }
    QMenuBar::item {
        background-color: transparent;
    }
    QMenuBar::item:selected {
        background-color: #5E81AC;
    }
"""


class SiteButton(QPushButton):
    """Bouton personnalisé pour ouvrir un site."""
    def __init__(self, name, url, icon=None, parent=None):
        super().__init__(name, parent)
        self.url = url
        self.setIcon(QIcon(icon) if icon else QIcon())
        self.setStyleSheet("text-align: left; padding-left: 10px;")
        self.clicked.connect(self.open_site)

    def open_site(self):
        """Ouvre le site dans un nouvel onglet du navigateur."""
        self.browser = QWebEngineView()
        self.browser.setWindowTitle(self.text())
        self.browser.load(self.url)
        self.browser.show()


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Site Connector Pro")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet(STYLE_SHEET)

        # Initialisation de la base de données
        self.init_db()

        # Barre de menu
        self.create_menu_bar()

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Liste des sites
        self.site_list = QListWidget()
        self.site_list.itemDoubleClicked.connect(self.open_selected_site)
        self.layout.addWidget(self.site_list)

        # Formulaire pour ajouter un site
        self.add_site_layout = QHBoxLayout()
        self.site_name_input = QLineEdit(self)
        self.site_name_input.setPlaceholderText("Nom du site")
        self.site_url_input = QLineEdit(self)
        self.site_url_input.setPlaceholderText("URL du site")
        self.add_site_button = QPushButton("Ajouter", self)
        self.add_site_button.clicked.connect(self.add_site)
        self.add_site_layout.addWidget(self.site_name_input)
        self.add_site_layout.addWidget(self.site_url_input)
        self.add_site_layout.addWidget(self.add_site_button)
        self.layout.addLayout(self.add_site_layout)

        # Timer pour les tâches planifiées
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_scheduled_tasks)
        self.timer.start(60000)  # Vérifie toutes les minutes

        # Charger les sites au démarrage
        self.load_sites()

    def init_db(self):
        """Initialise la base de données SQLite."""
        self.db_path = os.path.join(os.getenv('APPDATA'), 'SiteConnectorPro', 'sites.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sites
                             (id INTEGER PRIMARY KEY, name TEXT, url TEXT, icon TEXT, schedule_time TEXT)''')
        self.conn.commit()

    def create_menu_bar(self):
        """Crée la barre de menu."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Fichier")
        export_action = QAction("Exporter les sites", self)
        export_action.triggered.connect(self.export_sites)
        file_menu.addAction(export_action)
        import_action = QAction("Importer les sites", self)
        import_action.triggered.connect(self.import_sites)
        file_menu.addAction(import_action)

    def load_sites(self):
        """Charge les sites depuis la base de données."""
        self.site_list.clear()
        self.cursor.execute("SELECT name, url, icon FROM sites")
        sites = self.cursor.fetchall()
        for name, url, icon in sites:
            item = QListWidgetItem(name)
            item.setIcon(QIcon(icon) if icon else QIcon())
            item.setData(Qt.UserRole, url)
            self.site_list.addItem(item)

    def add_site(self):
        """Ajoute un nouveau site."""
        name = self.site_name_input.text()
        url = self.site_url_input.text()
        if name and url:
            icon, _ = QInputDialog.getText(self, "Icône", "Entrez le chemin de l'icône (facultatif):")
            self.cursor.execute("INSERT INTO sites (name, url, icon) VALUES (?, ?, ?)", (name, url, icon))
            self.conn.commit()
            self.load_sites()
            self.site_name_input.clear()
            self.site_url_input.clear()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def open_selected_site(self, item):
        """Ouvre le site sélectionné."""
        url = item.data(Qt.UserRole)
        browser = QWebEngineView()
        browser.setWindowTitle(item.text())
        browser.load(url)
        browser.show()

    def export_sites(self):
        """Exporte les sites vers un fichier."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Exporter les sites", "", "Fichiers SQLite (*.db)")
        if file_path:
            with open(file_path, 'wb') as f:
                with open(self.db_path, 'rb') as db_file:
                    f.write(db_file.read())

    def import_sites(self):
        """Importe les sites depuis un fichier."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Importer les sites", "", "Fichiers SQLite (*.db)")
        if file_path:
            with open(file_path, 'rb') as f:
                with open(self.db_path, 'wb') as db_file:
                    db_file.write(f.read())
            self.load_sites()

    def check_scheduled_tasks(self):
        """Vérifie les tâches planifiées."""
        self.cursor.execute("SELECT name, url, schedule_time FROM sites WHERE schedule_time IS NOT NULL")
        sites = self.cursor.fetchall()
        for name, url, schedule_time in sites:
            current_time = QTime.currentTime()
            scheduled_time = QTime.fromString(schedule_time, "HH:mm")
            if current_time <= scheduled_time:
                delay = current_time.secsTo(scheduled_time) * 1000
                QTimer.singleShot(delay, lambda u=url: self.open_scheduled_site(u))

    def open_scheduled_site(self, url):
        """Ouvre un site planifié."""
        browser = QWebEngineView()
        browser.load(url)
        browser.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # Style moderne
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())