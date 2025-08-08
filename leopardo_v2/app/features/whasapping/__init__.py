from .whasapping_widget import WhasappingWidget
from .whasapping_controller import WhasappingController

class WhasappingModel:
    pass

def create_whasapping_feature():
    model = WhasappingModel()
    controller = WhasappingController(model)
    widget = WhasappingWidget()
    widget.set_controller(controller)
    return widget, controller
