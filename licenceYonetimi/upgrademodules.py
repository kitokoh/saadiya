from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QRadioButton, QButtonGroup,
    QPushButton, QMessageBox, QHBoxLayout, QFrame, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import webbrowser
import sqlite3
import os

class LicenseRequestPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Leopardo AI - License Request"))
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #f4f4f9; font-family: Arial;")

        # Database setup
        self.setup_database()

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel(self.tr("Leopardo AI - License Request"))
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("color: #bbb;")
        layout.addWidget(divider)

        # Module Selection
        module_label = QLabel(self.tr("Select Module:"))
        module_label.setFont(QFont("Arial", 12))
        module_label.setStyleSheet("color: #555;")
        layout.addWidget(module_label)

        self.module_combo = QComboBox()
        self.module_combo.setFont(QFont("Arial", 11))
        self.module_combo.addItems([self.tr("WA CRM"), self.tr("FB Robot Pro"), self.tr("XBot")])
        self.module_combo.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 5px; background-color: #fff;"
        )
        layout.addWidget(self.module_combo)

        # License Duration Selection
        duration_label = QLabel(self.tr("Select License Duration:"))
        duration_label.setFont(QFont("Arial", 12))
        duration_label.setStyleSheet("color: #555;")
        layout.addWidget(duration_label)

        self.duration_group = QButtonGroup(self)
        duration_layout = QHBoxLayout()
        duration_layout.setSpacing(10)
        for duration in [self.tr("Monthly"), self.tr("Annual"), self.tr("Lifetime")]:
            btn = QRadioButton(duration)
            btn.setFont(QFont("Arial", 11))
            btn.setStyleSheet(
                "QRadioButton { color: #333; } QRadioButton::indicator { width: 18px; height: 18px; }"
            )
            self.duration_group.addButton(btn)
            duration_layout.addWidget(btn)
        layout.addLayout(duration_layout)

        # Email Input
        email_label = QLabel(self.tr("Enter Email Address:"))
        email_label.setFont(QFont("Arial", 12))
        email_label.setStyleSheet("color: #555;")
        layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setFont(QFont("Arial", 11))
        self.email_input.setPlaceholderText(self.tr("Enter your email..."))
        self.email_input.setStyleSheet(
            "padding: 8px; border: 1px solid #ccc; border-radius: 5px; background-color: #fff;"
        )
        layout.addWidget(self.email_input)

        # Submit Button
        submit_btn = QPushButton(self.tr("Submit Request"))
        submit_btn.setFont(QFont("Arial", 13, QFont.Bold))
        submit_btn.setStyleSheet(
            "background-color: #0078d4; color: white; padding: 10px 15px; border: none; border-radius: 5px;"
            "QPushButton:hover { background-color: #005a9e; }"
        )
        submit_btn.clicked.connect(self.submit_request)
        layout.addWidget(submit_btn)

        # Notification Area
        self.notification_label = QLabel("")
        self.notification_label.setFont(QFont("Arial", 10))
        self.notification_label.setStyleSheet("color: red;")
        self.notification_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.notification_label)

        self.setLayout(layout)

    def setup_database(self):
        user_home = os.path.expanduser("~")
        db_path = os.path.join(user_home, "AppData", "Roaming", "SaadiyaResources", "nova360.db")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        cursor = self.conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS license_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module TEXT NOT NULL,
                duration TEXT NOT NULL,
                email TEXT NOT NULL,
                request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_status TEXT DEFAULT 'Pending'
            )
        ''')
        self.conn.commit()

    def submit_request(self):
        module = self.module_combo.currentText()
        duration = None
        for btn in self.duration_group.buttons():
            if btn.isChecked():
                duration = btn.text()
                break

        email = self.email_input.text().strip()

        if not duration:
            self.notification_label.setText(self.tr("Please select a license duration."))
            return

        if not email or "@" not in email:
            self.notification_label.setText(self.tr("Please enter a valid email address."))
            return

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM license_requests WHERE email = ? AND module = ? AND duration = ? AND payment_status = 'Pending'", (email, module, duration))
        existing_requests = cursor.fetchone()[0]

        if existing_requests > 0:
            QMessageBox.warning(self, self.tr("Request Denied"), self.tr("You have already submitted a pending request for this module and duration."))
            return

        cursor.execute(
            "INSERT INTO license_requests (module, duration, email) VALUES (?, ?, ?)",
            (module, duration, email)
        )
        self.conn.commit()

        webbrowser.open("https://www.fiverr.com/your-payment-page")
        QMessageBox.information(
            self,
            self.tr("Request Submitted"),
            self.tr("Your license request has been submitted. After payment, you will receive your license by email.")
        )

        self.notification_label.setText("")

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LicenseRequestPage()
    window.show()
    sys.exit(app.exec_())
    