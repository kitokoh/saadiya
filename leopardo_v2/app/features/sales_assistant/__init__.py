from .sales_assistant_model import SalesAssistantModel
from .sales_assistant_widget import SalesAssistantWidget
from .sales_assistant_controller import SalesAssistantController

def create_sales_assistant_feature():
    model = SalesAssistantModel()
    view = SalesAssistantWidget()
    controller = SalesAssistantController(model, view)
    return view, controller
