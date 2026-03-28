from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox)

class UserManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Username', 'Email', 'Role'])
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

    def populate_table(self, users):
        self.table.setRowCount(len(users))
        for i, row in users.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['Username']))
            self.table.setItem(i, 1, QTableWidgetItem(row['Email']))
            self.table.setItem(i, 2, QTableWidgetItem(row['Role']))

    def get_selected_user_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, user_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit User" if user_data is None else "Edit User")

        form_layout = QFormLayout(dialog)

        username_input = QLineEdit(user_data['Username'] if user_data is not None else "")
        email_input = QLineEdit(user_data['Email'] if user_data is not None else "")

        role_input = QComboBox()
        roles = ["Admin", "User"]
        role_input.addItems(roles)
        if user_data is not None:
            role_input.setCurrentText(user_data['Role'])

        form_layout.addRow("Username:", username_input)
        form_layout.addRow("Email:", email_input)
        form_layout.addRow("Role:", role_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return username_input.text(), email_input.text(), role_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
