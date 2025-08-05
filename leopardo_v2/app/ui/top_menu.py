import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QPushButton, QLabel, QFrame, QMenu)
from PyQt5.QtCore import Qt

class TopMenu(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # App Title
        self.app_title = QLabel("Leopardo AI")
        self.app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2563eb; padding: 0 15px;")
        self.main_layout.addWidget(self.app_title)

        # Menu Bar
        self.menu_bar = QHBoxLayout()
        self.menu_bar.setSpacing(5)

        # File Menu
        self.file_menu_button = QPushButton("File")
        self.file_menu = QMenu()
        self.file_menu.addAction("New Tab")
        self.file_menu.addAction("Exit")
        self.file_menu_button.setMenu(self.file_menu)
        self.menu_bar.addWidget(self.file_menu_button)

        # Tools Menu
        self.tools_menu_button = QPushButton("Tools")
        self.tools_menu = QMenu()
        self.tools_menu.addAction("Edit PDF")
        self.tools_menu.addAction("Watermarks")
        self.tools_menu.addAction("Links")
        self.tools_menu.addAction("Scheduler")
        self.tools_menu_button.setMenu(self.tools_menu)
        self.menu_bar.addWidget(self.tools_menu_button)

        # Settings Menu
        self.settings_menu_button = QPushButton("Settings")
        self.settings_menu = QMenu()
        self.settings_menu.addAction("Instances")
        self.settings_menu.addAction("Language")
        self.settings_menu_button.setMenu(self.settings_menu)
        self.menu_bar.addWidget(self.settings_menu_button)

        # Data Menu
        self.data_menu_button = QPushButton("Data")
        self.data_menu = QMenu()
        self.data_menu.addAction("Prompts")
        self.data_menu.addAction("Stats")
        self.data_menu.addAction("Strategies")
        self.data_menu.addAction("Import Data")
        self.data_menu.addAction("ADN Backup")
        self.data_menu_button.setMenu(self.data_menu)
        self.menu_bar.addWidget(self.data_menu_button)

        # Support Menu
        self.support_menu_button = QPushButton("Support")
        self.support_menu = QMenu()
        self.support_menu.addAction("About")
        self.support_menu.addAction("Documents")
        self.support_menu.addAction("Contact")
        self.support_menu_button.setMenu(self.support_menu)
        self.menu_bar.addWidget(self.support_menu_button)

        # Upgrade Button
        self.upgrade_button = QPushButton("Upgrade")
        self.menu_bar.addWidget(self.upgrade_button)

        self.main_layout.addLayout(self.menu_bar)

        self.main_layout.addStretch()

        # Window Controls
        self.controls_layout = QHBoxLayout()
        self.controls_layout.setSpacing(5)

        self.minimize_button = QPushButton("—")
        self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("✕")

        for btn, color in [(self.minimize_button, "#f59e0b"), (self.maximize_button, "#10b981"), (self.close_button, "#ef4444")]:
            btn.setFixedSize(20, 20)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 10px;
                    font-size: 10px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                }}
            """)
            self.controls_layout.addWidget(btn)

        self.main_layout.addLayout(self.controls_layout)
