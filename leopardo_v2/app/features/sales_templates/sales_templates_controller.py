from .sales_templates_model import SalesTemplatesModel
from .sales_templates_widget import SalesTemplatesWidget, TemplateEditDialog, show_message
from PyQt5.QtWidgets import QApplication, QMessageBox

class SalesTemplatesController:
    def __init__(self, model: SalesTemplatesModel, view: SalesTemplatesWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_templates()

    def connect_signals(self):
        self.view.templates_list.currentItemChanged.connect(self.display_selected_template_content)
        self.view.add_button.clicked.connect(self.add_template)
        self.view.edit_button.clicked.connect(self.edit_template)
        self.view.delete_button.clicked.connect(self.delete_template)
        self.view.copy_button.clicked.connect(self.copy_template_content)

    def load_templates(self):
        try:
            templates = self.model.get_all_templates()
            self.view.display_templates(templates)
        except Exception as e:
            show_message("Error", f"Failed to load templates: {e}", icon=QMessageBox.Critical)

    def display_selected_template_content(self):
        title = self.view.get_selected_template_title()
        if title:
            content = self.view.template_data[title]['content']
            self.view.set_content_display(content)
        else:
            self.view.set_content_display("")

    def add_template(self):
        dialog = TemplateEditDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data["title"] or not data["content"]:
                show_message("Validation Error", "Title and content cannot be empty.", icon=QMessageBox.Warning)
                return
            try:
                self.model.add_template(data["title"], data["content"])
                self.load_templates()
                show_message("Success", "Template added successfully.")
            except Exception as e:
                show_message("Error", f"Failed to add template: {e}", icon=QMessageBox.Critical)

    def edit_template(self):
        title = self.view.get_selected_template_title()
        if not title:
            show_message("No Selection", "Please select a template to edit.", icon=QMessageBox.Information)
            return

        template_id = self.view.template_data[title]['id']
        try:
            template_data = self.model.get_template(template_id)
            dialog = TemplateEditDialog(template=template_data)
            if dialog.exec_():
                new_data = dialog.get_data()
                self.model.update_template(template_id, new_data["title"], new_data["content"])
                self.load_templates()
                show_message("Success", "Template updated successfully.")
        except Exception as e:
            show_message("Error", f"Failed to edit template: {e}", icon=QMessageBox.Critical)

    def delete_template(self):
        title = self.view.get_selected_template_title()
        if not title:
            show_message("No Selection", "Please select a template to delete.", icon=QMessageBox.Information)
            return

        template_id = self.view.template_data[title]['id']
        reply = QMessageBox.question(self.view, 'Confirm Deletion',
                                     f"Are you sure you want to delete the template '{title}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.model.delete_template(template_id)
                self.load_templates()
                show_message("Success", "Template deleted successfully.")
            except Exception as e:
                show_message("Error", f"Failed to delete template: {e}", icon=QMessageBox.Critical)

    def copy_template_content(self):
        content = self.view.get_content_for_copy()
        if not content:
            show_message("No Content", "There is no content to copy.", icon=QMessageBox.Information)
            return
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            show_message("Success", "Template content copied to clipboard.")
        except Exception as e:
            show_message("Error", f"Could not copy to clipboard: {e}", icon=QMessageBox.Critical)


    def get_view(self):
        return self.view
