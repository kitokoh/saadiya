from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox,
                             QDoubleSpinBox)

class InvoicesBillingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Invoice #', 'Customer', 'Amount', 'Status'])
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

    def populate_table(self, invoices):
        self.table.setRowCount(len(invoices))
        for i, row in invoices.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(row['Invoice #']))
            self.table.setItem(i, 1, QTableWidgetItem(row['Customer']))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['Amount'])))
            self.table.setItem(i, 3, QTableWidgetItem(row['Status']))

    def get_selected_invoice_index(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return -1
        return self.table.row(selected_items[0])

    def show_add_edit_dialog(self, invoice_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Invoice" if invoice_data is None else "Edit Invoice")

        form_layout = QFormLayout(dialog)

        invoice_number_input = QLineEdit(invoice_data['Invoice #'] if invoice_data is not None else "")
        customer_input = QLineEdit(invoice_data['Customer'] if invoice_data is not None else "")

        amount_input = QDoubleSpinBox()
        amount_input.setRange(0, 999999.99)
        if invoice_data is not None:
            amount_input.setValue(invoice_data['Amount'])

        status_input = QComboBox()
        statuses = ["Paid", "Unpaid", "Draft"]
        status_input.addItems(statuses)
        if invoice_data is not None:
            status_input.setCurrentText(invoice_data['Status'])

        form_layout.addRow("Invoice #:", invoice_number_input)
        form_layout.addRow("Customer:", customer_input)
        form_layout.addRow("Amount:", amount_input)
        form_layout.addRow("Status:", status_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return invoice_number_input.text(), customer_input.text(), amount_input.value(), status_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
