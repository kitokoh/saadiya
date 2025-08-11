from .contacts_model import ContactsModel
from .contacts_widget import ContactsWidget
from .contacts_controller import ContactsController

def create_contacts_feature():
    model = ContactsModel()
    view = ContactsWidget()
    controller = ContactsController(model, view)
    return view, controller
