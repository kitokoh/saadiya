from .ai_agent_model import AiAgentModel
from .ai_agent_widget import AiAgentWidget
from .ai_agent_controller import AiAgentController

def create_ai_agent_feature():
    model = AiAgentModel()
    view = AiAgentWidget()
    controller = AiAgentController(model, view)
    return view, controller
