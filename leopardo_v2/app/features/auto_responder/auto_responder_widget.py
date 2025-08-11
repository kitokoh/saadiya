from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox)

class AutoResponderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Keyword', 'Response'])
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

    def populate_table(self, responses):
        self.table.setRowCount(len(responses))
        for i, (keyword, response) in enumerate(responses.items()):
            self.table.setItem(i, 0, QTableWidgetItem(keyword))
            self.table.setItem(i, 1, QTableWidgetItem(response))

    def get_selected_response_keyword(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        return self.table.item(self.table.row(selected_items[0]), 0).text()

    def show_add_edit_dialog(self, response_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Response" if response_data is None else "Edit Response")

        form_layout = QFormLayout(dialog)

        keyword_input = QLineEdit(response_data['keyword'] if response_data is not None else "")
        response_input = QLineEdit(response_data['response'] if response_data is not None else "")

        form_layout.addRow("Keyword:", keyword_input)
        form_layout.addRow("Response:", response_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return keyword_input.text(), response_input.text()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
