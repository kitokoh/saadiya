from .invoices_billing_model import InvoicesBillingModel
from .invoices_billing_widget import InvoicesBillingWidget
from .invoices_billing_controller import InvoicesBillingController

def create_invoices_billing_feature():
    model = InvoicesBillingModel()
    view = InvoicesBillingWidget()
    controller = InvoicesBillingController(model, view)
    return view, controller
