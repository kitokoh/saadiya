from .prompts_tools_model import PromptsToolsModel
from .prompts_tools_widget import PromptsToolsWidget
from .prompts_tools_controller import PromptsToolsController

def create_prompts_tools_feature():
    """
    Creates the Prompts & Tools feature.

    Returns:
        A tuple containing the prompts_tools widget and controller.
    """
    model = PromptsToolsModel()
    view = PromptsToolsWidget()
    controller = PromptsToolsController(model, view)
    return view, controller
