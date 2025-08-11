import pandas as pd

class CrmModel:
    def __init__(self):
        self.customers = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'Status'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Name': 'Customer A', 'Email': 'customer.a@example.com', 'Phone': '111-222-3333', 'Status': 'Lead'},
            {'Name': 'Customer B', 'Email': 'customer.b@example.com', 'Phone': '444-555-6666', 'Status': 'Contacted'}
        ]
        self.customers = pd.DataFrame(data)

    def get_customers(self):
        return self.customers

    def add_customer(self, name, email, phone, status):
        new_customer = pd.DataFrame([{'Name': name, 'Email': email, 'Phone': phone, 'Status': status}])
        self.customers = pd.concat([self.customers, new_customer], ignore_index=True)

    def update_customer(self, index, name, email, phone, status):
        if 0 <= index < len(self.customers):
            self.customers.loc[index] = [name, email, phone, status]

    def delete_customer(self, index):
        if 0 <= index < len(self.customers):
            self.customers = self.customers.drop(index).reset_index(drop=True)
