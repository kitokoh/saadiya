import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                            QStackedWidget, QToolBar, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class RibbonButton(QPushButton):
    def __init__(self, text="", icon=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        if icon:
            self.setIcon(QIcon(icon))
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 6px 12px;
                background: transparent;
                color: #333;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #e6e6e6;
                border-radius: 4px;
            }
            QPushButton:pressed {
                background: #d0d0d0;
                border-radius: 4px;
            }
            QPushButton:checked {
                background: #d0d0d0;
                border-radius: 4px;
            }
        """)

class SalesDashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(QApplication.translate("SalesDashboardWidget", "Sales Dashboard"))

        self.page_instances = {
            'documents': None,
            'link_manager': None,
            'contacts': None,
            'prompts': None,
            'ai_agent': None,
            'customer_support': None,
            'projects': None
        }

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.create_ribbon()
        self.create_main_content()
        layout.addWidget(self.ribbon)
        layout.addWidget(self.stacked_widget)
        self.show_page("documents")

    def create_ribbon(self):
        self.ribbon = QToolBar(QApplication.translate("SalesDashboardWidget", "Main Menu"))
        self.ribbon.setIconSize(QSize(20, 20))

        buttons_to_create = [
            ("Documents", "documents"),
            ("Link Manager", "link_manager"),
            ("Contacts", "contacts"),
            ("Prompts", "prompts"),
            ("AI Agent", "ai_agent"),
            ("Customer Support", "customer_support"),
            ("Projects", "projects"),
        ]

        self.ribbon_buttons = {}
        for text, page_name in buttons_to_create:
            button = RibbonButton(QApplication.translate("SalesDashboardWidget", text))
            button.clicked.connect(lambda checked, name=page_name: self.show_page(name))
            self.ribbon.addWidget(button)
            self.ribbon_buttons[page_name] = button

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()

    def load_page(self, page_name):
        if self.page_instances.get(page_name) is None:
            widget = None
            if page_name == 'documents':
                from leopardo_v2.app.features.dms.dms_widget import DmsWidget
                widget = DmsWidget()
            elif page_name == 'link_manager':
                from leopardo_v2.app.features.short_links.short_links_widget import ShortLinksWidget
                widget = ShortLinksWidget()
            elif page_name == 'contacts':
                from leopardo_v2.app.features.contacts.contacts_widget import ContactsWidget
                widget = ContactsWidget()
            elif page_name == 'prompts':
                from leopardo_v2.app.features.prompts_tools.prompts_tools_widget import PromptsToolsWidget
                widget = PromptsToolsWidget()
            elif page_name == 'ai_agent':
                from leopardo_v2.app.features.ai_agent.ai_agent_widget import AiAgentWidget
                widget = AiAgentWidget()
            elif page_name == 'customer_support':
                from leopardo_v2.app.features.sav.sav_widget import SavWidget
                widget = SavWidget()
            elif page_name == 'projects':
                from leopardo_v2.app.features.project_management.project_management_widget import ProjectManagementWidget
                widget = ProjectManagementWidget()

            if widget:
                self.page_instances[page_name] = widget
                self.stacked_widget.addWidget(widget)

        return self.page_instances.get(page_name)

    def show_page(self, page_name):
        page = self.load_page(page_name)
        if page:
            self.stacked_widget.setCurrentWidget(page)
            self.update_button_states(page_name)

    def update_button_states(self, active_page):
        for page_name, button in self.ribbon_buttons.items():
            button.setChecked(page_name == active_page)
