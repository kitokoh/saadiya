from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox)

class GroupsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Title
        # self.title = QLabel("Groups")
        # self.title.setAlignment(Qt.AlignCenter)
        # self.title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        # self.main_layout.addWidget(self.title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Name', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_layout.addWidget(self.table)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.button_layout)

    def populate_table(self, groups):
        self.table.setRowCount(len(groups))
        for i, row in groups.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['Name']))
            self.table.setItem(i, 1, QTableWidgetItem(row['Description']))

    def get_selected_group_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, group_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Group" if group_data is None else "Edit Group")

        form_layout = QFormLayout(dialog)

        name_input = QLineEdit(group_data['Name'] if group_data is not None else "")
        description_input = QLineEdit(group_data['Description'] if group_data is not None else "")

        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Description:", description_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return name_input.text(), description_input.text()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
