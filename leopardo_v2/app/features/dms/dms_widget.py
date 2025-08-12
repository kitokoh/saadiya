from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox,
                             QFileDialog)

class DmsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Title', 'Type', 'Path'])
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

    def populate_table(self, documents):
        self.table.setRowCount(len(documents))
        for i, row in documents.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['title']))
            self.table.setItem(i, 1, QTableWidgetItem(row['type']))
            self.table.setItem(i, 2, QTableWidgetItem(row['path']))

    def get_selected_document_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, document_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Document" if document_data is None else "Edit Document")

        form_layout = QFormLayout(dialog)

        title_input = QLineEdit(document_data['title'] if document_data is not None else "")

        type_input = QComboBox()
        types = ["Quote", "Contract", "Invoice", "Other"]
        type_input.addItems(types)
        if document_data is not None:
            type_input.setCurrentText(document_data['type'])

        path_input = QLineEdit(document_data['path'] if document_data is not None else "")
        path_button = QPushButton("Browse...")
        path_button.clicked.connect(lambda: self.browse_file(path_input))

        form_layout.addRow("Title:", title_input)
        form_layout.addRow("Type:", type_input)
        path_layout = QHBoxLayout()
        path_layout.addWidget(path_input)
        path_layout.addWidget(path_button)
        form_layout.addRow("Path:", path_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return title_input.text(), type_input.currentText(), path_input.text()
        return None

    def browse_file(self, path_input):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Document")
        if file_path:
            path_input.setText(file_path)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
