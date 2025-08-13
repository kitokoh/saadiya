from .model import ContentGeneratorModel
from .view import ContentGeneratorWidget
from .controller import ContentGeneratorController
from ...core.database import DatabaseManager

def create_content_generator_feature():
    """
    Creates the Content Generator feature.

    Returns:
        A tuple containing the content generator widget and controller.
    """
    db_manager = DatabaseManager()
    model = ContentGeneratorModel(db_manager)
    view = ContentGeneratorWidget(db_manager)
    controller = ContentGeneratorController(model, view)
    return view, controller
