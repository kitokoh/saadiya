import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon, QClipboard
from PyQt5.QtCore import Qt

DB_PATH = "product_keys.db"  # Assume placed in same directory

class ActivationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Activation - Product Key")
        self.setFixedSize(420, 220)
        self.setStyleSheet(self.load_styles())
        self.initUI()

    def load_styles(self):
        return """
        QWidget {
            background-color: #f4f6f8;
            font-family: Segoe UI, sans-serif;
            font-size: 14px;
        }
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            padding: 10px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #005ea6;
        }
        QLabel {
            font-size: 16px;
        }
        """

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Enter your product key to activate:")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXXX-XXXXX-XXXXX-XXXXX-XXXXX")

        btn_layout = QHBoxLayout()
        paste_btn = QPushButton("Paste")
        paste_btn.clicked.connect(self.paste_from_clipboard)
        activate_btn = QPushButton("Activate")
        activate_btn.clicked.connect(self.check_activation)
        
        btn_layout.addWidget(paste_btn)
        btn_layout.addWidget(activate_btn)

        layout.addWidget(label)
        layout.addWidget(self.key_input)
        layout.addLayout(btn_layout)

        admin_btn = QPushButton("Admin: View Activated Keys")
        admin_btn.clicked.connect(self.view_activated_keys)
        layout.addWidget(admin_btn)

        self.setLayout(layout)

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        self.key_input.setText(clipboard.text())

    def check_activation(self):
        key = self.key_input.text().strip().upper()
        if not key:
            self.show_message("Error", "Please enter a product key.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT activated FROM product_keys WHERE key = ?", (key,))
        result = cursor.fetchone()
        if result:
            if result[0] == 1:
                self.show_message("Info", "This key is already activated.")
            else:
                cursor.execute("UPDATE product_keys SET activated = 1 WHERE key = ?", (key,))
                conn.commit()
                self.show_message("Success", "Product successfully activated!")
        else:
            self.show_message("Invalid", "This key is invalid.")
        conn.close()

    def view_activated_keys(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM product_keys WHERE activated = 1")
        keys = cursor.fetchall()
        conn.close()

        if not keys:
            msg = "No activated keys yet."
        else:
            msg = "Activated keys:\n" + "\n".join(k[0] for k in keys)
        self.show_message("Activated Keys", msg)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ActivationApp()
    window.show()
    sys.exit(app.exec_())
