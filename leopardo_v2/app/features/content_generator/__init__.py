from .content_generator_model import ContentGeneratorModel
from .content_generator_widget import ContentGeneratorWidget
from .content_generator_controller import ContentGeneratorController

def create_content_generator_feature():
    """
    Creates the Content Generator feature.

    Returns:
        A tuple containing the content generator widget and controller.
    """
    model = ContentGeneratorModel()
    view = ContentGeneratorWidget()
    controller = ContentGeneratorController(model, view)
    return view, controller
