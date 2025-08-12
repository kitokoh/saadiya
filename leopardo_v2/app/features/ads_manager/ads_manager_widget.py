from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox,
                             QDoubleSpinBox)

class AdsManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Platform', 'Budget', 'Status'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnHidden(0, True) # Hide the ID column
        self.main_layout.addWidget(self.table)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Campaign")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.button_layout)

    def populate_table(self, campaigns):
        self.table.setRowCount(len(campaigns))
        for i, row in campaigns.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(row['name']))
            self.table.setItem(i, 2, QTableWidgetItem(row['platform']))
            self.table.setItem(i, 3, QTableWidgetItem(str(row['budget'])))
            self.table.setItem(i, 4, QTableWidgetItem(row['status']))

    def get_selected_campaign_id(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        return int(self.table.item(self.table.row(selected_items[0]), 0).text())

    def get_selected_campaign_data(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None

        row = self.table.row(selected_items[0])

        return {
            'id': int(self.table.item(row, 0).text()),
            'name': self.table.item(row, 1).text(),
            'platform': self.table.item(row, 2).text(),
            'budget': float(self.table.item(row, 3).text()),
            'status': self.table.item(row, 4).text()
        }

    def show_add_edit_dialog(self, campaign_data=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add/Edit Campaign" if campaign_data is None else "Edit Campaign")

        form_layout = QFormLayout(dialog)

        name_input = QLineEdit(campaign_data['name'] if campaign_data is not None else "")

        platform_input = QComboBox()
        platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn"]
        platform_input.addItems(platforms)
        if campaign_data is not None:
            platform_input.setCurrentText(campaign_data['platform'])

        budget_input = QDoubleSpinBox()
        budget_input.setRange(0, 999999.99)
        if campaign_data is not None:
            budget_input.setValue(campaign_data['budget'])

        status_input = QComboBox()
        statuses = ["Active", "Paused", "Completed"]
        status_input.addItems(statuses)
        if campaign_data is not None:
            status_input.setCurrentText(campaign_data['status'])

        form_layout.addRow("Campaign Name:", name_input)
        form_layout.addRow("Platform:", platform_input)
        form_layout.addRow("Budget:", budget_input)
        form_layout.addRow("Status:", status_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return name_input.text(), platform_input.currentText(), budget_input.value(), status_input.currentText()
        return None

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
