import pandas as pd

class ContactsModel:
    def __init__(self):
        self.contacts = pd.DataFrame(columns=['Name', 'Email', 'Phone'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Name': 'John Doe', 'Email': 'john.doe@example.com', 'Phone': '123-456-7890'},
            {'Name': 'Jane Smith', 'Email': 'jane.smith@example.com', 'Phone': '098-765-4321'}
        ]
        self.contacts = pd.DataFrame(data)

    def get_contacts(self):
        return self.contacts

    def add_contact(self, name, email, phone):
        new_contact = pd.DataFrame([{'Name': name, 'Email': email, 'Phone': phone}])
        self.contacts = pd.concat([self.contacts, new_contact], ignore_index=True)

    def update_contact(self, index, name, email, phone):
        if 0 <= index < len(self.contacts):
            self.contacts.loc[index] = [name, email, phone]

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            self.contacts = self.contacts.drop(index).reset_index(drop=True)
