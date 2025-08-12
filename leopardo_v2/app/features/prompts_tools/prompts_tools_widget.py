from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QTextEdit,
                             QPushButton, QHBoxLayout, QDialog, QFormLayout,
                             QLineEdit, QMessageBox, QDialogButtonBox, QSplitter,
                             QComboBox, QApplication)
from PyQt5.QtCore import Qt

class PromptsToolsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Prompts & Tools")

        # Title
        self.title_label = QLabel("Manage Prompts")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Category Filter
        self.filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.category_combo)
        self.filter_layout.addStretch()
        self.layout.addLayout(self.filter_layout)

        # Main layout with splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.main_splitter)

        # Left side: Prompt list
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_label = QLabel("Prompts")
        self.prompts_list = QListWidget()
        self.list_layout.addWidget(self.list_label)
        self.list_layout.addWidget(self.prompts_list)
        self.main_splitter.addWidget(self.list_widget)

        # Right side: Content view
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_label = QLabel("Prompt Content")
        self.prompt_content_text = QTextEdit()
        self.prompt_content_text.setReadOnly(True)
        self.content_layout.addWidget(self.content_label)
        self.content_layout.addWidget(self.prompt_content_text)
        self.main_splitter.addWidget(self.content_widget)

        self.main_splitter.setSizes([250, 450])

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

    def populate_categories(self, categories):
        self.category_combo.clear()
        self.category_combo.addItem("All")
        self.category_combo.addItems(categories)

    def display_prompts(self, prompts):
        self.prompts_list.clear()
        self.prompt_data = {}
        for p_id, title, prompt, category in prompts:
            self.prompts_list.addItem(title)
            self.prompt_data[title] = {'id': p_id, 'prompt': prompt, 'category': category}

    def get_selected_prompt_title(self):
        selected_items = self.prompts_list.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def set_content_display(self, content):
        self.prompt_content_text.setText(content)

    def get_content_for_copy(self):
        return self.prompt_content_text.toPlainText()


class PromptEditDialog(QDialog):
    def __init__(self, parent=None, prompt=None, categories=[]):
        super().__init__(parent)
        self.setWindowTitle("Edit Prompt" if prompt else "Add New Prompt")
        self.layout = QFormLayout(self)
        self.setMinimumWidth(450)

        self.title_input = QLineEdit(prompt[1] if prompt else "")
        self.prompt_input = QTextEdit(prompt[2] if prompt else "")
        self.prompt_input.setMinimumHeight(200)
        self.category_input = QLineEdit(prompt[3] if prompt else "")
        self.category_input.setPlaceholderText("Or type a new category")

        self.category_combo = QComboBox()
        self.category_combo.addItems(categories)
        if prompt:
            self.category_combo.setCurrentText(prompt[3])
        self.category_combo.currentTextChanged.connect(self.category_input.setText)


        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("Prompt:", self.prompt_input)
        self.layout.addRow("Existing Category:", self.category_combo)
        self.layout.addRow("Category:", self.category_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.layout.addRow(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "prompt": self.prompt_input.toPlainText(),
            "category": self.category_input.text()
        }

def show_message(title, text, icon=QMessageBox.Information):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setText(text)
    msg_box.setWindowTitle(title)
    msg_box.exec_()

def copy_to_clipboard(text, parent):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)
    show_message("Success", "Content copied to clipboard.", parent)
