from .tools_model import ToolsModel
from .tools_widget import ToolsWidget
from .tools_controller import ToolsController

def create_tools_feature():
    model = ToolsModel()
    view = ToolsWidget()
    controller = ToolsController(model, view)
    return view, controller
