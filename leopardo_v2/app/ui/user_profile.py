from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt

class UserProfile(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-top: 1px solid #333333;
            }
        """)

        self.user_button = QPushButton("👤 Guest")
        self.user_button.setFixedHeight(40)
        self.user_button.setStyleSheet("""
            QPushButton {
                background-color: #3A3F4B;
                color: white;
                border: none;
                font-size: 14px;
                text-align: left;
                padding-left: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4A4F5C;
            }
        """)
        self.main_layout.addWidget(self.user_button)

        self.user_menu = QFrame()
        self.user_menu.setVisible(False)
        self.user_menu_layout = QVBoxLayout(self.user_menu)
        self.user_menu.setLayout(self.user_menu_layout)

        self.login_button = QPushButton("🔑 Login")
        self.logout_button = QPushButton("🚪 Logout")
        self.enterprise_button = QPushButton("🏢 Enterprise Mode")
        self.personal_button = QPushButton("👤 Personal Mode")

        for btn in [self.login_button, self.logout_button, self.enterprise_button, self.personal_button]:
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3A3F4B;
                    color: white;
                    border: none;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4A4F5C;
                }
            """)
            self.user_menu_layout.addWidget(btn)

        self.main_layout.addWidget(self.user_menu)

        self.user_button.clicked.connect(self.toggle_user_menu)

    def toggle_user_menu(self):
        self.user_menu.setVisible(not self.user_menu.isVisible())
