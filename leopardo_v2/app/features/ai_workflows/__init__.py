from .ai_workflows_model import AiWorkflowsModel
from .ai_workflows_widget import AiWorkflowsWidget
from .ai_workflows_controller import AiWorkflowsController

def create_ai_workflows_feature():
    model = AiWorkflowsModel()
    view = AiWorkflowsWidget()
    controller = AiWorkflowsController(model, view)
    return view, controller
