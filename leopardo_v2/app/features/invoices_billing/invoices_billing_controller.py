from .invoices_billing_model import InvoicesBillingModel
from .invoices_billing_widget import InvoicesBillingWidget

class InvoicesBillingController:
    def __init__(self, model: InvoicesBillingModel, view: InvoicesBillingWidget):
        self.model = model
        self.view = view
        self.connect_signals()
        self.load_invoices()

    def connect_signals(self):
        self.view.add_button.clicked.connect(self.add_invoice)
        self.view.edit_button.clicked.connect(self.edit_invoice)
        self.view.delete_button.clicked.connect(self.delete_invoice)

    def load_invoices(self):
        invoices = self.model.get_invoices()
        self.view.populate_table(invoices)

    def add_invoice(self):
        invoice_data = self.view.show_add_edit_dialog()
        if invoice_data:
            invoice_number, customer, amount, status = invoice_data
            self.model.add_invoice(invoice_number, customer, amount, status)
            self.load_invoices()

    def edit_invoice(self):
        index = self.view.get_selected_invoice_index()
        if index == -1:
            self.view.show_message("No selection", "Please select an invoice to edit.")
            return

        invoice = self.model.get_invoices().iloc[index]
        invoice_data = self.view.show_add_edit_dialog(invoice)
        if invoice_data:
            invoice_number, customer, amount, status = invoice_data
            self.model.update_invoice(index, invoice_number, customer, amount, status)
            self.load_invoices()

    def delete_invoice(self):
        index = self.view.get_selected_invoice_index()
        if index == -1:
            self.view.show_message("No selection", "Please select an invoice to delete.")
            return

        self.model.delete_invoice(index)
        self.load_invoices()
