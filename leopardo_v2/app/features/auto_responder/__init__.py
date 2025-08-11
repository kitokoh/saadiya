from .auto_responder_model import AutoResponderModel
from .auto_responder_widget import AutoResponderWidget
from .auto_responder_controller import AutoResponderController

def create_auto_responder_feature():
    model = AutoResponderModel()
    view = AutoResponderWidget()
    controller = AutoResponderController(model, view)
    return view, controller
