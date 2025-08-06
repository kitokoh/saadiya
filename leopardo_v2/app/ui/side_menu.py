import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QMenu)
from PyQt5.QtCore import Qt
from .user_profile import UserProfile

class SideMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QFrame {
                background-color: #1A1A2E;
                border-right: 1px solid #2E2E3E;
            }
        """)

        # Title
        title = QLabel("Leopardo AI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #7AA2F7; padding: 10px;")
        self.main_layout.addWidget(title)

        # Home Button
        self.home_button = QPushButton("🏠 Home")
        self.home_button.setFixedHeight(40)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #D0D0FF;
                border: none;
                font-size: 14px;
                text-align: left;
                padding-left: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2A2A4A;
                color: #FFFFFF;
            }
        """)
        self.main_layout.addWidget(self.home_button)

        # Tools Menu
        self.tools_button = QPushButton("🧰 Tools")
        self.tools_button.setFixedHeight(40)
        self.tools_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.tools_button)
        self.tools_menu = QMenu()
        self.tools_menu.addAction("Interconnexion")
        self.tools_menu.addAction("Add-On")
        self.tools_menu.addAction("Remote Control")
        self.tools_menu.addAction("Manuelle")
        self.tools_menu.addAction("Scheduler")
        self.tools_menu.addAction("Edit PDF")
        self.tools_menu.addAction("Watermarks")
        self.tools_menu.addAction("Remove BG")
        self.tools_menu.addAction("Links")
        self.tools_menu.addAction("Contacts")
        self.tools_menu.addAction("Groups")
        self.tools_menu.addAction("Media")
        self.tools_button.setMenu(self.tools_menu)

        # Beta Feature Menu
        self.beta_button = QPushButton("✨ Beta Feature")
        self.beta_button.setFixedHeight(40)
        self.beta_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.beta_button)
        self.beta_menu = QMenu()
        self.beta_menu.addAction("IA BETA")
        self.beta_menu.addAction("Licences")
        self.beta_button.setMenu(self.beta_menu)

        # Data Menu
        self.data_button = QPushButton("💡 Data")
        self.data_button.setFixedHeight(40)
        self.data_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.data_button)
        self.data_menu = QMenu()
        self.data_menu.addAction("Prompts")
        self.data_menu.addAction("Stats")
        self.data_menu.addAction("Strategies")
        self.data_menu.addAction("Import Data")
        self.data_menu.addAction("ADN Backup")
        self.data_button.setMenu(self.data_menu)

        # Support Menu
        self.support_button = QPushButton("🆘 Support")
        self.support_button.setFixedHeight(40)
        self.support_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.support_button)
        self.support_menu = QMenu()
        self.support_menu.addAction("About")
        self.support_menu.addAction("Documents")
        self.support_menu.addAction("Contact")
        self.support_button.setMenu(self.support_menu)

        # Upgrade Button
        self.upgrade_button = QPushButton("💎 Upgrade")
        self.upgrade_button.setFixedHeight(40)
        self.upgrade_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.upgrade_button)

        # Settings Menu
        self.settings_button = QPushButton("⚙️ Settings")
        self.settings_button.setFixedHeight(40)
        self.settings_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.settings_button)
        self.settings_menu = QMenu()
        self.settings_menu.addAction("Vision")
        self.settings_menu.addAction("Com Interne")
        self.settings_menu.addAction("Com Externe")
        self.settings_menu.addAction("Instances")
        self.settings_menu.addAction("Installer")
        self.settings_menu.addAction("Add-On")
        self.connection_menu = QMenu()
        self.connection_menu.addAction("SSH Connect")
        self.connection_menu.addAction("FTP Server")
        self.connection_menu.addAction("API Link")
        self.connection_menu.addAction("Remote Desktop")
        self.connection_menu.addAction("VPN Connect")
        self.connection_menu.addAction("AI Service")
        self.settings_menu.addMenu(self.connection_menu)

        self.archive_menu = QMenu("Archive")
        self.archive_menu.addAction("Local ZIP Archive")
        self.archive_menu.addAction("Google Drive")
        self.archive_menu.addAction("Dropbox")
        self.archive_menu.addAction("FTP Server")
        self.archive_menu.addAction("SFTP Secure")
        self.archive_menu.addAction("External Disk")
        self.archive_menu.addAction("Schedule Backup")
        self.settings_menu.addMenu(self.archive_menu)

        self.settings_button.setMenu(self.settings_menu)

        # Language Menu
        self.language_menu_button = QPushButton("🌍 Language")
        self.language_menu_button.setFixedHeight(40)
        self.language_menu_button.setStyleSheet(self.home_button.styleSheet())

        self.language_menu = QMenu()
        self.language_menu.addAction("English")
        self.language_menu.addAction("Français")
        self.language_menu.addAction("Türkçe")
        self.language_menu.addAction("العربية")
        self.language_menu.addAction("Português")
        self.language_menu_button.setMenu(self.language_menu)
        self.main_layout.addWidget(self.language_menu_button)

        self.main_layout.addStretch()

        # Menu Config Button
        self.menu_config_button = QPushButton("⚙️ MENU")
        self.menu_config_button.setFixedHeight(48)
        self.menu_config_button.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                padding-left: 10px;
                border: none;
                margin: 10px 5px;
            }
        """)
        self.main_layout.addWidget(self.menu_config_button)

        # User Profile
        self.user_profile = UserProfile()
        self.main_layout.addWidget(self.user_profile)
