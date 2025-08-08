import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QStackedWidget, QToolBar, QAction, QMainWindow, QGroupBox,
                             QFormLayout, QLineEdit, QTextEdit, QComboBox, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class WhasappingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.init_ui()

    def set_controller(self, controller):
        self.controller = controller
        self.connect_signals()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar
        self.toolbar = QToolBar("Whasapping Toolbar")
        main_layout.addWidget(self.toolbar)

        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Robot Page
        self.robot_page = QWidget()
        self.init_robot_page()
        self.stacked_widget.addWidget(self.robot_page)

        # Accounts Page
        self.accounts_page = QWidget()
        self.init_accounts_page()
        self.stacked_widget.addWidget(self.accounts_page)

        # Toolbar Actions
        self.robot_action = QAction("Robot", self)
        self.robot_action.setCheckable(True)
        self.robot_action.setChecked(True)
        self.toolbar.addAction(self.robot_action)

        self.accounts_action = QAction("Comptes", self)
        self.accounts_action.setCheckable(True)
        self.toolbar.addAction(self.accounts_action)

    def init_robot_page(self):
        layout = QVBoxLayout(self.robot_page)

        # Toolbar for Robot Page
        robot_toolbar = QToolBar("Robot Actions")
        layout.addWidget(robot_toolbar)

        self.start_action = QAction("Start Robot", self)
        self.stop_action = QAction("Stop Robot", self)
        self.add_media_action = QAction("Ajouter Média", self)
        self.add_doc_action = QAction("Ajouter Document", self)

        robot_toolbar.addAction(self.start_action)
        robot_toolbar.addAction(self.stop_action)
        robot_toolbar.addAction(self.add_media_action)
        robot_toolbar.addAction(self.add_doc_action)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # GroupBox for settings
        settings_groupbox = QGroupBox("Configuration du Robot")
        scroll_area.setWidget(settings_groupbox)
        form_layout = QFormLayout(settings_groupbox)

        self.message_edit = QTextEdit()
        self.contact_name_edit = QLineEdit()
        self.message_type_combo = QComboBox()
        self.message_type_combo.addItems(["Message Texte", "Message Image"])
        self.status_label = QLabel("Prêt")

        form_layout.addRow("Message:", self.message_edit)
        form_layout.addRow("Nom du contact ou groupe:", self.contact_name_edit)
        form_layout.addRow("Type de message:", self.message_type_combo)
        form_layout.addRow("Statut:", self.status_label)

        # Contacts Table
        self.contacts_table = QTableWidget(0, 2)
        self.contacts_table.setHorizontalHeaderLabels(["Nom", "Statut"])
        self.contacts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.contacts_table)

    def init_accounts_page(self):
        layout = QVBoxLayout(self.accounts_page)

        # Toolbar for Accounts Page
        accounts_toolbar = QToolBar("Account Actions")
        layout.addWidget(accounts_toolbar)

        self.add_account_action = QAction("Ajouter un compte", self)
        self.delete_account_action = QAction("Supprimer le compte", self)
        self.check_status_action = QAction("Vérifier le statut", self)

        accounts_toolbar.addAction(self.add_account_action)
        accounts_toolbar.addAction(self.delete_account_action)
        accounts_toolbar.addAction(self.check_status_action)

        # Accounts Table
        self.accounts_table = QTableWidget(0, 3)
        self.accounts_table.setHorizontalHeaderLabels(["Nom du Compte", "Numéro", "Statut"])
        self.accounts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.accounts_table)

    def connect_signals(self):
        # Main toolbar
        self.robot_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.robot_page))
        self.accounts_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.accounts_page))

        # Robot page signals
        self.start_action.triggered.connect(self.controller.start_robot)
        self.stop_action.triggered.connect(self.controller.stop_robot)
        self.add_media_action.triggered.connect(self.controller.add_media)
        self.add_doc_action.triggered.connect(self.controller.add_document)

        # Accounts page signals
        self.add_account_action.triggered.connect(self.controller.add_account)
        self.delete_account_action.triggered.connect(self.controller.delete_account)
        self.check_status_action.triggered.connect(self.controller.check_status)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Dummy Controller for testing
    class DummyController:
        def start_robot(self): print("Start robot clicked")
        def stop_robot(self): print("Stop robot clicked")
        def add_media(self): print("Add media clicked")
        def add_document(self): print("Add document clicked")
        def add_account(self): print("Add account clicked")
        def delete_account(self): print("Delete account clicked")
        def check_status(self): print("Check status clicked")

    main_win = QMainWindow()
    whasapping_widget = WhasappingWidget()
    whasapping_widget.set_controller(DummyController())
    main_win.setCentralWidget(whasapping_widget)
    main_win.show()
    sys.exit(app.exec_())
