from .trader_model import TraderModel
from .trader_widget import TraderWidget
from .trader_controller import TraderController

def create_trader_feature():
    model = TraderModel()
    view = TraderWidget()
    controller = TraderController(model, view)
    return view, controller
