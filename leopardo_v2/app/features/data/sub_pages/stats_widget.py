import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class StatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = "nova360.db"
        self.init_ui()
        self.load_stats()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)

        self.total_users_card = self.create_stat_card("Total Users", "0")
        self.grid_layout.addWidget(self.total_users_card, 0, 0)

        self.active_bots_card = self.create_stat_card("Active Bots", "0")
        self.grid_layout.addWidget(self.active_bots_card, 0, 1)

        self.facebook_accounts_card = self.create_stat_card("Facebook Accounts", "0")
        self.grid_layout.addWidget(self.facebook_accounts_card, 1, 0)

        self.instances_card = self.create_stat_card("Instances Created", "0")
        self.grid_layout.addWidget(self.instances_card, 1, 1)

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: #3498db;")
        layout.addWidget(value_label)

        card.value_label = value_label
        return card

    def load_stats(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            self.total_users_card.value_label.setText(str(total_users))

            # Active bots
            cursor.execute("SELECT COUNT(*) FROM modules")
            active_bots = cursor.fetchone()[0]
            self.active_bots_card.value_label.setText(str(active_bots))

            # Facebook accounts
            cursor.execute("SELECT COUNT(*) FROM facebook_users")
            facebook_accounts = cursor.fetchone()[0]
            self.facebook_accounts_card.value_label.setText(str(facebook_accounts))

            # Instances created
            cursor.execute("SELECT COUNT(*) FROM instances")
            instances_created = cursor.fetchone()[0]
            self.instances_card.value_label.setText(str(instances_created))

            conn.close()
        except Exception as e:
            print(f"Error loading stats: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StatsWidget()
    widget.show()
    sys.exit(app.exec_())
