import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QMenu)
from PyQt5.QtCore import Qt

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

        # Beta Feature Menu
        self.beta_button = QPushButton("✨ Beta Feature")
        self.beta_button.setFixedHeight(40)
        self.beta_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.beta_button)

        # Data Menu
        self.data_button = QPushButton("💡 Data")
        self.data_button.setFixedHeight(40)
        self.data_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.data_button)

        # Support Menu
        self.support_button = QPushButton("🆘 Support")
        self.support_button.setFixedHeight(40)
        self.support_button.setStyleSheet(self.home_button.styleSheet())
        self.main_layout.addWidget(self.support_button)

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
