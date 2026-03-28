import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QStackedWidget, QAction, QMenu)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ...features.my_media.my_media_widget import MyMediaWidget
from ...features.my_groups.my_groups_widget import MyGroupsWidget
from ...features.instances.instances_widget import InstancesWidget
from ...features.facebook.fb_robot_install_widget import FbRobotInstallWidget
from ...features.statistics.statistics_widget import StatisticsWidget

class FacebookDashboardWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Facebook Dashboard")
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_main_content()
        self.connect_actions()

    def create_menu(self):
        menubar = self.menuBar()

        self.instance_action = QAction(QIcon(), 'Instance', self)
        menubar.addAction(self.instance_action)

        self.media_action = QAction(QIcon(), 'Médias', self)
        menubar.addAction(self.media_action)

        self.group_action = QAction(QIcon(), 'Groupes', self)
        menubar.addAction(self.group_action)

        self.dashboard_action = QAction(QIcon(), 'Dashboard', self)
        menubar.addAction(self.dashboard_action)

        self.install_action = QAction(QIcon(), 'Installer', self)
        menubar.addAction(self.install_action)

    def create_main_content(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.instance_widget = InstancesWidget()
        self.media_widget = MyMediaWidget()
        self.group_widget = MyGroupsWidget()
        self.dashboard_widget = StatisticsWidget()
        self.install_widget = FbRobotInstallWidget()

        self.stacked_widget.addWidget(self.instance_widget)
        self.stacked_widget.addWidget(self.media_widget)
        self.stacked_widget.addWidget(self.group_widget)
        self.stacked_widget.addWidget(self.dashboard_widget)
        self.stacked_widget.addWidget(self.install_widget)

    def connect_actions(self):
        self.instance_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.instance_widget))
        self.media_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.media_widget))
        self.group_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.group_widget))
        self.dashboard_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_widget))
        self.install_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.install_widget))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FacebookDashboardWidget()
    window.show()
    sys.exit(app.exec_())
