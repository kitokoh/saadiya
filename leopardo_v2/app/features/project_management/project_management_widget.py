from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox)

class ProjectManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Status'])
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

    def populate_table(self, projects):
        self.table.setRowCount(len(projects))
        for i, row in projects.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['name']))
            self.table.setItem(i, 1, QTableWidgetItem(row['description']))
            self.table.setItem(i, 2, QTableWidgetItem(row['status']))

    def get_selected_project_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, project_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Project" if project_data is None else "Edit Project")

        form_layout = QFormLayout(dialog)

        name_input = QLineEdit(project_data['name'] if project_data is not None else "")
        description_input = QLineEdit(project_data['description'] if project_data is not None else "")

        status_input = QComboBox()
        statuses = ["Not Started", "In Progress", "Completed", "On Hold"]
        status_input.addItems(statuses)
        if project_data is not None:
            status_input.setCurrentText(project_data['status'])

        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Description:", description_input)
        form_layout.addRow("Status:", status_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return name_input.text(), description_input.text(), status_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
