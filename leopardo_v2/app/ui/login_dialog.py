from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.layout = QFormLayout(self)

        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        self.layout.addRow("Username:", self.username_field)
        self.layout.addRow("Password:", self.password_field)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.accept)
        self.layout.addWidget(self.login_button)

    def get_credentials(self):
        return self.username_field.text(), self.password_field.text()
