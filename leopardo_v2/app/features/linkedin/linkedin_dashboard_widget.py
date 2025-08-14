import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QStackedWidget, QAction, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class LinkedInDashboardWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LinkedIn Dashboard")
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_main_content()

    def create_menu(self):
        menubar = self.menuBar()

        self.instance_action = QAction(QIcon(), 'Instance', self)
        menubar.addAction(self.instance_action)

        self.media_action = QAction(QIcon(), 'Médias', self)
        menubar.addAction(self.media_action)

        self.group_action = QAction(QIcon(), 'Groupes', self)
        menubar.addAction(self.group_action)

        self.about_action = QAction(QIcon(), 'About', self)
        menubar.addAction(self.about_action)

        self.certificate_action = QAction(QIcon(), 'Certif', self)
        menubar.addAction(self.certificate_action)

        self.settings_menu = menubar.addMenu('Param')
        self.dark_mode_action = QAction('Activer le mode sombre', self, checkable=True)
        self.settings_menu.addAction(self.dark_mode_action)

        self.language_menu = QMenu('Langue', self)
        menubar.addMenu(self.language_menu)

        self.tools_menu = menubar.addMenu("Tools")

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LinkedInDashboardWidget()
    window.show()
    sys.exit(app.exec_())
