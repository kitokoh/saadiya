"""
Main window of the Leopardo V2 application.
"""

import sys
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox

# Local application imports
from .splash_screen import SplashScreen
from .top_menu import TopMenu
from .side_menu import SideMenu
from .status_bar import StatusBar
from ..utils.language import LanguageManager
from ..services.auth import AuthService
from .login_dialog import LoginDialog
from ..services.notifications import NotificationService
from ..services.updater import UpdaterService
from ..services.config_service import ConfigService
from ..services.service_container import container
from .dialogs.menu_config_dialog import MenuConfigDialog
from ..core.app_setup import init_features, connect_signals
from ..features.upgrade.upgrade_window import SpecialOfferWindow


class MainWindow(QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        super().__init__()
        self.setWindowTitle("Leopardo V2")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize core services, UI components, features, and signals
        self._init_core_services()
        self._init_ui_components()
        init_features(self)
        connect_signals(self)

        # Perform initial checks
        self.check_login()
        self.updater_service.check_for_updates()
        self.update_menu_visibility()

    def _init_core_services(self):
        """
        Initializes the core services of the application.
        """
        container.register('config_service', ConfigService())
        container.register('auth_service', AuthService())
        container.register('language_manager', LanguageManager(QApplication.instance()))
        container.register('notification_service', NotificationService(self))
        container.register('updater_service', UpdaterService(self))

        self.config_service = container.get('config_service')
        self.auth_service = container.get('auth_service')
        self.language_manager = container.get('language_manager')
        self.notification_service = container.get('notification_service')
        self.updater_service = container.get('updater_service')

        # Load menu configuration
        self.menu_config = self.config_service.get('menu_config', {
            'Tools': True,
            'Beta Feature': True,
            'Data': True,
            'Support': True,
            'Upgrade': True,
            'Settings': True,
            'Language': True
        })

    def _init_ui_components(self):
        """
        Initializes the UI components of the main window.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top menu
        self.top_menu = TopMenu()
        self.main_layout.addWidget(self.top_menu)

        # Main content area
        self.main_content = QHBoxLayout()
        self.main_layout.addLayout(self.main_content)

        # Side menu
        self.side_menu = SideMenu()
        self.main_content.addWidget(self.side_menu)

        # Content stack to hold the different feature widgets
        self.content_stack = QStackedWidget()
        self.main_content.addWidget(self.content_stack)

        # Status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def check_login(self):
        """
        Checks if the user is logged in. If not, shows the login dialog.
        """
        if not self.auth_service.is_logged_in:
            self.show_login_dialog()

    def show_login_dialog(self):
        """
        Shows the login dialog.
        """
        dialog = LoginDialog(self)
        if dialog.exec_() == QMessageBox.Accepted:
            username, password = dialog.get_credentials()
            if self.auth_service.login(username, password):
                self.update_user_profile()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
                self.show_login_dialog()
        else:
            # Close the application if the user cancels the login dialog
            if not self.auth_service.is_logged_in:
                self.close()

    def logout(self):
        """
        Logs out the current user.
        """
        self.auth_service.logout()
        self.update_user_profile()
        self.check_login()

    def show_upgrade_window(self):
        """
        Shows the special offer window for upgrading the plan.
        """
        dialog = SpecialOfferWindow(self)
        dialog.exec_()

    def switch_to_enterprise(self):
        """
        Switches the user to enterprise mode.
        """
        self.auth_service.is_enterprise_mode = True
        self.update_user_profile()

    def switch_to_personal(self):
        """
        Switches the user to personal mode.
        """
        self.auth_service.is_enterprise_mode = False
        self.update_user_profile()

    def update_user_profile(self):
        """
        Updates the user profile section in the side menu.
        """
        if self.auth_service.is_logged_in:
            self.side_menu.user_profile.user_button.setText(f"👤 {self.auth_service.current_user}")
            self.side_menu.user_profile.login_button.setVisible(False)
            self.side_menu.user_profile.logout_button.setVisible(True)
            self.side_menu.user_profile.enterprise_button.setVisible(not self.auth_service.is_enterprise_mode)
            self.side_menu.user_profile.personal_button.setVisible(self.auth_service.is_enterprise_mode)
        else:
            self.side_menu.user_profile.user_button.setText("👤 Guest")
            self.side_menu.user_profile.login_button.setVisible(True)
            self.side_menu.user_profile.logout_button.setVisible(False)
            self.side_menu.user_profile.enterprise_button.setVisible(False)
            self.side_menu.user_profile.personal_button.setVisible(False)

    def show_menu_config_dialog(self):
        """
        Shows the menu configuration dialog.
        """
        dialog = MenuConfigDialog(self.menu_config, self)
        if dialog.exec_() == QMessageBox.Accepted:
            self.menu_config = dialog.get_menu_config()
            self.config_service.set('menu_config', self.menu_config)
            self.update_menu_visibility()

    def update_menu_visibility(self):
        """
        Updates the visibility of the menu items based on the menu configuration.
        """
        self.side_menu.marketing_button.setVisible(self.menu_config.get('Marketing', True))
        self.side_menu.sales_button.setVisible(self.menu_config.get('Sales', True))
        self.side_menu.run_button.setVisible(self.menu_config.get('Run', True))
        self.side_menu.ai_agent_button.setVisible(self.menu_config.get('AI Agent', True))
        self.side_menu.finance_button.setVisible(self.menu_config.get('Finance', True))
        self.side_menu.upgrade_button.setVisible(self.menu_config.get('Upgrade', True))
        self.side_menu.anciens_button.setVisible(self.menu_config.get('Anciens', True))
        self.side_menu.language_menu_button.setVisible(self.menu_config.get('Language', True))
