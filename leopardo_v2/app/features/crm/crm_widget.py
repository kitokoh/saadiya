from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox)

class CrmWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Name', 'Email', 'Phone', 'Status'])
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

    def populate_table(self, customers):
        self.table.setRowCount(len(customers))
        for i, row in customers.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['name']))
            self.table.setItem(i, 1, QTableWidgetItem(row['email']))
            self.table.setItem(i, 2, QTableWidgetItem(row['phone']))
            self.table.setItem(i, 3, QTableWidgetItem(row['status']))

    def get_selected_customer_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, customer_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Customer" if customer_data is None else "Edit Customer")

        form_layout = QFormLayout(dialog)

        name_input = QLineEdit(customer_data['name'] if customer_data is not None else "")
        email_input = QLineEdit(customer_data['email'] if customer_data is not None else "")
        phone_input = QLineEdit(customer_data['phone'] if customer_data is not None else "")

        status_input = QComboBox()
        statuses = ["Lead", "Contacted", "Proposal", "Negotiation", "Won", "Lost"]
        status_input.addItems(statuses)
        if customer_data is not None:
            status_input.setCurrentText(customer_data['status'])


        form_layout.addRow("Name:", name_input)
        form_layout.addRow("Email:", email_input)
        form_layout.addRow("Phone:", phone_input)
        form_layout.addRow("Status:", status_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return name_input.text(), email_input.text(), phone_input.text(), status_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
