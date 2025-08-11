from .ai_agent_model import AiAgentModel
from .ai_agent_widget import AiAgentWidget

class AiAgentController:
    def __init__(self, model: AiAgentModel, view: AiAgentWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
