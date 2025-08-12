from .prompts_tools_model import PromptsToolsModel
from .prompts_tools_widget import PromptsToolsWidget, PromptEditDialog, show_message, copy_to_clipboard
from PyQt5.QtWidgets import QMessageBox

class PromptsToolsController:
    def __init__(self, model: PromptsToolsModel, view: PromptsToolsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_initial_data()

    def connect_signals(self):
        self.view.category_combo.currentTextChanged.connect(self.filter_by_category)
        self.view.prompts_list.currentItemChanged.connect(self.display_selected_prompt_content)
        self.view.add_button.clicked.connect(self.add_prompt)
        self.view.edit_button.clicked.connect(self.edit_prompt)
        self.view.delete_button.clicked.connect(self.delete_prompt)
        self.view.copy_button.clicked.connect(self.copy_prompt_content)

    def load_initial_data(self):
        self.load_categories()
        self.load_all_prompts()

    def load_all_prompts(self):
        try:
            prompts = self.model.get_all_prompts()
            self.view.display_prompts(prompts)
        except Exception as e:
            show_message("Error", f"Failed to load prompts: {e}", icon=QMessageBox.Critical)

    def load_categories(self):
        try:
            categories = self.model.get_categories()
            self.view.populate_categories(categories)
        except Exception as e:
            show_message("Error", f"Failed to load categories: {e}", icon=QMessageBox.Critical)

    def filter_by_category(self):
        category = self.view.category_combo.currentText()
        if category == "All":
            self.load_all_prompts()
        else:
            try:
                prompts = self.model.get_prompts_by_category(category)
                self.view.display_prompts(prompts)
            except Exception as e:
                show_message("Error", f"Failed to filter prompts: {e}", icon=QMessageBox.Critical)

    def display_selected_prompt_content(self):
        title = self.view.get_selected_prompt_title()
        if title:
            content = self.view.prompt_data[title]['prompt']
            self.view.set_content_display(content)
        else:
            self.view.set_content_display("")

    def add_prompt(self):
        categories = self.model.get_categories()
        dialog = PromptEditDialog(categories=categories)
        if dialog.exec_():
            data = dialog.get_data()
            if not data["title"] or not data["prompt"]:
                show_message("Validation Error", "Title and prompt cannot be empty.", icon=QMessageBox.Warning)
                return
            try:
                self.model.add_prompt(data["title"], data["prompt"], data["category"])
                self.load_initial_data()
                show_message("Success", "Prompt added successfully.")
            except Exception as e:
                show_message("Error", f"Failed to add prompt: {e}", icon=QMessageBox.Critical)

    def edit_prompt(self):
        title = self.view.get_selected_prompt_title()
        if not title:
            show_message("No Selection", "Please select a prompt to edit.", icon=QMessageBox.Information)
            return

        prompt_id = self.view.prompt_data[title]['id']
        try:
            # We need to get the full prompt data to pass to the dialog
            prompt_data = (prompt_id, title, self.view.prompt_data[title]['prompt'], self.view.prompt_data[title]['category'])
            categories = self.model.get_categories()
            dialog = PromptEditDialog(prompt=prompt_data, categories=categories)

            if dialog.exec_():
                new_data = dialog.get_data()
                self.model.update_prompt(prompt_id, new_data["title"], new_data["prompt"], new_data["category"])
                self.load_initial_data()
                show_message("Success", "Prompt updated successfully.")
        except Exception as e:
            show_message("Error", f"Failed to edit prompt: {e}", icon=QMessageBox.Critical)

    def delete_prompt(self):
        title = self.view.get_selected_prompt_title()
        if not title:
            show_message("No Selection", "Please select a prompt to delete.", icon=QMessageBox.Information)
            return

        prompt_id = self.view.prompt_data[title]['id']
        reply = QMessageBox.question(self.view, 'Confirm Deletion',
                                     f"Are you sure you want to delete the prompt '{title}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.model.delete_prompt(prompt_id)
                self.load_initial_data()
                show_message("Success", "Prompt deleted successfully.")
            except Exception as e:
                show_message("Error", f"Failed to delete prompt: {e}", icon=QMessageBox.Critical)

    def copy_prompt_content(self):
        content = self.view.get_content_for_copy()
        if not content:
            show_message("No Content", "There is no content to copy.", icon=QMessageBox.Information)
            return
        copy_to_clipboard(content, self.view)

    def get_view(self):
        return self.view
