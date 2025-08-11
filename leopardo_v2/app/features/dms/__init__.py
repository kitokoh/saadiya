from .dms_model import DmsModel
from .dms_widget import DmsWidget
from .dms_controller import DmsController

def create_dms_feature():
    model = DmsModel()
    view = DmsWidget()
    controller = DmsController(model, view)
    return view, controller
