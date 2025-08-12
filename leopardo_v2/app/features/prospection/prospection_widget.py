from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
                             QPushButton, QHBoxLayout, QHeaderView, QDialog,
                             QFormLayout, QLineEdit, QTextEdit, QComboBox, QMessageBox,
                             QDialogButtonBox)

class ProspectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Prospection & Relances")

        # Title
        self.title_label = QLabel("Manage Sales Prospects and Follow-ups")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Action Buttons
        self.button_layout = QHBoxLayout()
        self.add_prospect_button = QPushButton("Add Prospect")
        self.edit_prospect_button = QPushButton("View/Edit Prospect")
        self.delete_prospect_button = QPushButton("Delete Prospect")
        self.refresh_button = QPushButton("Refresh")
        self.button_layout.addWidget(self.add_prospect_button)
        self.button_layout.addWidget(self.edit_prospect_button)
        self.button_layout.addWidget(self.delete_prospect_button)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

        # Prospects Table
        self.prospects_table = QTableWidget()
        self.prospects_table.setColumnCount(6)
        self.prospects_table.setHorizontalHeaderLabels(["ID", "Name", "Contact Info", "Status", "Last Follow-up", "Notes"])
        self.prospects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prospects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.prospects_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.prospects_table)

    def display_prospects(self, prospects):
        self.prospects_table.setRowCount(len(prospects))
        for row, prospect_data in enumerate(prospects):
            # id, prospect_name, contact_info, status, last_follow_up, notes
            self.prospects_table.setItem(row, 0, QTableWidgetItem(str(prospect_data[0])))
            self.prospects_table.setItem(row, 1, QTableWidgetItem(prospect_data[1]))
            self.prospects_table.setItem(row, 2, QTableWidgetItem(prospect_data[2]))
            self.prospects_table.setItem(row, 3, QTableWidgetItem(prospect_data[3]))
            self.prospects_table.setItem(row, 4, QTableWidgetItem(str(prospect_data[4])))
            self.prospects_table.setItem(row, 5, QTableWidgetItem(prospect_data[5]))

    def get_selected_prospect_id(self):
        selected_items = self.prospects_table.selectedItems()
        if selected_items:
            return int(self.prospects_table.item(selected_items[0].row(), 0).text())
        return None

class ProspectDialog(QDialog):
    def __init__(self, parent=None, prospect=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Prospect" if prospect else "Add New Prospect")
        self.layout = QFormLayout(self)

        self.name_input = QLineEdit(prospect[1] if prospect else "")
        self.contact_input = QLineEdit(prospect[2] if prospect else "")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["New", "Contacted", "Proposal", "Negotiation", "Won", "Lost"])
        if prospect:
            self.status_combo.setCurrentText(prospect[3])
        self.notes_input = QTextEdit(prospect[5] if prospect else "")

        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Contact Info:", self.contact_input)
        self.layout.addRow("Status:", self.status_combo)
        self.layout.addRow("Notes:", self.notes_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.layout.addRow(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "contact_info": self.contact_input.text(),
            "status": self.status_combo.currentText(),
            "notes": self.notes_input.toPlainText()
        }

def show_message(title, text, icon=QMessageBox.Information):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(text)
    msg_box.setWindowTitle(title)
    msg_box.exec_()
