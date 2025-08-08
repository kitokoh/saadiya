"""
Side menu of the Leopardo V2 application.
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QMenu)
from PyQt5.QtCore import Qt
from .user_profile import UserProfile

class SideMenu(QFrame):
    """
    The side menu of the application.
    """
    def __init__(self, parent=None):
        """
        Initializes the side menu.
        """
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

        # Marketing Menu
        self.marketing_button = QPushButton("📈 Marketing")
        self.marketing_button.setFixedHeight(40)
        self.marketing_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.marketing_button)
        self.marketing_menu = QMenu()
        self.marketing_menu.addAction("My Media")
        self.marketing_menu.addAction("My Groups")
        self.marketing_menu.addAction("Marketing Robots")
        self.marketing_menu.addAction("Ads Manager")
        self.marketing_menu.addAction("Campaign Scheduler")
        self.marketing_menu.addAction("Email & SMS")
        self.marketing_menu.addAction("Content Generator")
        self.marketing_button.setMenu(self.marketing_menu)

        # Sales Menu
        self.sales_button = QPushButton("💰 Sales")
        self.sales_button.setFixedHeight(40)
        self.sales_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.sales_button)
        self.sales_menu = QMenu()
        self.sales_menu.addAction("Project Management")
        self.sales_menu.addAction("SAV")
        self.sales_menu.addAction("Short Links & Trackers")
        self.sales_menu.addAction("Prospection & Relances")
        self.sales_menu.addAction("DMS & Quotes")
        self.sales_menu.addAction("CRM")
        self.sales_menu.addAction("Sales Prompts / Templates")
        self.sales_button.setMenu(self.sales_menu)

        # Run Button
        self.run_button = QPushButton("▶️ Run")
        self.run_button.setFixedHeight(40)
        self.run_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.run_button)

        # Telecommande Button
        self.telecommande_button = QPushButton("📡 Telecommande")
        self.telecommande_button.setFixedHeight(40)
        self.telecommande_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.telecommande_button)

        # Instances Button
        self.instances_button = QPushButton("🖥️ Instances")
        self.instances_button.setFixedHeight(40)
        self.instances_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.instances_button)

        # Statistics Button
        self.statistics_button = QPushButton("📊 Statistics")
        self.statistics_button.setFixedHeight(40)
        self.statistics_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.statistics_button)

        # Facebook Button
        self.facebook_button = QPushButton("👍 Facebook")
        self.facebook_button.setFixedHeight(40)
        self.facebook_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.facebook_button)

        # AI Agent Menu
        self.ai_agent_button = QPushButton("🤖 AI Agent")
        self.ai_agent_button.setFixedHeight(40)
        self.ai_agent_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.ai_agent_button)
        self.ai_agent_menu = QMenu()
        self.ai_agent_menu.addAction("Auto-Responder")
        self.ai_agent_menu.addAction("Sales Assistant")
        self.ai_agent_menu.addAction("Prompts & Tools")
        self.ai_agent_menu.addAction("Competitor Analysis")
        self.ai_agent_menu.addAction("Assistant ventes")
        self.ai_agent_menu.addAction("AI Workflows")
        self.ai_agent_button.setMenu(self.ai_agent_menu)

        # Finance Menu
        self.finance_button = QPushButton("💵 Finance")
        self.finance_button.setFixedHeight(40)
        self.finance_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.finance_button)
        self.finance_menu = QMenu()
        self.finance_menu.addAction("Invoices & Billing")
        self.finance_menu.addAction("Trader")
        self.finance_button.setMenu(self.finance_menu)

        # Upgrade Button
        self.upgrade_button = QPushButton("💎 Upgrade")
        self.upgrade_button.setFixedHeight(40)
        self.upgrade_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.upgrade_button)

        # Anciens Menu
        self.anciens_button = QPushButton("📜 Anciens")
        self.anciens_button.setFixedHeight(40)
        self.anciens_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.anciens_button)
        self.anciens_menu = QMenu()
        self.tools_menu = self.anciens_menu.addMenu("🧰 Tools")
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
        self.beta_menu = self.anciens_menu.addMenu("✨ Beta Feature")
        self.beta_menu.addAction("IA BETA")
        self.beta_menu.addAction("Licences")
        self.data_menu = self.anciens_menu.addMenu("💡 Data")
        self.data_menu.addAction("Prompts")
        self.data_menu.addAction("Stats")
        self.data_menu.addAction("Strategies")
        self.data_menu.addAction("Import Data")
        self.data_menu.addAction("ADN Backup")
        self.support_menu = self.anciens_menu.addMenu("🆘 Support")
        self.support_menu.addAction("About")
        self.support_menu.addAction("Documents")
        self.support_menu.addAction("Contact")
        self.settings_menu = self.anciens_menu.addMenu("⚙️ Settings")
        self.settings_menu.addAction("Vision")
        self.settings_menu.addAction("Com Interne")
        self.settings_menu.addAction("Com Externe")
        self.settings_menu.addAction("Instances")
        self.settings_menu.addAction("Installer")
        self.settings_menu.addAction("Add-On")
        self.connection_menu = self.settings_menu.addMenu("Connection")
        self.connection_menu.addAction("SSH Connect")
        self.connection_menu.addAction("FTP Server")
        self.connection_menu.addAction("API Link")
        self.connection_menu.addAction("Remote Desktop")
        self.connection_menu.addAction("VPN Connect")
        self.connection_menu.addAction("AI Service")
        self.archive_menu = self.settings_menu.addMenu("Archive")
        self.archive_menu.addAction("Local ZIP Archive")
        self.archive_menu.addAction("Google Drive")
        self.archive_menu.addAction("Dropbox")
        self.archive_menu.addAction("FTP Server")
        self.archive_menu.addAction("SFTP Secure")
        self.archive_menu.addAction("External Disk")
        self.archive_menu.addAction("Schedule Backup")
        self.anciens_button.setMenu(self.anciens_menu)

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
