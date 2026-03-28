from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QHeaderView, QDialog,
                             QFormLayout, QLineEdit, QTextEdit, QComboBox, QMessageBox)

class SavWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("SAV - After-Sales Service")

        # Title
        self.title_label = QLabel("Manage Customer Support Tickets")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Action Buttons
        self.button_layout = QHBoxLayout()
        self.new_ticket_button = QPushButton("New Ticket")
        self.refresh_button = QPushButton("Refresh")
        self.button_layout.addWidget(self.new_ticket_button)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

        # Tickets Table
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(5)
        self.tickets_table.setHorizontalHeaderLabels(["ID", "Customer", "Issue", "Status", "Date"])
        self.tickets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tickets_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tickets_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.tickets_table)

    def display_tickets(self, tickets):
        self.tickets_table.setRowCount(len(tickets))
        for row, ticket in enumerate(tickets):
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket[0])))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket[1]))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket[2]))
            self.tickets_table.setItem(row, 3, QTableWidgetItem(ticket[3]))
            self.tickets_table.setItem(row, 4, QTableWidgetItem(ticket[4]))

    def get_selected_ticket_id(self):
        selected_items = self.tickets_table.selectedItems()
        if selected_items:
            return int(selected_items[0].text())
        return None

class TicketDialog(QDialog):
    def __init__(self, parent=None, ticket=None):
        super().__init__(parent)
        self.setWindowTitle("Ticket Details" if ticket else "New Ticket")
        self.layout = QFormLayout(self)

        self.customer_name_input = QLineEdit(ticket[1] if ticket else "")
        self.issue_description_input = QTextEdit(ticket[2] if ticket else "")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Open", "In Progress", "Closed"])
        if ticket:
            self.status_combo.setCurrentText(ticket[3])

        self.layout.addRow("Customer Name:", self.customer_name_input)
        self.layout.addRow("Issue Description:", self.issue_description_input)
        if ticket:
            self.layout.addRow("Status:", self.status_combo)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addRow(self.button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        return {
            "customer_name": self.customer_name_input.text(),
            "issue_description": self.issue_description_input.toPlainText(),
            "status": self.status_combo.currentText()
        }

def show_message(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()
