from .ai_workflows_model import AiWorkflowsModel
from .ai_workflows_widget import AiWorkflowsWidget

class AiWorkflowsController:
    def __init__(self, model: AiWorkflowsModel, view: AiWorkflowsWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
