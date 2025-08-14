import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QPushButton, QDialog, QLineEdit,
                             QTextEdit, QDialogButtonBox, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime

class AddStrategyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Strategy")
        self.layout = QVBoxLayout(self)

        self.name_label = QLabel("Strategy Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.description_label = QLabel("Description:")
        self.description_input = QTextEdit()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_strategy_data(self):
        return self.name_input.text(), self.description_input.toPlainText()

class StrategiesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = "nova360.db"
        self.init_ui()
        self.load_strategies()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.add_button = QPushButton("Add Strategy")
        self.add_button.clicked.connect(self.add_strategy)
        main_layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Created At"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

    def load_strategies(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM strategies")
            strategies = cursor.fetchall()

            self.table.setRowCount(len(strategies))
            for row, strategy in enumerate(strategies):
                for col, data in enumerate(strategy):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))

            conn.close()
        except Exception as e:
            print(f"Error loading strategies: {e}")

    def add_strategy(self):
        dialog = AddStrategyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, description = dialog.get_strategy_data()
            if name:
                self.save_strategy(name, description)
                self.load_strategies()

    def save_strategy(self, name, description):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO strategies (name, description, created_at) VALUES (?, ?, ?)",
                           (name, description, created_at))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving strategy: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = StrategiesWidget()
    widget.show()
    sys.exit(app.exec_())
