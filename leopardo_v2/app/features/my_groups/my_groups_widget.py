import csv
import json
import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QLocale
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QKeySequence, QPainter, QLinearGradient, QTranslator
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QAbstractItemView, QLineEdit, QHBoxLayout, QCheckBox,
                             QMenu, QAction, QComboBox, QScrollBar, QFrame, QDialog, QFormLayout,
                             QFileDialog, QDialogButtonBox, QMessageBox)

# from .....imports import *
# from .....translation import TranslatorManager
# from .....ui.footer import FooterSection
# from .....ui.header import HeaderSection
# from .....ui.secondry_menu import SecondaryMenu

class AddGroupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Group")
        self.setFixedSize(300, 200)

        layout = QFormLayout(self)

        self.name_input = QLineEdit(self)
        self.link_input = QLineEdit(self)
        self.remarks_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.description_input = QLineEdit(self)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Link:", self.link_input)
        layout.addRow("Remarks:", self.remarks_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Description:", self.description_input)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.accept)
        layout.addWidget(self.submit_button)

    def get_group_data(self):
        return {
            'name': self.name_input.text(),
            'link': self.link_input.text(),
            'remarks': self.remarks_input.text(),
            'category': self.category_input.text(),
            'description': self.description_input.text()
        }

class MyGroupsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_list = self.load_groups()
        self.visible_columns = ['Select', 'Name', 'Link', 'Remarks',
                                'Category', 'Description', 'Actions']
        self.items_per_page = 10
        self.current_page = 1

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        group_label = QLabel("Group List:", self)
        group_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_layout.addWidget(group_label)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Search in groups...")
        self.search_field.textChanged.connect(self.filter_table)
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        top_layout.addWidget(self.search_field)

        self.import_button = QPushButton('Import Groups', self)
        self.import_button.setStyleSheet("background-color: #6c757d; color: white; padding: 5px 10px;")
        self.import_button.clicked.connect(self.import_groups)
        top_layout.addWidget(self.import_button)

        self.export_button = QPushButton('Export', self)
        self.export_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px;")
        self.export_button.clicked.connect(self.export_groups)
        top_layout.addWidget(self.export_button)

        self.add_group_button = QPushButton('+ 1 Group', self)
        self.add_group_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px;")
        self.add_group_button.clicked.connect(self.open_add_group_dialog)
        top_layout.addWidget(self.add_group_button)

        layout.addLayout(top_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.visible_columns))
        self.table.setHorizontalHeaderLabels(self.visible_columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        self.checkboxes_layout = QHBoxLayout()
        for index, col_name in enumerate(self.visible_columns):
            checkbox = QCheckBox(col_name)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_visible_columns)
            self.checkboxes_layout.addWidget(checkbox)
        layout.addLayout(self.checkboxes_layout)

        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.pagination_label = QLabel(f"Page {self.current_page}")
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.pagination_label)
        self.pagination_layout.addWidget(self.next_button)
        layout.addLayout(self.pagination_layout)

        self.populate_table()

    def load_groups(self):
        try:
            filedirect= os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-BLOG-Robot', 'text','text1' , 'groups.json')
            if not os.path.exists(os.path.dirname(filedirect)):
                os.makedirs(os.path.dirname(filedirect))
            if not os.path.exists(filedirect):
                with open(filedirect, 'w') as f:
                    json.dump({"groups": []}, f)

            with open(filedirect, 'r') as f:
                data = json.load(f)
                return data.get("groups", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def populate_table(self):
        self.table.setRowCount(len(self.group_list))
        self.update_table()

    def update_table(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        visible_groups = self.group_list[start_index:end_index]

        self.table.setRowCount(len(visible_groups))

        for row, group in enumerate(visible_groups):
            if isinstance(group, dict):
                checkbox = QCheckBox()
                self.table.setCellWidget(row, 0, checkbox)
                self.table.setItem(row, 1, QTableWidgetItem(group.get('name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(group.get('link', '')))
                self.table.setItem(row, 3, QTableWidgetItem(group.get('remarks', '')))
                self.table.setItem(row, 4, QTableWidgetItem(group.get('category', '')))
                self.table.setItem(row, 5, QTableWidgetItem(group.get('description', '')))
                action_button = QPushButton('Actions')
                action_menu = QMenu(self)
                edit_action = QAction('Edit', self)
                delete_action = QAction('Delete', self)
                edit_action.triggered.connect(lambda _, r=row: self.edit_group(r))
                delete_action.triggered.connect(lambda _, r=row: self.delete_group(r))
                action_menu.addAction(edit_action)
                action_menu.addAction(delete_action)
                action_button.setMenu(action_menu)
                self.table.setCellWidget(row, 6, action_button)

        self.pagination_label.setText(f"Page {self.current_page}")

    def import_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Groups", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.group_list.append(row)
                    self.save_groups()
                    self.populate_table()
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Error during import: {e}")

    def export_groups(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Groups", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.group_list[0].keys())
                    writer.writeheader()
                    writer.writerows(self.group_list)
                QMessageBox.information(self, "Export Success", "Groups exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error during export: {e}")

    def open_add_group_dialog(self):
        dialog = AddGroupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_group = dialog.get_group_data()
            self.group_list.append(new_group)
            self.save_groups()
            self.populate_table()

    def edit_group(self, row):
        group = self.group_list[row]
        dialog = AddGroupDialog(self)
        dialog.name_input.setText(group.get('name', ''))
        dialog.link_input.setText(group.get('link', ''))
        dialog.remarks_input.setText(group.get('remarks', ''))
        dialog.category_input.setText(group.get('category', ''))
        dialog.description_input.setText(group.get('description', ''))

        if dialog.exec_() == QDialog.Accepted:
            updated_group = dialog.get_group_data()
            self.group_list[row] = updated_group
            self.save_groups()
            self.populate_table()

    def delete_group(self, row):
        del self.group_list[row]
        self.save_groups()
        self.populate_table()

    def filter_table(self):
        search_text = self.search_field.text().lower()
        if not search_text:
            self.populate_table()
            return
        filtered_groups = [group for group in self.group_list if search_text in group.get('name', '').lower()]
        self.group_list = filtered_groups
        self.populate_table()

    def next_page(self):
        if (self.current_page * self.items_per_page) < len(self.group_list):
            self.current_page += 1
            self.populate_table()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()

    def save_groups(self):
        filedirect= os.path.join(os.path.expanduser('~'), 'Downloads', 'AI-BLOG-Robot', 'text','text1' , 'groups.json')
        with open(filedirect, 'w') as f:
            json.dump({"groups": self.group_list}, f, indent=4)

    def update_visible_columns(self):
        for i in range(self.checkboxes_layout.count()):
            checkbox = self.checkboxes_layout.itemAt(i).widget()
            self.table.setColumnHidden(i, not checkbox.isChecked())
