from .crm_model import CrmModel
from .crm_widget import CrmWidget
from .crm_controller import CrmController

def create_crm_feature():
    model = CrmModel()
    view = CrmWidget()
    controller = CrmController(model, view)
    return view, controller
