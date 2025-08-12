from .sav_model import SavModel
from .sav_widget import SavWidget, TicketDialog, show_message

class SavController:
    def __init__(self, model: SavModel, view: SavWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_tickets()

    def connect_signals(self):
        self.view.new_ticket_button.clicked.connect(self.open_new_ticket_dialog)
        self.view.refresh_button.clicked.connect(self.load_tickets)
        self.view.tickets_table.doubleClicked.connect(self.open_edit_ticket_dialog)

    def load_tickets(self):
        try:
            tickets = self.model.get_all_tickets()
            self.view.display_tickets(tickets)
        except Exception as e:
            show_message("Error", f"Failed to load tickets: {e}")

    def open_new_ticket_dialog(self):
        dialog = TicketDialog()
        if dialog.exec_():
            data = dialog.get_data()
            if not data["customer_name"] or not data["issue_description"]:
                show_message("Validation Error", "Customer name and issue description are required.")
                return
            try:
                self.model.create_ticket(data["customer_name"], data["issue_description"])
                self.load_tickets()
                show_message("Success", "New ticket created successfully.")
            except Exception as e:
                show_message("Error", f"Failed to create ticket: {e}")

    def open_edit_ticket_dialog(self):
        selected_id = self.view.get_selected_ticket_id()
        if selected_id is None:
            return

        try:
            ticket = self.model.get_ticket(selected_id)
            if not ticket:
                show_message("Error", "Ticket not found.")
                return

            dialog = TicketDialog(ticket=ticket)
            if dialog.exec_():
                data = dialog.get_data()
                self.model.update_ticket_status(selected_id, data["status"])
                self.load_tickets()
                show_message("Success", f"Ticket {selected_id} updated successfully.")
        except Exception as e:
            show_message("Error", f"Failed to open or update ticket: {e}")

    def get_view(self):
        return self.view
