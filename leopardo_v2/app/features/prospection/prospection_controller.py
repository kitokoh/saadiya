from .prospection_model import ProspectionModel
from .prospection_widget import ProspectionWidget, ProspectDialog, show_message
from PyQt5.QtWidgets import QMessageBox

class ProspectionController:
    def __init__(self, model: ProspectionModel, view: ProspectionWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_prospects()

    def connect_signals(self):
        self.view.add_prospect_button.clicked.connect(self.add_prospect)
        self.view.edit_prospect_button.clicked.connect(self.edit_prospect)
        self.view.delete_prospect_button.clicked.connect(self.delete_prospect)
        self.view.refresh_button.clicked.connect(self.load_prospects)
        self.view.prospects_table.doubleClicked.connect(self.edit_prospect)


    def load_prospects(self):
        try:
            prospects = self.model.get_all_prospects()
            self.view.display_prospects(prospects)
        except Exception as e:
            show_message("Error", f"Failed to load prospects: {e}", icon=QMessageBox.Critical)

    def add_prospect(self):
        dialog = ProspectDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data["name"]:
                show_message("Validation Error", "Prospect name is required.", icon=QMessageBox.Warning)
                return
            try:
                self.model.add_prospect(data["name"], data["contact_info"], data["notes"])
                self.load_prospects()
                show_message("Success", "New prospect added successfully.")
            except Exception as e:
                show_message("Error", f"Failed to add prospect: {e}", icon=QMessageBox.Critical)

    def edit_prospect(self):
        prospect_id = self.view.get_selected_prospect_id()
        if prospect_id is None:
            show_message("No Selection", "Please select a prospect to edit.", icon=QMessageBox.Information)
            return

        try:
            prospect = self.model.get_prospect(prospect_id)
            if not prospect:
                show_message("Error", "Prospect not found.", icon=QMessageBox.Critical)
                return

            dialog = ProspectDialog(prospect=prospect)
            if dialog.exec_():
                data = dialog.get_data()
                self.model.update_prospect(
                    prospect_id,
                    data["name"],
                    data["contact_info"],
                    data["status"],
                    data["notes"]
                )
                self.load_prospects()
                show_message("Success", f"Prospect {prospect_id} updated successfully.")
        except Exception as e:
            show_message("Error", f"Failed to open or update prospect: {e}", icon=QMessageBox.Critical)

    def delete_prospect(self):
        prospect_id = self.view.get_selected_prospect_id()
        if prospect_id is None:
            show_message("No Selection", "Please select a prospect to delete.", icon=QMessageBox.Information)
            return

        reply = QMessageBox.question(self.view, 'Confirm Deletion',
                                     f"Are you sure you want to delete prospect ID {prospect_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.model.delete_prospect(prospect_id)
                self.load_prospects()
                show_message("Success", f"Prospect {prospect_id} deleted.")
            except Exception as e:
                show_message("Error", f"Failed to delete prospect: {e}", icon=QMessageBox.Critical)

    def get_view(self):
        return self.view
