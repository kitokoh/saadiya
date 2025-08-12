from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox)

class MarketingRobotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Platform', 'Status'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnHidden(0, True) # Hide the ID column
        self.main_layout.addWidget(self.table)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Robot")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.delete_button = QPushButton("Delete")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.button_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.button_layout)

    def populate_table(self, robots):
        self.table.setRowCount(len(robots))
        for i, row in robots.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(row['name']))
            self.table.setItem(i, 2, QTableWidgetItem(row['platform']))
            self.table.setItem(i, 3, QTableWidgetItem(row['status']))

    def get_selected_robot_id(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        return int(self.table.item(self.table.row(selected_items[0]), 0).text())

    def show_add_robot_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Marketing Robot")

        form_layout = QFormLayout(dialog)

        name_input = QLineEdit()
        platform_input = QComboBox()
        platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn"]
        platform_input.addItems(platforms)

        form_layout.addRow("Robot Name:", name_input)
        form_layout.addRow("Platform:", platform_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return name_input.text(), platform_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
