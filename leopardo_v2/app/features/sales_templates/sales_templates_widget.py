from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit,
                             QPushButton, QHBoxLayout, QDialog, QFormLayout,
                             QLineEdit, QMessageBox, QDialogButtonBox, QSplitter)
from PyQt5.QtCore import Qt

class SalesTemplatesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Sales Prompts / Templates")

        # Title
        self.title_label = QLabel("Manage Sales Prompts and Templates")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Main layout with splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.main_splitter)

        # Left side: Template list
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_label = QLabel("Templates")
        self.templates_list = QListWidget()
        self.list_layout.addWidget(self.list_label)
        self.list_layout.addWidget(self.templates_list)
        self.main_splitter.addWidget(self.list_widget)

        # Right side: Content view
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_label = QLabel("Template Content")
        self.template_content_text = QTextEdit()
        self.template_content_text.setReadOnly(True)
        self.content_layout.addWidget(self.content_label)
        self.content_layout.addWidget(self.template_content_text)
        self.main_splitter.addWidget(self.content_widget)

        self.main_splitter.setSizes([200, 500]) # Initial size ratio

        # Action Buttons
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add New")
        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")
        self.copy_button = QPushButton("Copy Content")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

    def display_templates(self, templates):
        self.templates_list.clear()
        self.template_data = {} # To store id and content
        for t_id, title, content in templates:
            self.templates_list.addItem(title)
            self.template_data[title] = {'id': t_id, 'content': content}

    def get_selected_template_title(self):
        selected_items = self.templates_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def set_content_display(self, content):
        self.template_content_text.setText(content)

    def get_content_for_copy(self):
        return self.template_content_text.toPlainText()


class TemplateEditDialog(QDialog):
    def __init__(self, parent=None, template=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Template" if template else "Add New Template")
        self.layout = QFormLayout(self)
        self.setMinimumWidth(400)

        self.title_input = QLineEdit(template[1] if template else "")
        self.content_input = QTextEdit(template[2] if template else "")
        self.content_input.setMinimumHeight(200)

        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Content:", self.content_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.layout.addRow(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "content": self.content_input.toPlainText()
        }

def show_message(title, text, icon=QMessageBox.Information):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(text)
    msg_box.setWindowTitle(title)
    msg_box.exec_()
