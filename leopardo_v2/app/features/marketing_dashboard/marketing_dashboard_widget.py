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

class MarketingDashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(QApplication.translate("MarketingDashboardWidget", "Marketing Dashboard"))

        self.page_instances = {
            'media': None,
            'groups': None,
            'content': None,
            'planning': None,
            'email': None,
            'sms': None,
            'settings': None,
            'analytics': None,
            'ads': None
        }

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.create_ribbon()
        self.create_main_content()
        layout.addWidget(self.ribbon)
        layout.addWidget(self.stacked_widget)
        self.show_page("media")

    def create_ribbon(self):
        self.ribbon = QToolBar(QApplication.translate("MarketingDashboardWidget", "Main Menu"))
        self.ribbon.setIconSize(QSize(20, 20))

        buttons_to_create = [
            ("Media Library", "media"),
            ("Audience Groups", "groups"),
            ("Content Creator", "content"),
            ("Content Calendar", "planning"),
            ("Email Campaigns", "email"),
            ("SMS Marketing", "sms"),
            ("Settings", "settings"),
            ("Performance Analytics", "analytics"),
            ("Ad Campaigns", "ads"),
        ]

        self.ribbon_buttons = {}
        for text, page_name in buttons_to_create:
            button = RibbonButton(QApplication.translate("MarketingDashboardWidget", text))
            button.clicked.connect(lambda checked, name=page_name: self.show_page(name))
            self.ribbon.addWidget(button)
            self.ribbon_buttons[page_name] = button

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()

    def load_page(self, page_name):
        if self.page_instances.get(page_name) is None:
            widget = None
            if page_name == 'media':
                from leopardo_v2.app.features.my_media.my_media_widget import MyMediaWidget
                widget = MyMediaWidget()
            elif page_name == 'groups':
                from leopardo_v2.app.features.my_groups.my_groups_widget import MyGroupsWidget
                widget = MyGroupsWidget()
            elif page_name == 'content':
                from leopardo_v2.app.features.content_generator.content_generator_widget import ContentGeneratorWidget
                widget = ContentGeneratorWidget()
            elif page_name == 'planning':
                from leopardo_v2.app.features.campaign_scheduler.campaign_scheduler_widget import CampaignSchedulerWidget
                widget = CampaignSchedulerWidget()
            elif page_name == 'email' or page_name == 'sms':
                from leopardo_v2.app.features.email_sms.email_sms_widget import EmailSmsWidget
                widget = EmailSmsWidget()
            elif page_name == 'settings':
                from leopardo_v2.app.features.settings.settings_widget import SettingsWidget
                widget = SettingsWidget()
            elif page_name == 'analytics':
                from leopardo_v2.app.features.statistics.statistics_widget import StatisticsWidget
                widget = StatisticsWidget()
            elif page_name == 'ads':
                from leopardo_v2.app.features.ads_manager.ads_manager_widget import AdsManagerWidget
                widget = AdsManagerWidget()

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
