from .crm_model import CrmModel
from .crm_widget import CrmWidget

class CrmController:
    def __init__(self, model: CrmModel, view: CrmWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_customers()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_customer)
        self.view.edit_button.clicked.connect(self.edit_customer)
        self.view.delete_button.clicked.connect(self.delete_customer)

    def load_customers(self):
        customers = self.model.get_customers()
        self.view.populate_table(customers)

    def add_customer(self):
        customer_data = self.view.show_add_edit_dialog()
        if customer_data:
            name, email, phone, status = customer_data
            self.model.add_customer(name, email, phone, status)
            self.load_customers()

    def edit_customer(self):
        index = self.view.get_selected_customer_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a customer to edit.")
            return

        customer = self.model.get_customers().iloc[index]
        customer_data = self.view.show_add_edit_dialog(customer)
        if customer_data:
            name, email, phone, status = customer_data
            self.model.update_customer(index, name, email, phone, status)
            self.load_customers()

    def delete_customer(self):
        index = self.view.get_selected_customer_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a customer to delete.")
            return

        self.model.delete_customer(index)
        self.load_customers()
