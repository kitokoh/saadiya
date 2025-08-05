import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QStackedWidget, QMessageBox
from .ui.top_menu import TopMenu
from .ui.side_menu import SideMenu
from .ui.status_bar import StatusBar
from .features.home import create_home_feature
from .features.marketing import create_marketing_feature
from .features.sales import create_sales_feature
from .features.run import create_run_feature
from .features.finance import create_finance_feature
from .features.settings import create_settings_feature
from .features.tools import create_tools_feature
from .features.tools.sub_pages.interconnexion_widget import InterconnexionWidget
from .features.tools.sub_pages.add_on_widget import AddOnWidget
from .features.tools.sub_pages.remote_control_widget import RemoteControlWidget
from .features.tools.sub_pages.manuelle_widget import ManuelleWidget
from .features.tools.sub_pages.scheduler_widget import SchedulerWidget
from .features.tools.sub_pages.edit_pdf_widget import EditPDFWidget
from .features.tools.sub_pages.watermark_widget import WatermarkWidget
from .features.tools.sub_pages.remove_bg_widget import RemoveBgWidget
from .features.tools.sub_pages.links_widget import LinksWidget
from .features.tools.sub_pages.contacts_widget import ContactsWidget
from .features.tools.sub_pages.groups_widget import GroupsWidget
from .features.tools.sub_pages.media_widget import MediaWidget
from .features.settings.sub_pages.vision_widget import VisionWidget
from .features.settings.sub_pages.com_interne_widget import ComInterneWidget
from .features.settings.sub_pages.com_externe_widget import ComExterneWidget
from .features.beta.sub_pages.licences_widget import LicencesWidget
from .features.beta.sub_pages.ia_beta_widget import IABetaWidget
from .features.data.sub_pages.stats_widget import StatsWidget
from .features.data.sub_pages.strategies_widget import StrategiesWidget
from .features.data.sub_pages.import_data_widget import ImportDataWidget
from .features.data.sub_pages.adn_backup_widget import AdnBackupWidget
from .features.support.sub_pages.about_widget import AboutWidget
from .features.support.sub_pages.documents_widget import DocumentsWidget
from .features.support.sub_pages.contact_widget import ContactWidget
from .features.upgrade.upgrade_window import SpecialOfferWindow
from .features.settings.sub_pages.online_connect.ssh_connect_widget import SshConnectWidget
from .features.settings.sub_pages.online_connect.ftp_server_widget import FtpServerWidget
from .features.settings.sub_pages.online_connect.api_link_widget import ApiLinkWidget
from .features.settings.sub_pages.online_connect.remote_desktop_widget import RemoteDesktopWidget
from .features.settings.sub_pages.online_connect.vpn_connect_widget import VpnConnectWidget
from .features.settings.sub_pages.online_connect.ai_service_widget import AiServiceWidget
from .features.settings.sub_pages.archive.local_zip_widget import LocalZipWidget
from .features.settings.sub_pages.archive.gdrive_widget import GDriveWidget
from .features.settings.sub_pages.archive.dropbox_widget import DropboxWidget
from .features.settings.sub_pages.archive.ftp_backup_widget import FtpBackupWidget
from .features.settings.sub_pages.archive.sftp_widget import SftpWidget
from .features.settings.sub_pages.archive.external_disk_widget import ExternalDiskWidget
from .features.settings.sub_pages.archive.schedule_backup_widget import ScheduleBackupWidget
from .utils.language import LanguageManager
from .services.auth import AuthService
from .ui.login_dialog import LoginDialog
from .services.notifications import NotificationService
from .services.updater import UpdaterService
from .ui.dialogs.menu_config_dialog import MenuConfigDialog

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

        # Menu Config
        self.menu_config = {
            'Tools': True,
            'Beta Feature': True,
            'Data': True,
            'Support': True,
            'Upgrade': True,
            'Settings': True,
            'Language': True
        }

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
        self.home_widget, self.home_controller = create_home_feature()
        self.marketing_widget, self.marketing_controller = create_marketing_feature()
        self.sales_widget, self.sales_controller = create_sales_feature()
        self.run_widget, self.run_controller = create_run_feature()
        self.finance_widget, self.finance_controller = create_finance_feature()
        self.settings_widget, self.settings_controller = create_settings_feature()
        self.tools_widget, self.tools_controller = create_tools_feature()
        self.interconnexion_widget = InterconnexionWidget()
        self.add_on_widget = AddOnWidget()
        self.remote_control_widget = RemoteControlWidget()
        self.manuelle_widget = ManuelleWidget()
        self.scheduler_widget = SchedulerWidget()
        self.edit_pdf_widget = EditPDFWidget()
        self.watermark_widget = WatermarkWidget()
        self.remove_bg_widget = RemoveBgWidget()
        self.links_widget = LinksWidget()
        self.contacts_widget = ContactsWidget()
        self.groups_widget = GroupsWidget()
        self.media_widget = MediaWidget()
        self.vision_widget = VisionWidget()
        self.com_interne_widget = ComInterneWidget()
        self.com_externe_widget = ComExterneWidget()
        self.licences_widget = LicencesWidget()
        self.ia_beta_widget = IABetaWidget()
        self.stats_widget = StatsWidget()
        self.strategies_widget = StrategiesWidget()
        self.import_data_widget = ImportDataWidget()
        self.adn_backup_widget = AdnBackupWidget()
        self.about_widget = AboutWidget()
        self.documents_widget = DocumentsWidget()
        self.contact_widget = ContactWidget()
        self.ssh_connect_widget = SshConnectWidget()
        self.ftp_server_widget = FtpServerWidget()
        self.api_link_widget = ApiLinkWidget()
        self.remote_desktop_widget = RemoteDesktopWidget()
        self.vpn_connect_widget = VpnConnectWidget()
        self.ai_service_widget = AiServiceWidget()
        self.local_zip_widget = LocalZipWidget()
        self.gdrive_widget = GDriveWidget()
        self.dropbox_widget = DropboxWidget()
        self.ftp_backup_widget = FtpBackupWidget()
        self.sftp_widget = SftpWidget()
        self.external_disk_widget = ExternalDiskWidget()
        self.schedule_backup_widget = ScheduleBackupWidget()

        self.content_stack.addWidget(self.home_widget)
        self.content_stack.addWidget(self.marketing_widget)
        self.content_stack.addWidget(self.sales_widget)
        self.content_stack.addWidget(self.run_widget)
        self.content_stack.addWidget(self.finance_widget)
        self.content_stack.addWidget(self.settings_widget)
        self.content_stack.addWidget(self.tools_widget)
        self.content_stack.addWidget(self.interconnexion_widget)
        self.content_stack.addWidget(self.add_on_widget)
        self.content_stack.addWidget(self.remote_control_widget)
        self.content_stack.addWidget(self.manuelle_widget)
        self.content_stack.addWidget(self.scheduler_widget)
        self.content_stack.addWidget(self.edit_pdf_widget)
        self.content_stack.addWidget(self.watermark_widget)
        self.content_stack.addWidget(self.remove_bg_widget)
        self.content_stack.addWidget(self.links_widget)
        self.content_stack.addWidget(self.contacts_widget)
        self.content_stack.addWidget(self.groups_widget)
        self.content_stack.addWidget(self.media_widget)
        self.content_stack.addWidget(self.vision_widget)
        self.content_stack.addWidget(self.com_interne_widget)
        self.content_stack.addWidget(self.com_externe_widget)
        self.content_stack.addWidget(self.licences_widget)
        self.content_stack.addWidget(self.ia_beta_widget)
        self.content_stack.addWidget(self.stats_widget)
        self.content_stack.addWidget(self.strategies_widget)
        self.content_stack.addWidget(self.import_data_widget)
        self.content_stack.addWidget(self.adn_backup_widget)
        self.content_stack.addWidget(self.about_widget)
        self.content_stack.addWidget(self.documents_widget)
        self.content_stack.addWidget(self.contact_widget)
        self.content_stack.addWidget(self.ssh_connect_widget)
        self.content_stack.addWidget(self.ftp_server_widget)
        self.content_stack.addWidget(self.api_link_widget)
        self.content_stack.addWidget(self.remote_desktop_widget)
        self.content_stack.addWidget(self.vpn_connect_widget)
        self.content_stack.addWidget(self.ai_service_widget)
        self.content_stack.addWidget(self.local_zip_widget)
        self.content_stack.addWidget(self.gdrive_widget)
        self.content_stack.addWidget(self.dropbox_widget)
        self.content_stack.addWidget(self.ftp_backup_widget)
        self.content_stack.addWidget(self.sftp_widget)
        self.content_stack.addWidget(self.external_disk_widget)
        self.content_stack.addWidget(self.schedule_backup_widget)

        # Status Bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        # Connect side menu buttons to show/hide widgets
        self.side_menu.home_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget))
        self.side_menu.tools_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.tools_widget))
        self.side_menu.beta_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.marketing_widget))
        self.side_menu.data_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.finance_widget))
        self.side_menu.support_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget))
        self.side_menu.upgrade_button.clicked.connect(self.show_upgrade_window)
        self.side_menu.settings_button.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_widget))

        # Connect language switching
        self.side_menu.language_menu.actions()[0].triggered.connect(lambda: self.language_manager.switch_language('en'))
        self.side_menu.language_menu.actions()[1].triggered.connect(lambda: self.language_manager.switch_language('fr'))
        self.side_menu.language_menu.actions()[2].triggered.connect(lambda: self.language_manager.switch_language('tr'))
        self.side_menu.language_menu.actions()[3].triggered.connect(lambda: self.language_manager.switch_language('ar'))
        self.side_menu.language_menu.actions()[4].triggered.connect(lambda: self.language_manager.switch_language('pt'))

        # Connect User Profile
        self.side_menu.user_profile.login_button.clicked.connect(self.show_login_dialog)
        self.side_menu.user_profile.logout_button.clicked.connect(self.logout)
        self.side_menu.user_profile.enterprise_button.clicked.connect(self.switch_to_enterprise)
        self.side_menu.user_profile.personal_button.clicked.connect(self.switch_to_personal)

        # Connect Menu Config
        self.side_menu.menu_config_button.clicked.connect(self.show_menu_config_dialog)

        # Connect Tools Menu
        self.side_menu.tools_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.interconnexion_widget))
        self.side_menu.tools_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.add_on_widget))
        self.side_menu.tools_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.remote_control_widget))
        self.side_menu.tools_menu.actions()[3].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.manuelle_widget))
        self.side_menu.tools_menu.actions()[4].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.scheduler_widget))
        self.side_menu.tools_menu.actions()[5].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.edit_pdf_widget))
        self.side_menu.tools_menu.actions()[6].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.watermark_widget))
        self.side_menu.tools_menu.actions()[7].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.remove_bg_widget))
        self.side_menu.tools_menu.actions()[8].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.links_widget))
        self.side_menu.tools_menu.actions()[9].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.contacts_widget))
        self.side_menu.tools_menu.actions()[10].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.groups_widget))
        self.side_menu.tools_menu.actions()[11].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.media_widget))

        # Connect Settings Menu
        self.side_menu.settings_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.vision_widget))
        self.side_menu.settings_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.com_interne_widget))
        self.side_menu.settings_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.com_externe_widget))
        self.side_menu.settings_menu.actions()[3].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.settings_widget)) # Instances
        self.side_menu.settings_menu.actions()[4].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.home_widget)) # Installer
        self.side_menu.settings_menu.actions()[5].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.add_on_widget)) # Add-On

        # Connect Online Connect Menu
        self.side_menu.connection_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.ssh_connect_widget))
        self.side_menu.connection_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.ftp_server_widget))
        self.side_menu.connection_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.api_link_widget))
        self.side_menu.connection_menu.actions()[3].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.remote_desktop_widget))
        self.side_menu.connection_menu.actions()[4].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.vpn_connect_widget))
        self.side_menu.connection_menu.actions()[5].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.ai_service_widget))

        # Connect Archive Menu
        self.side_menu.archive_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.local_zip_widget))
        self.side_menu.archive_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.gdrive_widget))
        self.side_menu.archive_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.dropbox_widget))
        self.side_menu.archive_menu.actions()[3].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.ftp_backup_widget))
        self.side_menu.archive_menu.actions()[4].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.sftp_widget))
        self.side_menu.archive_menu.actions()[5].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.external_disk_widget))
        self.side_menu.archive_menu.actions()[6].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.schedule_backup_widget))

        # Connect Beta Feature Menu
        self.side_menu.beta_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.ia_beta_widget))
        self.side_menu.beta_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.licences_widget))

        # Connect Data Menu
        self.side_menu.data_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.tools_widget)) # Prompts
        self.side_menu.data_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.stats_widget))
        self.side_menu.data_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.strategies_widget))
        self.side_menu.data_menu.actions()[3].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.import_data_widget))
        self.side_menu.data_menu.actions()[4].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.adn_backup_widget))

        # Connect Support Menu
        self.side_menu.support_menu.actions()[0].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.about_widget))
        self.side_menu.support_menu.actions()[1].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.documents_widget))
        self.side_menu.support_menu.actions()[2].triggered.connect(lambda: self.content_stack.setCurrentWidget(self.contact_widget))

        # Connect Notifications
        self.top_menu.file_menu.addAction("Show Notification").triggered.connect(lambda: self.notification_service.show_notification("Test", "This is a test notification."))

        # Connect Updater
        self.top_menu.file_menu.addAction("Check for Updates").triggered.connect(self.updater_service.check_for_updates)

        self.check_login()
        self.updater_service.check_for_updates()
        self.update_menu_visibility()

    def check_login(self):
        if not self.auth_service.is_logged_in:
            self.show_login_dialog()

    def show_login_dialog(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
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
        self.auth_service.logout()
        self.update_user_profile()
        self.check_login()

    def show_upgrade_window(self):
        dialog = SpecialOfferWindow(self)
        dialog.exec_()

    def switch_to_enterprise(self):
        self.auth_service.is_enterprise_mode = True
        self.update_user_profile()

    def switch_to_personal(self):
        self.auth_service.is_enterprise_mode = False
        self.update_user_profile()

    def update_user_profile(self):
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
        dialog = MenuConfigDialog(self.menu_config, self)
        if dialog.exec_() == QDialog.Accepted:
            self.menu_config = dialog.get_menu_config()
            self.update_menu_visibility()

    def update_menu_visibility(self):
        self.side_menu.tools_button.setVisible(self.menu_config.get('Tools', True))
        self.side_menu.beta_button.setVisible(self.menu_config.get('Beta Feature', True))
        self.side_menu.data_button.setVisible(self.menu_config.get('Data', True))
        self.side_menu.support_button.setVisible(self.menu_config.get('Support', True))
        self.side_menu.upgrade_button.setVisible(self.menu_config.get('Upgrade', True))
        self.side_menu.settings_button.setVisible(self.menu_config.get('Settings', True))
        self.side_menu.language_menu_button.setVisible(self.menu_config.get('Language', True))


if __name__ == "__main__":
    from PyQt5.QtCore import Qt, QCoreApplication, QTimer
    from .ui.splash_screen import SplashScreen
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    def show_main_window():
        window = RefactoredApp()
        window.show()
        splash.finish(window)

    QTimer.singleShot(3000, show_main_window)
    sys.exit(app.exec_())
