from .run_model import RunModel
from .run_widget import RunWidget
from .run_controller import RunController

def create_run_feature():
    model = RunModel()
    view = RunWidget()
    controller = RunController(model, view)
    return view, controller
