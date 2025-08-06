import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QStackedWidget, QPushButton)
from PyQt5.QtCore import Qt
from ...components.widgets.ribbon_menu import RibbonMenu

class SalesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Ribbon Menu
        ribbon_buttons = [
            {"text": "DASHBOARD", "icon": "path/to/icon.png"},
            {"text": "PRODUCTS", "icon": "path/to/icon.png"},
            {"text": "ORDERS", "icon": "path/to/icon.png"},
            {"text": "CUSTOMERS", "icon": "path/to/icon.png"},
            {"text": "REPORTS", "icon": "path/to/icon.png"},
        ]
        self.ribbon_menu = RibbonMenu(buttons=ribbon_buttons)
        self.main_layout.addWidget(self.ribbon_menu)

        # Page Content
        self.page_content = QStackedWidget()
        self.main_layout.addWidget(self.page_content)

        # Add pages
        self.page_content.addWidget(QLabel("DASHBOARD PAGE (Under Construction)"))
        self.page_content.addWidget(QLabel("PRODUCTS PAGE (Under Construction)"))
        self.page_content.addWidget(QLabel("ORDERS PAGE (Under Construction)"))
        self.page_content.addWidget(QLabel("CUSTOMERS PAGE (Under Construction)"))
        self.page_content.addWidget(QLabel("REPORTS PAGE (Under Construction)"))

        # Connect ribbon buttons to pages
        for i, button_info in enumerate(ribbon_buttons):
            button = self.ribbon_menu.findChild(QPushButton, f"ribbon_button_{button_info['text']}")
            if button:
                button.clicked.connect(lambda _, index=i: self.page_content.setCurrentIndex(index))
