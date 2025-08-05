import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QStackedWidget, QMessageBox
from .ui.top_menu import TopMenu
from .ui.side_menu import SideMenu
from .ui.status_bar import StatusBar
from .features.home.home_widget import HomeWidget
from .features.marketing.marketing_widget import MarketingWidget
from .features.sales.sales_widget import SalesWidget
from .features.run.run_widget import RunWidget
from .features.finance.finance_widget import FinanceWidget
from .features.settings.settings_widget import SettingsWidget
from .features.tools.tools_widget import ToolsWidget
from .utils.language import LanguageManager
from .services.auth import AuthService
from .ui.login_dialog import LoginDialog
from .services.notifications import NotificationService
from .services.updater import UpdaterService

class RefactoredApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leopardo V2")
        self.setGeometry(100, 100, 1200, 800)

        # Auth Service
        self.auth_service = AuthService()

        # Language Manager
        self.language_manager = LanguageManager(QApplication.instance())

        # Notification Service
        self.notification_service = NotificationService(self)

        # Updater Service
        self.updater_service = UpdaterService(self)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top Menu
        self.top_menu = TopMenu()
        self.main_layout.addWidget(self.top_menu)

        # Main content area
        self.main_content = QHBoxLayout()
        self.main_layout.addLayout(self.main_content)

        # Side Menu
        self.side_menu = SideMenu()
        self.main_content.addWidget(self.side_menu)

        # Content Stack
        self.content_stack = QStackedWidget()
        self.main_content.addWidget(self.content_stack)

        # Feature Widgets
        self.home_widget = HomeWidget()
        self.marketing_widget = MarketingWidget()
        self.sales_widget = SalesWidget()
        self.run_widget = RunWidget()
        self.finance_widget = FinanceWidget()
        self.settings_widget = SettingsWidget()
        self.tools_widget = ToolsWidget()

        self.content_stack.addWidget(self.home_widget)
        self.content_stack.addWidget(self.marketing_widget)
        self.content_stack.addWidget(self.sales_widget)
        self.content_stack.addWidget(self.run_widget)
        self.content_stack.addWidget(self.finance_widget)
        self.content_stack.addWidget(self.settings_widget)
        self.content_stack.addWidget(self.tools_widget)

        # Status Bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        # Connect side menu buttons to show/hide widgets
        self.side_menu.home_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget))
        self.side_menu.tools_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.tools_widget))
        self.side_menu.beta_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.marketing_widget))
        self.side_menu.data_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.finance_widget))
        self.side_menu.support_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget))
        self.side_menu.upgrade_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget))
        self.side_menu.settings_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_widget))

        # Connect language switching
        self.side_menu.language_menu.actions()[0].triggered.connect(lambda: self.language_manager.switch_language('en'))
        self.side_menu.language_menu.actions()[1].triggered.connect(lambda: self.language_manager.switch_language('fr'))
        self.side_menu.language_menu.actions()[2].triggered.connect(lambda: self.language_manager.switch_language('tr'))
        self.side_menu.language_menu.actions()[3].triggered.connect(lambda: self.language_manager.switch_language('ar'))
        self.side_menu.language_menu.actions()[4].triggered.connect(lambda: self.language_manager.switch_language('pt'))

        # Connect Login/Logout
        self.top_menu.file_menu.addAction("Login").triggered.connect(self.show_login_dialog)
        self.top_menu.file_menu.addAction("Logout").triggered.connect(self.logout)

        # Connect Notifications
        self.top_menu.file_menu.addAction("Show Notification").triggered.connect(lambda: self.notification_service.show_notification("Test", "This is a test notification."))

        # Connect Updater
        self.top_menu.file_menu.addAction("Check for Updates").triggered.connect(self.updater_service.check_for_updates)

        self.check_login()
        self.updater_service.check_for_updates()

    def check_login(self):
        if not self.auth_service.is_logged_in:
            self.show_login_dialog()

    def show_login_dialog(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            username, password = dialog.get_credentials()
            if not self.auth_service.login(username, password):
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
                self.show_login_dialog()
        else:
            if not self.auth_service.is_logged_in:
                self.close()

    def logout(self):
        self.auth_service.logout()
        self.check_login()


if __name__ == "__main__":
    from PyQt5.QtCore import Qt, QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = RefactoredApp()
    window.show()
    sys.exit(app.exec_())
