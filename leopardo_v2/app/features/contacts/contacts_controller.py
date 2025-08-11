from .contacts_model import ContactsModel
from .contacts_widget import ContactsWidget

class ContactsController:
    def __init__(self, model: ContactsModel, view: ContactsWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_contacts()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_contact)
        self.view.edit_button.clicked.connect(self.edit_contact)
        self.view.delete_button.clicked.connect(self.delete_contact)

    def load_contacts(self):
        contacts = self.model.get_contacts()
        self.view.populate_table(contacts)

    def add_contact(self):
        contact_data = self.view.show_add_edit_dialog()
        if contact_data:
            name, email, phone = contact_data
            self.model.add_contact(name, email, phone)
            self.load_contacts()

    def edit_contact(self):
        index = self.view.get_selected_contact_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a contact to edit.")
            return

        contact = self.model.get_contacts().iloc[index]
        contact_data = self.view.show_add_edit_dialog(contact)
        if contact_data:
            name, email, phone = contact_data
            self.model.update_contact(index, name, email, phone)
            self.load_contacts()

    def delete_contact(self):
        index = self.view.get_selected_contact_index()
        if index == -1:
            self.view.show_message("No selection", "Please select a contact to delete.")
            return

        self.model.delete_contact(index)
        self.load_contacts()
