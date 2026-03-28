import pandas as pd

class InvoicesBillingModel:
    def __init__(self):
        self.invoices = pd.DataFrame(columns=['Invoice #', 'Customer', 'Amount', 'Status'])
        self._load_initial_data()

    def _load_initial_data(self):
        # Initial data for demonstration
        data = [
            {'Invoice #': 'INV-001', 'Customer': 'Customer A', 'Amount': 100.00, 'Status': 'Paid'},
            {'Invoice #': 'INV-002', 'Customer': 'Customer B', 'Amount': 250.50, 'Status': 'Unpaid'}
        ]
        self.invoices = pd.DataFrame(data)

    def get_invoices(self):
        return self.invoices

    def add_invoice(self, invoice_number, customer, amount, status):
        new_invoice = pd.DataFrame([{'Invoice #': invoice_number, 'Customer': customer, 'Amount': amount, 'Status': status}])
        self.invoices = pd.concat([self.invoices, new_invoice], ignore_index=True)

    def update_invoice(self, index, invoice_number, customer, amount, status):
        if 0 <= index < len(self.invoices):
            self.invoices.loc[index] = [invoice_number, customer, amount, status]

    def delete_invoice(self, index):
        if 0 <= index < len(self.invoices):
            self.invoices = self.invoices.drop(index).reset_index(drop=True)
