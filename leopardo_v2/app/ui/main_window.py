"""
Main window of the Leopardo V2 application.
"""

import sys
from PyQt5.QtCore import Qt, QCoreApplication, QTimer, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
from ..features.marketing_dashboard.marketing_dashboard_widget import MarketingDashboardWidget
from ..features.sales_dashboard.sales_dashboard_widget import SalesDashboardWidget
from ..features.finance_dashboard.finance_dashboard_widget import FinanceDashboardWidget
from ..features.management_dashboard.management_dashboard_widget import ManagementDashboardWidget
from ..features.social_media.instagram_dashboard import InstagramDashboardWidget
from ..features.social_media.linkedin_dashboard import LinkedInDashboardWidget
from ..features.social_media.twitter_dashboard import TwitterDashboardWidget
from ..features.social_media.youtube_dashboard import YouTubeDashboardWidget
from ..features.social_media.pinterest_dashboard import PinterestDashboardWidget
from ..features.social_media.reddit_dashboard import RedditDashboardWidget
from ..features.social_media.snapchat_dashboard import SnapchatDashboardWidget


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
        self._connect_signals()

        # Perform initial checks
        self.check_login()
        self.updater_service.check_for_updates()
        self.test_notification()

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
            'Marketing Dashboard': True,
            'Sales Dashboard': True,
            'Finance Dashboard': True,
            'Management Dashboard': True,
            'Presence Plan': True,
            'Instagram Dashboard': True,
            'LinkedIn Dashboard': True,
            'Twitter Dashboard': True,
            'YouTube Dashboard': True,
            'Pinterest Dashboard': True,
            'Reddit Dashboard': True,
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
        self.notification_service.add_badge("marketing_dashboard", self.side_menu.marketing_dashboard_button)


        # Content stack to hold the different feature widgets
        self.content_stack = QStackedWidget()
        self.main_content.addWidget(self.content_stack)

        # Add MarketingDashboardWidget to the stack
        self.marketing_dashboard_widget = MarketingDashboardWidget()
        self.content_stack.addWidget(self.marketing_dashboard_widget)

        # Add SalesDashboardWidget to the stack
        self.sales_dashboard_widget = SalesDashboardWidget()
        self.content_stack.addWidget(self.sales_dashboard_widget)

        # Add FinanceDashboardWidget to the stack
        self.finance_dashboard_widget = FinanceDashboardWidget()
        self.content_stack.addWidget(self.finance_dashboard_widget)

        # Add ManagementDashboardWidget to the stack
        self.management_dashboard_widget = ManagementDashboardWidget()
        self.content_stack.addWidget(self.management_dashboard_widget)

        # Add QWebEngineView for the presence plan
        self.presence_plan_view = QWebEngineView()
        self.presence_plan_view.setUrl(QUrl("https://leopardo-ai.web.app/"))
        self.content_stack.addWidget(self.presence_plan_view)

        # Add InstagramDashboardWidget to the stack
        self.instagram_dashboard_widget = InstagramDashboardWidget()
        self.content_stack.addWidget(self.instagram_dashboard_widget)

        # Add LinkedInDashboardWidget to the stack
        self.linkedin_dashboard_widget = LinkedInDashboardWidget()
        self.content_stack.addWidget(self.linkedin_dashboard_widget)

        # Add TwitterDashboardWidget to the stack
        self.twitter_dashboard_widget = TwitterDashboardWidget()
        self.content_stack.addWidget(self.twitter_dashboard_widget)

        # Add YouTubeDashboardWidget to the stack
        self.youtube_dashboard_widget = YouTubeDashboardWidget()
        self.content_stack.addWidget(self.youtube_dashboard_widget)

        # Add PinterestDashboardWidget to the stack
        self.pinterest_dashboard_widget = PinterestDashboardWidget()
        self.content_stack.addWidget(self.pinterest_dashboard_widget)

        # Add RedditDashboardWidget to the stack
        self.reddit_dashboard_widget = RedditDashboardWidget()
        self.content_stack.addWidget(self.reddit_dashboard_widget)

        # Status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def _connect_signals(self):
        """
        Connects the signals from the UI components to the main window slots.
        """
        connect_signals(self)
        self.side_menu.marketing_dashboard_requested.connect(self.show_marketing_dashboard)
        self.side_menu.sales_dashboard_requested.connect(self.show_sales_dashboard)
        self.side_menu.finance_dashboard_requested.connect(self.show_finance_dashboard)
        self.side_menu.management_dashboard_requested.connect(self.show_management_dashboard)
        self.side_menu.presence_plan_requested.connect(self.show_presence_plan)
        self.side_menu.instagram_dashboard_requested.connect(self.show_instagram_dashboard)
        self.side_menu.linkedin_dashboard_requested.connect(self.show_linkedin_dashboard)
        self.side_menu.twitter_dashboard_requested.connect(self.show_twitter_dashboard)
        self.side_menu.youtube_dashboard_requested.connect(self.show_youtube_dashboard)
        self.side_menu.pinterest_dashboard_requested.connect(self.show_pinterest_dashboard)
        self.side_menu.reddit_dashboard_requested.connect(self.show_reddit_dashboard)

    def show_marketing_dashboard(self):
        """
        Shows the marketing dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.marketing_dashboard_widget)
        self.notification_service.set_badge_count("marketing_dashboard", 0)


    def show_sales_dashboard(self):
        """
        Shows the sales dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.sales_dashboard_widget)

    def show_finance_dashboard(self):
        """
        Shows the finance dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.finance_dashboard_widget)

    def show_management_dashboard(self):
        """
        Shows the management dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.management_dashboard_widget)

    def show_presence_plan(self):
        """
        Shows the presence plan web page.
        """
        self.content_stack.setCurrentWidget(self.presence_plan_view)

    def show_instagram_dashboard(self):
        """
        Shows the instagram dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.instagram_dashboard_widget)

    def show_linkedin_dashboard(self):
        """
        Shows the linkedin dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.linkedin_dashboard_widget)

    def show_twitter_dashboard(self):
        """
        Shows the twitter dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.twitter_dashboard_widget)

    def show_youtube_dashboard(self):
        """
        Shows the youtube dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.youtube_dashboard_widget)

    def show_pinterest_dashboard(self):
        """
        Shows the pinterest dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.pinterest_dashboard_widget)

    def show_reddit_dashboard(self):
        """
        Shows the reddit dashboard widget.
        """
        self.content_stack.setCurrentWidget(self.reddit_dashboard_widget)

    def check_login(self):
        """
        Checks if the user is logged in. If not, shows the login dialog.
        """
        if not self.auth_service.is_logged_in:
            self.show_login_dialog()
        self.update_menu_visibility()


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
        self.auth_service.is_enterprise = True
        self.update_user_profile()

    def switch_to_personal(self):
        """
        Switches the user to personal mode.
        """
        self.auth_service.is_enterprise = False
        self.update_user_profile()

    def update_user_profile(self):
        """
        Updates the user profile section in the side menu.
        """
        if self.auth_service.is_logged_in:
            self.side_menu.user_profile.user_button.setText(f"👤 {self.auth_service.current_user}")
            self.side_menu.user_profile.login_button.setVisible(False)
            self.side_menu.user_profile.logout_button.setVisible(True)
            self.side_menu.user_profile.enterprise_button.setVisible(not self.auth_service.is_enterprise)
            self.side_menu.user_profile.personal_button.setVisible(self.auth_service.is_enterprise)
        else:
            self.side_menu.user_profile.user_button.setText("👤 Guest")
            self.side_menu.user_profile.login_button.setVisible(True)
            self.side_menu.user_profile.logout_button.setVisible(False)
            self.side_menu.user_profile.enterprise_button.setVisible(False)
            self.side_menu.user_profile.personal_button.setVisible(False)
        self.update_menu_visibility()

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
        Updates the visibility of the menu items based on the menu configuration and user access level.
        """
        self.side_menu.marketing_dashboard_button.setVisible(
            self.menu_config.get('Marketing Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.sales_dashboard_button.setVisible(
            self.menu_config.get('Sales Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.finance_dashboard_button.setVisible(
            self.menu_config.get('Finance Dashboard', True) and self.auth_service.has_access('enterprise')
        )
        self.side_menu.management_dashboard_button.setVisible(
            self.menu_config.get('Management Dashboard', True) and self.auth_service.has_access('enterprise')
        )
        self.side_menu.presence_plan_button.setVisible(
            self.menu_config.get('Presence Plan', True)
        )
        self.side_menu.instagram_dashboard_button.setVisible(
            self.menu_config.get('Instagram Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.linkedin_dashboard_button.setVisible(
            self.menu_config.get('LinkedIn Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.twitter_dashboard_button.setVisible(
            self.menu_config.get('Twitter Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.youtube_dashboard_button.setVisible(
            self.menu_config.get('YouTube Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.pinterest_dashboard_button.setVisible(
            self.menu_config.get('Pinterest Dashboard', True) and self.auth_service.has_access('pro')
        )
        self.side_menu.reddit_dashboard_button.setVisible(
            self.menu_config.get('Reddit Dashboard', True) and self.auth_service.has_access('pro')
        )

    def test_notification(self):
        """
        Tests the notification service.
        """
        self.notification_service.set_badge_count("marketing_dashboard", 5)
        self.notification_service.show_notification("Test Notification", "This is a test notification.")
